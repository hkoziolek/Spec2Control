import json
import re
import argparse
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from click import prompt
import requests
import uuid
from datetime import datetime
import time
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

base_url="http://127.0.0.1:8001"


# ============================================================================
# Configuration and Data Structures
# ============================================================================

@dataclass
class ChapterMetadata:
    """Metadata for a single chapter extracted from markdown."""
    number: int
    title: str
    content: str
    tag_count: int = 0

    def __str__(self):
        return f"Chapter {self.number}: {self.title} ({self.tag_count} tags)"


@dataclass
class NarrativeConfig:
    """Configuration for a single control narrative."""
    name: str
    enabled: bool
    chapters: List[int] | str  # List of chapter numbers or "all"
    description: str = ""


@dataclass
class ProcessConfig:
    """Complete process configuration loaded from YAML."""
    narratives: List[NarrativeConfig]
    output_base_dir: str
    include_timestamp: bool = True
    skip_chapter_1: bool = True
    max_retries: int = 3
    retry_delay: int = 2


# ============================================================================
# Helper Functions
# ============================================================================

def load_config(config_path: Optional[Path] = None) -> ProcessConfig:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config file, or None to use default location

    Returns:
        ProcessConfig object with loaded settings
    """
    if config_path is None:
        # Default config location
        config_path = Path(__file__).resolve().parent.parent / "data" / "process_config.yaml"

    if not config_path.exists():
        print(f"Warning: Config file not found at {config_path}, using defaults")
        return ProcessConfig(
            narratives=[],
            output_base_dir="data/fbd-llm-output",
            include_timestamp=True,
            skip_chapter_1=True,
            max_retries=3,
            retry_delay=2
        )

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        # Parse narratives
        narratives = []
        for n in config_data.get('narratives', []):
            narratives.append(NarrativeConfig(
                name=n['name'],
                enabled=n.get('enabled', False),
                chapters=n.get('chapters', []),
                description=n.get('description', '')
            ))

        # Parse output settings
        output_cfg = config_data.get('output', {})
        processing_cfg = config_data.get('processing', {})

        return ProcessConfig(
            narratives=narratives,
            output_base_dir=output_cfg.get('base_dir', 'data/fbd-llm-output'),
            include_timestamp=output_cfg.get('include_timestamp', True),
            skip_chapter_1=processing_cfg.get('skip_chapter_1', True),
            max_retries=processing_cfg.get('max_retries', 3),
            retry_delay=processing_cfg.get('retry_delay', 2)
        )
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        print("Using default configuration")
        return ProcessConfig(
            narratives=[],
            output_base_dir="data/fbd-llm-output"
        )


def discover_narratives(cn_dir: Path) -> Dict[str, Path]:
    """
    Discover available control narrative files in the directory.

    Args:
        cn_dir: Path to control-narratives directory

    Returns:
        Dictionary mapping narrative name to file path
    """
    narratives = {}

    if not cn_dir.exists():
        print(f"Warning: Control narratives directory not found: {cn_dir}")
        return narratives

    for subdir in cn_dir.iterdir():
        if not subdir.is_dir():
            continue

        # Look for markdown file matching directory name
        md_file = subdir / f"{subdir.name}.md"
        if md_file.exists():
            narratives[subdir.name] = md_file

    return narratives


def parse_chapters_metadata(file_path: Path) -> List[ChapterMetadata]:
    """
    Extract chapter metadata from markdown file including titles and tag counts.

    Args:
        file_path: Path to markdown file

    Returns:
        List of ChapterMetadata objects
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Find all chapter headers using regex
        chapter_pattern = r'^## (\d+) \*\*(.*?)\*\*'
        chapter_matches = list(re.finditer(chapter_pattern, content, re.MULTILINE))

        if not chapter_matches:
            return []

        chapters = []

        # Extract each chapter with metadata
        for i, match in enumerate(chapter_matches):
            chapter_num = int(match.group(1))
            chapter_title = match.group(2).strip()
            chapter_start = match.start()

            # Find the next chapter to determine where this chapter ends
            if i + 1 < len(chapter_matches):
                chapter_end = chapter_matches[i + 1].start()
                chapter_content = content[chapter_start:chapter_end]
            else:
                # This is the last chapter
                doc_info_pattern = r'^---\s*$.*?^## Document Information'
                doc_info_match = re.search(doc_info_pattern, content[chapter_start:], re.MULTILINE | re.DOTALL)
                if doc_info_match:
                    chapter_end = chapter_start + doc_info_match.start()
                    chapter_content = content[chapter_start:chapter_end]
                else:
                    chapter_content = content[chapter_start:]

            # Clean up the content
            plain_text = chapter_content.strip()
            plain_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', plain_text)
            plain_text = re.sub(r'[ \t]+', ' ', plain_text)

            # Count tags (look for |Tagname | Type | pattern)
            tag_pattern = r'^\|([A-Z]{2,5}-\d{3})'
            tag_count = len(re.findall(tag_pattern, chapter_content, re.MULTILINE))

            chapters.append(ChapterMetadata(
                number=chapter_num,
                title=chapter_title,
                content=plain_text.strip(),
                tag_count=tag_count
            ))

        return chapters

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


