# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 02:23:58

## Step 1: contextgen1-sensors
**Time:** 02:23:58

### Output:
```
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
```

---

## Step 2: contextgen1-actuators
**Time:** 02:24:38

### Output:
```
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
```

---

## Step 3: contextgen1-strategies
**Time:** 02:24:57

### Output:
```
*** Available Control Strategies ***
|Control Strategy|Probability|
|PID Control|0.98|
|OVERRIDE|0.65|
|Cascade Control|0.10|
|FEEDFORWARD|0.05|
|SPLIT RANGE|0.05|
|Ratio Control|0.02|
|VOTING|0.02|
|Duty-Standby|0.01|

Selected Control Strategy: PID Control
Short explanation: The narrative specifies a single PID loop (PIC-104) regulating pressure (PIT-103) by manipulating FV-106.

* Control Strategy * 
PID Control
** Description **
The system consists of an analog input, a PID controller, and an actuator. The analog input provides a process variable to the PID controller, which compares it to a predefined setpoint. Based on the difference (error), the PID controller calculates a control signal and sends it to the actuator to regulate the process.
** Intended Block-to-Block Connections Types **
ANALOG_IN.PV, PID_BASIC.PV 
PID_BASIC.XOUT, VALVE_ELECTRIC.Control_Signal

*** Available Function Block Types ***
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
```

---


# Prompt Chain: openplc-function-block-chain-v3.txt
**Timestamp:** 2025-09-24 02:25:31

## Step 1: openplc-function-blocks-v2
**Time:** 02:25:31

### Output:
```
* Function Blocks *
ANALOG_IN PIT-103
ANALOG_IN PT-101
ANALOG_IN DT-301
PID_BASIC PIC-104
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-107
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 02:25:48

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN PIT-103
ANALOG_IN PT-101
ANALOG_IN DT-301
PID_BASIC PIC-104
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-107
DIGITAL_IN XV-102-OPEN-LS
DIGITAL_IN XV-107-OPEN-LS
BOOL_IN ILK-FEED-PRESSURE-OK
BOOL_IN ILK-OVERPRESSURE-TRIP
BOOL_IN ILK-DENSITY-OK
BOOL_IN ILK-XV102-OPEN
BOOL_IN ILK-XV107-OPEN
BOOL_IN ILK-SYSTEM-FAULT
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 02:26:17

### Output:
```
* Functions *
NOT Deadband_Inverter_NOT

* Block-to-Block Connections *
PIT-103.PV, PIC-104.PV
PIC-104.XOUT, FV-106.Control_Signal
FV-106.Feedback_Pos, PIC-104.X0
PIC-104.Deviation_Alarm, Deadband_Inverter_NOT.IN
Deadband_Inverter_NOT.OUT, PIC-104.Inhibit
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 02:27:21

