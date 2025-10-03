"""
PLCOpen TC6 XML Export and Conversion Module for Spec2Control

Copyright (c) 2025 Spec2Control Contributors
Licensed under the MIT License. See LICENSE file in the project root.
SPDX-License-Identifier: MIT OR Apache-2.0

================================================================================
Overview
================================================================================

This module provides bidirectional conversion between textual control logic
notation and PLCOpen TC6 XML Function Block Diagrams (FBDs). It serves as the
final stage of the Spec2Control pipeline, converting LLM-generated textual
control specifications into standard-compliant PLCOpen XML that can be imported
into industrial PLC programming environments (OpenPLC, CODESYS, TIA Portal, etc.).

Key Features:
    - Textual → XML: Parse structured text notation into PLCOpen TC6 compliant XML
    - XML → Textual: Extract textual representation from PLCOpen XML (round-trip)
    - Auto-Layout: Integrate IEC 61131-3 aware diagram layout via autolayout_openplc_fbd
    - Standards Compliance: Full PLCOpen TC6 v2.01 XML schema support via xsdata bindings
    - Variable Management: Support for local, input, output, and in/out variables
    - Connection Types: Data connections (block-to-block) and parameter connections (literals)
    - Validation: Comprehensive validation with actionable error messages

================================================================================
Architecture
================================================================================

Main Components:
    1. TextualNotationParser: Parses structured text into Python dictionaries
       - Section detection (Variables, Functions, Function Blocks, Connections)
       - Line-by-line parsing with error recovery

    2. ProjectBuilder: Constructs PLCOpen object hierarchy
       - Creates Project → POU → FBD structure
       - Generates blocks, variables, connections
       - Manages localId assignment

    3. ConnectionManager: Handles FBD connection logic
       - Data connections (variable → block, block → block, block → variable)
       - Parameter connections (literal values → block inputs)
       - Connection point management (in/out pins)

    4. ValidationHelper: Validates PLCOpen structures
       - Checks for orphaned blocks
       - Validates connection endpoints
       - Detects missing or invalid references

    5. PLCOpenConverter: High-level API facade
       - convert_to_plcopen(): Textual notation → PLCOpen XML
       - apply_auto_layout(): Positions blocks using semantic layout
       - Error handling and logging

================================================================================
Textual Notation Format
================================================================================

The module expects structured text with marked sections:

    * Variables *
    VAR_NAME : DATA_TYPE

    * Functions *
    FUNCTION_TYPE

    * Function Blocks *
    INSTANCE_NAME : BLOCK_TYPE

    * Data Connections *
    SOURCE -> DESTINATION [PIN_NAME]

    * Parameter Data Connections *
    VALUE -> DESTINATION [PIN_NAME]

Example:
    * Variables *
    TI_101_PV : REAL
    TI_101_SP : REAL

    * Function Blocks *
    TI_101 : ANALOG_IN
    PID_101 : PID_BASIC

    * Data Connections *
    TI_101_PV -> TI_101 [PV]
    TI_101 -> PID_101 [PV]

    * Parameter Data Connections *
    100.0 -> PID_101 [SP]

================================================================================
Usage Examples
================================================================================

Basic Conversion:
    >>> from export_openplc import PLCOpenConverter
    >>> textual_notation = \"\"\"
    ... * Function Blocks *
    ... TI_101 : ANALOG_IN
    ... * Parameter Data Connections *
    ... 100.0 -> TI_101 [SP]
    ... \"\"\"
    >>> converter = PLCOpenConverter()
    >>> xml_string = converter.convert_to_plcopen(textual_notation, "MAIN_CONTROL")
    >>> print(xml_string)

With Auto-Layout:
    >>> xml_string = converter.convert_to_plcopen(
    ...     textual_notation,
    ...     "MAIN_CONTROL",
    ...     use_autolayout=True,
    ...     debug_autolayout=True
    ... )

From File:
    >>> with open("control_logic.txt") as f:
    ...     notation = f.read()
    >>> xml = converter.convert_to_plcopen(notation, "PROCESS_CONTROL")
    >>> with open("output.xml", "w") as f:
    ...     f.write(xml)

================================================================================
Dependencies
================================================================================

External:
    - xsdata: XML schema dataclass bindings for PLCOpen TC6
    - tc6_xml_v201: Generated PLCOpen TC6 v2.01 schema classes
    - autolayout_openplc_fbd: IEC 61131-3 aware diagram layout (optional)

Standard Library:
    - xml.etree.ElementTree: XML manipulation
    - dataclasses: Structured data containers
    - typing: Type annotations
    - pathlib: File path handling

================================================================================
References
================================================================================

- PLCOpen TC6 XML v2.01: https://plcopen.org/technical-activities/xml-exchange-format
- IEC 61131-3:2013 - Programmable Controllers - Part 3: Programming Languages
- OpenPLC Project: https://autonomylogic.com/

================================================================================
"""

import sys
import pathlib
import traceback
import time
import shutil
import xml.etree.ElementTree as ET
from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

# Add parent directory to path to import the PLCOpen schema classes
sys.path.append(str(pathlib.Path(__file__).parent))
from tc6_xml_v201 import *

# Import auto-layout functionality
try:
    from autolayout_openplc_fbd import autolayout_fbd
    AUTOLAYOUT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Auto-layout functionality not available: {e}")
    AUTOLAYOUT_AVAILABLE = False


# ============================================================================
# Configuration Constants
# ============================================================================

# Default element dimensions (pixels)
DEFAULT_LITERAL_WIDTH = 50        # Width for boolean and time literals
DEFAULT_LITERAL_CHAR_WIDTH = 8    # Character width for literal value strings
MIN_LITERAL_WIDTH = 50            # Minimum literal width
DEFAULT_VARIABLE_CHAR_WIDTH = 8   # Character width for variable names
MIN_VARIABLE_WIDTH = 60           # Minimum variable width

# Default block dimensions (pixels)
DEFAULT_BLOCK_WIDTH = 80          # Standard block width
DEFAULT_BLOCK_HEIGHT = 60         # Standard block height
DEFAULT_VARIABLE_HEIGHT = 40      # Standard variable height

# Layout configuration
DEFAULT_LAYOUT_X_GAP = 120        # Horizontal spacing between elements
DEFAULT_LAYOUT_Y_GAP = 40         # Vertical spacing between elements
DEFAULT_LAYOUT_LEFT_MARGIN = 50   # Left margin of diagram
DEFAULT_LAYOUT_TOP_MARGIN = 50    # Top margin of diagram
DEFAULT_FBD_SCALING = 10          # FBD coordinate scaling factor

# ============================================================================


@dataclass
class ParsedSections:
    """
    Container for parsed textual notation sections.

    Holds the structured representation of textual control logic after parsing.
    Each section is represented as a list of dictionaries containing the parsed
    attributes for that element type.

    Attributes:
        variables (List[Dict[str, str]]): Variable declarations
            Format: [{'name': 'TI_101_PV', 'type': 'REAL'}, ...]

        functions (List[Dict[str, str]]): Function instances (auto-named blocks)
            Format: [{'type': 'ADD', 'generated_name': 'ADD_0'}, ...]

        function_blocks (List[Dict[str, str]]): Function block instances
            Format: [{'name': 'TI_101', 'type': 'ANALOG_IN'}, ...]

        data_connections (List[Dict[str, str]]): Block-to-block or var-to-block connections
            Format: [{'source': 'TI_101', 'destination': 'PID_101',
                     'source_pin': 'PV', 'dest_pin': 'PV'}, ...]

        parameter_connections (List[Dict[str, str]]): Literal value connections
            Format: [{'value': '100.0', 'destination': 'PID_101', 'pin': 'SP'}, ...]

    Example:
        >>> sections = ParsedSections(
        ...     variables=[{'name': 'TI_101_PV', 'type': 'REAL'}],
        ...     functions=[],
        ...     function_blocks=[{'name': 'TI_101', 'type': 'ANALOG_IN'}],
        ...     data_connections=[{'source': 'TI_101_PV', 'destination': 'TI_101', 'dest_pin': 'PV'}],
        ...     parameter_connections=[]
        ... )
    """
    variables: List[Dict[str, str]]
    functions: List[Dict[str, str]]
    function_blocks: List[Dict[str, str]]
    data_connections: List[Dict[str, str]]
    parameter_connections: List[Dict[str, str]]


class TextualNotationParser:
    """
    Parser for converting structured textual control logic into ParsedSections.

    Processes multi-section textual notation format used in Spec2Control pipeline.
    Sections are delimited by headers like "* Variables *", "* Function Blocks *", etc.
    Each section contains line-by-line declarations in specific formats.

    Supported Sections:
        - Variables: VAR_NAME : DATA_TYPE
        - Functions: FUNCTION_TYPE (auto-generates instance names)
        - Function Blocks: INSTANCE_NAME : BLOCK_TYPE
        - Data Connections: SOURCE -> DESTINATION [PIN]
        - Parameter Data Connections: LITERAL_VALUE -> DESTINATION [PIN]

    The parser is stateful, tracking which section is currently being parsed
    and applying appropriate line parsing logic for each section type.

    Example:
        >>> notation = '''
        ... * Variables *
        ... TI_101_PV : REAL
        ...
        ... * Function Blocks *
        ... TI_101 : ANALOG_IN
        ...
        ... * Data Connections *
        ... TI_101_PV -> TI_101 [PV]
        ... '''
        >>> sections = TextualNotationParser.parse(notation)
        >>> len(sections.variables)
        1
        >>> len(sections.function_blocks)
        1
    """

    @staticmethod
    def parse(textual_notation: str) -> ParsedSections:
        """
        Parse complete textual notation into structured sections.

        Iterates through lines, detecting section headers and routing content
        lines to appropriate parsing methods. Skips empty lines and handles
        section transitions.

        Args:
            textual_notation: Multi-line string with section-delimited control logic

        Returns:
            ParsedSections containing all extracted variables, blocks, and connections

        Example:
            >>> sections = TextualNotationParser.parse(notation_string)
            >>> print(f"Found {len(sections.function_blocks)} function blocks")
        """
        sections = ParsedSections(
            variables=[],
            functions=[],
            function_blocks=[],
            data_connections=[],
            parameter_connections=[]
        )
        
        current_section = None
        
        for line in textual_notation.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if line.startswith('* ') and line.endswith(' *'):
                current_section = TextualNotationParser._detect_section(line)
                continue
            
            # Parse content based on current section
            if current_section and line:
                TextualNotationParser._parse_line(sections, current_section, line)
        
        return sections
    
    @staticmethod
    def _detect_section(line: str) -> Optional[str]:
        """Detect which section type from header line."""
        section_name = line[2:-2].strip().lower()
        if 'variables' in section_name:
            return 'variables'
        elif 'functions' in section_name and 'blocks' not in section_name:
            return 'functions'
        elif 'function blocks' in section_name:
            return 'function_blocks'
        elif 'parameter data connections' in section_name:
            return 'parameter_connections'
        elif 'data connections' in section_name:
            return 'data_connections'
        return None
    
    @staticmethod
    def _parse_line(sections: ParsedSections, section: str, line: str):
        """Parse a single line into the appropriate section."""
        if section == 'variables':
            # Parse "TYPE name" format
            parts = line.split(' ', 1)
            if len(parts) == 2:
                sections.variables.append({'type': parts[0], 'name': parts[1]})
        elif section in ['functions', 'function_blocks']:
            # Parse "TYPE instance_name" format
            parts = line.split(' ', 1)
            if len(parts) == 2:
                getattr(sections, section).append({'type': parts[0], 'instance': parts[1]})
        elif section in ['data_connections', 'parameter_connections']:
            # Parse "source, destination" format
            if ', ' in line:
                source, dest = line.split(', ', 1)
                getattr(sections, section).append({'source': source, 'destination': dest})


