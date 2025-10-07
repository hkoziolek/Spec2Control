# OpenPLC Function Block Diagram Generation Prompts

This document contains the complete set of prompts used to generate OpenPLC Function Block Diagrams (FBD) from control specifications. This prompt chain constitutes the second phase of the Spec2Control workflow, following the context generation phase to produce complete control system implementations.

## Process Overview

The generation process executes 10 sequential steps:

1. **Function Block Identification** - Identify required sensors, transmitters, actuators, and controllers
2. **Function Block Validation** - Cross-reference and validate completeness against specifications
3. **Main Control Logic** - Create primary control connections and logic functions
4. **Interlock & Alarm Logic** - Implement safety systems and alarm handling
5. **Parameter Configuration (Initial)** - Set configuration values and setpoints
6. **Parameter Refinement** - Complete and refine parameter assignments
7. **Output Variables** - Create system interfaces and monitoring points
8. **Comprehensive Validation** - Perform rule checks and system integrity validation
9. **Additional Rule Checks** - Function categorization and specification cleanup
10. **Boolean Optimization** - Minimize expressions and optimize signal routing

## Input Specification Format

The {{specification}} variable used throughout these prompts contains the control narrative merged with the context data generated from the preceding context generation prompt chain. This composite input includes:

- **Original Control Narrative** - The textual description of the control requirements
- **Identified Sensor Types** - Function block specifications for required sensors (ANALOG_IN, DIGITAL_IN, BOOL_IN)
- **Identified Actuator Types** - Function block specifications for required actuators (motors, valves)
- **Selected Control Strategy** - The chosen control approach with associated function blocks and connection patterns
- **BASIC_LIB Function Block Specifications** - Detailed pin definitions and parameter specifications

This composite specification provides the function block diagram generation process with complete contextual information to produce accurate, validated, and BASIC_LIB-compatible control implementations.

---

## Step 1: Function Block Identification

This step analyzes the control specification to identify all required function blocks. It focuses on identifying sensors, transmitters, actuators, controllers, and other main control elements while avoiding basic logic functions.

**Prompt Name:** `openplc-function-blocks-v2`

**Purpose:** Analyze the provided specification to identify all required function blocks for the control system.

**Prompt:**

```
Analyze the provided specification, interlocks and alarms to identify all required function blocks.

Provide output in the following format, no explanations, no markdown:

* Function Blocks *
MyFBType MyFB1
MyOtherFBType MyOtherFB1

Rules:
- Only include function blocks that are explicitly required by the specification
- Instantiate any alarm switches explicitly listed in taglists as function blocks of type DIGITAL_IN
- Do not create DIGITAL_IN blocks for alarms that are not in the taglist, these are not separate devices but are handled with parameters of other blocks.
- Instantiate interlocks explicitly listed in taglists as function blocks of type BOOL_IN
- Use instance names based on tagnames
- Do not include basic logic functions (OR, AND, NOT, XOR) - these will be handled separately
- Focus on main control elements like sensors, transmitters, actuators, controllers, etc.

{{specification}}
```

---

## Step 2: Function Block Validation

This validation step ensures that all required function blocks are properly identified and included in the list. It cross-references the specification against the generated function block list to catch any missing elements.

**Prompt Name:** `openplc-function-blocks-validation`

**Purpose:** Validate and update the function block list to ensure completeness against the control narrative.

**Prompt:**

```
Based on the provided control narrative, function block specifications, and the already generated function block list from a previous step, update the list to make sure that all required function blocks are in the list. 

Rules
- check tagname references in the specification and make sure all sensors (e.g., LIT-101), transmitters, actuators (e.g., LV-101), and controllers (e.g., LIC-101) are covered, add missing ones.
- check that alarm switches from taglists are mapped to DIGITAL_IN function blocks
- check that interlocks from taglists are mapped to BOOL_IN function blocks
- remove any function blocks created for alarms, which are not mentioned in the taglist.


Provide output in the same format as before, no explanations, no markdown.

* Control Narrative and Function Block Types * 
{{specification}}

* Function Block List * 
{{function-blocks}}
```

---

## Step 3: Block Connections and Main Control Logic

This step creates the fundamental connections between function blocks for the main control strategy. It focuses on process control connections while deliberately excluding interlock and alarm logic, which are handled in a separate step.

**Prompt Name:** `openplc-block-connections-and-logic`

**Purpose:** Create connections between function blocks and add necessary logic functions for the main control strategy.

**Prompt:**

