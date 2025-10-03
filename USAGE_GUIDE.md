# Spec2Control Quick Start Guide

## TL;DR - Quick Start

**Terminal 1 (Backend):**
```bash
# Windows: start-backend.bat
# Linux/Mac: ./start-backend.sh
```

**Terminal 2 (CLI):**
```bash
# List narratives
# Windows: process.bat --list
# Linux/Mac: ./process.sh --list

# Process specific chapters
# Windows: process.bat --narrative ammonium-nitrates --chapters 2,3
# Linux/Mac: ./process.sh --narrative ammonium-nitrates --chapters 2,3
```

---

## First Time Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** - Create `.env` file in project root:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5
   AZURE_OPENAI_MODEL_NAME=gpt-5
   ```

3. **Make scripts executable** (Linux/Mac only):
   ```bash
   chmod +x start-backend.sh process.sh
   ```

## Starting the System

The backend API must be running before using the CLI. You have multiple options:

### Option A: Use Startup Scripts (Recommended - Simplest)

**Terminal 1 - Start Backend:**
```bash
# Windows
start-backend.bat

# Linux/Mac
./start-backend.sh
```

**Terminal 2 - Run CLI:**
```bash
# Windows
process.bat --list

# Linux/Mac
./process.sh --list
```

### Option B: Direct Python Execution

**Terminal 1 - Start Backend:**
```bash
cd src
python spec2control_backend.py
```

**Terminal 2 - Run CLI:**
```bash
cd src
python spec2control_cli.py --list
```

### Option C: Using Uvicorn Directly (Advanced)

**Terminal 1 - Start Backend:**
```bash
cd src
uvicorn spec2control_backend:app --port 8001 --reload
```

**Terminal 2 - Run CLI:**
```bash
cd src
python spec2control_cli.py --list
```

## Common Use Cases

### 1. List Available Narratives

**Using wrapper scripts:**
```bash
# Windows
process.bat --list

# Linux/Mac
./process.sh --list
```

**Or direct execution:**
```bash
cd src
python spec2control_cli.py --list
```

This shows all available control narratives with their chapter counts and titles.

### 2. Quick Test - Single Chapter

**Using wrapper scripts:**
```bash
# Preview what will be processed (Windows)
process.bat --narrative ammonium-nitrates --chapters 2 --dry-run

# Execute if preview looks good (Linux/Mac)
./process.sh --narrative ammonium-nitrates --chapters 2
```

**Or direct execution:**
```bash
cd src
python spec2control_cli.py --narrative ammonium-nitrates --chapters 2 --dry-run
python spec2control_cli.py --narrative ammonium-nitrates --chapters 2
```

### 3. Process Multiple Chapters

```bash
# Using wrapper (Windows)
process.bat --narrative steel-plant --chapters 2-4

# Using wrapper (Linux/Mac)
./process.sh --narrative lng-production --chapters 2,3,5
```

### 4. Process Multiple Narratives

```bash
# Windows
process.bat --narrative desalination steel-plant --chapters 2,3

# Linux/Mac
./process.sh --narrative desalination steel-plant --chapters 2,3
```

### 5. Batch Processing with Config File

**Step 1**: Edit `data/process_config.yaml`:
```yaml
narratives:
  - name: ammonium-nitrates
    enabled: true
    chapters: [2, 3]

  - name: steel-plant
    enabled: true
    chapters: [2, 3, 4]

  # Set others to enabled: false
```

**Step 2**: Run:
```bash
# Windows
process.bat

# Linux/Mac
./process.sh

# Or direct:
cd src && python spec2control_cli.py
```

The system will:
- Show you a processing plan
- Ask for confirmation
- Process all enabled narratives

## Understanding the Output

After processing, outputs are saved to `data/fbd-llm-output/`:

```
data/fbd-llm-output/
└── ammonium-nitrates_1003_143022/     # Narrative name + timestamp
    ├── ammonium-nitrates.xml          # Combined PLCOpen XML
    └── chapter_2/                      # Per-chapter outputs
        ├── 0_cn_chapter.txt            # Original chapter text
        ├── 1_categorization.txt        # Context extraction
        ├── 2_control_logic.txt         # FBD textual notation
        ├── prompt_chain_log.md         # Full LLM conversation
        └── Section2.xml                # Chapter PLCOpen XML