class DataTypeHelper:
    """
    Helper class for PLCOpen IEC 61131-3 data type management.

    Provides utilities for creating and inspecting PLCOpen DataType objects,
    which use xsdata-generated schema classes. Maps between string type names
    (e.g., "REAL", "BOOL") and PLCOpen XML type representations.

    Key Responsibilities:
        - Create DataType objects from type name strings
        - Extract type names from DataType objects
        - Distinguish between basic types, derived types, and function blocks
        - Map IEC 61131-3 type names to xsdata attribute names

    IEC 61131-3 Type Categories:
        - Basic Types: BOOL, INT, REAL, TIME, STRING, etc.
        - Derived Types: User-defined types, ENUMs, STRUCTs, ARRAYs
        - Function Block Types: TON, TOF, PID, SR, etc.

    Note:
        PLCOpen uses attribute-based type representation where each basic type
        is a separate attribute (e.g., real="", bool_value="", int_value="").
        Derived types use nested <derived> elements.
    """

    BASIC_TYPES = {
        'BOOL': 'bool_value', 'BYTE': 'byte', 'WORD': 'word', 'DWORD': 'dword', 'LWORD': 'lword',
        'SINT': 'sint', 'INT': 'int_value', 'DINT': 'dint', 'LINT': 'lint',
        'USINT': 'usint', 'UINT': 'uint', 'UDINT': 'udint', 'ULINT': 'ulint',
        'REAL': 'real', 'LREAL': 'lreal', 'TIME': 'time', 'DATE': 'date',
        'DT': 'dt', 'TOD': 'tod', 'STRING': 'string', 'WSTRING': 'wstring'
    }
    
    FUNCTION_BLOCK_TYPES = {
        'TOF', 'TON', 'TP', 'F_TRIG', 'R_TRIG', 'CTU', 'CTD', 'CTUD',
        'SR', 'RS', 'R', 'S', 'OR', 'AND', 'XOR', 'NOT', 'ADD', 'SUB',
        'MUL', 'DIV', 'MOD', 'MOVE', 'SEL', 'MAX', 'MIN', 'LIMIT',
    }
    
    @classmethod
    def create_data_type(cls, type_name: str) -> DataType:
        """Create a DataType object for the given type name."""
        data_type = DataType()
        
        # Map basic types - use empty string for PLCOpen basic types
        type_upper = type_name.upper()
        if type_upper in cls.BASIC_TYPES:
            setattr(data_type, cls.BASIC_TYPES[type_upper], "")
        else:
            # For derived types (function blocks, user types)
            data_type.derived = DataTypeDerived(name=type_name)
        
        return data_type
    
    @classmethod
    def get_type_name(cls, data_type: DataType) -> str:
        """Extract the type name from a DataType object."""
        if not data_type:
            return "Unknown"
        
        # Check for basic types
        for type_name, attr_name in cls.BASIC_TYPES.items():
            if hasattr(data_type, attr_name) and getattr(data_type, attr_name) is not None:
                return type_name
        
        # Check for other types
        if hasattr(data_type, 'derived') and data_type.derived and hasattr(data_type.derived, 'name'):
            return data_type.derived.name
        if hasattr(data_type, 'array') and data_type.array:
            return "ARRAY"
        if hasattr(data_type, 'enum') and data_type.enum:
            return "ENUM"
        if hasattr(data_type, 'struct') and data_type.struct:
            return "STRUCT"
        
        return "Unknown"
    
    @classmethod
    def is_function_block_type(cls, data_type: DataType) -> bool:
        """Check if a data type represents a function block instance."""
        if not data_type or not hasattr(data_type, 'derived') or not data_type.derived:
            return False
        
        if hasattr(data_type.derived, 'name'):
            return data_type.derived.name in cls.FUNCTION_BLOCK_TYPES
        
        return False


class ElementSizeHelper:
    """Helper class for calculating element sizes in FBD diagrams."""
    
    @staticmethod
    def get_literal_width(literal: str) -> int:
        """Get appropriate width for literal based on content."""
        if literal in ['TRUE', 'FALSE']:
            return DEFAULT_LITERAL_WIDTH
        elif literal.startswith('T#'):
            return DEFAULT_LITERAL_WIDTH
        else:
            return max(MIN_LITERAL_WIDTH, len(literal) * DEFAULT_LITERAL_CHAR_WIDTH)

    @staticmethod
    def get_variable_width(var_name: str) -> int:
        """Get appropriate width for variable based on name length."""
        return max(MIN_VARIABLE_WIDTH + 30, len(var_name) * DEFAULT_VARIABLE_CHAR_WIDTH)


class BlockSizeCalculator:
    """Helper class for calculating function block dimensions based on parameters."""
    
    # Cache for library POU parameters to avoid repeated extraction
    _library_pou_cache = {}
    
    # Fixed dimensions for specific block types
    FIXED_DIMENSIONS = {
        # Industrial/Control blocks - keep their specific dimensions
        'ANALOG_IN': (210, 180),
        'BOOL_IN': (240, 160),
        'DIGITAL_IN': (200, 120),
        'DUTY_STANDBY': (360, 340),
        'MOTOR_2SPD': (280, 160),
        'MOTOR_ON_OFF': (280, 160),
        'MOTOR_VSD': (320, 160),
        'PID_BASIC': (260, 200),
        'RATIO_CONTROL': (200, 280),
        'SPLIT_RANGE': (160, 180),
        'VALVE_ELECTRIC': (250, 180),
        'VALVE_ON_OFF': (310, 160),
        'VOTING_ANALOG': (310, 180),
        
        # Standard blocks - all 70x60 dimensions
        # Timers
        'TOF': (70, 60),
        'TON': (70, 60),
        'TP': (70, 60),
        # Triggers  
        'F_TRIG': (70, 60),
        'R_TRIG': (70, 60),
        # Logic
        'OR': (70, 60),
        'AND': (70, 60),
        'XOR': (70, 60),
        'NOT': (70, 60),
        # Counters
        'CTU': (70, 60),
        'CTD': (70, 60),
        'CTUD': (70, 60),
        # Bistables
        'SR': (70, 60),
        'RS': (70, 60),
        # Math
        'ADD': (70, 60),
        'SUB': (70, 60),
        'MUL': (70, 60),
        'DIV': (70, 60),
        'MOD': (70, 60),
        # Selection
        'SEL': (70, 60),
        'MAX': (70, 60),
        'MIN': (70, 60),
        'LIMIT': (70, 60),
        'MOVE': (70, 60),
        # Comparison
        'GT': (70, 60),
        'GE': (70, 60),
        'EQ': (70, 60),
        'LT': (70, 60),
        'LE': (70, 60),
        'NE': (70, 60)
    }
    
    # Known standard block types with their typical parameters
    STANDARD_BLOCKS = {
        # Timers
        'TOF': {'inputs': ['IN', 'PT'], 'outputs': ['Q', 'ET']},
        'TON': {'inputs': ['IN', 'PT'], 'outputs': ['Q', 'ET']},
        'TP': {'inputs': ['IN', 'PT'], 'outputs': ['Q', 'ET']},
        # Triggers
        'F_TRIG': {'inputs': ['CLK'], 'outputs': ['Q']},
        'R_TRIG': {'inputs': ['CLK'], 'outputs': ['Q']},
        # Logic
        'OR': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'AND': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'XOR': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'NOT': {'inputs': ['IN'], 'outputs': ['OUT']},
        # Counters
        'CTU': {'inputs': ['CU', 'R', 'PV'], 'outputs': ['Q', 'CV']},
        'CTD': {'inputs': ['CD', 'LD', 'PV'], 'outputs': ['Q', 'CV']},
        'CTUD': {'inputs': ['CU', 'CD', 'R', 'LD', 'PV'], 'outputs': ['Q', 'CV']},
        # Bistables
        'SR': {'inputs': ['S1', 'R'], 'outputs': ['Q1']},
        'RS': {'inputs': ['S', 'R1'], 'outputs': ['Q1']},
        # Math
        'ADD': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'SUB': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'MUL': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'DIV': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'MOD': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        # Selection
        'SEL': {'inputs': ['G', 'IN0', 'IN1'], 'outputs': ['OUT']},
        'MAX': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'MIN': {'inputs': ['IN1', 'IN2'], 'outputs': ['OUT']},
        'LIMIT': {'inputs': ['MN', 'IN', 'MX'], 'outputs': ['OUT']},
        'MOVE': {'inputs': ['IN'], 'outputs': ['OUT']},
    }
    
    @classmethod
    def extract_pou_parameters(cls, pou: 'ProjectTypesPousPou') -> Dict[str, List[str]]:
        """
        Extract input and output parameter names from a POU object.
        
        Args:
            pou: ProjectTypesPousPou object from library
            
        Returns:
            Dictionary with 'inputs' and 'outputs' lists
        """
        params = {'inputs': [], 'outputs': []}
        
        if not pou or not pou.interface:
            return params
        
        # Extract input variables
        if pou.interface.input_vars:
            for var_list in pou.interface.input_vars:
                if hasattr(var_list, 'variable') and var_list.variable:
                    for var in var_list.variable:
                        if hasattr(var, 'name') and var.name:
                            params['inputs'].append(var.name)
        
        # Extract output variables
        if pou.interface.output_vars:
            for var_list in pou.interface.output_vars:
                if hasattr(var_list, 'variable') and var_list.variable:
                    for var in var_list.variable:
                        if hasattr(var, 'name') and var.name:
                            params['outputs'].append(var.name)
        
        # Extract in/out variables (treat as both input and output)
        if pou.interface.in_out_vars:
            for var_list in pou.interface.in_out_vars:
                if hasattr(var_list, 'variable') and var_list.variable:
                    for var in var_list.variable:
                        if hasattr(var, 'name') and var.name:
                            params['inputs'].append(var.name)
                            params['outputs'].append(var.name)
        
        return params
    
    @classmethod
    def get_library_pou_parameters(cls, block_type: str, library_pous: List['ProjectTypesPousPou'] = None) -> Dict[str, List[str]]:
        """
        Get parameters for a library POU by its type name.
        
        Args:
            block_type: The type name of the block
            library_pous: List of library POUs to search
            
        Returns:
            Dictionary with 'inputs' and 'outputs' lists
        """
        # Check cache first
        if block_type in cls._library_pou_cache:
            return cls._library_pou_cache[block_type]
        
        # Search in library POUs
        if library_pous:
            for pou in library_pous:
                if pou.name == block_type:
                    params = cls.extract_pou_parameters(pou)
                    cls._library_pou_cache[block_type] = params
                    return params
        
        return {'inputs': [], 'outputs': []}
    
    @classmethod
    def calculate_block_dimensions(cls, block_type: str, block_name: str, 
                                  input_connections: Dict[str, List] = None,
                                  output_connections: Set[str] = None,
                                  library_pous: List['ProjectTypesPousPou'] = None) -> Tuple[int, int]:
        """
        Calculate width and height for a function block based on its parameters.
        
        Args:
            block_type: The type of the block (e.g., 'TOF', 'AND')
            block_name: The instance name of the block
            input_connections: Dictionary of input parameter names from connections
            output_connections: Set of output parameter names from connections
            library_pous: List of library POUs for parameter extraction
            
        Returns:
            Tuple of (width, height)
        """
        # First check if this block type has fixed dimensions
        if block_type in cls.FIXED_DIMENSIONS:
            return cls.FIXED_DIMENSIONS[block_type]
        
        # Otherwise, calculate dimensions dynamically
        # First try to get parameters from library POUs
        library_params = cls.get_library_pou_parameters(block_type, library_pous)
        
        if library_params['inputs'] or library_params['outputs']:
            # Use library POU parameters (these are complete)
            input_params = library_params['inputs']
            output_params = library_params['outputs']
        elif block_type in cls.STANDARD_BLOCKS:
            # Fall back to standard parameters for known block types
            standard_params = cls.STANDARD_BLOCKS[block_type]
            input_params = standard_params.get('inputs', [])
            output_params = standard_params.get('outputs', [])
        else:
            # For unknown blocks, use actual connections if available
            input_params = list(input_connections.keys()) if input_connections else []
            output_params = list(output_connections) if output_connections else []
        
        # Calculate width based on parameter names
        # Formula: (longest_input_param + longest_output_param) * 10
        longest_input = max([len(p) for p in input_params], default=2)  # minimum 2 chars
        longest_output = max([len(p) for p in output_params], default=2)  # minimum 2 chars
        
        # Also consider the block name/type itself
        block_label_length = max(len(block_type), len(block_name) if block_name else 0)
        
        # Width calculation: max of parameter-based width and label-based width
        param_width = (longest_input + longest_output) * 10
        label_width = block_label_length * 8 + 20  # Add padding for block label
        width = max(param_width, label_width, 60)  # Minimum width of 60
        
        # Calculate height based on number of parameters
        # Formula: max(input_count, output_count) * 20 + base_height
        input_count = len(input_params)
        output_count = len(output_params)
        max_params = max(input_count, output_count, 1)  # At least 1
        
        # Height calculation: base height + parameter height
        base_height = 30  # Base height for block header
        param_height = max_params * 20
        height = base_height + param_height
        height = max(height, 40)  # Minimum height of 40
        
        return (width, height)
    
    @classmethod
    def get_block_dimensions_from_sections(cls, block_type: str, block_name: str,
                                          sections: 'ParsedSections',
                                          library_pous: List['ProjectTypesPousPou'] = None) -> Tuple[int, int]:
        """
        Calculate block dimensions by analyzing connections in sections.
        
        Args:
            block_type: The type of the block
            block_name: The instance name of the block
            sections: ParsedSections containing connection information
            library_pous: List of library POUs for parameter extraction
            
        Returns:
            Tuple of (width, height)
        """
        input_params = {}
        output_params = set()
        
        # Collect input parameters from data connections
        for conn in sections.data_connections:
            if conn['destination'].startswith(f"{block_name}."):
                param_name = conn['destination'].split('.', 1)[1]
                if param_name not in input_params:
                    input_params[param_name] = []
        
        # Collect input parameters from parameter connections
        for conn in sections.parameter_connections:
            if conn['destination'].startswith(f"{block_name}."):
                param_name = conn['destination'].split('.', 1)[1]
                if param_name not in input_params:
                    input_params[param_name] = []
        
        # Collect output parameters from data connections
        for conn in sections.data_connections:
            if conn['source'].startswith(f"{block_name}."):
                param_name = conn['source'].split('.', 1)[1]
                output_params.add(param_name)
            elif conn['source'] == block_name:
                output_params.add("OUT")
        
        return cls.calculate_block_dimensions(block_type, block_name, 
                                             input_params, output_params, library_pous)