def parse_chapter_selection(spec: str, total_chapters: int) -> List[int]:
    """
    Parse chapter selection specification into list of chapter numbers.

    Supports formats:
    - "all": all chapters
    - "2-4": range (chapters 2, 3, 4)
    - "2,3,5": individual chapters (2, 3, 5)
    - "2-4,7,9-11": combination

    Args:
        spec: Chapter selection string
        total_chapters: Total number of chapters available

    Returns:
        List of chapter numbers (sorted, deduplicated)
    """
    if spec.lower() == "all":
        return list(range(1, total_chapters + 1))

    chapters = set()
    parts = spec.split(',')

    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range specification
            try:
                start, end = part.split('-', 1)
                start_num = int(start.strip())
                end_num = int(end.strip())
                chapters.update(range(start_num, end_num + 1))
            except ValueError:
                print(f"Warning: Invalid range format '{part}', skipping")
        else:
            # Individual chapter
            try:
                chapters.add(int(part))
            except ValueError:
                print(f"Warning: Invalid chapter number '{part}', skipping")

    # Filter out invalid chapter numbers
    valid_chapters = [c for c in sorted(chapters) if 1 <= c <= total_chapters]

    if len(valid_chapters) < len(chapters):
        invalid = sorted(chapters - set(valid_chapters))
        print(f"Warning: Ignoring invalid chapter numbers: {invalid}")

    return valid_chapters


def list_available_narratives(cn_dir: Path):
    """
    Display all available narratives with their chapter information.

    Args:
        cn_dir: Path to control-narratives directory
    """
    narratives = discover_narratives(cn_dir)

    if not narratives:
        print("No control narratives found.")
        return

    print("\nAvailable Control Narratives:")
    print("=" * 80)

    for name in sorted(narratives.keys()):
        file_path = narratives[name]
        chapters = parse_chapters_metadata(file_path)

        print(f"\n{name}")
        print(f"  File: {file_path}")
        print(f"  Chapters: {len(chapters)}")

        if chapters:
            for chapter in chapters:
                tag_info = f" ({chapter.tag_count} tags)" if chapter.tag_count > 0 else ""
                print(f"    [{chapter.number}] {chapter.title}{tag_info}")

    print("\n" + "=" * 80)