```
Create connections between function blocks and add necessary logic functions exclusively for the main control strategy identified in the specification. Disregard any connections required for interlocks or alarms.

Rules for Functions:
- Only use IEC 61131-3 functions: OR, TON, NOT, etc.
- When creating functions with two input parameter (e.g., OR, ADD, GT, EQ, TON, etc.), always create also two data connections or parameter data connection, so that no input is left unbound.
- For IEC 61131-3 function with an variable number of input parameters (OR, XOR, AND, ADD, etc.) it is ok to use more than two, also to limit the number of necessary functions.
- Only include functions prescribed by the control strategy
- Give each function a descriptive instance name, ending with suffix _TypeName (examples: _OR, _TON).
- If no functions are needed for the control strategy, leave the section * Functions * empty

Rules for Block-to-Block Connections:
- Connect outputs of one function block directly to inputs of another
- Use the exact function block instance names from the previous step
- For each created logic function, create appropriate connections both for inputs and outputs

Provide output in the following format, no explanations, no markdown:

* Functions *
GT Comparator1_GT
TON Timer1_TON

* Block-to-Block Connections *
FB1.OUT, FB2.IN1
FB2.Signal, FB3.Control



Specification:
{{specification}}

Function Blocks:
{{function-blocks}}
```

---

## Step 4: Interlock and Alarm Logic Implementation

This step specifically handles the implementation of interlock and alarm logic, which is kept separate from the main control strategy. It creates the necessary boolean logic functions and connections to implement safety and alarm systems.

**Prompt Name:** `openplc-block-connections-interlocks`

**Purpose:** Create functions, data connections, and parameter data connections that implement interlock and alarm logic.

**Prompt:**

```
Create functions, data connections, and parameter data connections that implement interlock and alarm logic, as needed per the specification. Assume IEC 61131-3 naming and types.

Rules for Functions:
- Only use IEC 61131-3 boolean functions (OR, XOR, AND, NOT) with IN1, IN2, IN, OUT if needed. If the boolean function only has one input (e.g NOT), make sure that there is no number behind the input parameter (IN in stead of IN1).
- Single alarm output signals driving an inhibit can be directly connected without a function.
- Only include functions required for an interlock, permissive, or alarm
- Give each function a descriptive instance name ending with _OR, _AND, _NOT (e.g., HighTempTrip_OR).
- If no functions are needed, leave the section * Functions * empty

Rules for Data Connections:
- Only create connections that refer to interlocks and alarms, but make sure to cover all interlocks and alarms completely.
- Connect alarm output signals (BOOL) to inhibit input parameters (no permissive parameter available), as prescribed by the specification, unless the alarm output is already connected to DIGITAL_IN or BOOL_IN. 
- Use only BOOL alarm/limit/trip outputs (e.g., *.High_Alarm, *.Low_Alarm, *.DI_Out) for interlocks/permissives/inhibits; do not route REAL signals into boolean logic.
- Do not modify previously created data connections for process values and the main control strategies.
- Ensure for functions that at minimum IN1 and IN2 are connected with distinct sources, but more inputs (IN3, IN4, ...) are ok if needed.
- Do not create any numeric comparison or arithmetic functions.
- Use the exact function block instance names from the previous step.
- Do not connect boolean output signals to real type input parameters.
- Ensure that function blocks DIGITIAL_IN and BOOL_IN receiving alarms or interlock signals as input also connects its output (*DI_Out or *.Bool_Out)  to the related inhibit input. 

Rules for Parameter Data Connections:
- Parameter data connections consist of comma-separated pair <source>, <target>.
- <source> is always a literal value (e.g., an alarm range literal), never a function block or function
- <target> must be an existing input parameter of a function or function block
- Map from specification all allowed ranges to configured alarm high and low levels (example PV_High, PV_Low)
- Make sure to cover alarm high and low parameters if information available, do not have highs without lows
- Connect literals for alarm limits to PV_High, PV_Low
- Never connect literals to DI_Raw input parameters
- Never connect literal TRUE directly to inhibit inputs; only map alarms/trips to such inputs.

If a section has no items, keep the header and leave it empty (no placeholder text).
Provide output in the following format, no explanations, no markdown, no XML tags:

* Functions * 
OR InterlockTank1_OR
AND Alarm23_AND

* Data Connections *
FB1.OUT, FB2.IN1
FB2.Alarm, FB3.Inhibit
InterlockTank1_OR.OUT, Valve.Inhibit

* Parameter Data Connections *
42, FB1.AlarmHigh
500, FB2.MV_Min


Specification:
{{specification}}

Function Blocks:
{{function-blocks}}

Data Connections:
{{data-connections}}
```

---

## Step 5: Parameter Data Connections (Initial)

This step identifies specific parameter values from the specification and creates parameter data connections. It focuses on configuration parameters, setpoints, and enable/disable flags that are explicitly mentioned in the specification.

**Prompt Name:** `openplc-parameter-data-connections`

**Purpose:** Identify specific values in the specification for input parameters of function blocks and functions.

**Prompt:**