### Output:
```
* Functions * 
OR PIC104_Inhibit_OR
OR FV106_Inhibit_OR
OR SystemFault_OR
NOT XV102_OpenPermissive_NOT
NOT XV107_OpenPermissive_NOT

* Data Connections *
Deadband_Inverter_NOT.OUT, PIC104_Inhibit_OR.IN1
PT-101.Low_Alarm, ILK-FEED-PRESSURE-OK.Bool_In
ILK-FEED-PRESSURE-OK.Bool_Out, PIC104_Inhibit_OR.IN2
DT-301.High_Alarm, ILK-DENSITY-OK.Bool_In
ILK-DENSITY-OK.Bool_Out, PIC104_Inhibit_OR.IN3
XV-107-OPEN-LS.DI_Out, ILK-XV107-OPEN.Bool_In
ILK-XV107-OPEN.Bool_Out, XV107_OpenPermissive_NOT.IN
XV107_OpenPermissive_NOT.OUT, PIC104_Inhibit_OR.IN4
PIT-103.General_Fault, PIC104_Inhibit_OR.IN5
PIC104_Inhibit_OR.OUT, PIC-104.Inhibit
PT-101.High_Alarm, ILK-OVERPRESSURE-TRIP.Bool_In
ILK-OVERPRESSURE-TRIP.Bool_Out, FV106_Inhibit_OR.IN1
XV-102-OPEN-LS.DI_Out, ILK-XV102-OPEN.Bool_In
ILK-XV102-OPEN.Bool_Out, XV102_OpenPermissive_NOT.IN
XV102_OpenPermissive_NOT.OUT, FV106_Inhibit_OR.IN2
PIT-103.General_Fault, FV106_Inhibit_OR.IN3
FV106_Inhibit_OR.OUT, FV-106.Inhibit
PT-101.General_Fault, SystemFault_OR.IN1
DT-301.General_Fault, SystemFault_OR.IN2
SystemFault_OR.OUT, ILK-SYSTEM-FAULT.Bool_In
ILK-SYSTEM-FAULT.Bool_Out, XV-102.Inhibit
ILK-SYSTEM-FAULT.Bool_Out, XV-107.Inhibit

* Parameter Data Connections *
275, PIC-104.PV_High
200, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
150, PT-101.PV_Low
400, PT-101.PV_High
TRUE, PT-101.Alarm_Enable
3.5, DT-301.PV_High
0, DT-301.PV_Low
TRUE, DT-301.Alarm_Enable
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 02:29:14

### Output:
```
* Parameter Data Connections *
250.0, PIC-104.SP
3.0, PIC-104.KP
1.2, PIC-104.TR
0.1, PIC-104.TD
0.0, PIC-104.MV_MIN
100.0, PIC-104.MV_MAX
275.0, PIC-104.PV_High
200.0, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
31.25, PIT-103.Scaling_Slope
-125.0, PIT-103.Scaling_Offset
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
T#2s, FV-106.Timeout
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 02:30:53

### Output:
```
* Parameter Data Connections *
250.0, PIC-104.SP
3.0, PIC-104.KP
1.2, PIC-104.TR
0.1, PIC-104.TD
0.0, PIC-104.MV_MIN
100.0, PIC-104.MV_MAX
275.0, PIC-104.PV_High
200.0, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
31.25, PIT-103.Scaling_Slope
-125.0, PIT-103.Scaling_Offset
0.0, PIT-103.PV_Low
500.0, PIT-103.PV_High
TRUE, PIT-103.Alarm_Enable
150.0, PT-101.PV_Low
400.0, PT-101.PV_High
TRUE, PT-101.Alarm_Enable
0.0, DT-301.PV_Low
3.5, DT-301.PV_High
TRUE, DT-301.Alarm_Enable
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
T#2s, FV-106.Timeout
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 02:33:20

### Output:
```
* Variables *
REAL PIT103_Pressure_PV
REAL PT101_UpstreamPressure_PV
REAL DT301_Density_PV
REAL PIC104_MV_to_FV106
REAL FV106_Position_Feedback

* Data Connections *
PIT-103.PV, PIT103_Pressure_PV
PT-101.PV, PT101_UpstreamPressure_PV
DT-301.PV, DT301_Density_PV
PIC-104.XOUT, PIC104_MV_to_FV106
FV-106.Feedback_Pos, FV106_Position_Feedback
```

---

## Step 8: openplc-rule-checks
**Time:** 02:34:07

### Output:
```
* Function Blocks *
ANALOG_IN PIT-103
ANALOG_IN PT-101
ANALOG_IN DT-301
PID_BASIC PIC-104
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-107
DIGITAL_IN XV-102-OPEN-LS
DIGITAL_IN XV-107-OPEN-LS
BOOL_IN ILK-FEED-PRESSURE-OK
BOOL_IN ILK-OVERPRESSURE-TRIP
BOOL_IN ILK-DENSITY-OK
BOOL_IN ILK-XV102-OPEN
BOOL_IN ILK-XV107-OPEN
BOOL_IN ILK-SYSTEM-FAULT

* Variables *
REAL PIT103_Pressure_PV
REAL PT101_UpstreamPressure_PV
REAL DT301_Density_PV
REAL PIC104_MV_to_FV106
REAL FV106_Position_Feedback

* Functions *
NOT Deadband_Inverter_NOT
OR PIC104_Inhibit_OR
OR FV106_Inhibit_OR
OR SystemFault_OR
NOT XV102_OpenPermissive_NOT
NOT XV107_OpenPermissive_NOT

