#!/usr/bin/env python3
import argparse
import csv
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom


def parse_csv_spec(csv_file_path):
    """Parse CSV specification file and extract inputs/outputs."""
    inputs = []
    outputs = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Process lines manually to handle malformed CSV
    lines = content.strip().split('\n')
    
    # Skip header
    for i, line in enumerate(lines[1:], 1):
        # Handle cases where there might be multiple entries on one line
        # Split by common patterns that indicate a new entry
        entries = []
        
        # Check if line contains multiple entries (e.g., "Input,PV_Low,REAL,Low alarm limit for PV.")
        if line.count('Input,') > 1 or line.count('Output,') > 1:
            # Split on Input/Output markers
            parts = line.replace(' Output,', '|Output,').replace(' Input,', '|Input,').split('|')
            for part in parts:
                if part.strip():
                    entries.append(part.strip())
        else:
            entries = [line]
        
        for entry in entries:
            # Parse CSV fields
            fields = entry.split(',')
            if len(fields) >= 4:
                direction = fields[0].strip()
                pin_name = fields[1].strip()
                pin_type = fields[2].strip().upper()
                # Join remaining fields as description (in case description has commas)
                description = ','.join(fields[3:]).strip()
                
                pin_info = {
                    'name': pin_name,
                    'type': pin_type,
                    'description': description
                }
                
                if direction.lower() == 'input':
                    inputs.append(pin_info)
                elif direction.lower() == 'output':
                    outputs.append(pin_info)
    
    return inputs, outputs


def create_variable_element(name, type_str):
    """Create a variable XML element."""
    variable = ET.Element('variable', name=name)
    type_elem = ET.SubElement(variable, 'type')
    
    # Map types to XML elements
    if type_str == 'STRING':
        ET.SubElement(type_elem, 'string')
    elif type_str == 'REAL':
        ET.SubElement(type_elem, 'REAL')
    elif type_str == 'BOOL':
        ET.SubElement(type_elem, 'BOOL')
    elif type_str == 'INT':
        ET.SubElement(type_elem, 'INT')
    elif type_str == 'DINT':
        ET.SubElement(type_elem, 'DINT')
    elif type_str == 'WORD':
        ET.SubElement(type_elem, 'WORD')
    elif type_str == 'DWORD':
        ET.SubElement(type_elem, 'DWORD')
    else:
        # Default to string for unknown types
        ET.SubElement(type_elem, 'string')
    
    return variable


def create_pou_xml(block_name, inputs, outputs):
    """Create POU (Program Organization Unit) XML structure."""
    # Create root POU element
    pou = ET.Element('pou', name=block_name, pouType='functionBlock')
    
    # Create interface
    interface = ET.SubElement(pou, 'interface')
    
    # Add input variables
    if inputs:
        input_vars = ET.SubElement(interface, 'inputVars')
        for inp in inputs:
            var = create_variable_element(inp['name'], inp['type'])
            input_vars.append(var)
    
    # Add output variables
    if outputs:
        output_vars = ET.SubElement(interface, 'outputVars')
        for out in outputs:
            var = create_variable_element(out['name'], out['type'])
            output_vars.append(var)
    
    # Add empty body with ST (Structured Text)
    body = ET.SubElement(pou, 'body')
    st = ET.SubElement(body, 'ST')
    xhtml_p = ET.SubElement(st, '{http://www.w3.org/1999/xhtml}p')
    xhtml_p.text = ''  # CDATA will be added in prettify
    
    return pou


def format_xml_output(elem):
    """Format XML output to match expected PLCOpen structure."""
    # Build the XML string manually for precise formatting
    lines = []
    lines.append('      <pou name="{}" pouType="functionBlock">'.format(elem.get('name')))
    lines.append('        <interface>')
    
    # Find inputVars and outputVars
    interface = elem.find('interface')
    
    # Process input variables
    input_vars = interface.find('inputVars')
    if input_vars is not None:
        lines.append('          <inputVars>')
        for var in input_vars.findall('variable'):
            var_name = var.get('name')
            lines.append('            <variable name="{}">'.format(var_name))
            lines.append('              <type>')
            
            # Get the type element
            type_elem = var.find('type')
            for child in type_elem:
                type_tag = child.tag
                lines.append('                <{}/>'.format(type_tag))
            
            lines.append('              </type>')
            lines.append('            </variable>')
        lines.append('          </inputVars>')
    
    # Process output variables
    output_vars = interface.find('outputVars')
    if output_vars is not None:
        lines.append('          <outputVars>')
        for var in output_vars.findall('variable'):
            var_name = var.get('name')
            lines.append('            <variable name="{}">'.format(var_name))
            lines.append('              <type>')
            
            # Get the type element
            type_elem = var.find('type')
            for child in type_elem:
                type_tag = child.tag
                lines.append('                <{}/>'.format(type_tag))
            
            lines.append('              </type>')
            lines.append('            </variable>')
        lines.append('          </outputVars>')
    
    lines.append('        </interface>')
    lines.append('        <body>')
    lines.append('          <ST>')
    lines.append('            <xhtml:p><![CDATA[]]></xhtml:p>')
    lines.append('          </ST>')
    lines.append('        </body>')
    lines.append('      </pou>')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Convert CSV specification files to PLCOpen XML format'
    )
    parser.add_argument(
        'input_file',
        help='Input CSV file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output XML file path (default: same name as input with .xml extension)',
        default=None
    )
    parser.add_argument(
        '-n', '--name',
        help='Function block name (default: derived from input filename)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Determine output file path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.xml')
    
    # Determine block name
    if args.name:
        block_name = args.name
    else:
        block_name = input_path.stem.upper()
    
    try:
        # Parse CSV file
        print(f"Reading CSV file: {input_path}")
        inputs, outputs = parse_csv_spec(input_path)
        
        print(f"Found {len(inputs)} inputs and {len(outputs)} outputs")
        
        # Create XML structure
        pou_elem = create_pou_xml(block_name, inputs, outputs)
        
        # Generate formatted XML string
        xml_content = format_xml_output(pou_elem)
        
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"Successfully created XML file: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()