```
Identify specific values in the specification for input parameters of already instantiated function blocks and functions.


Rules for Parameter Data Connections:
- Consist of comma-separate pair <source>, <target>
- <source> is always a literal, never another function block or function
- The <source> literal always complies to a 61131 data type ((BOOL, REAL, INT, TIME, ...)
- <target> is always an input parameter of a function or function block
- For input parameters of functions, use data type real for any GT, GE, EQ, LT, LE, NE inputs, make sure that the input parameters are IN1, IN2, OUT.
- If no parameter connections with specific values are mentioned, leave section empty
- Focus on configuration parameters, setpoints, and enable/disable flags
- Do not use Parameter Data Connections for DIGITAL_IN function blocks.
- For ranges in the specification, try to map their start and end to low and high input parameter of respective function blocks.
- Connect literals for alarm limits to the respective alarm limit input parameters of function blocks
- Never connect literals to DI_Raw input parameters
- Never connect literal TRUE directly to an inhibit

Provide output in the following format, no explanations, no markdown:

* Parameter Data Connections *
some_value, FB1.Param1
another_value, FB2.SetPoint
TRUE, FB1.Enable
my_value, Function1.IN1
my_value2, Function2.IN2


Specification:
{{specification}}

Function Blocks:
{{function-blocks}}

Functions and Connections:
{{functions-connections}}
```

---

## Step 6: Parameter Data Connections (Updated)

This step updates and refines the parameter data connections from the previous step, ensuring that all specification requirements are fully covered and that ranges are properly mapped to high and low parameters.

**Prompt Name:** `openplc-input-variables-and-connections`

**Purpose:** Update the previously created Parameter Data Connections by identifying additional specific values from the specification.

**Prompt:**

```
Update the previously created Parameter Data Connections by identifying specific values in the specification for input parameters of already instantiated function blocks and functions.

Rules for Parameter Data Connections:
- If the specification is already fully covered by the previously generated Parameter Data Connections, output them as before.
- For input parameters of functions, use data type real for any GT, GE, EQ, LT, LE, NE inputs, make sure that the input parameters are IN1, IN2, OUT.
- Do not use Parameter Data Connections for DIGITAL_IN function blocks.
- For ranges (alarms, ratios, operating range, etc.) in the specification, map the range start and end to low and high input parameters of respective function blocks (e.g., PV_High, PV_Low, MV_MIN, MV_MAX, etc.)
- Make sure to cover range high and low parameters if information or defaults available, do not have highs without lows or vice versa
- Connect literals for alarm limits to the respective alarm limit input parameters of function blocks
- Never connect literals to DI_Raw input parameters
- Never connect literal TRUE directly to an inhibit

Update the previous output for Parameter Data Connection and provide it in the following format, no explanations, no markdown:

* Parameter Data Connections *
some_value, FB1.Param1
another_value, FB2.SetPoint
TRUE, FB1.Enable
my_value, Function1.IN1
my_value2, Function2.IN2


Specification:
{{specification}}

Function Blocks:
{{function-blocks}}

Block Connections and Logic:
{{block-connections-and-logic}}
{{interlocks-alarms}}

Parameter Data Connections:
{{parameter-data-connections}}
```

---

## Step 7: Output Variables and Connections

This step creates output variables that receive outputs from function blocks, enabling the function block diagram to interface with external systems or provide monitoring points for the control system.

**Prompt Name:** `openplc-output-variables-and-connections`

**Purpose:** Create output variables and their connections to function blocks for system interfacing and monitoring.

**Prompt:**

```
Create output variables and their connections to function blocks.

Provide output in the following format, no explanations, no markdown:

* Variables *
VarType MyOutputVar
OtherVarType MyOutputVar2

* Data Connections *
FB1.OutputParam, MyOutputVar
FB2.Status, MyOutputVar2

Rules for Output Variables:
- Only create variables that receive outputs from function blocks
- Use appropriate IEC 61131-3 data types (BOOL, INT, REAL, etc.)
- Do not create boolean output variables in case there are already corresponding DIGITAL_IN function blocks.
- Variable names must refer to the related tag name and the variable's purpose in the control strategy.
- Only create variables explicitly mentioned in the specification
- Do not create output variables for alarms.

Rules for Data Connections concerning output variables:
- Connect function block outputs to output variables
- Make sure that each created output variable has a data connection
- Use exact instance names from previous steps
- If no output variables are needed, leave sections empty

Specification:
{{specification}}

Function Blocks:
{{function-blocks}}
```

---

## Step 8: Rule Checks and Validation

This comprehensive validation step performs multiple checks to ensure the complete function block diagram is consistent, properly connected, and follows IEC 61131-3 standards. It consolidates all connections and validates the overall system integrity.

**Prompt Name:** `openplc-rule-checks`

**Purpose:** Perform comprehensive rule checks and validation on the complete OpenPLC Function Block Diagram.

**Prompt:**