```

## Chapter Selection Reference

| Format | Meaning | Example |
|--------|---------|---------|
| `2,3,4` | Individual chapters | Chapters 2, 3, and 4 |
| `2-5` | Range | Chapters 2, 3, 4, 5 |
| `2-4,7,9-11` | Combination | Chapters 2,3,4,7,9,10,11 |
| `all` | All chapters | All available chapters |

## Command-Line Options Reference

```bash
# List narratives
python spec2control_cli.py --list

# Use specific config file
python spec2control_cli.py --config my_config.yaml

# Override output directory
python spec2control_cli.py --output /path/to/output

# Process all narratives (ignores enabled flag)
python spec2control_cli.py --all

# Dry run (preview without processing)
python spec2control_cli.py --narrative ammonium-nitrates --dry-run
```

## Troubleshooting

### "No narratives found"
- Check that `data/control-narratives/` directory exists
- Each narrative should have a matching markdown file (e.g., `ammonium-nitrates/ammonium-nitrates.md`)

### "ERROR: Missing Azure OpenAI Configuration"
- The CLI validates environment variables at startup
- Create a `.env` file in the project root with required variables:
  ```
  AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
  AZURE_OPENAI_API_KEY=your-api-key
  AZURE_OPENAI_API_VERSION=2024-02-15-preview
  AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
  AZURE_OPENAI_MODEL_NAME=gpt-5
  ```
- The error message will tell you exactly which variables are missing or empty

### "Connection refused" or API errors
- Ensure backend is running: `python spec2control_backend.py`
- Check backend is on http://127.0.0.1:8001
- Verify Azure OpenAI credentials in `.env` are correct (not just present)

### "Empty LLM responses"
- Check Azure OpenAI quota and deployment status
- Verify model name matches deployment
- Retry logic will attempt 3 times automatically

### "Chapter not found"
- Use `--list` to see available chapters
- Chapter numbering starts at 1 (not 0)
- Chapter 1 is often skipped (process overview)

## Tips for Efficient Processing

1. **Start small**: Test with a single chapter before processing multiple narratives
2. **Use dry-run**: Always preview with `--dry-run` before large batch jobs
3. **Watch the logs**: `prompt_chain_log.md` shows the LLM's reasoning at each step
4. **Iterative development**: Edit config file for quick iteration cycles
5. **Review outputs**: Check `2_control_logic.txt` for FBD structure before viewing XML

## Viewing Results in OpenPLC Editor

After processing completes, you can visualize the generated Function Block Diagrams in OpenPLC Editor.

### Quick Steps:

1. **Download OpenPLC Editor:** https://autonomylogic.com/download/
2. **Locate output folder:** `data/fbd-llm-output/<narrative_name_timestamp>/`
3. **Open in OpenPLC:**
   - File → Open Project
   - **Select the folder** (e.g., `ammonium-nitrates_1003_143022/`)
   - NOT the plc.xml file - select the folder itself
4. **View diagrams:** Double-click `Section2`, `Section3`, etc. in the project tree

The generated PLCOpen XML includes:
- Complete function block diagrams with auto-layout
- All data connections and parameter assignments
- Input/output variables
- Standard IEC 61131-3 function blocks

For detailed OpenPLC instructions, see the **Working with OpenPLC** section in `README.md`.

## Next Steps

- See `CLAUDE.md` for detailed architecture documentation
- Examine `data/BASIC_LIB/specification/` for available function blocks
- Review `data/prompt-sets/openplc-fbd.txt` to understand the LLM prompt chain
- Study generated `prompt_chain_log.md` files to debug LLM behavior
- Import results into OpenPLC Editor to visualize and export control logic