* Data Connections *
PIT-103.PV, PIC-104.PV
PIC-104.XOUT, FV-106.Control_Signal
FV-106.Feedback_Pos, PIC-104.X0
PIC-104.Deviation_Alarm, Deadband_Inverter_NOT.IN
Deadband_Inverter_NOT.OUT, PIC104_Inhibit_OR.IN1
PT-101.Low_Alarm, ILK-FEED-PRESSURE-OK.Bool_In
ILK-FEED-PRESSURE-OK.Bool_Out, PIC104_Inhibit_OR.IN2
DT-301.High_Alarm, ILK-DENSITY-OK.Bool_In
ILK-DENSITY-OK.Bool_Out, PIC104_Inhibit_OR.IN3
XV-107-OPEN-LS.DI_Out, ILK-XV107-OPEN.Bool_In
ILK-XV107-OPEN.Bool_Out, XV107_OpenPermissive_NOT.IN
XV107_OpenPermissive_NOT.OUT, PIC104_Inhibit_OR.IN4
PIT-103.General_Fault, PIC104_Inhibit_OR.IN5
PIC104_Inhibit_OR.OUT, PIC-104.Inhibit
PT-101.High_Alarm, ILK-OVERPRESSURE-TRIP.Bool_In
ILK-OVERPRESSURE-TRIP.Bool_Out, FV106_Inhibit_OR.IN1
XV-102-OPEN-LS.DI_Out, ILK-XV102-OPEN.Bool_In
ILK-XV102-OPEN.Bool_Out, XV102_OpenPermissive_NOT.IN
XV102_OpenPermissive_NOT.OUT, FV106_Inhibit_OR.IN2
PIT-103.General_Fault, FV106_Inhibit_OR.IN3
FV106_Inhibit_OR.OUT, FV-106.Inhibit
PT-101.General_Fault, SystemFault_OR.IN1
DT-301.General_Fault, SystemFault_OR.IN2
SystemFault_OR.OUT, ILK-SYSTEM-FAULT.Bool_In
ILK-SYSTEM-FAULT.Bool_Out, XV-102.Inhibit
ILK-SYSTEM-FAULT.Bool_Out, XV-107.Inhibit
PIT-103.PV, PIT103_Pressure_PV
PT-101.PV, PT101_UpstreamPressure_PV
DT-301.PV, DT301_Density_PV
PIC-104.XOUT, PIC104_MV_to_FV106
FV-106.Feedback_Pos, FV106_Position_Feedback

* Parameter Data Connections *
250.0, PIC-104.SP
3.0, PIC-104.KP
1.2, PIC-104.TR
0.1, PIC-104.TD
0.0, PIC-104.MV_MIN
100.0, PIC-104.MV_MAX
275.0, PIC-104.PV_High
200.0, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
31.25, PIT-103.Scaling_Slope
-125.0, PIT-103.Scaling_Offset
0.0, PIT-103.PV_Low
500.0, PIT-103.PV_High
TRUE, PIT-103.Alarm_Enable
150.0, PT-101.PV_Low
400.0, PT-101.PV_High
TRUE, PT-101.Alarm_Enable
0.0, DT-301.PV_Low
3.5, DT-301.PV_High
TRUE, DT-301.Alarm_Enable
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
T#2s, FV-106.Timeout
```

---

## Step 9: openplc-rule-checks2
**Time:** 02:36:04

### Output:
```
* Function Blocks *
ANALOG_IN PIT-103
ANALOG_IN PT-101
ANALOG_IN DT-301
PID_BASIC PIC-104
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-107
DIGITAL_IN XV-102-OPEN-LS
DIGITAL_IN XV-107-OPEN-LS
BOOL_IN ILK-FEED-PRESSURE-OK
BOOL_IN ILK-OVERPRESSURE-TRIP
BOOL_IN ILK-DENSITY-OK
BOOL_IN ILK-XV102-OPEN
BOOL_IN ILK-XV107-OPEN
BOOL_IN ILK-SYSTEM-FAULT