```
Perform rule checks and validation on the complete OpenPLC Function Block Diagram.

Validation Rules:
- Check that all function block instance names are consistent across all sections, refer only to tags, and include no reference to any types (e.g., AI, AnalogIn, PID, etc.)
- Verify all connections reference valid function block instances and parameters
- Ensure all variables have appropriate IEC 61131-3 data types
- Confirm no orphaned connections (connections to non-existent blocks/variables)
- Ensure that all AND, OR, XOR, IN, NOT, ADD, SUB, MULT, DIV blocks have valid data connections on all inputs and outputs
- Ensure that all TON, TOF, TP blocks have timing values via parameter data connections or data connections
- Validate that required connections from specification are present
- Check for logical consistency in the control flow
- Merge all connections in a section * Data Connections *, do not have a separate section * Block-to-Block Connections *
- Ensure that each function has a descriptive name.
- Ensure that no Parameter Data Connection refers to a DIGITAL_IN


Provide the output as text (no markdown) in following format, no explanations: 

* Function Blocks *
MyFBType MyFB1
MyOtherFBType MyOtherFB1

* Variables *
VarType MyVar
OtherVarType MyVar2

* Functions *
ADD SetpointSUM_ADD
MyOtherFuncType MyOtherFunc2_MyOtherFuncType
GT Comparator1_GT
TON Timer1_TON

* Data Connections * 
MyFB1.ParC, MyOtherFB.B
MyVar, MyFB1.ParB
MyCM1.C, MyVar2

* Parameter Data Connections *
some_value, MyFB1.Param1



Specification:
{{specification}}

Function Blocks:
{{function-blocks}}

Block Connections and Logic:
{{block-connections-and-logic}}
{{connections2}}
{{connections3}}

Parameter Data Connections:
{{parameter-data-connections}}

Output Variables and Connections:
{{output-variables-and-connections}}
```

---

## Step 9: Additional Rule Checks

<!-- 
This step performs additional specific rule checks focusing on proper categorization
of IEC 61131-3 standard functions versus function blocks, removal of prose text,
and elimination of improper parameter data connections.
-->

**Prompt Name:** `openplc-rule-checks2`

**Purpose:** Perform additional rule checks for proper function categorization and specification cleanup.

**Prompt:**

```
Update the following function block diagram specification. For output, keep the same format as before and output also all unmodified entries as before, no explanations, no markdown.

Check the following rules:
- FunctionCategorization: make sure that 61131 standard functions (NOT, AND, OR, XOR, SEL, ADD, SUB, etc.) appear under section *Functions* but not under section *Function Blocks*, move wrongly-assigned entries to *Functions*.

- NoProse: make sure that the specification does not contain prose text, remove entries with prose text.

- NoDI_RawParameterDataConnections: remove any entries in * Parameter Data Connections * that refer to DI_Raw parameters.


{{function-block-diagram-specification}}
```

---

## Step 10: Boolean Expression Optimization

<!-- 
This final optimization step minimizes boolean expressions, moves literal values
to appropriate sections, and handles multiple inputs to boolean targets by
creating appropriate OR functions for proper signal combination.
-->

**Prompt Name:** `append_two_inputs`

**Purpose:** Optimize boolean expressions and handle multiple inputs to boolean targets.

**Prompt:**

```
Update the following function block diagram specification. For output, keep the same format as before and output also all unmodified entries as before, no explanations, no markdown.

Check the following rules:
- LiteralToParameterDataConnection: move any entries in * Data Connections * where the first item before the comma is a literal to * Parameter Data Connections *

- MinimizeBooleanExpressions: analyze the boolean functions and data connections and minimize the number of functions as much as possible without altering the functionality, rewire accordingly. For example, combine different OR functions or AND functions or XOR functions.

- MultipleInputsOR: check if there are any two entries in * Data Connections * with identical boolean targets (parameters named inhibit, enable, auto). For each of these cases add a new function of type OR with appropriate instance name in * Functions *, replace the targets in the previous data connection entries with OR.IN1 and OR.IN2, and add a new data connection OR.OUT,<common target>


{{function-block-diagram-specification}}
```

---

## Process Flow Summary

The complete process follows this systematic approach:

1. **Function Block Identification** - Identify all required control elements
2. **Validation** - Ensure completeness against specification
3. **Main Control Logic** - Create primary control connections
4. **Interlock/Alarm Logic** - Implement safety and alarm systems
5. **Parameter Configuration** - Set up configuration values
6. **Parameter Refinement** - Complete parameter assignments
7. **Output Variables** - Create system interfaces
8. **Validation & Consolidation** - Comprehensive rule checking
9. **Additional Checks** - Function categorization and cleanup
10. **Optimization** - Boolean expression minimization and optimization

Each step builds upon the previous outputs, creating a comprehensive and validated OpenPLC Function Block Diagram specification that can be used to generate actual control system code.