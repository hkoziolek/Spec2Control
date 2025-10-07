# Context Generation Prompts for Control System Analysis

This document contains the complete set of prompts used for context generation in control system analysis. The context generation process forms the first prompt chain in the Spec2Control workflow, systematically analyzing control narratives to identify required sensors, actuators, and control strategies. This foundational analysis provides essential context that simplifies and guides the subsequent prompt chain for generating comprehensive function block diagrams.

The prompts have been specifically customized and tailored to align with the specifications, restrictions, and functionality of the BASIC_LIB library. All function block types, parameter names, connection patterns, and control strategies referenced in these prompts correspond directly to the components available in the BASIC_LIB, ensuring seamless integration and compatibility with the target control system implementation.

---

## Step 1: Sensor Function Block Identification

This step analyzes the control narrative to identify all sensor types required for the control system. It focuses on determining which sensor function blocks (ANALOG_IN, DIGITAL_IN, BOOL_IN) are needed based on the types of measurements and monitoring requirements described in the control narrative. The step provides complete function block specifications for each identified sensor type.

**Prompt Name:** `contextgen1-sensors`

**Purpose:** Analyze the control narrative to determine which sensor function block types are required for implementation.

**Prompt:**

```
Determine which of the available sensor function block types are needed to implement the control logic in the provided control narrative. 
Output first the heading "*** Available Function Block Types ***"
Output the full specification of all required block types (each block type only once) including Direction,Pin Name,Type,Description for all pins.

If transmitters are mentioned, always include ANALOG_IN.
If alarm switches are mentioned, always include DIGITAL_IN.
If interlock alarms are mentioned, always include BOOL_IN. 
If no sensors are mentioned in the control narrative or only signals coming from actuators, just output "No sensors."
Provide no additional explanations.

*** Available Function Block Types ***
ANALOG_IN
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the AI block for HMI and alarms.
Input,Description,STRING,Longer description of the measurement purpose.
Input,Raw_Signal,REAL,Raw 4-20mA input signal from field transmitter (mA).
Input,PV_High,REAL,High alarm limit for PV. 
Input,PV_Low,REAL,Low alarm limit for PV.
Input,Scaling_Slope,REAL,Slope for linear scaling of raw signal to engineering units.
Input,Scaling_Offset,REAL,Offset for scaling raw input to engineering units.
Input,Alarm_Enable,BOOL,Enables or disables alarm monitoring.
Output,PV,REAL,Process Variable, scaled engineering value (e.g. flow rate).
Output,High_Alarm,BOOL,TRUE if PV exceeds PV_High limit.
Output,Low_Alarm,BOOL,TRUE if PV falls below PV_Low limit.
Output,General_Fault,BOOL,TRUE if sensor fault.

BOOL_IN
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of the measurement purpose.
Input,Bool_In,BOOL,The boolean value to be monitored.
Input,Alarm_OnTrue,BOOL,Enable alarm when Bool_In is TRUE.
Input,Alarm_OnFalse,BOOL,Enable alarm when Bool_In is FALSE.
Input,Latch_Enable,BOOL,Enables latching of the alarm/status.
Input,Reset_Latch,BOOL,Resets a latched alarm/status.
Output,Bool_Out,BOOL,The monitored boolean value.
Output,Alarm_Active,BOOL,Indicates if an alarm condition is active.
Output,Latched_Status,BOOL,The latched state if latching is enabled.

DIGITAL_IN
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of the measurement purpose.
Input,DI_Raw,BOOL,Raw digital input from the field.
Input,DebounceTime,TIME,Time for debouncing the input to prevent false triggers.
Input,EnableAlarm,BOOL,Enables or disables alarm monitoring for the digital input.
Output,DI_Out,BOOL,,Debounced and stable digital output.
Output,Fault_State,BOOL,Indicates a fault in the input signal (e.g. wiring fault).

*** Control Narrative *** 
{{control-narrative}}
```

---

## Step 2: Actuator Function Block Identification

This step analyzes the control narrative to identify all actuator types required for the control system. It determines which actuator function blocks (motors, valves, etc.) are needed based on the control requirements described in the narrative. The step provides default selections for ambiguous cases and complete specifications for each identified actuator type.

**Prompt Name:** `contextgen1-actuators`

**Purpose:** Analyze the control narrative to determine which actuator function block types are required for implementation.