def get_input_from_file(file_path: Path) -> list[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all chapter headers using regex
        chapter_pattern = r'^## (\d+) \*\*(.*?)\*\*'
        chapter_matches = list(re.finditer(chapter_pattern, content, re.MULTILINE))
        
        if not chapter_matches:
            print(f"No chapters found in {file_path}")
            return []
        
        chapters = []
        
        # Extract each chapter
        for i, match in enumerate(chapter_matches):
            chapter_start = match.start()
            
            # Find the next chapter to determine where this chapter ends
            if i + 1 < len(chapter_matches):
                chapter_end = chapter_matches[i + 1].start()
                chapter_content = content[chapter_start:chapter_end]
            else:
                # This is the last chapter, include everything until the end
                # but stop at document information section if it exists
                doc_info_pattern = r'^---\s*$.*?^## Document Information'
                doc_info_match = re.search(doc_info_pattern, content[chapter_start:], re.MULTILINE | re.DOTALL)
                if doc_info_match:
                    chapter_end = chapter_start + doc_info_match.start()
                    chapter_content = content[chapter_start:chapter_end]
                else:
                    chapter_content = content[chapter_start:]
            
            # Clean up the content and convert to plain text
            # Remove markdown formatting while preserving structure
            plain_text = chapter_content.strip()
            
            # Remove excessive whitespace and normalize line breaks
            plain_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', plain_text)
            plain_text = re.sub(r'[ \t]+', ' ', plain_text)
            
            chapters.append(plain_text.strip())
        
        print(f"Successfully extracted {len(chapters)} chapters from {file_path}")
        return chapters
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []   

def execute_single_prompt(prompt_text, base_url, session_id):
    """Execute a single prompt."""
    url = f"{base_url}/qa"
    body = {
        "prompt": prompt_text,
        "llmModel": os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-5"),
        "temperature": 1,
        "maxTokens": 16000,
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "apiKey": os.getenv("AZURE_OPENAI_API_KEY"),
        "apiVersion": os.getenv("AZURE_OPENAI_API_VERSION"),
        "deploymentName": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5"),
        "session_id": session_id
    }
   
    max_retries = 3
    retry_delay = 2  # seconds between retries
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=body, stream=True)
            if response.status_code == 200:
                # Collect all streaming text, preserving line breaks
                result_text = ""
                for line in response.iter_lines(decode_unicode=True):
                    # Add all lines, including empty ones, to preserve formatting
                    result_text += line + "\n"
                
                result_text = result_text.strip()
                
                # Check if response is empty
                if not result_text:
                    if attempt < max_retries:
                        print(f"Attempt {attempt}/{max_retries}: Received empty response, retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"Attempt {attempt}/{max_retries}: All attempts returned empty response")
                        return None
                
                print(f"Single prompt executed successfully on attempt {attempt}/{max_retries}")
                return result_text
            else:
                print(f"Attempt {attempt}/{max_retries}: Failed to execute prompt. Status: {response.status_code}")
                print(f"Response: {response.text}")
                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                return None
        except Exception as e:
            print(f"Attempt {attempt}/{max_retries}: Error executing prompt: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            return None
    
    return None

def call_transfer_openplc(project: str, application: str, export_path: str, content: str, base_url: str) -> bool:
    """
    Call the /transfer-openplc endpoint to export control logic to OpenPLC format.
    
    Args:
        project: Project name (e.g., "ammonium-nitrates")
        application: Application name (e.g., "Section2")
        export_path: Path where the exported files should be saved
        content: The control logic content to export
        base_url: Base URL of the API server
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        url = f"{base_url}/transfer-openplc"
        
        body = {
            "project": project,
            "application": application,
            "diagram": "",  # Empty string as it's ignored for OpenPLC
            "content": content,
            "exportPath": export_path
        }
        
        print(f"Calling /transfer-openplc for project: {project}, application: {application}")
        print(f"Export path: {export_path}")
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            print(f"Successfully transferred to OpenPLC for {application}")
            return True
        else:
            print(f"Failed to transfer to OpenPLC. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error calling /transfer-openplc: {e}")
        return False

def run_prompt_chain(auto_content: Dict, prompt_path: Path, session_id: str, log_file_path: Optional[Path] = None) -> str:
    print(f"Running prompt chain {prompt_path.name}")
    # Read prompt path file and interpret as json
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            prompt_chain = file.read()
    except FileNotFoundError:
        print(f"Prompt file not found: {prompt_path}")
        return ""
    except Exception as e:
        print(f"Error reading prompt file {prompt_path}: {e}")
        return ""

    prompt_chain = json.loads(prompt_chain)
    result = ""
    
    # Initialize log content - simplified
    log_content = []
    log_content.append(f"# Prompt Chain: {prompt_path.name}")
    log_content.append(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_content.append("")

    for i, step in enumerate(prompt_chain["steps"]):
        print(f"Executing step {i + 1} of {len(prompt_chain['steps'])}")
        
        # Simple log entry for step
        step_name = step.get('promptName') or step.get('name', f'Step_{i+1}')
        log_content.append(f"## Step {i + 1}: {step_name}")
        log_content.append(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
        log_content.append("")
        
        prompt = step["prompt"]
        
        for inputMapping in step["inputMappings"]:
            if inputMapping["source"] == "autoContent":
                prompt = prompt.replace(inputMapping['variable'], auto_content[inputMapping['variable']])
            elif inputMapping["source"].startswith("step_"):
                step_index = int(inputMapping["source"].split("_")[1])
                mapped_value = prompt_chain["steps"][step_index]["result"] if prompt_chain["steps"][step_index].get("result") else "[EMPTY]"
                prompt = prompt.replace(inputMapping['variable'], mapped_value)
                
        # Execute prompt with retry logic for short responses
        max_prompt_retries = 3
        step_result = None
        
        for retry_attempt in range(1, max_prompt_retries + 1):
            step_result = execute_single_prompt(prompt, base_url, session_id)
            
            # Count characters in the result and print to console
            char_count = len(step_result) if step_result else 0
            print(f"Step {i + 1} result character count: {char_count}")
            
            # Check if result is too short (less than 3 characters)
            if step_result and len(step_result) >= 3:
                print(f"Step {i + 1} executed successfully with {char_count} characters")
                break
            elif retry_attempt < max_prompt_retries:
                print(f"Step {i + 1} result too short ({char_count} chars), retrying... (attempt {retry_attempt}/{max_prompt_retries})")
                time.sleep(2)  # Wait 2 seconds before retry
            else:
                print(f"Step {i + 1} failed after {max_prompt_retries} attempts - result too short ({char_count} chars)")
        
        # Log only the result - simplified
        log_content.append("### Output:")
        log_content.append("```")
        if step_result:
            log_content.append(step_result)
        else:
            log_content.append("[NO RESULT]")
        log_content.append("```")
        log_content.append("")
        log_content.append("---")
        log_content.append("")
                
        step["result"] = step_result
        if step_result is not None and step["includeInOutput"]:
            result += step_result + "\n\n"
    
    # Save log to file if log_file_path is provided
    if log_file_path:
        try:
            # Append to existing log file or create new one
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write('\n'.join(log_content) + '\n\n')
        except Exception as e:
            print(f"Error saving log file: {e}")

    return result


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Spec2Control: Convert control narratives to IEC 61131-3 FBDs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use config file (default behavior)
  python spec2control_cli.py

  # List available narratives
  python spec2control_cli.py --list

  # Process specific narratives with specific chapters
  python spec2control_cli.py --narrative ammonium-nitrates --chapters 2,3,4

  # Process all narratives from config
  python spec2control_cli.py --all

  # Process with custom config file
  python spec2control_cli.py --config my_config.yaml

  # Dry run to preview selections
  python spec2control_cli.py --dry-run
        """
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Path to config file (default: data/process_config.yaml)'
    )

    parser.add_argument(
        '--narrative', '--narratives',
        type=str,
        nargs='+',
        metavar='NAME',
        help='Process specific narrative(s) (overrides config)'
    )

    parser.add_argument(
        '--chapters',
        type=str,
        metavar='SPEC',
        help='Chapter selection: "2-4", "2,3,5", or "all" (applies to all selected narratives)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all narratives from config file'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available narratives and exit'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be processed without actually processing'
    )

    parser.add_argument(
        '--output',
        type=Path,
        help='Override output directory'
    )

    return parser.parse_args()


def check_environment_variables():
    """
    Check that required Azure OpenAI environment variables are set.
    Exits with error message if any required variables are missing.
    """
    required_vars = {
        'AZURE_OPENAI_ENDPOINT': 'Azure OpenAI endpoint URL',
        'AZURE_OPENAI_API_KEY': 'Azure OpenAI API key',
        'AZURE_OPENAI_API_VERSION': 'Azure OpenAI API version',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'Azure OpenAI deployment name'
    }

    missing_vars = []
    empty_vars = []

    for var_name, var_description in required_vars.items():
        var_value = os.getenv(var_name)
        if var_value is None:
            missing_vars.append((var_name, var_description))
        elif not var_value.strip():
            empty_vars.append((var_name, var_description))

    if missing_vars or empty_vars:
        print("\n" + "=" * 80)
        print("ERROR: Missing Azure OpenAI Configuration")
        print("=" * 80)

        if missing_vars:
            print("\nThe following required environment variables are not set:")
            for var_name, var_description in missing_vars:
                print(f"  - {var_name} ({var_description})")

        if empty_vars:
            print("\nThe following environment variables are set but empty:")
            for var_name, var_description in empty_vars:
                print(f"  - {var_name} ({var_description})")

        print("\nTo fix this issue:")
        print("1. Create a '.env' file in the project root directory")
        print("2. Add the following variables with your Azure OpenAI credentials:")
        print()
        print("   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/")
        print("   AZURE_OPENAI_API_KEY=your-api-key-here")
        print("   AZURE_OPENAI_API_VERSION=2024-02-15-preview")
        print("   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name")
        print("   AZURE_OPENAI_MODEL_NAME=gpt-5")
        print()
        print("3. Restart the CLI tool")
        print()
        print("For more details, see USAGE_GUIDE.md")
        print("=" * 80 + "\n")

        sys.exit(1)


def main():
    """Main entry point for spec2control_cli."""
    args = parse_args()

    # Check environment variables before doing anything else
    # Skip check for --list since it doesn't need API access
    if not args.list:
        check_environment_variables()

    # Setup paths
    base_path = Path(__file__).resolve().parent.parent / "data"
    cn_dir = base_path / "control-narratives"
    categorization_prompt_path = base_path / "prompt-sets" / "contextgen.txt"
    function_block_prompt_path = base_path / "prompt-sets" / "openplc-fbd.txt"

    # Handle --list option
    if args.list:
        list_available_narratives(cn_dir)
        return

    # Load configuration
    config = load_config(args.config)

    # Determine output directory
    if args.output:
        out_dir = args.output
    else:
        out_dir = base_path / config.output_base_dir.lstrip("data/")

    # Discover available narratives
    available_narratives = discover_narratives(cn_dir)

    # Determine which narratives to process
    narratives_to_process = []

    if args.narrative:
        # CLI override: process specified narratives
        for name in args.narrative:
            if name in available_narratives:
                # Use chapters from CLI if specified, otherwise use all
                chapters_spec = args.chapters if args.chapters else "all"
                narratives_to_process.append(NarrativeConfig(
                    name=name,
                    enabled=True,
                    chapters=chapters_spec,
                    description=""
                ))
            else:
                print(f"Warning: Narrative '{name}' not found, skipping")
    elif args.all:
        # Process all narratives from config
        narratives_to_process = [n for n in config.narratives if n.name in available_narratives]
    else:
        # Default: process enabled narratives from config
        narratives_to_process = [n for n in config.narratives if n.enabled and n.name in available_narratives]

    if not narratives_to_process:
        print("No narratives selected for processing.")
        print("Use --list to see available narratives, or --narrative to specify one.")
        return

    # Display processing plan
    print("\n" + "=" * 80)
    print("PROCESSING PLAN")
    print("=" * 80)

    for narrative_cfg in narratives_to_process:
        narrative_file = available_narratives[narrative_cfg.name]
        chapters_meta = parse_chapters_metadata(narrative_file)

        # Determine which chapters to process
        if isinstance(narrative_cfg.chapters, str):
            if narrative_cfg.chapters.lower() == "all":
                chapter_numbers = [c.number for c in chapters_meta]
            else:
                chapter_numbers = parse_chapter_selection(narrative_cfg.chapters, len(chapters_meta))
        else:
            chapter_numbers = narrative_cfg.chapters

        # Filter chapters based on selection
        selected_chapters = [c for c in chapters_meta if c.number in chapter_numbers]

        print(f"\n{narrative_cfg.name}:")
        print(f"  File: {narrative_file}")
        print(f"  Chapters to process: {len(selected_chapters)}")
        for chapter in selected_chapters:
            print(f"    - {chapter}")

    print("\n" + "=" * 80)

    if args.dry_run:
        print("\n[DRY RUN] No processing performed. Remove --dry-run to execute.")
        return

    # Confirm before proceeding
    response = input("\nProceed with processing? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("Processing cancelled.")
        return

    print("\nStarting processing...")
    print("=" * 80 + "\n")

    # Process each narrative
    for narrative_cfg in narratives_to_process:
        narrative_file = available_narratives[narrative_cfg.name]
        chapters_meta = parse_chapters_metadata(narrative_file)

        # Determine which chapters to process
        if isinstance(narrative_cfg.chapters, str):
            if narrative_cfg.chapters.lower() == "all":
                chapter_numbers = [c.number for c in chapters_meta]
            else:
                chapter_numbers = parse_chapter_selection(narrative_cfg.chapters, len(chapters_meta))
        else:
            chapter_numbers = narrative_cfg.chapters

        # Filter chapters
        selected_chapters = [c for c in chapters_meta if c.number in chapter_numbers]

        if not selected_chapters:
            print(f"No chapters selected for {narrative_cfg.name}, skipping")
            continue

        # Create output directory
        timestamp = datetime.now().strftime("%m%d_%H%M%S")
        timestamp_readable_start = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        print(f"\n{'=' * 80}")
        print(f"Processing: {narrative_cfg.name}")
        print(f"Start time: {timestamp_readable_start}")
        print(f"{'=' * 80}\n")

        if config.include_timestamp:
            file_out_dir = out_dir / f"{narrative_cfg.name}_{timestamp}"
        else:
            file_out_dir = out_dir / narrative_cfg.name

        file_out_dir.mkdir(parents=True, exist_ok=True)

        # Process each selected chapter
        for chapter in selected_chapters:
            session_id = str(uuid.uuid4())
            print(f"\n{'-' * 80}")
            print(f"Processing: Chapter {chapter.number} - {chapter.title}")
            timestamp_readable = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            print(f"Start time: {timestamp_readable}")
            print(f"{'-' * 80}\n")

            # Create chapter output directory
            chapter_out_dir = file_out_dir / f"chapter_{chapter.number}"
            chapter_out_dir.mkdir(parents=True, exist_ok=True)

            # Save chapter content
            with open(chapter_out_dir / "0_cn_chapter.txt", "w", encoding="utf-8") as f:
                f.write(chapter.content)

            auto_content = {"{{control-narrative}}": chapter.content}

            try:
                # Run categorization prompt chain
                log_file_path = chapter_out_dir / "prompt_chain_log.md"
                categorization_result = run_prompt_chain(
                    auto_content,
                    categorization_prompt_path,
                    session_id,
                    log_file_path
                )
                timestamp_readable2 = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print(f"Context generation done: {timestamp_readable2}\n")

                with open(chapter_out_dir / "1_categorization.txt", "w", encoding="utf-8") as f:
                    f.write(categorization_result)
            except Exception as e:
                print(f"Error during categorization for chapter {chapter.number}: {e}")
                continue

            try:
                auto_content = {"{{specification}}": chapter.content + "\n\n" + categorization_result}

                # Run function block generation prompt chain
                log_file_path = chapter_out_dir / "prompt_chain_log.md"
                function_block = run_prompt_chain(
                    auto_content,
                    function_block_prompt_path,
                    session_id,
                    log_file_path
                )
                timestamp_readable3 = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print(f"FBD generation done: {timestamp_readable3}\n")

                with open(chapter_out_dir / "2_control_logic.txt", "w", encoding="utf-8") as f:
                    f.write(function_block)

                # Call /transfer-openplc
                project_name = narrative_cfg.name
                application_name = f"Section{chapter.number}"
                export_path = str(file_out_dir)

                transfer_success = call_transfer_openplc(
                    project=project_name,
                    application=application_name,
                    export_path=export_path,
                    content=function_block,
                    base_url=base_url
                )

                if transfer_success:
                    print(f"OpenPLC transfer completed for {application_name}")
                else:
                    print(f"OpenPLC transfer failed for {application_name}, continuing with next chapter")

            except Exception as e:
                print(f"Error during function block generation for chapter {chapter.number}: {e}")
                continue

        print(f"\n{'=' * 80}")
        print(f"Completed: {narrative_cfg.name}")
        print(f"Output: {file_out_dir}")
        print(f"{'=' * 80}\n")

    print("\n" + "=" * 80)
    print("ALL PROCESSING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