class ConnectionManager:
    """
    Manages creation and validation of FBD connections.

    Handles all aspects of connecting blocks, variables, and parameters in a
    Function Block Diagram. Creates appropriate connection point structures
    (ConnectionPointIn/Out) and Connection elements following PLCOpen TC6 schema.

    Connection Types:
        1. Data Connections: Block output → Block input
           Example: TI_101 [PV] -> PID_101 [PV]

        2. Variable to Block: InVariable → Block input
           Example: TI_101_PV -> TI_101 [PV]

        3. Block to Variable: Block output → OutVariable
           Example: PID_101 [CV] -> CV_OUT

        4. Parameter Connections: Literal value → Block input
           Example: 100.0 -> PID_101 [SP]

    Responsibilities:
        - Build localId ↔ instance name mapping
        - Create input/output connection points for blocks
        - Link connections using refLocalId references
        - Handle auto-naming for function instances without explicit names
        - Validate connection endpoints exist

    Args:
        fbd: BodyFbd element to populate with connections
        sections: Parsed sections containing connection definitions
        element_mapping: Dict mapping element names to their localId values

    Example:
        >>> manager = ConnectionManager(fbd, sections, element_mapping)
        >>> manager.add_all_connections()
    """

    def __init__(self, fbd: 'BodyFbd', sections: ParsedSections, element_mapping: Dict[str, int]):
        self.fbd = fbd
        self.sections = sections
        self.element_mapping = element_mapping
        self.id_to_name = self._build_id_to_name_mapping()
    
    def add_all_connections(self):
        """Add all connections to blocks and output variables."""
        self._add_connections_to_blocks()
        self._add_connections_to_output_variables()
    
    def _build_id_to_name_mapping(self) -> Dict[int, str]:
        """Build a mapping of local_id to instance names for all blocks."""
        id_to_name = {}
        type_counters = {}
        
        if self.fbd.block:
            for block in self.fbd.block:
                type_name = block.type_name if block.type_name else "UnknownType"
                
                if block.instance_name:
                    instance_name = block.instance_name
                else:
                    # Function without instance name - generate name based on type with counter
                    if type_name not in type_counters:
                        type_counters[type_name] = 1
                    else:
                        type_counters[type_name] += 1
                    instance_name = f"{type_name}_{type_counters[type_name]}"
                
                if block.local_id:
                    id_to_name[block.local_id] = instance_name
        
        return id_to_name
    
    def _add_connections_to_blocks(self):
        """Add input and output connection points to blocks based on parsed connections."""
        if not self.fbd.block:
            return
        
        # Import necessary classes at runtime to avoid circular imports
        from tc6_xml_v201 import (
            BodyFbdBlockInputVariables, BodyFbdBlockInputVariablesVariable,
            BodyFbdBlockInOutVariables, BodyFbdBlockOutputVariables, BodyFbdBlockOutputVariablesVariable,
            ConnectionPointIn, ConnectionPointOut, Connection
        )
        
        # Process each block to add input/output variables and connections
        for block in self.fbd.block:
            block_name = self._get_block_name(block)
            self._initialize_block_variables(block)
            
            # Add input connections
            input_connections = self._collect_input_connections(block_name)
            self._create_input_variables(block, input_connections)
            
            # Add output variables
            output_params = self._collect_output_parameters(block_name)
            self._create_output_variables(block, output_params)
    
    def _get_block_name(self, block) -> str:
        """Get the name of a block from element mapping."""
        for name, local_id in self.element_mapping.items():
            if local_id == block.local_id:
                return name
        return f"Block_{block.local_id}"
    
    def _initialize_block_variables(self, block):
        """Initialize block variable containers if not present."""
        from tc6_xml_v201 import (
            BodyFbdBlockInputVariables, BodyFbdBlockInOutVariables, BodyFbdBlockOutputVariables
        )
        
        if not block.input_variables:
            block.input_variables = BodyFbdBlockInputVariables()
            block.input_variables.variable = []
        
        if not block.in_out_variables:
            block.in_out_variables = BodyFbdBlockInOutVariables()
            block.in_out_variables.variable = []
        
        if not block.output_variables:
            block.output_variables = BodyFbdBlockOutputVariables()
            block.output_variables.variable = []
    
    def _collect_input_connections(self, block_name: str) -> Dict[str, List[Tuple[int, Optional[str]]]]:
        """Collect all input connections for a block."""
        input_connections = {}
        
        # Process data connections
        for conn in self.sections.data_connections:
            if conn['destination'].startswith(f"{block_name}."):
                param_name = conn['destination'].split('.', 1)[1]
                source_id, source_param = self._resolve_source(conn['source'])
                
                if source_id:
                    if param_name not in input_connections:
                        input_connections[param_name] = []
                    input_connections[param_name].append((source_id, source_param))
        
        # Process parameter connections
        for conn in self.sections.parameter_connections:
            if conn['destination'].startswith(f"{block_name}."):
                param_name = conn['destination'].split('.', 1)[1]
                
                # Look for the specific literal variable created for this target
                target_key = f"literal_for_{conn['destination']}"
                source_id = self.element_mapping.get(target_key)
                
                if source_id:
                    if param_name not in input_connections:
                        input_connections[param_name] = []
                    input_connections[param_name].append((source_id, None))
        
        return input_connections
    
    def _resolve_source(self, source: str) -> Tuple[Optional[int], Optional[str]]:
        """Resolve source string to source_id and source_param."""
        if '.' in source:
            # Source has an output parameter (e.g., "F_TRIG0.Q")
            source_name, source_param = source.split('.', 1)
            source_id = self.element_mapping.get(source_name)
            return source_id, source_param
        else:
            # Source is just the name (e.g., "First_cycle")
            source_id = self.element_mapping.get(source)
            return source_id, None
    
    def _create_input_variables(self, block, input_connections: Dict[str, List[Tuple[int, Optional[str]]]]):
        """Create input variables for each parameter with connections."""
        from tc6_xml_v201 import BodyFbdBlockInputVariablesVariable, ConnectionPointIn, Connection
        
        for param_name, source_info_list in input_connections.items():
            # Check if input variable already exists
            existing_var = None
            for var in block.input_variables.variable:
                if var.formal_parameter == param_name:
                    existing_var = var
                    break
            
            if not existing_var:
                input_var = BodyFbdBlockInputVariablesVariable(formal_parameter=param_name)
                input_var.connection_point_in = ConnectionPointIn()
                input_var.connection_point_in.rel_position = Position(x=0, y=30)
                input_var.connection_point_in.connection = []
                block.input_variables.variable.append(input_var)
            else:
                input_var = existing_var
                if not input_var.connection_point_in:
                    input_var.connection_point_in = ConnectionPointIn()
                    input_var.connection_point_in.rel_position = Position(x=0, y=30)
                if not input_var.connection_point_in.connection:
                    input_var.connection_point_in.connection = []
                if not input_var.connection_point_in.rel_position:
                    input_var.connection_point_in.rel_position = Position(x=0, y=30)
            
            # Add connections for this input with position information
            for source_id, source_param in source_info_list:
                connection = Connection(ref_local_id=source_id)
                
                if source_param:
                    connection.formal_parameter = source_param
                
                # Add connection path positions
                connection.position = [
                    Position(x=0, y=30),   # Input pin position
                    Position(x=70, y=30)   # Output pin position
                ]
                input_var.connection_point_in.connection.append(connection)
    
    def _collect_output_parameters(self, block_name: str) -> Set[str]:
        """Collect output parameters for a block."""
        output_params = set()
        
        for conn in self.sections.data_connections:
            if conn['source'].startswith(f"{block_name}."):
                param_name = conn['source'].split('.', 1)[1]
                output_params.add(param_name)
            elif conn['source'] == block_name:
                output_params.add("OUT")
        
        return output_params
    
    def _create_output_variables(self, block, output_params: Set[str]):
        """Create output variables for the block."""
        from tc6_xml_v201 import BodyFbdBlockOutputVariablesVariable, ConnectionPointOut
        
        for param_name in output_params:
            # Check if output variable already exists
            existing_var = None
            for var in block.output_variables.variable:
                if var.formal_parameter == param_name:
                    existing_var = var
                    break
            
            if not existing_var:
                output_var = BodyFbdBlockOutputVariablesVariable(formal_parameter=param_name)
                output_var.connection_point_out = ConnectionPointOut()
                output_var.connection_point_out.rel_position = Position(x=70, y=30)
                block.output_variables.variable.append(output_var)
    
    def _add_connections_to_output_variables(self):
        """Add connection points to output variables based on parsed connections."""
        if not self.fbd.out_variable:
            return
        
        from tc6_xml_v201 import ConnectionPointIn, Connection
        
        # Process each output variable to add connections
        for out_var in self.fbd.out_variable:
            var_name = out_var.expression
            if not var_name:
                continue
            
            source_info_list = self._collect_output_variable_sources(var_name)
            
            # Add connection points if there are connections
            if source_info_list:
                if not out_var.connection_point_in:
                    out_var.connection_point_in = ConnectionPointIn()
                    out_var.connection_point_in.rel_position = Position(x=0, y=15)
                if not out_var.connection_point_in.connection:
                    out_var.connection_point_in.connection = []
                
                # Add connections with position information
                for source_id, source_param in source_info_list:
                    connection = Connection(ref_local_id=source_id)
                    
                    if source_param:
                        connection.formal_parameter = source_param
                    
                    connection.position = [
                        Position(x=0, y=15),   # Output variable input pin
                        Position(x=70, y=30)   # Source output pin
                    ]
                    out_var.connection_point_in.connection.append(connection)
    
    def _collect_output_variable_sources(self, var_name: str) -> List[Tuple[int, Optional[str]]]:
        """Collect all sources connected to an output variable."""
        source_info_list = []
        
        # Check data connections
        for conn in self.sections.data_connections:
            if conn['destination'] == var_name:
                source_id, source_param = self._resolve_source(conn['source'])
                if source_id:
                    source_info_list.append((source_id, source_param))
        
        # Check parameter connections
        for conn in self.sections.parameter_connections:
            if conn['destination'] == var_name:
                # Look for the specific literal variable created for this target
                target_key = f"literal_for_{conn['destination']}"
                source_id = self.element_mapping.get(target_key)
                if source_id:
                    source_info_list.append((source_id, None))
        
        return source_info_list