**Prompt:**

```
Determine which of the available actuator function block types are needed to implement the control logic in the provided control narrative. 
Output the full specification of all required block types (each block type only once) including Direction,Pin Name,Type,Description for all PINs.
Output two newlines.
If only transmitters and pure sensors are mentioned, just output "No actuators".
If unsure about a valve type, choose VALVE_ELECTRIC as default.
If unsure about a pump type, choose MOTOR_ON_OFF as default.
Provide no additional explanations.

*** Available Function Block Types ***
MOTOR_2SPD
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of motor's purpose.
Input,Start_Cmd,BOOL,Command to start the motor.
Input,Stop_Cmd,BOOL,Command to stop the motor.
Input,Speed_High_Cmd,BOOL,Command for high speed.
Input,Speed_Low_Cmd,BOOL,Command for low speed.
Input,Inhibit,BOOL,Inhibits starting the motor and can receive alarm signals.
Output,Motor_Start_Out,BOOL,Output to motor starter.
Output,FB_Running,BOOL,Feedback indicating motor is running.
Output,FB_Trip,BOOL,Feedback indicating motor has tripped.
Output,FB_HighSpeed,BOOL,Feedback indicating high speed is active.
Output,FB_LowSpeed,BOOL,Feedback indicating low speed is active.
Output,Alarm_Speed_Error,BOOL,Indicates failure to achieve commanded speed or speed conflict.

MOTOR_ON_OFF
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of motor's purpose.
Input,Start_Cmd,BOOL,Command to start the motor.
Input,Stop_Cmd,BOOL,Command to stop the motor.
Input,Start_Delay,TIME,Delay before motor starts after command.
Input,MinRunTime,TIME,Minimum time motor must run once started.
Input,Inhibit,BOOL,Inhibits starting the motor and can receive alarm signals.
Output,Motor_Start_Out,BOOL,Output to motor starter.
Output,FB_Running,BOOL,Feedback indicating motor is running.
Output,FB_Trip,BOOL,Feedback indicating motor has tripped (overload, fault).
Output,Alarm_Start_Fail,BOOL,Indicates motor failed to start.
Output,Alarm_Stop_Fail,BOOL,Indicates motor failed to stop.

MOTOR_VSD
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of motor's purpose.
Input,Start_Cmd,BOOL,Command to start the VSD.
Input,Stop_Cmd,BOOL,Command to stop the VSD.
Input,Speed_SP,REAL,Desired speed setpoint (e.g., 0-100%).
Input,Accel_Ramp,TIME,Acceleration ramp time.
Input,Decel_Ramp,TIME,Deceleration ramp time.
Input,Inhibit,BOOL,Inhibits starting the motor and can receive alarm signals.
Output,Speed_Out,REAL,Analog output to VSD for speed command.
Output,FB_Running,BOOL,Feedback from VSD indicating it is running.
Output,FB_Fault,BOOL,Feedback from VSD indicating a fault.
Output,FB_Ready,BOOL,Feedback from VSD indicating it is ready to run.
Output,FB_ActualSpeed,REAL,Actual motor speed feedback from VSD.
Output,Alarm_Speed_Deviation,BOOL,Indicates a significant difference between commanded and actual speed.
Output,Alarm_Comm_Fail,BOOL,Indicates communication failure with VSD.

VALVE_ELECTRIC
Direction,Pin Name,Type,Description 
Input,Name,STRING,Descriptive name of the electric control valve. 
Input,Description,STRING,Longer description of the valve's role. 
Input,Control_Signal,REAL,Valve position command input (0-100 percent). 
Input,Manual_Mode,BOOL,TRUE for manual control, FALSE for automatic control. 
Input,Manual_Position,REAL,Valve position used when Manual_Mode is TRUE (0-100%). 
Input,Open_Limit,REAL,Valve fully open position limit. 
Input,Close_Limit,REAL,Valve fully closed position limit. 
Input,Timeout,TIME,Maximum time allowed for valve to reach position. 
Input,Inhibit,BOOL,Inhibits operating the valve and can receive alarm signals
Output,Valve_Position,REAL,Current valve position output to the actuator. 
Output,Feedback_Pos,REAL,Actual valve position feedback (0-100%). 
Output,Valve_Moving,BOOL,TRUE if valve actuator is moving. 
Output,Position_Error,BOOL,TRUE if valve fails to reach commanded position within Timeout. 
Output,Alarm,BOOL,General alarm flag for valve faults or interlocks.

VALVE_ON_OFF
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the electric control valve. 
Input,Description,STRING,Longer description of the valve's role. 
Input,Open_Cmd,BOOL,Command to open the valve.
Input,Close_Cmd,BOOL,Command to close the valve.
Input,Timeout,TIME,Maximum time allowed for valve to reach position.
Input,Inhibit,BOOL,Inhibits operating the valve and can receive alarm signals.
Output,FB_Opened,BOOL,Feedback from 'Valve Open' limit switch.
Output,FB_Closed,BOOL,Feedback from 'Valve Closed' limit switch.
Output,Valve_Open_Out,BOOL,Output to open the valve.
Output,Valve_Close_Out,BOOL,Output to close the valve.
Output,Alarm_Position_Error,BOOL,Indicates position discrepancy or timeout.
Output,Alarm_General,BOOL,General valve fault.

*** Control Narrative *** 
{{control-narrative}}
```

