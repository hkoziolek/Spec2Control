# Copyright (c) 2025 Spec2Control Project Contributors
#
# This file is part of Spec2Control, an open-source tool for automating
# PLC/DCS control logic engineering from natural language specifications.
#
# For license information, see the LICENSE file in the project root.
# For contributing guidelines, see CONTRIBUTING.md in the project root.
#
# Project Repository: https://github.com/hkoziolek/Spec2Control

"""
Automatic Layout Engine for IEC 61131-3 Function Block Diagrams (FBD)

This module provides intelligent automatic layout for PLCOpen TC6 XML Function Block Diagrams,
with specialized support for industrial control system semantics defined in IEC 61131-3.

The layout algorithm goes beyond standard graph layout by incorporating domain knowledge about
industrial automation control patterns.

Architecture:
    The layout engine uses a multi-phase approach:
    1. Parse FBD XML into graph representation (nodes + edges)
    2. Classify blocks by industrial semantics (SENSOR, ACTUATOR, CONTROL, GLUE)
    3. Identify satellite elements (variables, constants, parameters)
    4. Break feedback cycles for DAG-based layering
    5. Assign blocks to semantic macro-layers (11-layer system)
    6. Order blocks within layers to minimize crossings
    7. Calculate coordinates with proper spacing
    8. Route edges with orthogonal pathfinding
    9. Update XML with new positions

11-Layer Semantic Positioning System:
    Layer 0:  SENSOR Input Satellites      (variables/constants feeding sensors)
    Layer 1:  SENSORS                       (measurement inputs from field devices)
    Layer 2:  SENSOR Output Satellites      (variables receiving sensor data)
    Layer 3:  GLUE-L                        (preprocessing logic, signal conditioning)
    Layer 4:  CONTROL Input Satellites      (setpoints, tuning parameters)
    Layer 5:  CONTROL                       (PID, ratio, cascade controllers - core logic)
    Layer 6:  CONTROL Output Satellites     (control outputs to variables)
    Layer 7:  GLUE-R                        (postprocessing logic, interlocks)
    Layer 8:  ACTUATOR Input Satellites     (commands to actuators)
    Layer 9:  ACTUATORS                     (valves, motors, final control elements)
    Layer 10: ACTUATOR Output Satellites    (actuator status and feedback)

Key Features:
    - Industrial control semantics awareness (not just graph topology)
    - Satellite positioning (variables/constants near parent blocks)
    - Affinity grouping (keeps related instruments together, e.g., FT_101, FT_102)
    - Two-pass median heuristic for crossing minimization
    - Orthogonal edge routing with collision avoidance
    - PLCOpen TC6 XML namespace handling
    - Cascaded controller support (multi-stage control loops)
    - Fallback to generic layout for non-control diagrams
    - Debug mode with before/after position reporting

Usage Examples:
    Basic usage:
        >>> xml_output = autolayout_fbd(xml_string)

    With custom spacing:
        >>> xml_output = autolayout_fbd(xml_string, x_gap=200, y_gap=50)

    Target specific POU:
        >>> xml_output = autolayout_fbd(xml_string, target_pou_name="MAIN", target_fbd_index=0)

    Disable IEC 61131 layout (use generic):
        >>> xml_output = autolayout_fbd(xml_string, use_iec61131_layout=False)

    Enable debug output:
        >>> xml_output = autolayout_fbd(xml_string, debug=True)

Performance:
    - Typical processing time: <1 second for diagrams with <100 blocks
    - Memory usage: O(n + m) where n=blocks, m=connections
    - Scales to diagrams with 500+ blocks

References:
    [1] PLCOpen TC6 XML Specification v2.01: https://plcopen.org/
    [2] IEC 61131-3 Standard for Programmable Logic Controllers
    [3] Spec2Control: Koziolek et al., "Automating PLC/DCS Control-Logic Engineering
        from Natural Language Requirements with LLMs"
    [4] Sugiyama Framework: "Methods for Visual Understanding of Hierarchical Systems"

Author: Spec2Control Project Contributors
License: See LICENSE file in project root
Repository: https://github.com/hkoziolek/Spec2Control
"""

from lxml import etree
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from copy import deepcopy
import re

# ============================================================================
# Layout Configuration Constants
# ============================================================================

# Default spacing parameters
DEFAULT_X_GAP = 150  # Horizontal spacing between layers (pixels)
DEFAULT_Y_GAP = 40   # Vertical spacing between blocks (pixels)
DEFAULT_LEFT_MARGIN = 50  # Left margin of diagram (pixels)
DEFAULT_TOP_MARGIN = 50   # Top margin of diagram (pixels)

# Satellite positioning parameters
DEFAULT_SATELLITE_GAP_BUFFER = 20  # Minimum gap between layer content and next layer
DEFAULT_SATELLITE_STACK_GAP = 5    # Vertical gap between stacked satellites on same parent
DEFAULT_SATELLITE_ALIGNMENT = 'center'  # Alignment mode: 'center', 'top', or 'bottom'

# Minimum layer widths
MIN_SATELLITE_LAYER_WIDTH = 120  # Minimum width for satellite layers (vars/constants)
MIN_BLOCK_LAYER_WIDTH = 150      # Minimum width for main block layers
BLOCK_WIDTH_PADDING = 20         # Extra padding around blocks in layer

# Edge routing parameters
VERTICAL_CHANNEL_MARGIN = 30      # Margin for vertical routing channels
FEEDBACK_EDGE_CLEARANCE = 50      # Clearance for feedback edges routing around diagram
FEEDBACK_EDGE_MARGIN_BELOW = 40   # Extra margin below diagram for feedback routing

# Collision detection
MIN_BLOCK_SEPARATION = 20         # Minimum separation between adjacent blocks

# ============================================================================
# Core Data Structures
# ============================================================================

@dataclass
class BlockDebugInfo:
    """
    Debug information container for tracking function block position transformations.

    Used to capture before/after coordinates during auto-layout operations, enabling
    verification and debugging of layout algorithms. The print_debug_table() function
    consumes this data to generate formatted comparison reports.

    Attributes:
        block_id: Unique local identifier of the block in the FBD (from localId attribute)
        block_type: Type name of the block (e.g., 'PID_BASIC', 'ANALOG_IN', 'IN_VAR')
        block_name: Instance name or expression (e.g., 'FT_101_AI', 'setpoint_var')
        x_before: X coordinate before auto-layout (pixels)
        y_before: Y coordinate before auto-layout (pixels)
        width_before: Block width before auto-layout (pixels)
        height_before: Block height before auto-layout (pixels)
        x_after: X coordinate after auto-layout (pixels, default 0)
        y_after: Y coordinate after auto-layout (pixels, default 0)
        width_after: Block width after auto-layout (pixels, default 0)
        height_after: Block height after auto-layout (pixels, default 0)

    Example:
        >>> debug_info = BlockDebugInfo(
        ...     block_id="42",
        ...     block_type="PID_BASIC",
        ...     block_name="TIC_101",
        ...     x_before=100, y_before=200,
        ...     width_before=80, height_before=60
        ... )
    """
    block_id: str
    block_type: str
    block_name: str
    x_before: int
    y_before: int
    width_before: int
    height_before: int
    x_after: int = 0
    y_after: int = 0
    width_after: int = 0
    height_after: int = 0

class BlockClassifier:
    """
    Classifier for industrial automation function blocks based on semantic roles.

    This classifier implements domain knowledge from IEC 61131-3 control engineering,
    categorizing function blocks by their role in the control system rather than just
    by programming construct. This enables semantic-aware layout that reflects the
    physical flow of information in industrial processes.

    Classification Categories:
        SENSOR: Input blocks that interface with field measurement devices
            Examples: ANALOG_IN (temperature transmitter), DIGITAL_IN (limit switch)

        ACTUATOR: Output blocks that control final elements in the physical process
            Examples: VALVE_ELECTRIC (control valve), MOTOR_ON_OFF (pump motor)

        CONTROL: Blocks implementing control algorithms and strategies
            Examples: PID_BASIC (PID controller), RATIO_CONTROL (ratio controller)

        GLUE: Logic blocks for signal processing, interlocks, and auxiliary functions
            Examples: AND (boolean logic), ADD (arithmetic), TON (timer)

        VARIABLE: Input/output variables (assigned automatically, not via classification)

        UNKNOWN: Blocks that don't match any known pattern

    Pattern Matching:
        - Exact match against predefined type sets (case-insensitive)
        - Fallback to pattern matching on type name substrings
        - Heuristic: names containing 'INPUT'/'_IN' → SENSOR
        - Heuristic: names containing 'OUTPUT'/'_OUT' → ACTUATOR
        - Heuristic: names containing 'PID'/'CONTROL' → CONTROL

    Thread Safety:
        This class is stateless and thread-safe. All classification is done via
        class methods operating on immutable type sets.

    Example:
        >>> BlockClassifier.classify('PID_BASIC')
        'CONTROL'
        >>> BlockClassifier.classify('ANALOG_IN')
        'SENSOR'
        >>> BlockClassifier.classify('MyCustom_PID_Controller')
        'CONTROL'
    """

    # Sensor block types (field input devices)
    SENSORS = {
        'ANALOG_IN', 'DIGITAL_IN', 'BOOL_IN',
        'ANALOG_INPUT', 'DIGITAL_INPUT', 'BOOL_INPUT'
    }

    # Actuator block types (final control elements)
    ACTUATORS = {
        'VALVE_ELECTRIC', 'VALVE_ON_OFF', 'MOTOR_ON_OFF',
        'MOTOR_2SPD', 'MOTOR_VSD',
        'ANALOG_OUT', 'DIGITAL_OUT', 'BOOL_OUT',
        'ANALOG_OUTPUT', 'DIGITAL_OUTPUT', 'BOOL_OUTPUT'
    }

    # Control strategy block types (algorithms and regulatory loops)
    CONTROL = {
        'PID_BASIC', 'RATIO_CONTROL', 'SPLIT_RANGE',
        'DUTY_STANDBY', 'VOTING_ANALOG',
        'PID', 'PI', 'PD', 'P',
        'CASCADE_CONTROL', 'FEEDFORWARD'
    }

    # Glue logic block types (auxiliary functions, interlocks, calculations)
    GLUE = {
        # Boolean logic
        'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR',
        # Arithmetic
        'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
        # Selection and conversion
        'MUX', 'SEL', 'SCALE', 'LIMIT',
        'MOVE', 'MAX', 'MIN', 'ABS',
        # Comparison
        'GT', 'GE', 'LT', 'LE', 'EQ', 'NE',
        # Timers and counters
        'TON', 'TOF', 'TP', 'CTU', 'CTD', 'CTUD',
        # Flip-flops and edge detection
        'SR', 'RS', 'F_TRIG', 'R_TRIG'
    }

    @classmethod
    def classify(cls, type_name: str) -> str:
        """
        Classify a function block based on its type name.

        Performs case-insensitive matching against known block type sets, with
        fallback to pattern-based classification for custom or vendor-specific blocks.

        Args:
            type_name: The typeName attribute from the function block XML element.
                      Can be None or empty string.

        Returns:
            Classification string: 'SENSOR', 'ACTUATOR', 'CONTROL', 'GLUE', or 'UNKNOWN'

        Classification Logic:
            1. Return 'UNKNOWN' if type_name is None or empty
            2. Check exact match in SENSORS set → 'SENSOR'
            3. Check exact match in ACTUATORS set → 'ACTUATOR'
            4. Check exact match in CONTROL set → 'CONTROL'
            5. Check exact match in GLUE set → 'GLUE'
            6. Apply pattern matching:
               - Contains 'INPUT' or '_IN' → 'SENSOR'
               - Contains 'OUTPUT' or '_OUT' → 'ACTUATOR'
               - Contains 'PID' or 'CONTROL' → 'CONTROL'
            7. Return 'UNKNOWN' if no matches found

        Examples:
            >>> BlockClassifier.classify('PID_BASIC')
            'CONTROL'
            >>> BlockClassifier.classify('Custom_Temperature_Input')
            'SENSOR'
            >>> BlockClassifier.classify('MyCompanyPID')
            'CONTROL'
            >>> BlockClassifier.classify('')
            'UNKNOWN'
        """
        if not type_name:
            return 'UNKNOWN'

        type_upper = type_name.upper()

        # Exact match in predefined sets
        if type_upper in cls.SENSORS:
            return 'SENSOR'
        elif type_upper in cls.ACTUATORS:
            return 'ACTUATOR'
        elif type_upper in cls.CONTROL:
            return 'CONTROL'
        elif type_upper in cls.GLUE:
            return 'GLUE'
        else:
            # Pattern-based fallback for custom blocks
            if 'INPUT' in type_upper or '_IN' in type_upper:
                return 'SENSOR'
            elif 'OUTPUT' in type_upper or '_OUT' in type_upper:
                return 'ACTUATOR'
            elif 'PID' in type_upper or 'CONTROL' in type_upper:
                return 'CONTROL'
            else:
                return 'UNKNOWN'