class ProjectBuilder:
    """
    Constructs complete PLCOpen TC6 XML project hierarchy from parsed sections.

    Orchestrates the creation of a valid PLCOpen project structure including:
    - Project metadata (file header, content header)
    - Types section (data types, POUs)
    - POU (Program Organization Unit) with FBD body
    - Instances section for global variable declarations
    - Library POUs (optional function block libraries)

    The builder follows the PLCOpen TC6 v2.01 schema structure:
        Project
        ├── FileHeader (company, product, version)
        ├── ContentHeader (name, coordinate scaling)
        ├── Types
        │   ├── DataTypes (user-defined types)
        │   └── POUs
        │       └── POU (program/function/functionBlock)
        │           ├── Interface (variables)
        │           └── Body
        │               └── FBD (diagram elements)
        └── Instances (global variables, configurations)

    Key Responsibilities:
        - Create project skeleton with metadata
        - Build POU with local variables and FBD body
        - Generate blocks, inVariables, outVariables
        - Manage localId assignment (unique identifiers for diagram elements)
        - Create literal blocks for parameter connections
        - Position elements with default coordinates (overridden by auto-layout)
        - Integrate library POUs for function block definitions

    Args:
        pou_name: Name of the main POU to generate (default "GeneratedPOU")
        library_pous: Optional list of library POU definitions
        project_name: Project name (defaults to pou_name if not provided)
        existing_project: Optional existing project to extend (for incremental builds)

    Example:
        >>> sections = TextualNotationParser.parse(notation)
        >>> builder = ProjectBuilder("MAIN_CONTROL", library_pous=libs)
        >>> project = builder.build_project(sections)
        >>> xml_string = XMLManager.to_xml(project)
    """

    def __init__(self, pou_name: str = "GeneratedPOU", library_pous: List['ProjectTypesPousPou'] = None, project_name: str = None, existing_project: Project = None):
        self.pou_name = pou_name
        self.project_name = project_name or pou_name  # Use project_name if provided, otherwise fallback to pou_name
        self.library_pous = library_pous or []
        self.existing_project = existing_project
    
    def build_project(self, sections: ParsedSections) -> Project:
        """Build a complete PLCOpen project from parsed sections."""
        project = self._create_basic_project_structure()
        pou = self._create_pou(sections)
        
        # Start with the main POU and add library POUs
        all_pous = [pou]
        if self.library_pous:
            all_pous.extend(self.library_pous)
            print(f"Added {len(self.library_pous)} library POUs to the project")
        
        project.types.pous.pou = all_pous
        self._add_instances(project)
        return project
    
    def _create_basic_project_structure(self) -> Project:
        """Create the basic project structure."""
        project = Project()
        
        # Create file header
        project.file_header = ProjectFileHeader(
            company_name="Generated",
            product_name="TextualNotationConverter",
            product_version="1.0",
            creation_date_time="2025-07-30T12:00:00"
        )
        
        # Create content header with coordinate info
        project.content_header = self._create_content_header()
        
        # Create types container
        project.types = ProjectTypes()
        project.types.data_types = ProjectTypesDataTypes()
        project.types.pous = ProjectTypesPous()
        
        return project
    
    def _create_content_header(self) -> ProjectContentHeader:
        """Create content header with coordinate information."""
        content_header = ProjectContentHeader(
            name=self.project_name,
            modification_date_time="2025-07-30T12:00:00"
        )
        
        # Add coordinate info for FBD scaling
        coord_info = ProjectContentHeaderCoordinateInfo()
        
        # FBD scaling
        fbd_info = ProjectContentHeaderCoordinateInfoFbd()
        fbd_info.scaling = ProjectContentHeaderCoordinateInfoFbdScaling(x=10, y=10)
        coord_info.fbd = fbd_info
        
        # LD scaling
        ld_info = ProjectContentHeaderCoordinateInfoLd()
        ld_info.scaling = ProjectContentHeaderCoordinateInfoLdScaling(x=10, y=10)
        coord_info.ld = ld_info
        
        # SFC scaling
        sfc_info = ProjectContentHeaderCoordinateInfoSfc()
        sfc_info.scaling = ProjectContentHeaderCoordinateInfoSfcScaling(x=10, y=10)
        coord_info.sfc = sfc_info
        
        content_header.coordinate_info = coord_info
        return content_header
    
    def _create_pou(self, sections: ParsedSections) -> ProjectTypesPousPou:
        """Create the POU with interface and body."""
        pou = ProjectTypesPousPou(name=self.pou_name, pou_type="program")
        
        # Build interface from variables
        if sections.variables:
            pou.interface = self._create_pou_interface(sections)
        
        # Build body from functions, function blocks, and connections
        if any([sections.functions, sections.function_blocks, 
               sections.data_connections, sections.parameter_connections]):
            pou.body = [self._create_fbd_body(sections)]
        
        return pou
    
    def _create_pou_interface(self, sections: ParsedSections) -> ProjectTypesPousPouInterface:
        """Create POU interface with proper variable declarations."""
        interface = ProjectTypesPousPouInterface()
        local_vars = []
        
        # Add regular variables
        regular_vars = []
        for var_def in sections.variables:
            var = VarListPlainVariable(name=var_def['name'])
            var.type_value = DataTypeHelper.create_data_type(var_def['type'])
            
            # Add address for specific output variables (Traffic Light specific)
            self._add_variable_address(var, var_def['name'])
            regular_vars.append(var)
        
        # Add function block instance variables
        fb_vars = []
        for fb_def in sections.function_blocks:
            var = VarListPlainVariable(name=fb_def['instance'])
            var.type_value = DataTypeHelper.create_data_type(fb_def['type'])
            fb_vars.append(var)
        
        # Create variable lists
        if regular_vars:
            var_list1 = ProjectTypesPousPouInterfaceLocalVars()
            var_list1.variable = regular_vars
            local_vars.append(var_list1)
        
        if fb_vars:
            var_list2 = ProjectTypesPousPouInterfaceLocalVars()
            var_list2.variable = fb_vars
            local_vars.append(var_list2)
        
        if local_vars:
            interface.local_vars = local_vars
        
        return interface
    
    def _add_variable_address(self, var: VarListPlainVariable, var_name: str):
        """Add address for specific variables (Traffic Light specific)."""
        if var_name.startswith('O_LED'):
            if 'Red' in var_name:
                var.address = "%QX0.0"
            elif 'Orange' in var_name:
                var.address = "%QX0.1"
            elif 'Green' in var_name:
                var.address = "%QX0.2"
        elif var_name == 'First_cycle':
            var.address = "%QX0.3"
    
    def _create_fbd_body(self, sections: ParsedSections) -> Body:
        """Create FBD body with proper blocks and connections."""
        body = Body()
        body.fbd = BodyFbd()
        
        # Initialize containers
        body.fbd.block = []
        body.fbd.in_variable = []
        body.fbd.out_variable = []
        
        element_mapping = {}
        # Start local_id_counter after existing IDs to avoid conflicts
        local_id_counter = self._get_next_available_id()
        
        # Create blocks
        local_id_counter = self._create_function_blocks(body.fbd, sections, element_mapping, local_id_counter)
        local_id_counter = self._create_function_blocks_with_instances(body.fbd, sections, element_mapping, local_id_counter)
        
        # Create variables
        local_id_counter = self._create_literal_variables(body.fbd, sections, element_mapping, local_id_counter)
        local_id_counter = self._create_output_variables(body.fbd, sections, element_mapping, local_id_counter)
        local_id_counter = self._create_input_variables(body.fbd, sections, element_mapping, local_id_counter)
        
        # Add connections
        connection_manager = ConnectionManager(body.fbd, sections, element_mapping)
        connection_manager.add_all_connections()
        
        print(f"Created FBD body with {len(body.fbd.block)} blocks, "
              f"{len(body.fbd.in_variable)} input variables, "
              f"{len(body.fbd.out_variable)} output variables")
        
        return body
    
    def _get_next_available_id(self) -> int:
        """Get the next available local_id by checking existing project for all used IDs."""
        used_ids = set()
        
        if self.existing_project and self.existing_project.types and self.existing_project.types.pous:
            for pou in self.existing_project.types.pous.pou:
                if pou.body:
                    for body in pou.body:
                        if hasattr(body, 'fbd') and body.fbd:
                            # Collect IDs from all FBD elements
                            if hasattr(body.fbd, 'block') and body.fbd.block:
                                for block in body.fbd.block:
                                    if hasattr(block, 'local_id') and block.local_id:
                                        used_ids.add(block.local_id)
                            
                            if hasattr(body.fbd, 'in_variable') and body.fbd.in_variable:
                                for in_var in body.fbd.in_variable:
                                    if hasattr(in_var, 'local_id') and in_var.local_id:
                                        used_ids.add(in_var.local_id)
                            
                            if hasattr(body.fbd, 'out_variable') and body.fbd.out_variable:
                                for out_var in body.fbd.out_variable:
                                    if hasattr(out_var, 'local_id') and out_var.local_id:
                                        used_ids.add(out_var.local_id)
                            
                            # Also check any other FBD elements that might have local_id
                            for attr_name in ['constant', 'connector', 'continuation']:
                                if hasattr(body.fbd, attr_name):
                                    elements = getattr(body.fbd, attr_name)
                                    if elements:
                                        for elem in elements:
                                            if hasattr(elem, 'local_id') and elem.local_id:
                                                used_ids.add(elem.local_id)
        
        # Find the next available ID starting from 1
        next_id = 1
        while next_id in used_ids:
            next_id += 1
        
        return next_id
    
    def _create_function_blocks(self, fbd: BodyFbd, sections: ParsedSections, 
                              element_mapping: Dict[str, int], local_id_counter: int) -> int:
        """Create blocks for functions (without instance names)."""
        for func_def in sections.functions:
            # Calculate dimensions based on connections and library definitions
            width, height = BlockSizeCalculator.get_block_dimensions_from_sections(
                func_def['type'], func_def['instance'], sections, self.library_pous
            )
            
            block = BodyFbdBlock(
                local_id=local_id_counter,
                type_name=func_def['type'],
                execution_order_id=0,
                height=height,
                width=width
            )
            block.position = Position(
                x=50 + ((local_id_counter - 1) % 4) * 100, 
                y=50
            )
            element_mapping[func_def['instance']] = local_id_counter
            fbd.block.append(block)
            local_id_counter += 1
        
        return local_id_counter
    
    def _create_function_blocks_with_instances(self, fbd: BodyFbd, sections: ParsedSections,
                                             element_mapping: Dict[str, int], local_id_counter: int) -> int:
        """Create blocks for function blocks (with instance names)."""
        for fb_def in sections.function_blocks:
            # Calculate dimensions based on connections and library definitions
            width, height = BlockSizeCalculator.get_block_dimensions_from_sections(
                fb_def['type'], fb_def['instance'], sections, self.library_pous
            )
            
            block = BodyFbdBlock(
                local_id=local_id_counter,
                type_name=fb_def['type'],
                instance_name=fb_def['instance'],
                execution_order_id=0,
                height=height,
                width=width
            )
            block.position = Position(
                x=50 + ((local_id_counter - 1) % 4) * 100,
                y=130
            )
            element_mapping[fb_def['instance']] = local_id_counter
            fbd.block.append(block)
            local_id_counter += 1
        
        return local_id_counter
    
    def _create_literal_variables(self, fbd: BodyFbd, sections: ParsedSections,
                                 element_mapping: Dict[str, int], local_id_counter: int) -> int:
        """Create input variables for literals/constants - one for each parameter connection."""
        # Create a separate variable for each parameter connection, even if values are the same
        literal_counter = {}
        
        for conn in sections.parameter_connections:
            literal = conn['source']
            
            # Generate unique key for each occurrence of the same literal
            if literal not in literal_counter:
                literal_counter[literal] = 0
            literal_counter[literal] += 1
            
            # Create unique mapping key for this specific occurrence
            unique_key = f"{literal}_{literal_counter[literal]}" if literal_counter[literal] > 1 else literal
            
            in_var = BodyFbdInVariable(
                local_id=local_id_counter,
                execution_order_id=0,
                height=30,
                width=ElementSizeHelper.get_literal_width(literal),
                negated=False
            )
            in_var.position = Position(x=30, y=250 + ((local_id_counter - 8) * 35))
            in_var.expression = literal
            in_var.connection_point_out = ConnectionPointOut()
            in_var.connection_point_out.rel_position = Position(
                x=ElementSizeHelper.get_literal_width(literal), y=15
            )
            
            # Store mapping using the unique key and also by connection index
            element_mapping[unique_key] = local_id_counter
            # Also store by connection target for easier lookup
            destination = conn['destination']
            element_mapping[f"literal_for_{destination}"] = local_id_counter
            
            fbd.in_variable.append(in_var)
            local_id_counter += 1
        
        return local_id_counter
    
    def _create_output_variables(self, fbd: BodyFbd, sections: ParsedSections,
                               element_mapping: Dict[str, int], local_id_counter: int) -> int:
        """Create output variables for regular variables that appear in connections."""
        output_vars = set()
        for conn in sections.data_connections:
            if '.' not in conn['destination']:  # It's a variable, not a block input
                output_vars.add(conn['destination'])
        
        for var_name in sorted(output_vars):
            out_var = BodyFbdOutVariable(
                local_id=local_id_counter,
                execution_order_id=0,
                height=30,
                width=ElementSizeHelper.get_variable_width(var_name),
                negated=False
            )
            out_var.position = Position(
                x=350,
                y=250 + ((local_id_counter - len(fbd.in_variable) - 8) * 35)
            )
            out_var.expression = var_name
            element_mapping[var_name] = local_id_counter
            fbd.out_variable.append(out_var)
            local_id_counter += 1
        
        return local_id_counter
    
    def _create_input_variables(self, fbd: BodyFbd, sections: ParsedSections,
                              element_mapping: Dict[str, int], local_id_counter: int) -> int:
        """Create input variables for regular variables that are sources in connections."""
        input_vars = set()
        for conn in sections.data_connections:
            source = conn['source']
            # Only add if:
            # 1. Not already mapped (not a block or literal)
            # 2. NOT a block output reference (doesn't contain '.')
            if source not in element_mapping and '.' not in source:
                input_vars.add(source)
        
        for var_name in sorted(input_vars):
            in_var = BodyFbdInVariable(
                local_id=local_id_counter,
                execution_order_id=0,
                height=30,
                width=ElementSizeHelper.get_variable_width(var_name),
                negated=False
            )
            in_var.position = Position(
                x=30,
                y=400 + ((local_id_counter - len(fbd.in_variable) - len(fbd.out_variable) - 8) * 35)
            )
            in_var.expression = var_name
            in_var.connection_point_out = ConnectionPointOut()
            in_var.connection_point_out.rel_position = Position(
                x=ElementSizeHelper.get_variable_width(var_name), y=15
            )
            element_mapping[var_name] = local_id_counter
            fbd.in_variable.append(in_var)
            local_id_counter += 1
        
        return local_id_counter
    
    def _add_instances(self, project: Project):
        """Add instances section (required by PLCOpen TC6 XSD schema)."""
        project.instances = ProjectInstances()
        project.instances.configurations = ProjectInstancesConfigurations()
        
        # Create default configuration
        config = ProjectInstancesConfigurationsConfiguration(name="Config0")
        
        # Create default resource
        resource = ProjectInstancesConfigurationsConfigurationResource(name="Res0")
        
        # Create default task
        task = ProjectInstancesConfigurationsConfigurationResourceTask(
            name="task0",
            priority=0,
            interval="T#20ms"
        )
        
        # Create POU instance
        pou_instance = PouInstance(name="instance0", type_name=self.pou_name)
        task.pou_instance = [pou_instance]
        
        # Build the hierarchy
        resource.task = [task]
        config.resource = [resource]
        project.instances.configurations.configuration = [config]