---

## Step 3: Control Strategy Selection and Function Block Specification

This step analyzes the control narrative to determine the most appropriate control strategy from a comprehensive library of available strategies. It evaluates multiple strategies with probability assessments, selects the most suitable one, and provides complete function block specifications for the selected strategy. This includes detailed pin specifications and intended block-to-block connections to guide the implementation.

**Prompt Name:** `contextgen1-strategies`

**Purpose:** Analyze the control narrative to select the most appropriate control strategy and provide corresponding function block specifications.

**Prompt:**

```
Determine which of the available control strategies and corresponding function block types are needed to implement the control logic in the provided control narrative. 
Output the heading *** Available Control Strategies ***.
Output a table of the needed control strategies names, each with an estimated probability that it is needed here. Output a single selected, most needed control strategy in next line. It should be like "Selected Control Strategy: <CONTROL STRATEGY NAME> ". In next line add short explaination "Short explanation:" 

Output the description and Intended Block-to-Block Connections Types of the selected strategy as described below without any changes.
Output the heading *** Available Function Block Types ***.
Then output the full specification of all required block types (each block type only once) for the selected control strategy including Direction,Pin Name,Type,Description for all PINs.
Provide no additional explanations.

*** Available Control Strategies *** 
* Control Strategy * 
PID Control
** Description **
The system consists of an analog input, a PID controller, and an actuator. The analog input provides a process variable to the PID controller, which compares it to a predefined setpoint. Based on the difference (error), the PID controller calculates a control signal and sends it to the actuator to regulate the process.
** Intended Block-to-Block Connections Types **
ANALOG_IN.PV, PID_BASIC.PV 
PID_BASIC.XOUT, VALVE_ELECTRIC.Control_Signal

* Control Strategy * 
Cascade Control 
** Description ** 
The system includes two PID controllers (primary and secondary), two analog inputs, and an actuator. The primary analog input measures the main process variable and feeds it into the primary PID controller, which compares it to a predefined setpoint. The primary controller outputs a setpoint to the secondary PID controller, which receives its own analog input from a faster-responding variable. The secondary controller then sends a control signal to the actuator to regulate the process more precisely and responsively.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.PV, PID_BASIC1.PV 
PID_BASIC1.XOUT, PID_BASIC2.SP
ANALOG_IN2.PV, PID_BASIC2.PV 
PID_BASIC2.XOUT, VALVE_ELECTRIC.Control_Signal

* Control Strategy *
Duty-Standby
** Description **
The system includes two identical actuators (e.g., pumps), runtime monitors, and a control logic unit. One actuator operates as the duty unit, while the other remains in standby. The control logic monitors runtime or fault conditions and switches to the standby actuator either if the duty cycle has expired or if one pump becomes faulty. Multiple timers can be involved.
** Intended Block-to-Block Connections Types **
MOTOR_ON_OFF1.FB_Running, DUTY_STANDBY.PumpA_RunFB
MOTOR_ON_OFF2.FB_Running, DUTY_STANDBY.PumpB_RunFB
<defined time for duty-standby cycle>,TON1.PT
TON1.Q, DUTY_STANDBY.DutyElapsed
DUTY_STANDBY.CmdPumpA, MOTOR_ON_OFF1.StartCmd
DUTY_STANDBY.CmdPumpB, MOTOR_ON_OFF2.StartCmd


* Control Strategy *
VOTING
** Description ** 
The system includes multiple identical sensors (e.g., three temperature transmitters), a voting logic unit, and an actuator. Each sensor provides an analog input to the voting logic unit, which compares the signals. Based on a predefined logic (e.g., 2-out-of-3 agreement), the unit selects the valid signal. This selected signal is then used to drive the actuator or trigger alarms, ensuring reliable operation even if one sensor fails.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.PV, VOTING_ANALOG.Input1
ANALOG_IN2.PV, VOTING_ANALOG.Input2
ANALOG_IN3.PV, VOTING_ANALOG.Input3
"Median", VOTING_ANALOG.Voting_Scheme
VOTING_ANALOG.Voted_Output, PID_BASIC.PV

* Control Strategy *
FEEDFORWARD
** Description ** 
The system includes a disturbance sensor (analog input), a feedforward controller, a process variable sensor, and an actuator. The disturbance sensor measures an external variable that affects the process (e.g., flow rate, load). The feedforward controller calculates a corrective control signal based on this input and sends it to the actuator.
** Intended Block-to-Block Connections Types **
ANALOG_IN.PV, MULT.IN1
<kff value>, MULT.IN2
MULT.OUT, ADD.IN1
PID_BASIC.XOUT, ADD.IN2
ADD.OUT, VALVE_ELECTRIC.Control_Signal

* Control Strategy *
OVERRIDE
** Description ** 
The system includes multiple analog inputs (e.g., pressure, temperature), limit detectors, a control selector, and an actuator. Each input is monitored for critical limits.
When a limit is exceeded, the control selector overrides the normal control signal and sends a protective signal to the actuator.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.High_Alarm, OR.IN1
ANALOG_IN2.High_Alarm, OR.IN2
ANALOG_IN3.High_Alarm, OR.IN3
OR.OUT, NOT.IN
NOT.OUT, PID_BASIC.AUTO
100.0, PID_BASIC.X0

* Control Strategy *
SPLIT RANGE
** Description ** 
The system includes one PID controller, one analog input, and two actuators (e.g., control valves). The analog input provides the process variable to the PID controller, which compares it to a setpoint. The controller outputs a single control signal that is split across two actuators, each operating in a different range of the signal.
** Intended Block-to-Block Connections Types **
ANALOG_IN.PV, PID_BASIC.PV 
PID_BASIC.XOUT, SPLIT_RANGE.IN
SPLIT_RANGE.OUT1, VALVE_ELECTRIC1.Control_Signal
SPLIT_RANGE.OUT2, VALVE_ELECTRIC2.Control_Signal

* Control Strategy *
Ratio Control
** Description ** 
The system includes two flow transmitters, a ratio controller, (optionally) a slave PID controller, and a control valve. Each flow transmitter provides an analog input to the ratio controller. The ratio controller maintains a predefined ratio between the two flows by sending a slave setpoint to the PID Controller. Multiplications are handled inside the controller and need no additional logic. If no slave PID controller is specified, the ratio controller directly drives the control valve and sends the slave setpoint to it.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.PV, RATIO_CONTROL.PrimaryPV
ANALOG_IN2.PV, RATIO_CONTROL.SecondaryPV
<specified ratio>, RATIO_CONTROL.RatioSP
RATIO_CONTROL.SlaveSP, PID_BASIC.SP
PID_BASIC.XOUT, VALVE_ELECTRIC.Control_Signal

*** Available Function Block Types ***
DUTY_STANDBY
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of function block's purpose.
Input,Enable,BOOL,Enable the function (TRUE=active).
Input,StartRequest,BOOL,Plant demand to have exactly one pump running.
Input,AlternateEnable,BOOL,Enable automatic alternation on each duty-cycle completion.
Input,ForcePumpA,BOOL,Force select Pump A as active (overrides alternation when TRUE).
Input,ForcePumpB,BOOL,Force select Pump B as active (overrides alternation when TRUE).
Input,DutyElapsed,BOOL,Timer output indicating the current duty period is over and a switchover is permitted.
Input,MinRunElapsed,BOOL,Timer output indicating the minimum run time has elapsed (prevents short cycling).
Input,SwitchoverDelayElapsed,BOOL,Timer output indicating the inter-pump pause is complete (safe to start standby).
Input,StartTimeoutElapsed,BOOL,Timer output indicating start confirmation timeout has expired for the running/starting pump.
Input,PumpA_RunFB,BOOL,Feedback that Pump A is proven running.
Input,PumpB_RunFB,BOOL,Feedback that Pump B is proven running.
Input,PumpA_Fault,BOOL,Fault input for Pump A (TRUE=faulted or not available).
Input,PumpB_Fault,BOOL,Fault input for Pump B (TRUE=faulted or not available).
Input,Reset,BOOL,Reset latched alarms/lockouts.
Input,Inhibit,BOOL,Inhibits starting the duty standby functionality and can receive alarm signals.
Output,CmdPumpA,BOOL,Command to run Pump A (exclusive with CmdPumpB).
Output,CmdPumpB,BOOL,Command to run Pump B (exclusive with CmdPumpA).
Output,ActiveIsA,BOOL,Status bit indicating Pump A is the selected active unit.
Output,SwitchedDueToDuty,BOOL,Pulse TRUE for one cycle when a switchover occurred due to DutyElapsed.
Output,SwitchedDueToFailure,BOOL,Pulse TRUE for one cycle when a switchover occurred due to a fault or failed start.
Output,Alarm_FailedStart_A,BOOL,Latched alarm when Pump A command did not achieve RunFB before StartTimeoutElapsed.
Output,Alarm_FailedStart_B,BOOL,Latched alarm when Pump B command did not achieve RunFB before StartTimeoutElapsed.
Output,Alarm_NoAvailablePump,BOOL,Latched alarm when neither pump is available to fulfill StartRequest.

PID_BASIC
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the PID block for HMI, alarms, or diagnostics.
Input,Description,STRING,Longer text explaining the loop's purpose and location. 
Input,AUTO,BOOL,Enables automatic mode when TRUE; output fixed at X0 when FALSE (manual).
Input,PV,REAL,Process Variable: actual measured value from the field instrument.
Input,SP,REAL,Setpoint: desired target value to maintain.
Input,MV_MIN,REAL,Manipulated value minimum: for clamping the output signal.
Input,MV_MAX,REAL,Manipulated value maximum: for clamping the output signal.
Input,X0,REAL,Manual output value used when AUTO = FALSE; typically 0–100%.
Input,KP,REAL,Proportional gain: higher gain means faster response but risk of overshoot.
Input,TR,REAL,Integral time (reset time): time needed for the integral term to repeat the proportional action.
Input,TD,REAL,Derivative time: dampens rate of change; often 0 for slow loops.
Input,PV_High,REAL,High PV limit for alarm triggering.
Input,PV_Low,REAL,Low PV limit for alarm triggering.
Input,Deviation_Limit,REAL,Allowed deviation between PV and SP before deviation alarm triggers.
Input,Inhibit,BOOL,Inhibits PID functionality can receive alarm signals.
Output,PV_High_Alarm,BOOL,TRUE when PV exceeds PV_High limit.
Output,PV_Low_Alarm,BOOL,TRUE when PV is below PV_Low limit.
Output,Deviation_Alarm,BOOL,TRUE when absolute deviation exceeds Deviation_Limit.
Output,XOUT,REAL,Controller output: final manipulated variable to actuator (valve, motor, or VFD). 

RATIO_CONTROL
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer text explaining the loop's purpose and location.
Input,Auto,BOOL,TRUE=automatic ratio control; FALSE=manual output.
Input,PrimaryPV,REAL,Measured master process value (e.g., water flow).
Input,SecondaryPV,REAL,Measured slave process value (e.g., chemical flow).
Input,RatioSP,REAL,Desired Secondary/Primary ratio.
Input,Bias,REAL,Additive bias applied to the computed setpoint (engineering units).
Input,TrimKp,REAL,Proportional trim gain applied to ratio error (ActiveRatio−RatioSP).
Input,TrimTi,TIME,Integral time for trim action; T#0s disables integration.
Input,MV_MIN,REAL,Manipulated value minimum: for clamping the slave setpoint output signal.
Input,MV_MAX,REAL,Manipulated value maximum: for clamping the slave setpoint output signal.
Input,ManOut,REAL,Operator-provided output when Auto=FALSE.
Input,Inhibit,BOOL,Inhibits ratio control functionality can receive alarm signals.
Output,SlaveSP,REAL,Setpoint to the slave controlle
Output,ActiveRatio,REAL,Computed actual ratio = SecondaryPV/PrimaryPV (valid when PrimaryPV>0).
Output,RatioErr,REAL,Ratio error = ActiveRatio−RatioSP.

SPLIT_RANGE
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the Split Range block for HMI.
Input,Description,STRING,Longer description of the split range purpose.
Input,IN,REAL,Single analog input from the upstream controller (0-100 percent).
Input,Split_Point,REAL,The controller input value where the control action shifts between outputs (e.g., 50 percent).
Input,Output1_Start,REAL,The controller input value where Output 1 begins to change.
Input,Output1_End,REAL,The controller input value where Output 1 reaches its end state.
Input,Output2_Start,REAL,The controller input value where Output 2 begins to change.
Input,Output2_End,REAL,The controller input value where Output 2 reaches its end state.
Input,Inhibit,BOOL,Inhibits split range functionality can receive alarm signals.
Output,OUT1,REAL,Analog output signal for the first final control element (0-100 percent).
Output,OUT2,REAL,Analog output signal for the second final control element (0-100 percent).

VOTING_ANALOG
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of the block's purpose
Input,Input1,REAL,First analog input.
Input,Input2,REAL,Second analog input.
Input,Input3,REAL,Third analog input (for 2oo3).
Input,Deviation_Limit,REAL,Maximum allowed deviation between inputs for agreement.
Input,Voting_Scheme,ENUM,Selection of voting scheme (e.g. 2oo3 or Median or Average).
Input,EnableAlarm,BOOL,Enables or disables alarm monitoring.
Input,Inhibit,BOOL,Inhibits voting functionality and can receive alarm signals.
Output,Voted_Output,REAL,The validated analog output value.
Output,Sensor1_Fault,BOOL,Indicates if Input1 is deemed faulty.
Output,Sensor2_Fault,BOOL,Indicates if Input2 is deemed faulty.
Output,Sensor3_Fault,BOOL,Indicates if Input3 is deemed faulty.
Output,Alarm_Voting_Error,BOOL,Indicates a disagreement among inputs or insufficient healthy sensors.
Output,Healthy_Sensors_Count,INT,Number of currently healthy sensors.

*** Control Narrative *** 
{{control-narrative}}
```