* Variables *
REAL PIT103_Pressure_PV
REAL PT101_UpstreamPressure_PV
REAL DT301_Density_PV
REAL PIC104_MV_to_FV106
REAL FV106_Position_Feedback

* Functions *
NOT Deadband_Inverter_NOT
OR PIC104_Inhibit_OR
OR FV106_Inhibit_OR
OR SystemFault_OR
NOT XV102_OpenPermissive_NOT
NOT XV107_OpenPermissive_NOT

* Data Connections *
PIT-103.PV, PIC-104.PV
PIC-104.XOUT, FV-106.Control_Signal
FV-106.Feedback_Pos, PIC-104.X0
PIC-104.Deviation_Alarm, Deadband_Inverter_NOT.IN
Deadband_Inverter_NOT.OUT, PIC104_Inhibit_OR.IN1
PT-101.Low_Alarm, ILK-FEED-PRESSURE-OK.Bool_In
ILK-FEED-PRESSURE-OK.Bool_Out, PIC104_Inhibit_OR.IN2
DT-301.High_Alarm, ILK-DENSITY-OK.Bool_In
ILK-DENSITY-OK.Bool_Out, PIC104_Inhibit_OR.IN3
XV-107-OPEN-LS.DI_Out, ILK-XV107-OPEN.Bool_In
ILK-XV107-OPEN.Bool_Out, XV107_OpenPermissive_NOT.IN
XV107_OpenPermissive_NOT.OUT, PIC104_Inhibit_OR.IN4
PIT-103.General_Fault, PIC104_Inhibit_OR.IN5
PIC104_Inhibit_OR.OUT, PIC-104.Inhibit
PT-101.High_Alarm, ILK-OVERPRESSURE-TRIP.Bool_In
ILK-OVERPRESSURE-TRIP.Bool_Out, FV106_Inhibit_OR.IN1
XV-102-OPEN-LS.DI_Out, ILK-XV102-OPEN.Bool_In
ILK-XV102-OPEN.Bool_Out, XV102_OpenPermissive_NOT.IN
XV102_OpenPermissive_NOT.OUT, FV106_Inhibit_OR.IN2
PIT-103.General_Fault, FV106_Inhibit_OR.IN3
FV106_Inhibit_OR.OUT, FV-106.Inhibit
PT-101.General_Fault, SystemFault_OR.IN1
DT-301.General_Fault, SystemFault_OR.IN2
SystemFault_OR.OUT, ILK-SYSTEM-FAULT.Bool_In
ILK-SYSTEM-FAULT.Bool_Out, XV-102.Inhibit
ILK-SYSTEM-FAULT.Bool_Out, XV-107.Inhibit
PIT-103.PV, PIT103_Pressure_PV
PT-101.PV, PT101_UpstreamPressure_PV
DT-301.PV, DT301_Density_PV
PIC-104.XOUT, PIC104_MV_to_FV106
FV-106.Feedback_Pos, FV106_Position_Feedback

* Parameter Data Connections *
250.0, PIC-104.SP
3.0, PIC-104.KP
1.2, PIC-104.TR
0.1, PIC-104.TD
0.0, PIC-104.MV_MIN
100.0, PIC-104.MV_MAX
275.0, PIC-104.PV_High
200.0, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
31.25, PIT-103.Scaling_Slope
-125.0, PIT-103.Scaling_Offset
0.0, PIT-103.PV_Low
500.0, PIT-103.PV_High
TRUE, PIT-103.Alarm_Enable
150.0, PT-101.PV_Low
400.0, PT-101.PV_High
TRUE, PT-101.Alarm_Enable
0.0, DT-301.PV_Low
3.5, DT-301.PV_High
TRUE, DT-301.Alarm_Enable
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
T#2s, FV-106.Timeout
```

---

## Step 10: append_two_inputs
**Time:** 02:36:44

### Output:
```
* Function Blocks *
ANALOG_IN PIT-103
ANALOG_IN PT-101
ANALOG_IN DT-301
PID_BASIC PIC-104
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-107
DIGITAL_IN XV-102-OPEN-LS
DIGITAL_IN XV-107-OPEN-LS
BOOL_IN ILK-FEED-PRESSURE-OK
BOOL_IN ILK-OVERPRESSURE-TRIP
BOOL_IN ILK-DENSITY-OK
BOOL_IN ILK-XV102-OPEN
BOOL_IN ILK-XV107-OPEN
BOOL_IN ILK-SYSTEM-FAULT