class VariableExtractor:
    """Extracts variables and their information from PLCOpen structures."""
    
    @staticmethod
    def get_function_block_instance_names(pou) -> Set[str]:
        """Get all function block instance names from the POU body."""
        fb_instance_names = set()
        if pou.body:
            for body in pou.body:
                if body.fbd and body.fbd.block:
                    for block in body.fbd.block:
                        if block.instance_name:
                            fb_instance_names.add(block.instance_name)
        return fb_instance_names
    
    @staticmethod
    def get_declared_variable_names(pou) -> Set[str]:
        """Extract all declared variable names from POU interface."""
        declared_vars = set()
        
        if not pou.interface:
            return declared_vars
        
        # Check all variable lists in the interface
        var_lists = [
            pou.interface.local_vars,
            pou.interface.input_vars,
            pou.interface.output_vars,
            pou.interface.in_out_vars
        ]
        
        for var_list_container in var_lists:
            if var_list_container:
                # Handle both single var_list and list of var_lists
                if hasattr(var_list_container, '__iter__') and not isinstance(var_list_container, str):
                    var_lists_to_check = var_list_container
                else:
                    var_lists_to_check = [var_list_container]
                
                for var_list in var_lists_to_check:
                    if var_list and hasattr(var_list, 'variable') and var_list.variable:
                        for var in var_list.variable:
                            if var.name:
                                declared_vars.add(var.name)
        
        return declared_vars


class FunctionExtractor:
    """Extracts functions and function blocks from PLCOpen structures."""
    
    @staticmethod
    def extract_functions_and_blocks(pou) -> Tuple[List[str], List[str]]:
        """Extract functions and function blocks from POU body."""
        functions = []
        function_blocks = []
        
        if pou.body:
            type_counters = {}
            for body in pou.body:
                if body.fbd and body.fbd.block:
                    for block in body.fbd.block:
                        type_name = block.type_name if block.type_name else "UnknownType"
                        
                        if block.instance_name:
                            # Function block with instance name
                            function_blocks.append(f"{type_name} {block.instance_name}")
                        else:
                            # Function without instance name - generate name with counter
                            if type_name not in type_counters:
                                type_counters[type_name] = 1
                            else:
                                type_counters[type_name] += 1
                            instance_name = f"{type_name}_{type_counters[type_name]}"
                            functions.append(f"{type_name} {instance_name}")
        
        return sorted(functions), sorted(function_blocks)


class ConnectionExtractor:
    """Extracts connections from PLCOpen FBD structures."""
    
    def __init__(self, pou):
        self.pou = pou
        self.declared_vars = VariableExtractor.get_declared_variable_names(pou)
    
    def extract_all_connections(self) -> Tuple[List[str], List[str]]:
        """Extract both data connections and parameter connections from POU body."""
        data_connections = []
        param_connections = []
        
        if self.pou.body:
            for body in self.pou.body:
                if body.fbd:
                    data_conns = self._extract_fbd_connections(body.fbd)
                    param_conns = self._extract_fbd_parameter_connections(body.fbd)
                    data_connections.extend(data_conns)
                    param_connections.extend(param_conns)
        
        return data_connections, param_connections
    
    def _extract_fbd_connections(self, fbd: BodyFbd) -> List[str]:
        """Extract data connections from FBD body."""
        connections = set()
        
        if not fbd:
            return list(connections)
        
        id_to_name = self._build_id_to_name_mapping(fbd)
        
        # Process blocks and their connections
        if fbd.block:
            for block in fbd.block:
                instance_name = id_to_name.get(block.local_id, f"Block_{block.local_id}")
                
                # Process input connections
                if block.input_variables and block.input_variables.variable:
                    for input_var in block.input_variables.variable:
                        if input_var.connection_point_in and input_var.connection_point_in.connection:
                            for connection in input_var.connection_point_in.connection:
                                if connection.ref_local_id:
                                    source = self._find_element_by_local_id_with_output_param(
                                        fbd, connection.ref_local_id, connection.formal_parameter, id_to_name
                                    )
                                    # Include if it's a block OR a declared variable
                                    if source and (self._is_block_source(fbd, connection.ref_local_id) or 
                                                 self._is_declared_variable_source(fbd, connection.ref_local_id)):
                                        param_name = input_var.formal_parameter if input_var.formal_parameter else "IN"
                                        connections.add(f"{source}, {instance_name}.{param_name}")
        
        # Process out variables - only include connections from blocks
        if fbd.out_variable:
            for out_var in fbd.out_variable:
                var_name = out_var.expression if out_var.expression else f"OutVar_{out_var.local_id}"
                if out_var.connection_point_in and out_var.connection_point_in.connection:
                    for connection in out_var.connection_point_in.connection:
                        if connection.ref_local_id:
                            source = self._find_element_by_local_id_with_output_param(
                                fbd, connection.ref_local_id, connection.formal_parameter, id_to_name
                            )
                            # Include if it's a block OR a declared variable
                            if source and (self._is_block_source(fbd, connection.ref_local_id) or 
                                         self._is_declared_variable_source(fbd, connection.ref_local_id)):
                                connections.add(f"{source}, {var_name}")
        
        return sorted(list(connections))
    
    def _extract_fbd_parameter_connections(self, fbd: BodyFbd) -> List[str]:
        """Extract parameter data connections from FBD body."""
        param_connections = set()
        
        if not fbd:
            return list(param_connections)
        
        id_to_name = self._build_id_to_name_mapping(fbd)
        
        # Process blocks and their input connections for parameter data
        if fbd.block:
            for block in fbd.block:
                instance_name = id_to_name.get(block.local_id, f"Block_{block.local_id}")
                
                # Process input connections
                if block.input_variables and block.input_variables.variable:
                    for input_var in block.input_variables.variable:
                        if input_var.connection_point_in and input_var.connection_point_in.connection:
                            for connection in input_var.connection_point_in.connection:
                                if connection.ref_local_id:
                                    source = self._find_element_by_local_id(fbd, connection.ref_local_id, id_to_name)
                                    # Include only literals (not blocks or declared variables)
                                    if source and self._is_literal_source(fbd, connection.ref_local_id):
                                        param_name = input_var.formal_parameter if input_var.formal_parameter else "IN"
                                        param_connections.add(f"{source}, {instance_name}.{param_name}")
        
        # Process out variables with literal/variable connections
        if fbd.out_variable:
            for out_var in fbd.out_variable:
                var_name = out_var.expression if out_var.expression else f"OutVar_{out_var.local_id}"
                if out_var.connection_point_in and out_var.connection_point_in.connection:
                    for connection in out_var.connection_point_in.connection:
                        if connection.ref_local_id:
                            source = self._find_element_by_local_id(fbd, connection.ref_local_id, id_to_name)
                            # Include only literals (not blocks or declared variables)
                            if source and self._is_literal_source(fbd, connection.ref_local_id):
                                param_connections.add(f"{source}, {var_name}")
        
        return sorted(list(param_connections))
    
    def _build_id_to_name_mapping(self, fbd: BodyFbd) -> Dict[int, str]:
        """Build a mapping of local_id to instance names for all blocks."""
        id_to_name = {}
        type_counters = {}
        
        if fbd.block:
            for block in fbd.block:
                type_name = block.type_name if block.type_name else "UnknownType"
                
                if block.instance_name:
                    instance_name = block.instance_name
                else:
                    # Function without instance name - generate name based on type with counter
                    if type_name not in type_counters:
                        type_counters[type_name] = 1
                    else:
                        type_counters[type_name] += 1
                    instance_name = f"{type_name}_{type_counters[type_name]}"
                
                if block.local_id:
                    id_to_name[block.local_id] = instance_name
        
        return id_to_name
    
    def _is_block_source(self, fbd: BodyFbd, local_id: int) -> bool:
        """Check if a local_id refers to a block output."""
        if not fbd or not local_id:
            return False
        
        if fbd.block:
            for block in fbd.block:
                if block.local_id == local_id:
                    return True
        
        return False
    
    def _is_declared_variable_source(self, fbd: BodyFbd, local_id: int) -> bool:
        """Check if a local_id refers to a declared variable (not a literal)."""
        if not fbd or not local_id or not self.declared_vars:
            return False
        
        # Check if it's an inVariable with an expression that matches a declared variable
        if fbd.in_variable:
            for in_var in fbd.in_variable:
                if in_var.local_id == local_id and in_var.expression:
                    expr = in_var.expression.strip()
                    return expr in self.declared_vars
        
        return False
    
    def _is_literal_source(self, fbd: BodyFbd, local_id: int) -> bool:
        """Check if a local_id refers to a literal/expression."""
        if not fbd or not local_id:
            return False
        
        # Check if it's an inVariable with a literal expression
        if fbd.in_variable:
            for in_var in fbd.in_variable:
                if in_var.local_id == local_id and in_var.expression:
                    expr = in_var.expression.strip()
                    # Check if it looks like a literal value
                    return (expr.startswith(("'", '"', 'T#')) or
                           expr.isdigit() or
                           expr in ['TRUE', 'FALSE', 'true', 'false'] or
                           expr.replace('.', '', 1).isdigit())
        
        # Check for constants
        if hasattr(fbd, 'constant') and fbd.constant:
            return any(hasattr(const, 'local_id') and const.local_id == local_id
                      for const in fbd.constant)
        
        return False
    
    def _find_element_by_local_id_with_output_param(self, fbd: BodyFbd, local_id: int, 
                                                   formal_parameter: str, id_to_name: Dict[int, str]) -> str:
        """Find an element by its local ID and return a descriptive name with output parameter."""
        if not fbd or not local_id:
            return f"Unknown_{local_id}"
        
        # Check if this is a block
        if fbd.block:
            for block in fbd.block:
                if block.local_id == local_id:
                    instance_name = block.instance_name or f"{block.type_name or 'UnknownType'}_1"
                    
                    # If this connection references a specific output parameter, include it
                    if formal_parameter:
                        return f"{instance_name}.{formal_parameter}"
                    else:
                        # For blocks without explicit formal parameter, determine the default output
                        if block.type_name in ['F_TRIG', 'R_TRIG', 'TON', 'TOF', 'TP', 'AnalogIn']:
                            return f"{instance_name}.Q"
                        elif block.type_name in ['OR', 'AND', 'XOR', 'NOT']:
                            return f"{instance_name}.OUT"
                        else:
                            return f"{instance_name}.OUT"
        
        # For non-block elements (variables, literals), use the original function
        return self._find_element_by_local_id(fbd, local_id, id_to_name)
    
    def _find_element_by_local_id(self, fbd: BodyFbd, local_id: int, id_to_name: Dict[int, str]) -> str:
        """Find an element by its local ID and return a descriptive name."""
        if not fbd or not local_id:
            return f"Unknown_{local_id}"
        
        # Check blocks first using the provided mapping
        if id_to_name and local_id in id_to_name:
            return id_to_name[local_id]
        
        # Check different element types
        element_lists = [
            (fbd.block, lambda x: x.instance_name or f"{x.type_name or 'UnknownType'}_1"),
            (fbd.in_variable, lambda x: x.expression or f"InVar_{local_id}"),
            (fbd.out_variable, lambda x: x.expression or f"OutVar_{local_id}")
        ]
        
        for element_list, name_func in element_lists:
            if element_list:
                for element in element_list:
                    if element.local_id == local_id:
                        return name_func(element)
        
        # Check for constants
        if hasattr(fbd, 'constant') and fbd.constant:
            for const in fbd.constant:
                if hasattr(const, 'local_id') and const.local_id == local_id:
                    return getattr(const, 'value', None) or getattr(const, 'expression', f"Const_{local_id}")
        
        return f"Element_{local_id}"