class Node:
    """
    Graph node representing a function block, input variable, or output variable in an FBD.

    Encapsulates all layout-relevant information for a single FBD element, including its
    position, dimensions, semantic classification, and relationships to other elements.

    Attributes:
        id: Unique local identifier from XML (localId attribute)
        kind: Element type - 'block', 'inVariable', or 'outVariable'
        width: Block width in pixels
        height: Block height in pixels
        elem: Reference to the original lxml Element for XML updates
        layer: Assigned layer number for hierarchical layout
        x: X coordinate (left edge) in pixels
        y: Y coordinate (top edge) in pixels
        type_name: Function block type (typeName attribute), e.g., 'PID_BASIC'
        instance_name: Block instance name (instanceName attribute), e.g., 'TIC_101'
        classification: Semantic category ('SENSOR', 'ACTUATOR', 'CONTROL', 'GLUE', 'VARIABLE')
        is_satellite: True if this is a satellite element (variable/constant)
        parent_id: ID of parent block for satellites, None otherwise
        macro_layer: Assigned macro layer (0-10) for IEC 61131 layout, None for generic layout

    Example:
        >>> node = Node("42", "block", 80, 60, block_element)
        >>> node.classification
        'CONTROL'
        >>> node.right_center()
        (180, 130)
    """

    def __init__(self, local_id: str, kind: str, width: int, height: int, elem):
        """
        Initialize a graph node from FBD element.

        Args:
            local_id: Unique identifier from localId XML attribute
            kind: Element kind ('block', 'inVariable', or 'outVariable')
            width: Element width in pixels
            height: Element height in pixels
            elem: lxml Element object (or None for testing)
        """
        self.id = local_id
        self.kind = kind  # "block", "inVariable", "outVariable"
        self.width = int(width)
        self.height = int(height)
        self.elem = elem
        self.layer = 0
        self.x = 0
        self.y = 0

        # Enhanced attributes for IEC 61131 layout
        self.type_name = elem.get('typeName', '') if elem is not None else ''
        self.instance_name = elem.get('instanceName', '') if elem is not None else ''
        self.classification = BlockClassifier.classify(self.type_name) if self.kind == 'block' else 'VARIABLE'
        self.is_satellite = False
        self.parent_id: Optional[str] = None
        self.macro_layer: Optional[int] = None

    @property
    def left(self) -> int:
        """X coordinate of left edge."""
        return self.x

    @property
    def right(self) -> int:
        """X coordinate of right edge."""
        return self.x + self.width

    @property
    def top(self) -> int:
        """Y coordinate of top edge."""
        return self.y

    @property
    def bottom(self) -> int:
        """Y coordinate of bottom edge."""
        return self.y + self.height

    def left_center(self) -> Tuple[int, int]:
        """
        Calculate center point of left edge for connection routing.

        Returns:
            Tuple of (x, y) coordinates for left edge center point.
        """
        return (self.x, self.y + self.height // 2)

    def right_center(self) -> Tuple[int, int]:
        """
        Calculate center point of right edge for connection routing.

        Returns:
            Tuple of (x, y) coordinates for right edge center point.
        """
        return (self.x + self.width, self.y + self.height // 2)


class Graph:
    """
    Directed graph representation of an FBD (Function Block Diagram).

    The graph models the control flow between function blocks, variables, and constants
    in IEC 61131-3 diagrams. Each node represents a diagram element (block, inVariable,
    outVariable), and directed edges represent data connections between elements.

    Attributes:
        nodes (Dict[str, Node]): Mapping from localId to Node objects
        adj (Dict[str, List[str]]): Adjacency list for forward edges (u → v)
        rev (Dict[str, List[str]]): Reverse adjacency list for backward edges (v → u)
        edges_xml (Dict[Tuple[str, str], List[etree._Element]]):
            XML connection elements keyed by (source_id, destination_id) tuple.
            Multiple connections may exist between the same pair of nodes.

    Example:
        >>> g = Graph()
        >>> g.add_node(Node("0", "block", 80, 60, block_elem))
        >>> g.add_node(Node("1", "inVariable", 60, 40, var_elem))
        >>> g.add_edge("1", "0", connection_elem)
        >>> sources = g.sources()  # ["1"]
        >>> sinks = g.sinks()      # ["0"]
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adj: Dict[str, List[str]] = defaultdict(list)  # u -> [v]
        self.rev: Dict[str, List[str]] = defaultdict(list)  # v -> [u]
        # Store connection XML elements keyed by (src, dst)
        self.edges_xml: Dict[Tuple[str, str], List[etree._Element]] = defaultdict(list)

    def add_node(self, node: Node):
        """
        Add a node to the graph.

        Args:
            node: Node object representing an FBD element
        """
        self.nodes[node.id] = node

    def add_edge(self, u: str, v: str, conn_elem: etree._Element):
        """
        Add a directed edge from node u to node v.

        Args:
            u: Source node localId
            v: Destination node localId
            conn_elem: XML <connection> element representing this edge
        """
        self.adj[u].append(v)
        self.rev[v].append(u)
        self.edges_xml[(u, v)].append(conn_elem)

    def sources(self) -> List[str]:
        """
        Return node IDs with no incoming edges (graph sources).

        Returns:
            List of localIds for nodes with in-degree = 0
        """
        return [nid for nid in self.nodes if not self.rev[nid]]

    def sinks(self) -> List[str]:
        """
        Return node IDs with no outgoing edges (graph sinks).

        Returns:
            List of localIds for nodes with out-degree = 0
        """
        return [nid for nid in self.nodes if not self.adj[nid]]


# --------- XML parsing helpers ---------

def parse_fbd(fbd_element, debug_info: Optional[List[BlockDebugInfo]] = None) -> Graph:
    """
    Parse a PLCOpen TC6 FBD element into a directed graph.

    Extracts function blocks, input/output variables, and their connections from
    a PLCOpen XML <FBD> element. Handles both namespace-qualified and unqualified
    XML elements.

    Args:
        fbd_element: lxml etree._Element representing the <FBD> root
        debug_info: Optional list to populate with BlockDebugInfo entries for
                    layout debugging. If provided, captures position and dimension
                    data for all elements.

    Returns:
        Graph object with nodes (blocks, inVariable, outVariable) and directed
        edges representing data connections.

    XML Structure:
        <FBD>
          <block localId="0" typeName="ANALOG_IN" instanceName="TI_101" width="80" height="60">
            <position x="100" y="200"/>
            ...
          </block>
          <inVariable localId="1" width="60" height="40">
            <position x="50" y="210"/>
            <expression>PT_101</expression>
          </inVariable>
          <outVariable localId="2" width="60" height="40">
            <position x="300" y="210"/>
            <expression>OUT_VAR</expression>
            <connectionPointIn>
              <connection refLocalId="0" formalParameter="PV"/>
            </connectionPointIn>
          </outVariable>
        </FBD>

    Example:
        >>> tree = etree.parse("diagram.xml")
        >>> fbd = tree.xpath("//FBD")[0]
        >>> debug = []
        >>> g = parse_fbd(fbd, debug)
        >>> print(f"Parsed {len(g.nodes)} nodes, {sum(len(adj) for adj in g.adj.values())} edges")
    """
    # Extract namespace if present
    ns = {}
    if fbd_element.nsmap and None in fbd_element.nsmap:
        ns = {'ns': fbd_element.nsmap[None]}
        block_prefix = 'ns:block'
        invar_prefix = 'ns:inVariable'
        outvar_prefix = 'ns:outVariable'
        connpt_prefix = 'ns:connectionPointIn'
        conn_prefix = 'ns:connection'
        pos_prefix = 'ns:position'
    else:
        block_prefix = 'block'
        invar_prefix = 'inVariable'
        outvar_prefix = 'outVariable'
        connpt_prefix = 'connectionPointIn'
        conn_prefix = 'connection'
        pos_prefix = 'position'
    
    g = Graph()

    # Nodes: blocks, inVariable, outVariable from the single FBD element
    for tag, prefixed_tag in [("block", block_prefix), ("inVariable", invar_prefix), ("outVariable", outvar_prefix)]:
        # Process elements from this specific FBD only
        if ns:
            elements = fbd_element.xpath(f'./{prefixed_tag}', namespaces=ns)
        else:
            elements = fbd_element.xpath(f'./{prefixed_tag}')
        
        for elem in elements:
            local_id = elem.get("localId")
            w = elem.get("width", "60")
            h = elem.get("height", "40")
            node = Node(local_id, tag, int(w), int(h), elem)
            g.add_node(node)
            
            # Capture debug information if requested (for all element types now)
            if debug_info is not None:
                # Get position if it exists
                if ns:
                    pos_elem = elem.find(f'{{{ns["ns"]}}}position')
                else:
                    pos_elem = elem.find('position')
                
                x_before = int(pos_elem.get('x', '0')) if pos_elem is not None else 0
                y_before = int(pos_elem.get('y', '0')) if pos_elem is not None else 0
                
                # Get element type and name based on element kind
                if tag == "block":
                    element_type = elem.get('typeName', 'UNKNOWN')
                    element_name = elem.get('instanceName', f'block_{local_id}')
                elif tag == "inVariable":
                    element_type = 'IN_VAR'
                    element_name = elem.get('expression', f'inVar_{local_id}')
                elif tag == "outVariable":
                    element_type = 'OUT_VAR'
                    element_name = elem.get('expression', f'outVar_{local_id}')
                else:
                    element_type = tag.upper()
                    element_name = f'{tag}_{local_id}'
                
                debug_entry = BlockDebugInfo(
                    block_id=local_id,
                    block_type=element_type,
                    block_name=element_name,
                    x_before=x_before,
                    y_before=y_before,
                    width_before=int(w),
                    height_before=int(h)
                )
                debug_info.append(debug_entry)

    # Edges: connection inside a connectionPointIn references refLocalId = source
    # Destination is the owner element (block or outVariable) localId
    if ns:
        dst_elements = fbd_element.xpath(f'./*[self::{block_prefix} or self::{outvar_prefix}]', namespaces=ns)
    else:
        dst_elements = fbd_element.xpath(f'./*[self::{block_prefix} or self::{outvar_prefix}]')
    
    for dst_elem in dst_elements:
        dst_id = dst_elem.get("localId")
        if ns:
            connections = dst_elem.xpath(f'.//{connpt_prefix}/{conn_prefix}', namespaces=ns)
        else:
            connections = dst_elem.xpath(f'.//{connpt_prefix}/{conn_prefix}')
        
        for conn in connections:
            src_id = conn.get("refLocalId")
            if not src_id:
                continue
            if src_id not in g.nodes:
                continue
            g.add_edge(src_id, dst_id, conn)

    return g


# --------- Satellite detection ---------

def identify_satellites(g: Graph) -> Set[str]:
    """
    Identify satellite blocks (variables, constants, parameters) that should be
    positioned close to their parent blocks rather than in the main flow.

    Satellite elements are secondary diagram components that provide constants,
    setpoints, or variable references to primary function blocks. They are laid
    out adjacent to their parent blocks rather than in the main control flow.

    Classification Rules:
        - inVariable and outVariable: Always satellites
        - Blocks with UNKNOWN classification, no inputs, but outputs: Likely constants/setpoints

    Parent Assignment:
        - Input variables: Attach to first downstream CONTROL or ACTUATOR block
        - Output variables: Attach to first upstream CONTROL or SENSOR block
        - Constants/setpoints: Attach to first downstream CONTROL or ACTUATOR block

    Args:
        g: Graph with classified nodes (requires BlockClassifier.classify_blocks)

    Returns:
        Set of node IDs identified as satellites

    Side Effects:
        - Sets node.is_satellite = True for satellites
        - Sets node.parent_id for each satellite

    Example:
        >>> g = parse_fbd(fbd_elem)
        >>> BlockClassifier.classify_blocks(g)
        >>> satellites = identify_satellites(g)
        >>> print(f"Found {len(satellites)} satellite elements")
    """
    satellites = set()
    
    for nid, node in g.nodes.items():
        # Variables are always satellites
        if node.kind in ['inVariable', 'outVariable']:
            satellites.add(nid)
            node.is_satellite = True
            
            # Find parent block (the block this variable connects to)
            if node.kind == 'inVariable' and g.adj[nid]:
                # Input variable feeds into a block
                potential_parents = [dst for dst in g.adj[nid] 
                                   if g.nodes[dst].classification in ['CONTROL', 'ACTUATOR']]
                if potential_parents:
                    node.parent_id = potential_parents[0]
            elif node.kind == 'outVariable' and g.rev[nid]:
                # Output variable receives from a block
                potential_parents = [src for src in g.rev[nid]
                                   if g.nodes[src].classification in ['CONTROL', 'SENSOR']]
                if potential_parents:
                    node.parent_id = potential_parents[0]
        
        # Constants and setpoints (blocks with no inputs) are satellites
        elif node.classification == 'UNKNOWN' and not g.rev[nid] and g.adj[nid]:
            # This is likely a constant or setpoint block
            satellites.add(nid)
            node.is_satellite = True
            
            # Attach to the first control or actuator block it feeds
            for dst in g.adj[nid]:
                if g.nodes[dst].classification in ['CONTROL', 'ACTUATOR']:
                    node.parent_id = dst
                    break
    
    return satellites


# --------- Cycle handling, layering, ordering ---------

def break_cycles(g: Graph) -> Set[Tuple[str, str]]:
    """
    Break cycles in the graph to enable layered layout using DFS-based back-edge detection.

    Uses depth-first search to identify back-edges (edges that create cycles) and
    removes them from the graph. This is a preprocessing step for hierarchical layout
    algorithms that require a directed acyclic graph (DAG).

    Algorithm:
        1. Perform DFS traversal with three-color marking:
           - White (0): Unvisited node
           - Gray (1): Currently visiting (on DFS stack)
           - Black (2): Finished visiting
        2. Any edge to a gray node is a back-edge (creates cycle)
        3. Remove back-edges from adjacency lists

    Args:
        g: Graph to modify (adjacency lists are modified in-place)

    Returns:
        Set of removed edges as (source_id, dest_id) tuples

    Side Effects:
        Modifies g.adj and g.rev by removing back-edges. The graph becomes acyclic.

    Example:
        >>> removed = break_cycles(g)
        >>> print(f"Removed {len(removed)} back-edges to break cycles")
    """
    removed = set()
    color = {nid: 0 for nid in g.nodes}  # 0=unseen,1=visiting,2=done

    def dfs(u):
        color[u] = 1
        for v in list(g.adj[u]):
            if color[v] == 0:
                dfs(v)
            elif color[v] == 1:
                # back-edge u->v, remove for layering
                g.adj[u].remove(v)
                g.rev[v].remove(u)
                removed.add((u, v))
        color[u] = 2

    for nid in list(g.nodes.keys()):
        if color[nid] == 0:
            dfs(nid)

    return removed


def assign_layers(g: Graph) -> None:
    """
    Assign topological layers using longest-path algorithm (Coffman-Graham layering).

    Uses BFS-based topological sort to assign each node to a layer based on the
    longest path from any source node. This is a fallback for generic diagrams
    that don't use IEC 61131-3 semantic layering.

    Algorithm:
        1. Start with all source nodes (in-degree = 0) at layer 0
        2. For each node, set layer = max(predecessor layers) + 1
        3. Process nodes in topological order via BFS queue

    Args:
        g: Acyclic graph (must call break_cycles first)

    Side Effects:
        Sets node.layer for all nodes in g.nodes

    Example:
        >>> break_cycles(g)
        >>> assign_layers(g)
        >>> max_layer = max(n.layer for n in g.nodes.values())
        >>> print(f"Graph has {max_layer + 1} layers")
    """
    indeg = {nid: len(g.rev[nid]) for nid in g.nodes}
    q = deque([nid for nid in g.nodes if indeg[nid] == 0])
    layer = {nid: 0 for nid in g.nodes}
    while q:
        u = q.popleft()
        for v in g.adj[u]:
            layer[v] = max(layer[v], layer[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for nid in g.nodes:
        g.nodes[nid].layer = layer[nid]


def assign_macro_layers(g: Graph) -> None:
    """
    Assign nodes to semantic macro layers based on IEC 61131-3 industrial control semantics.

    Implements the 11-layer semantic hierarchy designed for industrial control diagrams.
    Unlike topological layering, this uses domain knowledge about sensor → control → actuator
    flow patterns to create readable, standards-compliant layouts.

    11-Layer System:
        Layer  0: SENSOR Input Satellites (setpoints, constants for sensors)
        Layer  1: SENSORS (ANALOG_IN, DIGITAL_IN, measurement blocks)
        Layer  2: SENSOR Output Satellites (derived sensor values)
        Layer  3: GLUE-L (preprocessing: scaling, voting, selection)
        Layer  4: CONTROL Input Satellites (PID setpoints, tuning parameters)
        Layer  5: CONTROL (PID controllers, ratio control, advanced control)
        Layer  6: CONTROL Output Satellites (control status, intermediate values)
        Layer  7: GLUE-R (postprocessing: split range, interlocks)
        Layer  8: ACTUATOR Input Satellites (actuator commands)
        Layer  9: ACTUATORS (VALVE_*, MOTOR_*, output blocks)
        Layer 10: ACTUATOR Output Satellites (actuator status)

    Algorithm Phases:
        1. Assign fixed layers for SENSOR (1), CONTROL (5), ACTUATOR (9) blocks
        2. Handle cascaded control (PID chains) by offsetting downstream controllers
        3. Place GLUE blocks in preprocessing (3) or postprocessing (7) based on connections
        4. Handle standalone or bidirectional GLUE blocks (center them at layer 5)
        5. Position satellites adjacent to their parent blocks

    Args:
        g: Graph with classified nodes and identified satellites

    Side Effects:
        Sets node.macro_layer and node.layer for all nodes

    Example:
        >>> BlockClassifier.classify_blocks(g)
        >>> identify_satellites(g)
        >>> assign_macro_layers(g)
        >>> print(f"Sensors: layer 1, Control: layer 5, Actuators: layer 9")
    """
    # Phase 1: Assign fixed layers for sensors, actuators, and control blocks
    for nid, node in g.nodes.items():
        if node.is_satellite:
            continue  # Skip satellites - handle in Phase 5
        
        if node.classification == 'SENSOR':
            node.macro_layer = 1  # Updated from 0 to 1
            node.layer = 1  # For compatibility
        elif node.classification == 'ACTUATOR':
            node.macro_layer = 9  # Updated from 4 to 9
            node.layer = 9
        elif node.classification == 'CONTROL':
            node.macro_layer = 5  # Updated from 2 to 5
            node.layer = 5
    
    # Phase 2: Handle cascaded control (e.g., PID feeding another PID)
    control_nodes = [n for n in g.nodes.values() 
                    if n.classification == 'CONTROL' and not n.is_satellite]
    
    if len(control_nodes) > 1:
        # Check for cascaded control relationships
        for node in control_nodes:
            # Find control blocks that feed into this one
            control_preds = [g.nodes[p] for p in g.rev[node.id] 
                           if not g.nodes[p].is_satellite and g.nodes[p].classification == 'CONTROL']
            if control_preds:
                # This is a downstream controller - place it one layer after its predecessors
                max_pred_layer = max(p.macro_layer for p in control_preds if p.macro_layer is not None)
                node.macro_layer = min(7, max_pred_layer + 2)  # Updated: skip satellite layer
                node.layer = node.macro_layer
    
    # Phase 3: Place GLUE blocks optimally
    for nid, node in g.nodes.items():
        if node.classification != 'GLUE' or node.is_satellite:
            continue
        
        # Skip if already assigned
        if node.macro_layer is not None:
            continue
        
        # Analyze connections (excluding satellites)
        predecessors = [g.nodes[p] for p in g.rev[nid] 
                       if not g.nodes[p].is_satellite and g.nodes[p].macro_layer is not None]
        successors = [g.nodes[s] for s in g.adj[nid] 
                     if not g.nodes[s].is_satellite and g.nodes[s].macro_layer is not None]
        
        if not predecessors and not successors:
            # Disconnected glue block - place in GLUE-L layer
            node.macro_layer = 3
        elif not predecessors:
            # No inputs - place before earliest successor
            min_succ = min(s.macro_layer for s in successors)
            if min_succ <= 1:  # Before sensors
                node.macro_layer = 1
            elif min_succ <= 5:  # Before control
                node.macro_layer = 3
            else:  # Before actuators
                node.macro_layer = 7
        elif not successors:
            # No outputs - place after latest predecessor
            max_pred = max(p.macro_layer for p in predecessors)
            if max_pred <= 1:  # After sensors
                node.macro_layer = 3
            elif max_pred <= 5:  # After control
                node.macro_layer = 7
            else:  # After actuators
                node.macro_layer = 9
        else:
            # Has both inputs and outputs
            max_pred = max(p.macro_layer for p in predecessors)
            min_succ = min(s.macro_layer for s in successors)
            
            # Determine optimal placement based on new layer structure
            if max_pred <= 1 and min_succ >= 5:
                # Between sensors and control -> GLUE-L
                node.macro_layer = 3
            elif max_pred >= 5 and min_succ >= 9:
                # Between control and actuators -> GLUE-R
                node.macro_layer = 7
            elif max_pred < min_succ:
                # Find appropriate GLUE layer between pred and succ
                if min_succ <= 5:
                    node.macro_layer = 3  # GLUE-L
                else:
                    node.macro_layer = 7  # GLUE-R
            else:
                # If constraints conflict, prefer GLUE-L
                node.macro_layer = 3
        
        node.layer = node.macro_layer
    
    # Phase 4: Handle any remaining unassigned nodes
    for nid, node in g.nodes.items():
        if node.macro_layer is None and not node.is_satellite:
            # Use topological position as fallback
            if not g.rev[nid]:
                node.macro_layer = 1  # Source node (sensors)
            elif not g.adj[nid]:
                node.macro_layer = 9  # Sink node (actuators)
            else:
                node.macro_layer = 5  # Middle (control)
            node.layer = node.macro_layer
    
    # Phase 5: Assign satellites to dedicated satellite layers
    for nid, node in g.nodes.items():
        if not node.is_satellite:
            continue
            
        # Find parent block (the block this satellite connects to)
        parent_id = None
        parent_layer = None
        
        if node.kind == 'inVariable':
            # Input variable - find the block it feeds into
            for target in g.adj[nid]:
                target_node = g.nodes[target]
                if not target_node.is_satellite and target_node.macro_layer is not None:
                    parent_id = target
                    parent_layer = target_node.macro_layer
                    break
        elif node.kind == 'outVariable':
            # Output variable - find the block that feeds it
            for source in g.rev[nid]:
                source_node = g.nodes[source]
                if not source_node.is_satellite and source_node.macro_layer is not None:
                    parent_id = source
                    parent_layer = source_node.macro_layer
                    break
        
        # Assign satellite to appropriate satellite layer
        if parent_layer is not None:
            node.parent_id = parent_id
            if node.kind == 'inVariable':
                # Input satellite goes BEFORE its parent's layer
                if parent_layer == 1:  # SENSOR
                    node.macro_layer = 0
                elif parent_layer == 5:  # CONTROL  
                    node.macro_layer = 4
                elif parent_layer == 9:  # ACTUATOR
                    node.macro_layer = 8
                else:
                    # For GLUE blocks, put input satellites in preceding layer
                    node.macro_layer = max(0, parent_layer - 1)
            else:  # outVariable
                # Output satellite goes AFTER its parent's layer
                if parent_layer == 1:  # SENSOR
                    node.macro_layer = 2
                elif parent_layer == 5:  # CONTROL
                    node.macro_layer = 6
                elif parent_layer == 9:  # ACTUATOR
                    node.macro_layer = 10
                else:
                    # For GLUE blocks, put output satellites in following layer
                    node.macro_layer = min(10, parent_layer + 1)
            
            node.layer = node.macro_layer
        else:
            # Fallback: orphaned satellite - place in middle satellite layer
            node.macro_layer = 4  # CONTROL input satellites layer
            node.layer = 4


def extract_number(instance_name: str) -> tuple:
    """
    Extract numeric suffix from instance name for natural sorting.

    Enables natural ordering of blocks like TI_101, TI_102, ..., TI_110
    instead of lexicographic ordering (TI_101, TI_110, TI_102).

    Args:
        instance_name: Block instance name (e.g., "PID_101", "VALVE_202")

    Returns:
        Tuple (priority, number) where:
            - priority=0 if numeric suffix found
            - priority=1 if no suffix (sorts alphabetically)
            - priority=2 if empty/None (sorts last)

    Example:
        >>> extract_number("TI_101")
        (0, 101)
        >>> extract_number("PUMP_A")
        (1, "PUMP_A")
        >>> extract_number("")
        (2, 0)
    """
    if not instance_name:
        return (2, 0)
    match = re.search(r'(\d+)', instance_name)
    if match:
        return (0, int(match.group(1)))
    return (1, instance_name)


def order_within_layers(g: Graph) -> Dict[int, List[str]]:
    """
    Order nodes within each layer using median-of-parents heuristic.

    Implements a simplified version of the layer-by-layer sweep method from
    Sugiyama et al.'s hierarchical graph drawing framework. Reduces edge
    crossings by positioning each node near the median position of its parents.

    Algorithm:
        1. Initialize with stable ordering by localId within each layer
        2. For each layer L (bottom-up):
           - Compute median index of parent nodes in layer L-1
           - Sort nodes in layer L by median parent index
           - Use localId as tiebreaker

    Args:
        g: Graph with node.layer assigned

    Returns:
        Dict mapping layer number to ordered list of node IDs

    References:
        Sugiyama et al., "Methods for Visual Understanding of Hierarchical
        System Structures", IEEE Trans. Systems, Man, and Cybernetics, 1981

    Example:
        >>> assign_layers(g)
        >>> layers = order_within_layers(g)
        >>> print(f"Layer 0: {layers[0]}")
    """
    layers = defaultdict(list)
    for nid, node in g.nodes.items():
        layers[node.layer].append(nid)

    # initial stable order
    for L in layers:
        layers[L].sort(key=lambda nid: int(nid))

    # median heuristic: compute parent indices from previous layer
    for L in sorted(layers.keys()):
        if L == 0:
            continue
        prev = layers[L-1]
        pos = {nid: i for i, nid in enumerate(prev)}

        def median_parent_index(nid):
            parents = g.rev[nid]
            if not parents:
                return float('inf')
            indices = sorted(pos[p] for p in parents if p in pos)
            if not indices:
                return float('inf')
            m = len(indices)//2
            if len(indices) % 2 == 1:
                return indices[m]
            else:
                return (indices[m-1] + indices[m]) / 2.0

        layers[L].sort(key=lambda nid: (median_parent_index(nid), int(nid)))

    return layers


def order_within_macro_layers(g: Graph) -> Dict[int, List[str]]:
    """
    Order nodes within macro layers using affinity grouping and crossing minimization.

    Implements a multi-stage ordering strategy that combines industrial control
    conventions (grouping related instruments) with graph drawing heuristics
    (median and barycenter methods).

    Algorithm Stages:
        1. Affinity Grouping: Group blocks by instrument prefix (FT, PT, TI, etc.)
           and sort numerically within groups (FT_101, FT_102, ...)
        2. Barycenter Heuristic: Position ungrouped nodes based on average
           position of their predecessors
        3. Two-Pass Median Sweep: Apply forward and backward median heuristic
           passes to further reduce crossings while preserving grouping

    Ordering Priorities:
        - Maintain instrument families together (all FT blocks adjacent)
        - Natural numeric ordering within families (101, 102, 103 not 101, 110, 102)
        - Minimize edge crossings between layers
        - Place satellites near their parent blocks

    Args:
        g: Graph with macro_layer assigned to all nodes

    Returns:
        Dict mapping macro layer number to ordered list of node IDs

    Example:
        >>> assign_macro_layers(g)
        >>> layers = order_within_macro_layers(g)
        >>> for L, nodes in sorted(layers.items()):
        ...     print(f"Layer {L}: {[g.nodes[n].instance_name for n in nodes]}")
    """
    layers = defaultdict(list)
    
    # Group ALL nodes by macro layer (including satellites)
    for nid, node in g.nodes.items():
        if node.macro_layer is not None:
            layers[node.macro_layer].append(nid)
    
    # Order each layer
    for L in sorted(layers.keys()):
        nodes = layers[L]
        
        # Group by instance name prefix for affinity grouping
        groups = defaultdict(list)
        ungrouped = []
        
        for nid in nodes:
            node = g.nodes[nid]
            if node.instance_name:
                # Extract prefix (e.g., 'FT' from 'FT_101_AI')
                parts = node.instance_name.split('_')
                if len(parts) >= 2 and parts[0].isalpha():
                    # Group by instrument type prefix
                    prefix = parts[0]
                    groups[prefix].append((nid, node.instance_name))
                else:
                    ungrouped.append(nid)
            else:
                ungrouped.append(nid)
        
        # Sort within groups by numeric suffix
        ordered = []
        for prefix in sorted(groups.keys()):
            # Sort by numeric suffix if present
            group_nodes = sorted(groups[prefix], key=lambda x: extract_number(x[1]))
            ordered.extend([nid for nid, _ in group_nodes])
        
        # Add ungrouped nodes, sorted by barycenter heuristic
        if L > 0 and L-1 in layers:
            prev_layer = layers[L-1]
            pos = {nid: i for i, nid in enumerate(prev_layer)}
            
            def barycenter(nid):
                # Consider only non-satellite predecessors
                parents = [p for p in g.rev[nid] 
                          if not g.nodes[p].is_satellite and p in pos]
                if parents:
                    return sum(pos[p] for p in parents) / len(parents)
                return float('inf')
            
            ungrouped.sort(key=lambda nid: (barycenter(nid), int(nid)))
        else:
            # For first layer or layers without predecessors
            ungrouped.sort(key=lambda nid: (g.nodes[nid].type_name, int(nid)))
        
        ordered.extend(ungrouped)
        layers[L] = ordered
    
    # Two-pass median heuristic to further reduce crossings
    for iteration in range(2):
        # Forward pass (left to right)
        for L in sorted(layers.keys())[1:]:
            if L-1 not in layers:
                continue
                
            prev_layer = layers[L-1]
            pos = {nid: i for i, nid in enumerate(prev_layer)}
            
            def median_position(nid):
                parents = [p for p in g.rev[nid] 
                          if not g.nodes[p].is_satellite and p in pos]
                if parents:
                    positions = sorted(pos[p] for p in parents)
                    mid = len(positions) // 2
                    if len(positions) % 2 == 1:
                        return positions[mid]
                    else:
                        return (positions[mid-1] + positions[mid]) / 2.0
                # Keep current position if no parents
                return layers[L].index(nid)
            
            # Sort by median position but preserve grouping
            layer_nodes = layers[L]
            # Create position map
            node_positions = {nid: median_position(nid) for nid in layer_nodes}
            
            # Stable sort to minimize movement
            layers[L] = sorted(layer_nodes, key=lambda nid: (node_positions[nid], layer_nodes.index(nid)))
        
        # Backward pass (right to left) for symmetry
        for L in sorted(layers.keys(), reverse=True)[1:]:
            if L+1 not in layers:
                continue
                
            next_layer = layers[L+1]
            pos = {nid: i for i, nid in enumerate(next_layer)}
            
            def median_child_position(nid):
                children = [c for c in g.adj[nid]
                           if not g.nodes[c].is_satellite and c in pos]
                if children:
                    positions = sorted(pos[c] for c in children)
                    mid = len(positions) // 2
                    if len(positions) % 2 == 1:
                        return positions[mid]
                    else:
                        return (positions[mid-1] + positions[mid]) / 2.0
                return layers[L].index(nid)
            
            layer_nodes = layers[L]
            node_positions = {nid: median_child_position(nid) for nid in layer_nodes}
            layers[L] = sorted(layer_nodes, key=lambda nid: (node_positions[nid], layer_nodes.index(nid)))
    
    return layers


# --------- Geometry assignment ---------

def position_satellites(g: Graph) -> None:
    """
    Position satellite blocks (variables, constants) adjacent to their parent blocks.

    Legacy positioning function for simple satellite placement. Positions input
    satellites to the left of parent blocks and output satellites to the right.

    Note: This function is superseded by assign_coordinates_with_macro_layers()
    which provides more sophisticated satellite positioning with alignment options
    and collision avoidance.

    Args:
        g: Graph with parent_id assigned for satellite nodes

    Side Effects:
        Sets node.x, node.y, and node.layer for satellite nodes

    Example:
        >>> identify_satellites(g)
        >>> position_satellites(g)
    """
    for nid, node in g.nodes.items():
        if not node.is_satellite or not node.parent_id:
            continue
        
        parent = g.nodes.get(node.parent_id)
        if not parent:
            # If no parent found, position as regular node
            continue
        
        # Determine side based on connection type and node kind
        if node.kind == 'inVariable' or (node.kind == 'block' and not g.rev[nid]):
            # Input satellite - place on left side of parent
            node.x = parent.x - node.width - DEFAULT_SATELLITE_GAP_BUFFER
            node.y = parent.y + 10  # Slight vertical offset for better visual separation
        else:
            # Output satellite - place on right side of parent
            node.x = parent.x + parent.width + DEFAULT_SATELLITE_GAP_BUFFER
            node.y = parent.y + parent.height - node.height - 10  # Align near bottom

        # Ensure minimum bounds (prevent negative coordinates)
        node.x = max(10, node.x)
        node.y = max(10, node.y)
        
        # Copy layer from parent for consistency
        node.layer = parent.layer if parent.layer is not None else 0


def assign_coordinates_with_macro_layers(g: Graph, layers: Dict[int, List[str]],
                                         x_gap: int = 150, y_gap: int = 40,
                                         left_margin: int = 50, top_margin: int = 50,
                                         satellite_gap_buffer: int = 20,
                                         satellite_alignment: str = 'center',
                                         satellite_stack_gap: int = 5) -> None:
    """
    Assign (x, y) coordinates using dynamic macro layer positions with satellite alignment.

    Implements two-phase coordinate assignment optimized for IEC 61131-3 diagrams:
    1. Position main blocks (SENSOR, CONTROL, ACTUATOR, GLUE) with fixed vertical spacing
    2. Position satellites adjacent to their parents with configurable alignment

    Layer Width Calculation:
        - Dynamically calculates each layer width based on maximum block width
        - Satellite layers: min 120px (to accommodate variable names)
        - Main block layers: min 150px (to accommodate function blocks)
        - Adds gap buffer between layers to prevent crowding

    Satellite Positioning Modes:
        - 'center': Align satellite center with parent center (default)
        - 'top': Align satellite top edge with parent top edge
        - 'bottom': Align satellite bottom edge with parent bottom edge

    Args:
        g: Graph with macro_layer assigned
        layers: Dict mapping layer number to ordered node IDs
        x_gap: Minimum horizontal gap between layers (default 150)
        y_gap: Vertical gap between nodes in same layer (default 40)
        left_margin: Left canvas margin (default 50)
        top_margin: Top canvas margin (default 50)
        satellite_gap_buffer: Extra gap between layer and next layer (default 20)
        satellite_alignment: Satellite vertical alignment mode (default 'center')
        satellite_stack_gap: Gap between stacked satellites (default 5)

    Side Effects:
        Sets node.x and node.y for all nodes

    Example:
        >>> assign_macro_layers(g)
        >>> layers = order_within_macro_layers(g)
        >>> assign_coordinates_with_macro_layers(g, layers, y_gap=50)
    """
    # Calculate maximum width needed for each layer with enhanced minimums
    layer_max_width = {}
    for L in range(11):  # 11 macro layers (main + satellites)
        max_width = 0
        for nid in layers.get(L, []):
            node = g.nodes[nid]
            max_width = max(max_width, node.width)
        
        # Enhanced minimum widths with padding buffer
        if L in [0, 2, 4, 6, 8, 10]:  # Satellite layers
            # Use configured minimum for satellites to accommodate wide variable names
            layer_max_width[L] = max(max_width + BLOCK_WIDTH_PADDING, MIN_SATELLITE_LAYER_WIDTH) if max_width > 0 else MIN_SATELLITE_LAYER_WIDTH
        else:  # Main block layers
            # Use configured minimum for main blocks
            layer_max_width[L] = max(max_width + BLOCK_WIDTH_PADDING, MIN_BLOCK_LAYER_WIDTH) if max_width > 0 else MIN_BLOCK_LAYER_WIDTH
    
    # Dynamically calculate layer X positions based on actual content widths
    layer_x = {}
    current_x = left_margin
    
    for L in range(11):
        layer_x[L] = current_x
        layer_width = layer_max_width.get(L, MIN_BLOCK_LAYER_WIDTH)  # Fallback to default block width
        current_x += layer_width + satellite_gap_buffer
    
    # PHASE 1: Position main blocks first (layers 1, 3, 5, 7, 9)
    main_block_layers = [1, 3, 5, 7, 9]  # SENSORS, GLUE-L, CONTROL, GLUE-R, ACTUATORS
    
    for L in main_block_layers:
        if L not in layers:
            continue
            
        nids = layers[L]
        if not nids:
            continue
            
        if L not in layer_x:
            # Fallback for unexpected layers
            layer_x[L] = current_x + (L - 10) * 180
        
        x = layer_x[L]
        
        # Filter to main blocks only (exclude any satellites that might be in main layers)
        main_block_nodes = [nid for nid in nids if not g.nodes[nid].is_satellite]
        
        # Calculate total height needed for main blocks
        total_height = sum(g.nodes[nid].height + y_gap for nid in main_block_nodes) - y_gap if main_block_nodes else 0
        
        # Start y position
        current_y = top_margin
        
        for nid in main_block_nodes:
            node = g.nodes[nid]
            
            # Center node horizontally within its layer space
            layer_width = layer_max_width.get(L, 150)
            node_x_offset = (layer_width - node.width) // 2
            node.x = x + max(0, node_x_offset)
            node.y = current_y
            
            current_y += node.height + y_gap
    
    # PHASE 2: Position satellites aligned with their parent blocks
    satellite_layers = [0, 2, 4, 6, 8, 10]  # All satellite layers
    
    for L in satellite_layers:
        if L not in layers:
            continue
            
        nids = layers[L]
        if not nids:
            continue
            
        if L not in layer_x:
            # Fallback for unexpected layers
            layer_x[L] = current_x + (L - 10) * 180
        
        x = layer_x[L]
        
        # Group satellites by their parent blocks for better alignment
        satellites_by_parent = {}
        orphaned_satellites = []
        
        for nid in nids:
            node = g.nodes[nid]
            if not node.is_satellite:
                continue  # Skip any non-satellites that might be in satellite layers
                
            if hasattr(node, 'parent_id') and node.parent_id and node.parent_id in g.nodes:
                parent_id = node.parent_id
                if parent_id not in satellites_by_parent:
                    satellites_by_parent[parent_id] = []
                satellites_by_parent[parent_id].append(nid)
            else:
                orphaned_satellites.append(nid)
        
        # Position satellites aligned with their parent blocks
        for parent_id, satellite_ids in satellites_by_parent.items():
            parent = g.nodes[parent_id]
            
            # Calculate alignment positions for multiple satellites on same parent
            num_satellites = len(satellite_ids)
            
            for i, satellite_id in enumerate(satellite_ids):
                satellite = g.nodes[satellite_id]
                
                # Center satellite horizontally within its layer space
                layer_width = layer_max_width.get(L, 120)
                satellite_x_offset = (layer_width - satellite.width) // 2
                satellite.x = x + max(0, satellite_x_offset)
                
                # Align satellite vertically with parent block
                if satellite_alignment == 'center':
                    # Center satellite relative to parent
                    base_y = parent.y + (parent.height - satellite.height) // 2
                elif satellite_alignment == 'top':
                    # Align satellite top with parent top
                    base_y = parent.y
                elif satellite_alignment == 'bottom':
                    # Align satellite bottom with parent bottom  
                    base_y = parent.y + parent.height - satellite.height
                else:
                    # Default to center alignment
                    base_y = parent.y + (parent.height - satellite.height) // 2
                
                # Handle multiple satellites on same parent by stacking them
                if num_satellites == 1:
                    satellite.y = base_y
                else:
                    # Distribute satellites around the parent center
                    offset_from_center = (i - (num_satellites - 1) / 2) * (satellite.height + satellite_stack_gap)
                    satellite.y = base_y + int(offset_from_center)
                
                # Ensure satellite doesn't go above diagram bounds
                satellite.y = max(top_margin, satellite.y)
        
        # Position orphaned satellites (those without valid parent connections)
        current_y = top_margin
        for nid in orphaned_satellites:
            node = g.nodes[nid]
            
            # Center horizontally within layer space
            layer_width = layer_max_width.get(L, 120)
            node_x_offset = (layer_width - node.width) // 2
            node.x = x + max(0, node_x_offset)
            node.y = current_y
            
            current_y += node.height + y_gap
    
    # Apply collision detection and resolution for satellites in same layer
    _resolve_satellite_collisions(g, layers, satellite_layers, satellite_stack_gap)
    
    # Fine-tune positions to minimize crossings (main blocks only to preserve satellite alignment)
    main_layers_dict = {L: [nid for nid in layers.get(L, []) if not g.nodes[nid].is_satellite] 
                        for L in main_block_layers}
    minimize_crossings_simple(g, main_layers_dict, iterations=3)


def _resolve_satellite_collisions(g: Graph, layers: Dict[int, List[str]], satellite_layers: List[int], satellite_stack_gap: int):
    """
    Resolve Y-coordinate collisions between satellites in the same layer.
    Applies minimal adjustments while preserving parent alignment intent.
    """
    for L in satellite_layers:
        if L not in layers:
            continue
            
        satellite_nodes = [nid for nid in layers[L] if g.nodes[nid].is_satellite]
        if len(satellite_nodes) <= 1:
            continue  # No collisions possible
        
        # Sort satellites by Y position to detect overlaps
        satellites_with_pos = [(nid, g.nodes[nid].y, g.nodes[nid].height) for nid in satellite_nodes]
        satellites_with_pos.sort(key=lambda x: x[1])  # Sort by Y position
        
        # Detect and resolve collisions
        for i in range(len(satellites_with_pos) - 1):
            current_id, current_y, current_height = satellites_with_pos[i]
            next_id, next_y, next_height = satellites_with_pos[i + 1]
            
            current_bottom = current_y + current_height
            overlap = current_bottom + satellite_stack_gap - next_y
            
            if overlap > 0:
                # Collision detected - move the next satellite down
                new_next_y = current_bottom + satellite_stack_gap
                g.nodes[next_id].y = new_next_y
                
                # Update the position in our tracking list for subsequent collision checks
                satellites_with_pos[i + 1] = (next_id, new_next_y, next_height)


def count_crossings(g: Graph, n1: str, n2: str, prev_layer: List[str]) -> int:
    """Count edge crossings between two nodes and their connections to the previous layer."""
    crossings = 0
    
    # Get predecessors for both nodes
    n1_preds = [p for p in g.rev[n1] if p in prev_layer]
    n2_preds = [p for p in g.rev[n2] if p in prev_layer]
    
    # Count crossings: edges from n1_preds to n2 cross edges from n2_preds to n1
    for p1 in n1_preds:
        p1_idx = prev_layer.index(p1)
        for p2 in n2_preds:
            p2_idx = prev_layer.index(p2)
            # If p1 is above p2, but connects to n2 (which is below n1), it's a crossing
            if p1_idx < p2_idx:
                crossings += 1
    
    return crossings


def minimize_crossings_simple(g: Graph, layers: Dict[int, List[str]], iterations=3):
    """
    Simple crossing minimization by swapping adjacent nodes within layers.
    This is a greedy local optimization approach.
    """
    for _ in range(iterations):
        improved = False
        
        for L in sorted(layers.keys())[1:]:  # Skip first layer
            if L-1 not in layers:
                continue
                
            layer_nodes = layers[L]
            prev_layer = layers[L-1]
            
            # Try swapping adjacent nodes
            for i in range(len(layer_nodes) - 1):
                n1, n2 = layer_nodes[i], layer_nodes[i+1]
                
                # Skip if either is a satellite
                if g.nodes[n1].is_satellite or g.nodes[n2].is_satellite:
                    continue
                
                # Count crossings before swap
                crossings_before = count_crossings(g, n1, n2, prev_layer)
                
                # Count crossings if we were to swap (n2 above n1)
                crossings_after = count_crossings(g, n2, n1, prev_layer)
                
                if crossings_after < crossings_before:
                    # Perform the swap
                    layer_nodes[i], layer_nodes[i+1] = n2, n1
                    
                    # Also swap their y-coordinates
                    node1, node2 = g.nodes[n1], g.nodes[n2]
                    node1.y, node2.y = node2.y, node1.y
                    improved = True
        
        if not improved:
            break


def assign_coordinates(g: Graph, layers: Dict[int, List[str]], x_gap: int = 120, y_gap: int = 40,
                       left_margin: int = 50, top_margin: int = 50) -> None:
    """
    Assign (x, y) coordinates for generic topological layout with type-based grouping.

    Legacy coordinate assignment for non-IEC diagrams. Groups blocks, input variables,
    and output variables separately within each layer for cleaner organization.

    Algorithm:
        1. Calculate X positions: Each layer gets x based on max node width in that layer
        2. Assign Y positions: Stack nodes vertically with type grouping (blocks → inVars → outVars)
        3. Center-align nodes within their layer's allocated width
        4. Add extra vertical spacing between different node types

    Args:
        g: Graph with node.layer assigned
        layers: Dict mapping layer number to ordered node IDs
        x_gap: Horizontal gap between layers (default 120)
        y_gap: Vertical gap between nodes (default 40)
        left_margin: Left canvas margin (default 50)
        top_margin: Top canvas margin (default 50)

    Side Effects:
        Sets node.x and node.y for all nodes

    Note:
        Superseded by assign_coordinates_with_macro_layers() for IEC 61131-3 diagrams

    Example:
        >>> assign_layers(g)
        >>> layers = order_within_layers(g)
        >>> assign_coordinates(g, layers, y_gap=50)
    """
    # Separate nodes by type within each layer for better organization
    def separate_by_type(node_ids):
        blocks = []
        in_vars = []
        out_vars = []
        for nid in node_ids:
            node = g.nodes[nid]
            if node.kind == 'block':
                blocks.append(nid)
            elif node.kind == 'inVariable':
                in_vars.append(nid)
            else:  # outVariable
                out_vars.append(nid)
        # Return in order: blocks first, then variables
        return blocks + in_vars + out_vars
    
    # First pass: determine x-coordinate for each layer based on max width in layer
    max_layer = max(layers.keys()) if layers else 0
    layer_x = {}
    layer_max_width = {}
    
    cur_x = left_margin
    for L in range(0, max_layer+1):
        layer_x[L] = cur_x
        max_width = 0
        for nid in layers.get(L, []):
            max_width = max(max_width, g.nodes[nid].width)
        layer_max_width[L] = max_width
        cur_x += max_width + x_gap

    # Second pass: assign y-coordinates, ensuring no overlaps within each layer
    # Group by type for better visual organization
    for L, nids in layers.items():
        # Separate and sort nodes by type
        sorted_nids = separate_by_type(nids)
        
        cur_y = top_margin
        prev_kind = None
        for nid in sorted_nids:
            node = g.nodes[nid]
            # Add extra spacing between different node types
            if prev_kind and prev_kind != node.kind:
                cur_y += y_gap // 2  # Extra space between different types
            
            # Center-align node within its layer's allocated width
            layer_width = layer_max_width[L]
            node_x_offset = (layer_width - node.width) // 2  # Center the node in the layer
            node.x = layer_x[L] + node_x_offset
            node.y = cur_y
            cur_y += node.height + y_gap
            prev_kind = node.kind
    
    # Third pass: adjust positions to minimize edge crossings and improve aesthetics
    # Sort nodes in each layer by their connection patterns to minimize crossings
    for L in sorted(layers.keys())[1:]:  # Skip first layer
        layer_nodes = layers[L]
        
        # Create a list of (node_id, preferred_y) pairs
        node_preferences = []
        for nid in layer_nodes:
            node = g.nodes[nid]
            # Find predecessors
            predecessors = g.rev[nid]
            if predecessors:
                # Calculate average y position of predecessors
                avg_y = sum(g.nodes[p].y + g.nodes[p].height // 2 for p in predecessors) / len(predecessors)
                preferred_y = avg_y - node.height // 2
            else:
                # No predecessors, keep current position
                preferred_y = node.y
            node_preferences.append((nid, preferred_y))
        
        # Sort nodes by their preferred y position
        node_preferences.sort(key=lambda x: x[1])
        
        # Reassign y coordinates ensuring no overlaps, maintain proper x positioning
        cur_y = top_margin
        for nid, _ in node_preferences:
            node = g.nodes[nid]
            # Maintain center alignment within layer
            layer_width = layer_max_width[L]
            node_x_offset = (layer_width - node.width) // 2
            node.x = layer_x[L] + node_x_offset
            node.y = cur_y
            cur_y += node.height + y_gap


# --------- Edge routing (orthogonal) ---------

def route_edges(g: Graph, removed_back_edges: Set[Tuple[str, str]]) -> None:
    """
    Route connections with orthogonal lines, avoiding overlaps with blocks.
    Creates clean paths between blocks using horizontal and vertical segments.
    """
    def find_vertical_channel(src_node, dst_node, all_nodes):
        """Find a vertical channel (x-coordinate) between two nodes that avoids all blocks."""
        # Start with midpoint between source and destination
        src_right = src_node.x + src_node.width
        dst_left = dst_node.x
        
        if src_right < dst_left:
            # There's space between the nodes
            mid_x = (src_right + dst_left) // 2
            
            # Check if this x coordinate intersects any blocks
            for node in all_nodes.values():
                if node.id not in [src_node.id, dst_node.id]:
                    # Check if mid_x falls within this node's x range
                    if node.x <= mid_x <= node.x + node.width:
                        # Try to find space before or after this block
                        if node.x - src_right > 20:
                            mid_x = (src_right + node.x) // 2
                        elif dst_left - (node.x + node.width) > 20:
                            mid_x = ((node.x + node.width) + dst_left) // 2
            return mid_x
        else:
            # Nodes are in same layer or overlapping layers - route around
            return src_right + 30
    
    def route_forward_edge(src_pt, dst_pt, src_node, dst_node, all_nodes):
        """Route a forward edge with smart pathfinding."""
        sx, sy = src_pt
        dx, dy = dst_pt
        
        # Find a good vertical channel
        channel_x = find_vertical_channel(src_node, dst_node, all_nodes)
        
        # Create path segments
        path = []
        if abs(sy - dy) < 5:
            # Nodes are roughly aligned horizontally - simple straight connection
            path = [(sx, sy), (dx, dy)]
        else:
            # Use the vertical channel
            path = [
                (sx, sy),           # Start point
                (channel_x, sy),    # Horizontal to channel
                (channel_x, dy),    # Vertical in channel
                (dx, dy)            # Horizontal to destination
            ]
        
        # Remove redundant points (when consecutive points are the same)
        cleaned_path = []
        for i, pt in enumerate(path):
            if i == 0 or pt != path[i-1]:
                cleaned_path.append(pt)
        
        return cleaned_path
    
    def route_feedback_edge(src_pt, dst_pt, src_node, dst_node, all_nodes):
        """Route a feedback edge (back edge) around the diagram."""
        sx, sy = src_pt
        dx, dy = dst_pt
        
        # Find the minimum x and maximum y to route around
        min_x = min(src_node.x, dst_node.x) - 50
        max_y = max(node.y + node.height for node in all_nodes.values()) + 40
        
        # Route below all nodes
        path = [
            (sx, sy),           # Start point
            (sx - 20, sy),      # Small horizontal segment out
            (sx - 20, max_y),   # Down to below all nodes
            (min_x, max_y),     # Left to clear area
            (min_x, dy),        # Up to destination level
            (dx + 20, dy),      # Right to near destination
            (dx, dy)            # Final point
        ]
        
        return path
    
    # Process all edges
    for (u, v), conn_elems in g.edges_xml.items():
        if u not in g.nodes or v not in g.nodes:
            continue
            
        src = g.nodes[u]
        dst = g.nodes[v]
        
        # Determine if this is a forward or feedback edge
        is_forward = (src.layer < dst.layer) and ((u, v) not in removed_back_edges)
        
        # Determine connection points based on edge type
        if is_forward:
            start = src.right_center()
            end = dst.left_center()
            points = route_forward_edge(start, end, src, dst, g.nodes)
        else:
            start = src.left_center()
            end = dst.right_center()
            points = route_feedback_edge(start, end, src, dst, g.nodes)
        
        # Update the connection elements with the new path
        for conn in conn_elems:
            # Handle namespace for position elements
            ns = conn.nsmap
            if ns and None in ns:
                pos_tag = f'{{{ns[None]}}}position'
                # Remove old positions
                for p in list(conn.findall(pos_tag)):
                    conn.remove(p)
                # Add new positions
                for (x, y) in points:
                    p = etree.Element(pos_tag)
                    p.set('x', str(int(x)))
                    p.set('y', str(int(y)))
                    conn.append(p)
            else:
                # No namespace
                for p in list(conn.findall('position')):
                    conn.remove(p)
                for (x, y) in points:
                    p = etree.Element('position')
                    p.set('x', str(int(x)))
                    p.set('y', str(int(y)))
                    conn.append(p)


# --------- Debugging utilities ---------

def print_debug_table(debug_info: List[BlockDebugInfo], fbd_context: Optional[dict] = None) -> None:
    """
    Print formatted ASCII table showing block positions before and after auto-layout.

    Displays a comprehensive debugging table with:
    - FBD context (POU name, type, index)
    - Block details (ID, type, instance name)
    - Before positions and dimensions (x, y, width, height)
    - After positions and dimensions
    - Movement deltas (Δx, Δy)

    Useful for:
    - Verifying layout algorithm correctness
    - Understanding how blocks were repositioned
    - Debugging layout issues
    - Validating satellite positioning

    Args:
        debug_info: List of BlockDebugInfo entries captured during parse_fbd()
        fbd_context: Optional dict with POU metadata (pou_name, pou_type, fbd_index)

    Output Format:
        ================================================================================
        AUTO-LAYOUT DEBUG TABLE
        ================================================================================
        POU Name: MAIN_CONTROL
        POU Type: program
        FBD Index: 0
        --------------------------------------------------------------------------------
        | Block ID | Type          | Name          | Before (x,y,w,h) | After (x,y,w,h) | Δx   | Δy   |
        +----------+---------------+---------------+------------------+-----------------+------+------+
        | 0        | ANALOG_IN     | TI_101        | 100,200,80,60    | 50,50,80,60     | -50  | -150 |
        ...

    Example:
        >>> debug = []
        >>> g = parse_fbd(fbd_elem, debug)
        >>> # ... perform layout ...
        >>> print_debug_table(debug, {'pou_name': 'MAIN', 'pou_type': 'program'})
    """
    if not debug_info:
        print("\nNo FBD elements to display in debug table.")
        print("This may indicate an empty diagram or a parsing issue.")
        return
    
    # Print FBD context information
    if fbd_context:
        print("\n" + "="*80)
        print("AUTO-LAYOUT DEBUG TABLE")
        print("="*80)
        print(f"POU Name: {fbd_context.get('pou_name', 'Unknown')}")
        print(f"POU Type: {fbd_context.get('pou_type', 'Unknown')}")
        print(f"FBD Index: {fbd_context.get('fbd_index', 0)}")
        
        if 'total_fbds_in_pou' in fbd_context:
            print(f"Total FBDs in POU: {fbd_context['total_fbds_in_pou']}")
        if 'total_fbds_in_document' in fbd_context:
            print(f"Total FBDs in Document: {fbd_context['total_fbds_in_document']}")
        
        if fbd_context.get('fallback'):
            print("Note: Using fallback to first FBD in POU")
        if fbd_context.get('fallback_search'):
            print("Note: Using fallback document-wide search")
        if 'error' in fbd_context:
            print(f"Error: {fbd_context['error']}")
        
        print("-"*80)
    else:
        print("\n" + "="*80)
        print("AUTO-LAYOUT DEBUG TABLE")
        print("="*80)
    
    # Calculate column widths
    col_widths = {
        'id': max(8, max(len(str(d.block_id)) for d in debug_info)),
        'type': max(15, max(len(d.block_type) for d in debug_info)),
        'name': max(15, max(len(d.block_name) for d in debug_info)),
        'x_before': 10,
        'y_before': 10,
        'w_before': 10,
        'h_before': 10,
        'x_after': 10,
        'y_after': 10,
        'w_after': 10,
        'h_after': 10
    }
    
    # Print separator
    def print_separator():
        sep = "+"
        sep += "-" * (col_widths['id'] + 2) + "+"
        sep += "-" * (col_widths['type'] + 2) + "+"
        sep += "-" * (col_widths['name'] + 2) + "+"
        sep += "-" * (col_widths['x_before'] + 2) + "+"
        sep += "-" * (col_widths['y_before'] + 2) + "+"
        sep += "-" * (col_widths['w_before'] + 2) + "+"
        sep += "-" * (col_widths['h_before'] + 2) + "+"
        sep += "-" * (col_widths['x_after'] + 2) + "+"
        sep += "-" * (col_widths['y_after'] + 2) + "+"
        sep += "-" * (col_widths['w_after'] + 2) + "+"
        sep += "-" * (col_widths['h_after'] + 2) + "+"
        print(sep)
    
    # Print header
    print("\n" + "="*80)
    print("AUTO-LAYOUT DEBUG TABLE - Element Positions Before/After")
    print("="*80)
    
    print_separator()
    header = "| {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} | {:<{}} |".format(
        "Element ID", col_widths['id'],
        "Type", col_widths['type'],
        "Name", col_widths['name'],
        "X Before", col_widths['x_before'],
        "Y Before", col_widths['y_before'],
        "W Before", col_widths['w_before'],
        "H Before", col_widths['h_before'],
        "X After", col_widths['x_after'],
        "Y After", col_widths['y_after'],
        "W After", col_widths['w_after'],
        "H After", col_widths['h_after']
    )
    print(header)
    print_separator()
    
    # Print data rows
    for info in debug_info:
        row = "| {:<{}} | {:<{}} | {:<{}} | {:>{}} | {:>{}} | {:>{}} | {:>{}} | {:>{}} | {:>{}} | {:>{}} | {:>{}} |".format(
            info.block_id, col_widths['id'],
            info.block_type[:col_widths['type']], col_widths['type'],
            info.block_name[:col_widths['name']], col_widths['name'],
            info.x_before, col_widths['x_before'],
            info.y_before, col_widths['y_before'],
            info.width_before, col_widths['w_before'],
            info.height_before, col_widths['h_before'],
            info.x_after, col_widths['x_after'],
            info.y_after, col_widths['y_after'],
            info.width_after, col_widths['w_after'],
            info.height_after, col_widths['h_after']
        )
        print(row)
    
    print_separator()
    
    # Print summary statistics
    total_elements = len(debug_info)
    elements_moved = sum(1 for d in debug_info if d.x_before != d.x_after or d.y_before != d.y_after)
    avg_x_change = sum(abs(d.x_after - d.x_before) for d in debug_info) / total_elements if total_elements > 0 else 0
    avg_y_change = sum(abs(d.y_after - d.y_before) for d in debug_info) / total_elements if total_elements > 0 else 0
    
    # Count by element type
    type_counts = {}
    for d in debug_info:
        element_type = d.block_type
        if element_type in ['IN_VAR', 'OUT_VAR']:
            type_key = 'Variables'
        else:
            type_key = 'Blocks'
        type_counts[type_key] = type_counts.get(type_key, 0) + 1
    
    print(f"\nSummary:")
    print(f"  Total elements processed: {total_elements}")
    for type_key, count in sorted(type_counts.items()):
        print(f"    {type_key}: {count}")
    print(f"  Elements repositioned: {elements_moved}")
    print(f"  Average X displacement: {avg_x_change:.1f}")
    print(f"  Average Y displacement: {avg_y_change:.1f}")
    print("="*80 + "\n")


# --------- Rewrite node positions in XML ---------

def rewrite_node_positions(g: Graph) -> None:
    """
    Update XML position elements with computed node coordinates.

    Modifies the original XML elements in-place by updating or creating
    <position x="..." y="..."/> elements. Handles both namespace-qualified
    and unqualified XML.

    Args:
        g: Graph with node.x and node.y assigned

    Side Effects:
        Modifies node.elem XML elements in-place

    Example:
        >>> # After layout computation
        >>> rewrite_node_positions(g)
        >>> xml_string = etree.tostring(root).decode()
    """
    for nid, node in g.nodes.items():
        # Handle namespace if present
        ns = node.elem.nsmap
        if ns and None in ns:
            # Element has default namespace, need to use it for position
            pos_tag = f'{{{ns[None]}}}position'
            pos = node.elem.find(pos_tag)
        else:
            pos = node.elem.find('position')
            pos_tag = 'position'
        
        if pos is not None:
            # Update existing position element
            pos.set('x', str(int(node.x)))
            pos.set('y', str(int(node.y)))
        else:
            # Create new position element if it doesn't exist
            if ns and None in ns:
                pos = etree.Element(pos_tag)
            else:
                pos = etree.Element('position')
            pos.set('x', str(int(node.x)))
            pos.set('y', str(int(node.y)))
            # Insert at the beginning of the element
            node.elem.insert(0, pos)


# --------- FBD targeting helpers ---------

def _find_target_fbd(root, ns: dict, target_pou_name: Optional[str] = None,
                     target_fbd_index: int = 0) -> Tuple[Optional[etree._Element], dict]:
    """
    Locate target FBD element within PLCOpen XML using POU name and FBD index.

    Implements a multi-stage search strategy:
    1. If target_pou_name specified: Search that specific POU
    2. Otherwise: Search first POU with FBD content
    3. Fallback: Document-wide FBD search

    PLCOpen Structure:
        <project>
          <pous>
            <pou name="MAIN_CONTROL" pouType="program">
              <body>
                <FBD>  <!-- This is the target -->
                  <block .../>
                  ...
                </FBD>
              </body>
            </pou>
          </pous>
        </project>

    Args:
        root: PLCOpen XML root element
        ns: Namespace dict from root.nsmap (empty dict if no namespace)
        target_pou_name: Specific POU name to search (None = auto-detect)
        target_fbd_index: FBD index within target POU (default 0)

    Returns:
        Tuple[Optional[etree._Element], dict]:
            - FBD element if found, None otherwise
            - Context dict with keys:
                - 'pou_name': str
                - 'pou_type': str ('program', 'function', 'functionBlock')
                - 'fbd_index': int
                - 'total_fbds_in_pou': int (if found in POU)
                - 'total_fbds_in_document': int (if fallback search)
                - 'fallback': bool (if used first-FBD fallback)
                - 'fallback_search': bool (if used document-wide search)
                - 'error': str (if no FBD found)

    Example:
        >>> root = etree.fromstring(xml_bytes)
        >>> ns = {'ns': root.nsmap[None]} if root.nsmap else {}
        >>> fbd, ctx = _find_target_fbd(root, ns, target_pou_name="MAIN", target_fbd_index=0)
        >>> if fbd is not None:
        ...     print(f"Found FBD in POU: {ctx['pou_name']}")
    """
    pou_prefix = 'ns:pou' if ns else 'pou'
    fbd_prefix = 'ns:FBD' if ns else 'FBD'
    
    if target_pou_name:
        # Search for specific POU by name
        if ns:
            target_pous = root.xpath(f'.//ns:pous/{pou_prefix}[@name="{target_pou_name}"]', namespaces=ns)
        else:
            target_pous = root.xpath(f'.//pous/{pou_prefix}[@name="{target_pou_name}"]')
        
        if not target_pous:
            print(f"WARNING: POU '{target_pou_name}' not found in PLCOpen XML.")
            print(f"         Falling back to searching all POUs. To fix this:")
            print(f"         1. Check POU name spelling (case-sensitive)")
            print(f"         2. Verify the POU exists in the <pous> section")
            print(f"         3. Use target_pou_name=None to auto-detect first available POU")
            # Fall back to searching all POUs
            target_pou_name = None
        else:
            # Found target POU, search for FBDs within it
            target_pou = target_pous[0]
            if ns:
                fbds = target_pou.xpath(f'.//{fbd_prefix}', namespaces=ns)
            else:
                fbds = target_pou.xpath(f'.//{fbd_prefix}')
            
            if fbds and target_fbd_index < len(fbds):
                context_info = {
                    'pou_name': target_pou_name,
                    'pou_type': target_pou.get('pouType', 'unknown'),
                    'fbd_index': target_fbd_index,
                    'total_fbds_in_pou': len(fbds)
                }
                return fbds[target_fbd_index], context_info
            else:
                print(f"WARNING: FBD index {target_fbd_index} not found in POU '{target_pou_name}'.")
                print(f"         POU has {len(fbds)} FBD(s) (indices 0-{len(fbds)-1}).")
                print(f"         Using FBD index 0 as fallback. To fix: adjust target_fbd_index parameter.")
                # Fall back to first FBD if available
                if fbds:
                    context_info = {
                        'pou_name': target_pou_name,
                        'pou_type': target_pou.get('pouType', 'unknown'),
                        'fbd_index': 0,
                        'total_fbds_in_pou': len(fbds),
                        'fallback': True
                    }
                    return fbds[0], context_info
    
    # Fallback: search all FBDs in the document
    if ns:
        all_fbds = root.xpath(f'.//{fbd_prefix}', namespaces=ns)
    else:
        all_fbds = root.xpath(f'.//{fbd_prefix}')
    
    if all_fbds:
        # Use the specified index, or 0 if out of range
        fbd_index = min(target_fbd_index, len(all_fbds) - 1)
        target_fbd = all_fbds[fbd_index]
        
        # Try to find which POU this FBD belongs to
        pou_element = target_fbd
        while pou_element is not None:
            if pou_element.tag.endswith('pou'):
                break
            pou_element = pou_element.getparent()
        
        pou_name = pou_element.get('name') if pou_element is not None else 'unknown'
        pou_type = pou_element.get('pouType') if pou_element is not None else 'unknown'
        
        context_info = {
            'pou_name': pou_name,
            'pou_type': pou_type,
            'fbd_index': fbd_index,
            'total_fbds_in_document': len(all_fbds),
            'fallback_search': True
        }
        
        return target_fbd, context_info
    
    # No FBDs found at all
    return None, {
        'error': 'No FBD elements found in PLCOpen XML document',
        'hint': 'Verify the XML contains <FBD> elements within <pou><body> sections. '
                'The document may only contain other diagram types (LD, SFC, ST, IL).'
    }


# --------- Public API ---------

def autolayout_fbd(xml_string: str, x_gap: int = 150, y_gap: int = 40,
                   left_margin: int = 50, top_margin: int = 50,
                   use_iec61131_layout: bool = True, debug: bool = True,
                   target_pou_name: Optional[str] = None,
                   target_fbd_index: int = 0, satellite_gap_buffer: int = 20,
                   satellite_alignment: str = 'center', satellite_stack_gap: int = 5) -> str:
    """
    Apply automatic hierarchical layout to PLCOpen TC6 Function Block Diagrams.

    **Main Entry Point** for the IEC 61131-3 aware auto-layout system. Parses PLCOpen
    XML, applies semantic or topological layering, positions blocks and satellites,
    and returns updated XML with new coordinates.

    Layout Modes:
        1. **IEC 61131-3 Semantic Layout** (use_iec61131_layout=True, default):
           - Detects SENSOR, CONTROL, ACTUATOR, GLUE blocks
           - Applies 11-layer semantic hierarchy
           - Groups related instruments (FT_101, FT_102, ...)
           - Positions satellites adjacent to parent blocks
           - Optimized for industrial control diagrams

        2. **Generic Topological Layout** (use_iec61131_layout=False):
           - Longest-path layering (Coffman-Graham)
           - Median heuristic for crossing reduction
           - No domain-specific semantics
           - Suitable for general-purpose function block diagrams

    Algorithm Pipeline:
        1. Parse PLCOpen XML → Graph representation
        2. Classify blocks (SENSOR, CONTROL, ACTUATOR, GLUE)
        3. Identify satellites (variables, constants, setpoints)
        4. Break cycles using DFS back-edge detection
        5. Assign layers (semantic or topological)
        6. Order nodes within layers (affinity grouping + median heuristic)
        7. Assign (x, y) coordinates with dynamic layer widths
        8. Update XML position elements
        9. Optionally print debug table

    Args:
        xml_string: PLCOpen TC6 XML document as string
        x_gap: Horizontal spacing between layers (default 150)
        y_gap: Vertical spacing between nodes (default 40)
        left_margin: Left canvas margin (default 50)
        top_margin: Top canvas margin (default 50)
        use_iec61131_layout: Enable IEC 61131-3 semantic layout (default True)
        debug: Print before/after position table to console (default True)
        target_pou_name: Specific POU name to layout (default None = search all)
        target_fbd_index: FBD index within target POU (default 0)
        satellite_gap_buffer: Gap between layers (default 20)
        satellite_alignment: Satellite alignment mode: 'center', 'top', 'bottom' (default 'center')
        satellite_stack_gap: Gap between stacked satellites (default 5)

    Returns:
        Modified XML string with updated <position x="..." y="..."/> elements

    Raises:
        etree.XMLSyntaxError: If xml_string is malformed

    Example:
        >>> with open("diagram.xml") as f:
        ...     xml_in = f.read()
        >>> xml_out = autolayout_fbd(xml_in, y_gap=50, debug=True)
        >>> with open("diagram_layouted.xml", "w") as f:
        ...     f.write(xml_out)

    References:
        - PLCOpen TC6 XML v2.01: https://plcopen.org/technical-activities/xml-exchange-format
        - IEC 61131-3:2013 - Programmable Controllers - Part 3: Programming Languages
        - Sugiyama Framework: IEEE Trans. SMC 1981

    Performance:
        - Tested on diagrams up to 50 blocks
        - Typical runtime: <100ms for 20-block diagrams
        - Memory: O(V + E) where V=blocks, E=connections
    """
    root = etree.fromstring(xml_string.encode('utf-8'))
    
    # Check for FBD element with namespace support
    ns = {}
    if root.nsmap and None in root.nsmap:
        ns = {'ns': root.nsmap[None]}
    
    # Find target FBD based on POU name and index
    target_fbd, fbd_context = _find_target_fbd(root, ns, target_pou_name, target_fbd_index)
    
    if target_fbd is None:
        print(f"\nERROR: No suitable FBD found for layout.")
        if target_pou_name:
            print(f"       Target POU: '{target_pou_name}', FBD index: {target_fbd_index}")
        if 'error' in fbd_context:
            print(f"       {fbd_context['error']}")
        if 'hint' in fbd_context:
            print(f"       Hint: {fbd_context['hint']}")
        print(f"\nReturning original XML unchanged.")
        return xml_string  # nothing to do

    # Initialize debug info if requested
    debug_info = [] if debug else None
    
    g = parse_fbd(target_fbd, debug_info)
    
    # Identify satellites before main layout (for IEC 61131 mode)
    if use_iec61131_layout:
        satellites = identify_satellites(g)
    
    # Break cycles if any
    removed = break_cycles(g)
    
    # Check if this appears to be an IEC 61131 diagram
    has_control_blocks = any(node.classification in ['SENSOR', 'ACTUATOR', 'CONTROL'] 
                            for node in g.nodes.values() if node.kind == 'block')
    
    if use_iec61131_layout and has_control_blocks:
        # Use specialized IEC 61131 layout
        assign_macro_layers(g)
        layers = order_within_macro_layers(g)
        assign_coordinates_with_macro_layers(g, layers, x_gap=x_gap, y_gap=y_gap, 
                                            left_margin=left_margin, top_margin=top_margin,
                                            satellite_gap_buffer=satellite_gap_buffer,
                                            satellite_alignment=satellite_alignment,
                                            satellite_stack_gap=satellite_stack_gap)
    else:
        # Fall back to generic layout for non-control diagrams
        assign_layers(g)
        layers = order_within_layers(g)
        assign_coordinates(g, layers, x_gap=x_gap, y_gap=y_gap, 
                          left_margin=left_margin, top_margin=top_margin)
    
    # Route edges with orthogonal paths
    route_edges(g, removed)
    
    # Update debug info with final positions if debugging is enabled
    if debug_info is not None:
        for info in debug_info:
            if info.block_id in g.nodes:
                node = g.nodes[info.block_id]
                info.x_after = node.x
                info.y_after = node.y
                info.width_after = node.width
                info.height_after = node.height
        
        # Print the debug table with context information
        print_debug_table(debug_info, fbd_context)
    
    # Update XML with new positions
    rewrite_node_positions(g)

    return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')


# --------- CLI ---------

def main():
    import argparse, sys
    ap = argparse.ArgumentParser(description="Auto-layout IEC 61131-3 FBD XML (horizontal hierarchical)")
    ap.add_argument("input", help="input XML file path")
    ap.add_argument("-o", "--output", help="output XML file path (default: stdout)")
    ap.add_argument("--x-gap", type=int, default=120, help="horizontal gap between layers")
    ap.add_argument("--y-gap", type=int, default=40, help="vertical gap between nodes")
    ap.add_argument("--left-margin", type=int, default=50)
    ap.add_argument("--top-margin", type=int, default=50)
    ap.add_argument("--debug", action="store_true", help="enable debug output showing block positions before/after layout")
    args = ap.parse_args()

    data = sys.stdin.read() if args.input == "-" else open(args.input, "r", encoding="utf-8").read()
    out = autolayout_fbd(data, x_gap=args.x_gap, y_gap=args.y_gap, left_margin=args.left_margin, top_margin=args.top_margin, debug=args.debug)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

if __name__ == "__main__":
    main()