* Variables *
REAL PIT103_Pressure_PV
REAL PT101_UpstreamPressure_PV
REAL DT301_Density_PV
REAL PIC104_MV_to_FV106
REAL FV106_Position_Feedback

* Functions *
NOT Deadband_Inverter_NOT
OR PIC104_Inhibit_OR
OR FV106_Inhibit_OR
OR SystemFault_OR
NOT XV102_OpenPermissive_NOT
NOT XV107_OpenPermissive_NOT

* Data Connections *
PIT-103.PV, PIC-104.PV
PIC-104.XOUT, FV-106.Control_Signal
FV-106.Feedback_Pos, PIC-104.X0
PIC-104.Deviation_Alarm, Deadband_Inverter_NOT.IN
Deadband_Inverter_NOT.OUT, PIC104_Inhibit_OR.IN1
PT-101.Low_Alarm, ILK-FEED-PRESSURE-OK.Bool_In
ILK-FEED-PRESSURE-OK.Bool_Out, PIC104_Inhibit_OR.IN2
DT-301.High_Alarm, ILK-DENSITY-OK.Bool_In
ILK-DENSITY-OK.Bool_Out, PIC104_Inhibit_OR.IN3
XV-107-OPEN-LS.DI_Out, ILK-XV107-OPEN.Bool_In
ILK-XV107-OPEN.Bool_Out, XV107_OpenPermissive_NOT.IN
XV107_OpenPermissive_NOT.OUT, PIC104_Inhibit_OR.IN4
PIT-103.General_Fault, PIC104_Inhibit_OR.IN5
PIC104_Inhibit_OR.OUT, PIC-104.Inhibit
PT-101.High_Alarm, ILK-OVERPRESSURE-TRIP.Bool_In
ILK-OVERPRESSURE-TRIP.Bool_Out, FV106_Inhibit_OR.IN1
XV-102-OPEN-LS.DI_Out, ILK-XV102-OPEN.Bool_In
ILK-XV102-OPEN.Bool_Out, XV102_OpenPermissive_NOT.IN
XV102_OpenPermissive_NOT.OUT, FV106_Inhibit_OR.IN2
PIT-103.General_Fault, FV106_Inhibit_OR.IN3
FV106_Inhibit_OR.OUT, FV-106.Inhibit
PT-101.General_Fault, SystemFault_OR.IN1
DT-301.General_Fault, SystemFault_OR.IN2
SystemFault_OR.OUT, ILK-SYSTEM-FAULT.Bool_In
ILK-SYSTEM-FAULT.Bool_Out, XV-102.Inhibit
ILK-SYSTEM-FAULT.Bool_Out, XV-107.Inhibit
PIT-103.PV, PIT103_Pressure_PV
PT-101.PV, PT101_UpstreamPressure_PV
DT-301.PV, DT301_Density_PV
PIC-104.XOUT, PIC104_MV_to_FV106
FV-106.Feedback_Pos, FV106_Position_Feedback

* Parameter Data Connections *
250.0, PIC-104.SP
3.0, PIC-104.KP
1.2, PIC-104.TR
0.1, PIC-104.TD
0.0, PIC-104.MV_MIN
100.0, PIC-104.MV_MAX
275.0, PIC-104.PV_High
200.0, PIC-104.PV_Low
12.5, PIC-104.Deviation_Limit
31.25, PIT-103.Scaling_Slope
-125.0, PIT-103.Scaling_Offset
0.0, PIT-103.PV_Low
500.0, PIT-103.PV_High
TRUE, PIT-103.Alarm_Enable
150.0, PT-101.PV_Low
400.0, PT-101.PV_High
TRUE, PT-101.Alarm_Enable
0.0, DT-301.PV_Low
3.5, DT-301.PV_High
TRUE, DT-301.Alarm_Enable
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
T#2s, FV-106.Timeout
```

---