class PLCOpenConverter:
    """
    Main API facade for PLCOpen TC6 ↔ Textual Notation conversion.

    **Primary Interface** for the export_openplc module. Provides high-level
    methods for converting between textual control logic representations and
    PLCOpen TC6 XML, with optional auto-layout integration.

    Key Methods:
        - convert_to_plcopen(): Textual notation → PLCOpen XML string
        - diagram_to_textual_notation(): PLCOpen Project → Textual notation
        - apply_auto_layout(): Apply IEC 61131-3 aware layout to existing XML

    Workflow:
        1. Parse textual notation → ParsedSections
        2. Build Project object hierarchy → PLCOpen dataclass tree
        3. Optional: Apply auto-layout → Position blocks
        4. Serialize to XML → Valid PLCOpen TC6 v2.01 document

    Features:
        - Round-trip conversion (XML → Text → XML preserves semantics)
        - Library POU integration for function block definitions
        - Configurable auto-layout with debug output
        - Error handling with actionable messages
        - Validation of connections and references

    Example:
        >>> converter = PLCOpenConverter()
        >>> xml = converter.convert_to_plcopen(
        ...     textual_notation,
        ...     pou_name="MAIN_CONTROL",
        ...     use_autolayout=True,
        ...     debug_autolayout=True
        ... )
        >>> with open("output.xml", "w") as f:
        ...     f.write(xml)

    Round-Trip Example:
        >>> # XML → Textual
        >>> project = XMLManager.from_xml(xml_string)
        >>> text = PLCOpenConverter.diagram_to_textual_notation(project)
        >>> # Textual → XML
        >>> xml_out = converter.convert_to_plcopen(text, "REGENERATED")
    """

    @staticmethod
    def diagram_to_textual_notation(project: Project) -> str:
        """
        Convert PLCOpen TC6 Project to textual notation (reverse conversion).

        Extracts variables, functions, function blocks, and connections from
        a PLCOpen Project object and formats them as structured text sections.

        Useful for:
            - Inspecting LLM-generated control logic
            - Creating test fixtures
            - Debugging conversion pipeline
            - Round-trip validation

        Args:
            project: PLCOpen Project object (from XMLManager.from_xml())

        Returns:
            Multi-line string with section-delimited textual notation

        Example:
            >>> project = XMLManager.from_xml(xml_content)
            >>> text = PLCOpenConverter.diagram_to_textual_notation(project)
            >>> print(text)
            * Variables *
            TI_101_PV : REAL
            ...
        """
        tn = ""
        
        # Process each POU in the project
        if project.types and project.types.pous and project.types.pous.pou:
            for pou in project.types.pous.pou:
                
                tn += "* Variables *\n"
                # Extract variables from interface, excluding function block instances
                fb_instance_names = VariableExtractor.get_function_block_instance_names(pou)
                if pou.interface:
                    var_lists = [
                        pou.interface.local_vars,
                        pou.interface.input_vars,
                        pou.interface.output_vars,
                        pou.interface.in_out_vars
                    ]
                    for var_list_container in var_lists:
                        if var_list_container:
                            for var_list in var_list_container:
                                if hasattr(var_list, 'variable'):
                                    for var in var_list.variable:
                                        if (var.name not in fb_instance_names and
                                            not DataTypeHelper.is_function_block_type(var.type_value)):
                                            var_type = DataTypeHelper.get_type_name(var.type_value)
                                            tn += f"{var_type} {var.name}\n"
                tn += "\n"
                
                # Extract Functions and Function Blocks from body
                functions, function_blocks = FunctionExtractor.extract_functions_and_blocks(pou)
                
                tn += "* Functions *\n"
                for func in functions:
                    tn += f"{func}\n"
                tn += "\n"
                
                tn += "* Function Blocks *\n"
                for fb in function_blocks:
                    tn += f"{fb}\n"
                tn += "\n"
                
                # Extract Data Connections and Parameter Connections from FBD body
                extractor = ConnectionExtractor(pou)
                data_connections, param_connections = extractor.extract_all_connections()
                
                tn += "* Data Connections *\n"
                for conn in data_connections:
                    tn += f"{conn}\n"
                tn += "\n"
                
                tn += "* Parameter Data Connections *\n"
                for conn in param_connections:
                    tn += f"{conn}\n"
                tn += "\n"
        
        return tn
    
    @staticmethod
    def textual_notation_to_diagram(textual_notation: str, pou_name: str = "GeneratedPOU", 
                                   library_pous: List['ProjectTypesPousPou'] = None) -> Project:
        """Convert textual notation back to a PLCOpen TC6 Project."""
        print("Creating PLCOpen project from textual notation...")
        
        # Parse the textual notation into sections
        sections = TextualNotationParser.parse(textual_notation)
        
        # Build the project with library POUs
        builder = ProjectBuilder(pou_name, library_pous)
        project = builder.build_project(sections)
        
        return project


def _apply_autolayout(xml_content: str, layout_config: Optional[Dict] = None, target_pou_name: str = None) -> str:
    """
    Apply auto-layout to FBD XML content if auto-layout is available.
    
    Args:
        xml_content: The XML content to layout
        layout_config: Optional dictionary with layout parameters
        target_pou_name: Name of the POU being processed (for targeting specific FBDs)
        
    Returns:
        str: The XML content with auto-layout applied, or original content if auto-layout fails
    """
    if not AUTOLAYOUT_AVAILABLE:
        print("Auto-layout not available, skipping layout optimization")
        return xml_content
    
    try:
        # Set default layout configuration using module constants
        default_config = {
            'x_gap': DEFAULT_LAYOUT_X_GAP,
            'y_gap': DEFAULT_LAYOUT_Y_GAP,
            'left_margin': DEFAULT_LAYOUT_LEFT_MARGIN,
            'top_margin': DEFAULT_LAYOUT_TOP_MARGIN
        }
        
        # Merge user config with defaults
        if layout_config:
            default_config.update(layout_config)
        
        print(f"Applying auto-layout with config: {default_config}")
        layouted_xml = autolayout_fbd(
            xml_content,
            x_gap=default_config['x_gap'],
            y_gap=default_config['y_gap'],
            left_margin=default_config['left_margin'],
            top_margin=default_config['top_margin'],
            target_pou_name=target_pou_name
        )
        
        print("Auto-layout applied successfully")
        return layouted_xml
        
    except Exception as e:
        print(f"Warning: Auto-layout failed, using original layout: {e}")
        return xml_content