---

## Process Flow Summary

The context generation process follows this systematic approach:

1. **Sensor Analysis** - Identifies required sensor function blocks (ANALOG_IN, DIGITAL_IN, BOOL_IN) based on measurement and monitoring requirements
2. **Actuator Analysis** - Identifies required actuator function blocks (motors, valves) with intelligent defaults for ambiguous cases
3. **Control Strategy Selection** - Evaluates and selects the most appropriate control strategy from a comprehensive library, providing complete function block specifications

## Available Control Strategies

The system includes support for the following control strategies:

- **PID Control** - Basic feedback control with single PID controller
- **Cascade Control** - Two-level control with primary and secondary controllers
- **Duty-Standby** - Redundant equipment with automatic switchover
- **Voting** - Multiple sensor voting for fault tolerance
- **Feedforward** - Disturbance compensation control
- **Override** - Protective control with limit monitoring
- **Split Range** - Single controller driving multiple actuators
- **Ratio Control** - Maintains proportional relationship between flows

## Function Block Categories

### Sensor Function Blocks
- **ANALOG_IN** - Analog measurements with scaling and alarming
- **DIGITAL_IN** - Digital inputs with debouncing and fault detection
- **BOOL_IN** - Boolean monitoring with latching capabilities

### Actuator Function Blocks
- **MOTOR_ON_OFF** - Simple on/off motor control
- **MOTOR_2SPD** - Two-speed motor control
- **MOTOR_VSD** - Variable speed drive control
- **VALVE_ELECTRIC** - Analog valve positioning
- **VALVE_ON_OFF** - Digital valve control

### Control Function Blocks
- **PID_BASIC** - PID controller with comprehensive alarming
- **RATIO_CONTROL** - Ratio controller for flow applications
- **SPLIT_RANGE** - Signal splitting for multiple actuators
- **VOTING_ANALOG** - Sensor voting and fault detection
- **DUTY_STANDBY** - Equipment redundancy management

This context generation system provides the foundational analysis needed to create comprehensive control system specifications by systematically identifying all required components and their appropriate control strategies.