class XMLManager:
    """Handles XML file operations and validation."""
    
    @staticmethod
    def load_project_from_xml(xml_file_path: str) -> Project:
        """Load a PLCOpen TC6 project from an XML file."""
        config = ParserConfig()
        context = XmlContext()
        parser = XmlParser(context=context, config=config)
        
        return parser.parse(xml_file_path, Project)
    
    @staticmethod
    def save_project_to_xml(project: Project, xml_file_path: str, enable_autolayout: bool = True, layout_config: Optional[Dict] = None, target_pou_name: str = None):
        """Save a PLCOpen TC6 project to an XML file without namespace prefixes with optional auto-layout."""
        from xsdata.formats.dataclass.serializers import XmlSerializer
        from xsdata.formats.dataclass.serializers.config import SerializerConfig
        import re
        import xml.etree.ElementTree as ET
        import pathlib
        
        # Configure serializer for clean output
        config = SerializerConfig(
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8"
        )
        
        serializer = XmlSerializer(config=config)
        xml_content = serializer.render(project)
        
        # Clean up namespace prefixes
        xml_content = re.sub(r'ns0:', '', xml_content)
        xml_content = re.sub(
            r'<project xmlns:ns0="http://www\.plcopen\.org/xml/tc6_0201">',
            '<project xmlns="http://www.plcopen.org/xml/tc6_0201">',
            xml_content
        )
        xml_content = re.sub(r' xmlns:ns0="[^"]*"', '', xml_content)
        
        # Apply auto-layout if enabled
        if enable_autolayout:
            xml_content = _apply_autolayout(xml_content, layout_config, target_pou_name)
        
        # Save the XML content to file
        with open(xml_file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        # Basic XML structure validation
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            print("[OK] XML file generated successfully!")
            print(f"Root element: {root.tag}")
            
            # Check for instances element
            instances = root.find('.//{http://www.plcopen.org/xml/tc6_0201}instances')
            print(f"Has instances: {instances is not None}")
            
            # Try advanced XSD validation if lxml is available
            XMLManager._validate_with_xsd(xml_file_path)
                    
        except Exception as e:
            print(f"\n[ERROR] Failed to save PLCOpen XML project.")
            print(f"        Error: {e}")
            print(f"        File: {xml_file_path}")
            print(f"        Troubleshooting:")
            print(f"        - Verify file path is writable")
            print(f"        - Check project structure is valid")
            print(f"        - Ensure all required libraries are installed")
            raise
    
    @staticmethod
    def _validate_with_xsd(xml_file_path: str):
        """Validate XML against XSD schema if lxml is available."""
        try:
            from lxml import etree
            print(f"Validating generated XML against PLCOpen TC6 XSD schema...")
            
            # Load the XSD schema
            xsd_file = pathlib.Path(__file__).parent / "tc6_xml_v201.xsd"
            if not xsd_file.exists():
                print(f"\n⚠️  Warning: XSD schema file not found at {xsd_file}")
                print(f"           Skipping detailed schema validation.")
                print(f"           To enable validation: Place tc6_xml_v201.xsd in src/ directory")
                return
                
            with open(xsd_file, 'r', encoding='utf-8') as f:
                schema_doc = etree.parse(f)
            schema = etree.XMLSchema(schema_doc)
            
            # Parse the generated XML
            xml_doc = etree.parse(xml_file_path)
            
            # Validate
            if schema.validate(xml_doc):
                print("\n✓ [OK] XML validation successful!")
                print("       Generated XML is compliant with PLCOpen TC6 XSD schema.")
            else:
                print("\n✗ [ERROR] XML validation failed!")
                print("  Validation errors found:")
                for error in schema.error_log:
                    print(f"  • Line {error.line}: {error.message}")
                print("\n  Troubleshooting:")
                print("  - Check textual notation syntax")
                print("  - Verify all block types are valid PLCOpen types")
                print("  - Ensure connections reference existing elements")
                    
        except ImportError:
            print("[WARNING] Note: lxml library not available for detailed XSD validation.")
            print("    The XML structure is valid but detailed schema validation was skipped.")
        except Exception as e:
            print(f"[WARNING] XSD validation failed with error: {e}")


# Convenience functions for backward compatibility
def diagram_to_textual_notation(project: Project) -> str:
    """Convenience function for backward compatibility."""
    return PLCOpenConverter.diagram_to_textual_notation(project)


def textual_notation_to_diagram(textual_notation: str, pou_name: str = "GeneratedPOU", 
                               library_pous: List['ProjectTypesPousPou'] = None) -> Project:
    """Convenience function for backward compatibility."""
    return PLCOpenConverter.textual_notation_to_diagram(textual_notation, pou_name, library_pous)


def load_project_from_xml(xml_file_path: str) -> Project:
    """Convenience function for backward compatibility."""
    return XMLManager.load_project_from_xml(xml_file_path)


def save_project_to_xml(project: Project, xml_file_path: str, enable_autolayout: bool = True, layout_config: Optional[Dict] = None, target_pou_name: str = None):
    """Convenience function for backward compatibility."""
    return XMLManager.save_project_to_xml(project, xml_file_path, enable_autolayout, layout_config, target_pou_name)


def create_project_with_libraries(textual_notation: str, pou_name: str = "GeneratedPOU", 
                                 library_paths: List[pathlib.Path] = None) -> Project:
    """
    Create a PLCOpen project from textual notation and include POUs from library files or directories.
    
    Args:
        textual_notation: The textual notation to convert
        pou_name: Name for the main POU
        library_paths: List of library paths (directories or XML files) to include
        
    Returns:
        Project with main POU and library POUs included
    """
    library_pous = []
    
    if library_paths:
        for library_path in library_paths:
            try:
                pous = add_library(library_path)
                library_pous.extend(pous)
                if library_path.is_dir():
                    print(f"Added {len(pous)} POUs from library directory {library_path.name}")
                else:
                    print(f"Added {len(pous)} POUs from library file {library_path.name}")
            except Exception as e:
                print(f"Failed to load library {library_path}: {e}")
    
    return textual_notation_to_diagram(textual_notation, pou_name, library_pous)


def test_round_trip():
    """Test the round-trip conversion: XML -> textual notation -> XML."""
    print("Testing round-trip conversion...")
    
    # Load original XML and convert to textual notation
    xml_file = pathlib.Path(__file__).parent / "files" / "Traffic_Light_FBD.xml"
    if xml_file.exists():
        try:
            # XML to textual notation
            project = load_project_from_xml(str(xml_file))
            textual_notation = diagram_to_textual_notation(project)
            print("Original textual notation:")
            print("=" * 50)
            print(textual_notation)
            
            # Parse the textual notation to show the structured data
            print("\nParsed textual notation structure:")
            print("=" * 50)
            sections = TextualNotationParser.parse(textual_notation)
            for section_name in ['variables', 'functions', 'function_blocks', 'data_connections', 'parameter_connections']:
                items = getattr(sections, section_name)
                if items:
                    print(f"{section_name.upper()}:")
                    for item in items[:3]:  # Show first 3 items
                        print(f"  {item}")
                    if len(items) > 3:
                        print(f"  ... and {len(items) - 3} more")
                    print()
            
            # Textual notation back to XML (simplified)
            print("Attempting to convert back to XML...")
            print("=" * 50)
            new_project = textual_notation_to_diagram(textual_notation, "RoundTripTest")
            
            save_project_to_xml(new_project, str(xml_file.parent / "RoundTripTest.xml"))
            save_project_to_xml(new_project, "C:\\Users\\DETHBRA1\\OpenPLC_Editor\\editor\\examples\\Traffic_Light_FBD\\plc.xml")
            
            if new_project:
                print(f"Round-trip conversion completed")
                print(f"Created Project with file_header: {new_project.file_header.product_name}")
                print(f"Created Project with content_header: {new_project.content_header.name}")
            
        except Exception as e:
            print(f"Error in round-trip test: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Test XML file not found: {xml_file}")

def add_library_file(library_file: pathlib.Path) -> List['ProjectTypesPousPou']:
    """
    Parse a single library XML file containing one POU element and return a list with the POU object.
    
    Args:
        library_file: Path to the XML library file containing a single <pou> element
        
    Returns:
        List containing the ProjectTypesPousPou object parsed from the library file
        
    Raises:
        FileNotFoundError: If the library file doesn't exist
        ET.ParseError: If the XML file is malformed
        Exception: For other parsing errors
    """
    if not library_file.exists():
        raise FileNotFoundError(f"Library file not found: {library_file}")
    
    try:
        # Read the XML file as text first to handle namespace issues
        with open(library_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Add missing namespace declarations if needed
        if 'xmlns:xhtml' not in xml_content and 'xhtml:' in xml_content:
            # Insert xhtml namespace declaration
            if '<pou' in xml_content:
                xml_content = xml_content.replace(
                    '<pou', 
                    '<pou xmlns:xhtml="http://www.w3.org/1999/xhtml"'
                )
        
        # Parse the XML content using ElementTree
        root = ET.fromstring(xml_content)
        
        # Ensure we have a single POU element
        if root.tag != 'pou':
            print(f"Warning: Root element is not <pou> in {library_file}")
            return []
        
        pou_name = root.get('name', 'Unknown')
        # print(f"Loading POU '{pou_name}' from library file: {library_file}")
        
        # Configure XML parser for PLCOpen objects
        config = ParserConfig()
        context = XmlContext()
        parser = XmlParser(context=context, config=config)
        
        try:
            # Convert ElementTree element to string and parse with xsdata
            pou_xml_str = ET.tostring(root, encoding='unicode')
            
            # Add PLCOpen namespace and other necessary namespaces if not present
            if 'xmlns=' not in pou_xml_str:
                # Add both PLCOpen and xhtml namespaces
                pou_xml_str = pou_xml_str.replace(
                    '<pou', 
                    '<pou xmlns="http://www.plcopen.org/xml/tc6_0201" xmlns:xhtml="http://www.w3.org/1999/xhtml"'
                )
            
            # Parse the POU XML string into a ProjectTypesPousPou object
            from io import BytesIO
            pou_obj = parser.parse(BytesIO(pou_xml_str.encode('utf-8')), ProjectTypesPousPou)
            
            if pou_obj:
                # print(f"Successfully parsed POU: {pou_obj.name} (type: {pou_obj.pou_type})")
                return [pou_obj]
            else:
                print(f"Warning: Failed to parse POU element from {library_file}")
                return []
                
        except Exception as e:
            print(f"Error parsing POU '{pou_name}' from {library_file}: {e}")
            traceback.print_exc()
            return []
        
    except ET.ParseError as e:
        print(f"XML parsing error in library file {library_file}: {e}")
        raise
    except Exception as e:
        print(f"Error loading library file {library_file}: {e}")
        traceback.print_exc()
        raise


def add_library(library_path: pathlib.Path) -> List['ProjectTypesPousPou']:
    """
    Parse library XML files from a directory or single file containing POU elements.
    
    Args:
        library_path: Path to either:
                     - A directory containing XML files with individual POUs (new structure)
                     - A single XML file containing multiple POUs (legacy structure)
        
    Returns:
        List of ProjectTypesPousPou objects parsed from the library files
        
    Raises:
        FileNotFoundError: If the library path doesn't exist
        Exception: For other parsing errors
    """
    if not library_path.exists():
        raise FileNotFoundError(f"Library path not found: {library_path}")
    
    pou_objects = []
    
    if library_path.is_dir():
        # New structure: directory with individual XML files
        print(f"Loading library from directory: {library_path}")
        
        # Look for XML files in the directory
        xml_files = list(library_path.glob("*.xml"))
        if not xml_files:
            print(f"Warning: No XML files found in directory {library_path}")
            return []
        
        print(f"Found {len(xml_files)} XML file(s) in library directory")
        
        for xml_file in xml_files:
            try:
                pous = add_library_file(xml_file)
                pou_objects.extend(pous)
            except Exception as e:
                print(f"Failed to load POU from {xml_file}: {e}")
                continue
                
    elif library_path.is_file():
        # Legacy structure: single XML file with multiple POUs
        print(f"Loading library from single file: {library_path}")
        
        try:
            # Read the XML file as text first to handle namespace issues
            with open(library_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Add missing namespace declarations if needed
            if 'xmlns:xhtml' not in xml_content and 'xhtml:' in xml_content:
                # Insert xhtml namespace declaration
                if '<pou' in xml_content:
                    xml_content = xml_content.replace(
                        '<pou', 
                        '<pou xmlns:xhtml="http://www.w3.org/1999/xhtml"'
                    )
            
            # Wrap multiple POU elements in a root element if needed
            if xml_content.strip().startswith('<pou') and xml_content.count('<pou') > 1:
                xml_content = f'<library>{xml_content}</library>'
            elif xml_content.strip().startswith('<pou') and xml_content.count('<pou') == 1:
                # Single POU - keep as is but ensure proper namespace
                pass
            
            # Parse the XML content using ElementTree
            root = ET.fromstring(xml_content)
            
            # Check if root is a single POU or contains multiple POUs
            pou_elements = []
            if root.tag == 'pou':
                pou_elements = [root]
            else:
                # Look for POU elements in the root
                pou_elements = root.findall('.//pou')
            
            if not pou_elements:
                print(f"Warning: No <pou> elements found in {library_path}")
                return []
            
            print(f"Found {len(pou_elements)} POU(s) in library file: {library_path}")
            
            # Configure XML parser for PLCOpen objects
            config = ParserConfig()
            context = XmlContext()
            parser = XmlParser(context=context, config=config)
            
            for pou_element in pou_elements:
                try:
                    # Convert ElementTree element to string and parse with xsdata
                    pou_xml_str = ET.tostring(pou_element, encoding='unicode')
                    
                    # Add PLCOpen namespace and other necessary namespaces if not present
                    if 'xmlns=' not in pou_xml_str:
                        # Add both PLCOpen and xhtml namespaces
                        pou_xml_str = pou_xml_str.replace(
                            '<pou', 
                            '<pou xmlns="http://www.plcopen.org/xml/tc6_0201" xmlns:xhtml="http://www.w3.org/1999/xhtml"'
                        )
                    
                    # Parse the POU XML string into a ProjectTypesPousPou object
                    from io import BytesIO
                    pou_obj = parser.parse(BytesIO(pou_xml_str.encode('utf-8')), ProjectTypesPousPou)
                    
                    if pou_obj:
                        pou_objects.append(pou_obj)
                        print(f"Successfully parsed POU: {pou_obj.name} (type: {pou_obj.pou_type})")
                    else:
                        print(f"Warning: Failed to parse POU element")
                        
                except Exception as e:
                    pou_name = pou_element.get('name', 'Unknown')
                    print(f"Error parsing POU '{pou_name}': {e}")
                    traceback.print_exc()
                    continue
                    
        except ET.ParseError as e:
            print(f"XML parsing error in library file {library_path}: {e}")
            raise
        except Exception as e:
            print(f"Error loading library file {library_path}: {e}")
            traceback.print_exc()
            raise
    
    print(f"Successfully loaded {len(pou_objects)} POU(s) from library")
    return pou_objects


def export_to_openplc(project: str, application: str, export_path: str, content: str = None, 
                      enable_autolayout: bool = True, layout_config: Optional[Dict] = None) -> dict:
    """
    Export control logic to OpenPLC format.
    
    Args:
        project: Project name (used for POU naming)
        application: Application name (used for project metadata)
        export_path: Directory path where plc.xml should be created/updated
        content: Optional textual notation content to process (for future use)
        enable_autolayout: Whether to apply auto-layout optimization to FBD diagrams (default: True)
        layout_config: Optional dictionary with layout parameters (x_gap, y_gap, left_margin, top_margin)
        
    Returns:
        dict: Export result with status information
        
    Raises:
        FileNotFoundError: If export_path directory doesn't exist
        PermissionError: If unable to write to export_path
        Exception: For other processing errors
    """
    try:
        # Validate and create export path
        export_dir = pathlib.Path(export_path)
        if not export_dir.exists():
            print(f"Creating export directory: {export_dir}")
            export_dir.mkdir(parents=True, exist_ok=True)
        elif not export_dir.is_dir():
            raise ValueError(f"Export path exists but is not a directory: {export_path}")
        
        # Locate or create plc.xml file
        plc_xml_path = export_dir / "plc.xml"
        
        # Handle existing or new plc.xml file
        existing_project = None
        backup_path = None
        
        if plc_xml_path.exists():
            print(f"Found existing plc.xml at: {plc_xml_path}")
            # Create backup before modification
            backup_path = export_dir / f"plc_backup_{int(time.time())}.xml"
            shutil.copy2(plc_xml_path, backup_path)
            print(f"Created backup at: {backup_path}")
            
            # Load existing project
            try:
                existing_project = XMLManager.load_project_from_xml(str(plc_xml_path))
                print(f"Loaded existing project with {len(existing_project.types.pous.pou) if existing_project.types and existing_project.types.pous and existing_project.types.pous.pou else 0} POUs")
            except Exception as e:
                print(f"Warning: Could not load existing project: {e}")
                print("Will create new project instead")
                existing_project = None
        else:
            print(f"Creating new plc.xml at: {plc_xml_path}")
        
        # Set up library paths - use the same library directory as main function
        library_dir = pathlib.Path(__file__).parents[1] / "data" / "BASIC_LIB" / "src"
        library_paths = []
        
        # Load libraries if available
        if library_dir.exists():
            library_paths = [library_dir]
            print(f"Using library directory: {library_dir}")
        else:
            print("Warning: BASIC_LIB library directory not found, proceeding without libraries")
        
        # Process content and create/update OpenPLC project
        if content and content.strip():
            print("Processing textual notation content for OpenPLC export...")
            
            try:
                # Parse the textual notation into sections
                sections = TextualNotationParser.parse(content)
                
                if existing_project:
                    # Update existing project
                    print("Updating existing PLCOpen project...")
                    plc_project = _update_existing_project(existing_project, sections, application, project, library_paths)
                else:
                    # Create new project
                    print("Creating new PLCOpen project from textual notation...")
                    
                    # Load libraries if needed
                    library_pous = []
                    if library_paths:
                        for library_path in library_paths:
                            try:
                                pous = add_library(library_path)
                                library_pous.extend(pous)
                                if library_path.is_dir():
                                    print(f"Added {len(pous)} POUs from library directory {library_path.name}")
                                else:
                                    print(f"Added {len(pous)} POUs from library file {library_path.name}")
                            except Exception as e:
                                print(f"Failed to load library {library_path}: {e}")
                    
                    # Build the project with proper naming: POU name = application, project name = project
                    builder = ProjectBuilder(application, library_pous, project, existing_project)
                    plc_project = builder.build_project(sections)
                
                # Save the project to plc.xml with proper error handling
                try:
                    XMLManager.save_project_to_xml(plc_project, str(plc_xml_path), enable_autolayout, layout_config, application)
                    print(f"Successfully created OpenPLC project with {len(plc_project.types.pous.pou)} POUs")
                    
                    # Log POU information
                    for pou in plc_project.types.pous.pou:
                        print(f"  - {pou.name} ({pou.pou_type})")
                        
                except UnicodeEncodeError as ue:
                    print(f"Unicode encoding error during XML serialization: {str(ue)}")
                    print("This may be due to special characters in console output. The XML file should still be created correctly.")
                    # Check if file was actually created despite the error
                    if plc_xml_path.exists():
                        print(f"XML file was successfully created at: {plc_xml_path}")
                    else:
                        raise Exception("XML file creation failed due to encoding issues")
                    
            except Exception as e:
                print(f"Error during content conversion: {str(e)}")
                # Fall back to minimal project creation
                print("Falling back to minimal project creation...")
                if not plc_xml_path.exists():
                    _create_minimal_plc_project(plc_xml_path, project, application, enable_autolayout, layout_config)
                # Re-raise the exception to be handled by the caller
                raise Exception(f"Content conversion failed: {str(e)}")
        else:
            # No content provided, create minimal placeholder project
            print("No content provided, creating minimal placeholder project...")
            if not plc_xml_path.exists():
                _create_minimal_plc_project(plc_xml_path, project, application, enable_autolayout, layout_config)
        
        # Determine the final status and message
        if content and content.strip():
            final_message = f"OpenPLC export completed successfully for project '{project}' in application '{application}'"
            status = "conversion_completed"
        else:
            final_message = f"OpenPLC export prepared with minimal project for '{project}' in application '{application}'"
            status = "minimal_project_created"
        
        return {
            "success": True,
            "message": final_message,
            "export_path": str(export_dir),
            "plc_xml_path": str(plc_xml_path),
            "plc_xml_exists": plc_xml_path.exists(),
            "created_backup": backup_path is not None and backup_path.exists() if backup_path else False,
            "backup_path": str(backup_path) if backup_path else None,
            "content_processed": bool(content and content.strip()),
            "library_loaded": bool(library_paths),
            "library_path": str(library_dir) if library_dir.exists() else None,
            "autolayout_enabled": enable_autolayout,
            "autolayout_available": AUTOLAYOUT_AVAILABLE,
            "layout_config": layout_config,
            "status": status
        }
        
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": f"Export path not found: {str(e)}",
            "export_path": export_path
        }
    except PermissionError as e:
        return {
            "success": False,
            "error": f"Permission denied writing to export path: {str(e)}",
            "export_path": export_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"OpenPLC export failed: {str(e)}",
            "export_path": export_path
        }


def _update_existing_project(existing_project: Project, sections: ParsedSections, application_name: str, project_name: str, library_paths: List[pathlib.Path]) -> Project:
    """
    Update an existing PLCOpen project by replacing/adding a POU with the given application_name.
    Preserves existing library POUs to avoid duplication.
    """
    print(f"Updating project with POU: {application_name}")
    
    # Load new libraries if needed (but only those not already present)
    new_library_pous = []
    if library_paths:
        # Get existing POU names to avoid duplication
        existing_pou_names = set()
        if existing_project.types and existing_project.types.pous and existing_project.types.pous.pou:
            existing_pou_names = {pou.name for pou in existing_project.types.pous.pou if pou.name}
        
        for library_path in library_paths:
            try:
                pous = add_library(library_path)
                # Only add POUs that don't already exist
                added_count = 0
                skipped_count = 0
                for pou in pous:
                    if pou.name not in existing_pou_names:
                        new_library_pous.append(pou)
                        existing_pou_names.add(pou.name)
                        added_count += 1
                    else:
                        skipped_count += 1
                if added_count > 0 or skipped_count > 0:
                    print(f"Library: added {added_count} new POUs, skipped {skipped_count} existing POUs")
            except Exception as e:
                print(f"Failed to load library {library_path}: {e}")
    
    # Create the new POU from sections
    builder = ProjectBuilder(application_name, [], project_name, existing_project)  # Pass existing project for unique ID generation
    temp_project = builder.build_project(sections)
    
    if not temp_project.types or not temp_project.types.pous or not temp_project.types.pous.pou:
        raise ValueError("Failed to create POU from textual notation")
    
    new_pou = temp_project.types.pous.pou[0]  # Get the main POU
    print(f"Created new POU: {new_pou.name}")
    
    # Find and replace existing POU with same name, or add new one
    pou_replaced = False
    if existing_project.types and existing_project.types.pous and existing_project.types.pous.pou:
        for i, existing_pou in enumerate(existing_project.types.pous.pou):
            if existing_pou.name == application_name:
                print(f"Replacing existing POU: {application_name}")
                existing_project.types.pous.pou[i] = new_pou
                pou_replaced = True
                break
    
    if not pou_replaced:
        print(f"Adding new POU: {application_name}")
        if not existing_project.types:
            existing_project.types = ProjectTypes()
        if not existing_project.types.pous:
            existing_project.types.pous = ProjectTypesPous()
        if not existing_project.types.pous.pou:
            existing_project.types.pous.pou = []
        existing_project.types.pous.pou.append(new_pou)
    
    # Add new library POUs
    if new_library_pous:
        existing_project.types.pous.pou.extend(new_library_pous)
        print(f"Added {len(new_library_pous)} new library POUs")
    
    # Update project metadata
    if existing_project.content_header:
        existing_project.content_header.name = project_name
        existing_project.content_header.modification_date_time = "2025-01-30T12:00:00"
    
    # Update or add instance for the new/updated POU
    _update_project_instances(existing_project, application_name)
    
    print(f"Project updated with {len(existing_project.types.pous.pou)} total POUs")
    return existing_project


def _update_project_instances(project: Project, application_name: str):
    """Update or add project instances for the given application POU."""
    if not project.instances:
        project.instances = ProjectInstances()
    if not project.instances.configurations:
        project.instances.configurations = ProjectInstancesConfigurations()
    if not project.instances.configurations.configuration:
        project.instances.configurations.configuration = []
    
    # Find or create default configuration
    config = None
    for conf in project.instances.configurations.configuration:
        if conf.name == "Config0":
            config = conf
            break
    
    if not config:
        config = ProjectInstancesConfigurationsConfiguration(name="Config0")
        project.instances.configurations.configuration.append(config)
    
    # Find or create default resource
    if not config.resource:
        config.resource = []
    
    resource = None
    for res in config.resource:
        if res.name == "Res0":
            resource = res
            break
    
    if not resource:
        resource = ProjectInstancesConfigurationsConfigurationResource(name="Res0")
        config.resource.append(resource)
    
    # Find or create default task
    if not resource.task:
        resource.task = []
    
    task = None
    for t in resource.task:
        if t.name == "task0":
            task = t
            break
    
    if not task:
        task = ProjectInstancesConfigurationsConfigurationResourceTask(
            name="task0",
            priority=0,
            interval="T#20ms"
        )
        resource.task.append(task)
    
    # Update or add POU instance
    if not task.pou_instance:
        task.pou_instance = []
    
    # Check if instance already exists
    instance_found = False
    for instance in task.pou_instance:
        if instance.type_name == application_name:
            print(f"Updated existing POU instance: {instance.name}")
            instance_found = True
            break
    
    if not instance_found:
        # Add new instance
        instance_name = f"instance_{len(task.pou_instance)}"
        new_instance = PouInstance(name=instance_name, type_name=application_name)
        task.pou_instance.append(new_instance)
        print(f"Added new POU instance: {instance_name} for POU: {application_name}")


def _create_minimal_plc_project(plc_xml_path: pathlib.Path, project_name: str, application_name: str, 
                               enable_autolayout: bool = True, layout_config: Optional[Dict] = None):
    """Create a minimal PLCOpen project file as placeholder."""
    # Create a basic project structure
    project = Project()
    
    # Create file header
    project.file_header = ProjectFileHeader(
        company_name="Generated",
        product_name=f"OpenPLC Export - {application_name}",
        product_version="1.0",
        creation_date_time="2025-01-30T12:00:00"
    )
    
    # Create content header
    project.content_header = ProjectContentHeader(
        name=project_name,
        modification_date_time="2025-01-30T12:00:00"
    )
    
    # Create types container with empty POU
    project.types = ProjectTypes()
    project.types.data_types = ProjectTypesDataTypes()
    project.types.pous = ProjectTypesPous()
    
    # Create a minimal POU
    pou = ProjectTypesPousPou(name=application_name, pou_type="program")
    project.types.pous.pou = [pou]
    
    # Create instances section
    project.instances = ProjectInstances()
    project.instances.configurations = ProjectInstancesConfigurations()
    
    # Create default configuration
    config = ProjectInstancesConfigurationsConfiguration(name="Config0")
    resource = ProjectInstancesConfigurationsConfigurationResource(name="Res0")
    task = ProjectInstancesConfigurationsConfigurationResourceTask(
        name="task0",
        priority=0,
        interval="T#20ms"
    )
    
    pou_instance = PouInstance(name="instance0", type_name=application_name)
    task.pou_instance = [pou_instance]
    resource.task = [task]
    config.resource = [resource]
    project.instances.configurations.configuration = [config]
    
    # Save the project
    XMLManager.save_project_to_xml(project, str(plc_xml_path), enable_autolayout, layout_config, application_name)
    print(f"Created minimal PLCOpen project at: {plc_xml_path}")