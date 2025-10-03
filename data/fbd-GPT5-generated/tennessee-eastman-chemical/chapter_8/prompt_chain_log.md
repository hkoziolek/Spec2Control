# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 06:28:38

## Step 1: contextgen1-sensors
**Time:** 06:28:38

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
```

---

## Step 2: contextgen1-actuators
**Time:** 06:28:57

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
```

---

## Step 3: contextgen1-strategies
**Time:** 06:29:09

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| PID Control | 0.99 |
| OVERRIDE | 0.90 |

Selected Control Strategy: PID Control
Short explanation: Core regulation of Decanter 2 level (LIC-106) and downstream flow (FC-8) are implemented as standard PID loops with fixed setpoints and defined tuning.

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
**Timestamp:** 2025-09-24 06:29:49

## Step 1: openplc-function-blocks-v2
**Time:** 06:29:49

### Output:
```
* Function Blocks *
ANALOG_IN LT-102
ANALOG_IN LT-103
ANALOG_IN LT-107
ANALOG_IN FIT-105
PID_BASIC LIC-106
PID_BASIC FC-008
VALVE_ELECTRIC XV-101
VALVE_ELECTRIC PV-104
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 06:30:08

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN LT-102
ANALOG_IN LT-103
ANALOG_IN LT-107
ANALOG_IN FIT-105
PID_BASIC LIC-106
PID_BASIC FC-008
VALVE_ELECTRIC XV-101
VALVE_ELECTRIC PV-104
BOOL_IN LIC-106_OVERFLOW_IL
BOOL_IN FC-008_LOWLEVEL_IL
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 06:30:47

### Output:
```
* Functions *

* Block-to-Block Connections *
LT-102.PV, LIC-106.PV
LIC-106.XOUT, XV-101.Control_Signal
FIT-105.PV, FC-008.PV
FC-008.XOUT, PV-104.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 06:31:02

### Output:
```
* Functions * 
OR LIC106_Overflow_OR
OR LIC106_Fault_OR
OR LIC106_Close_OR

* Data Connections *
LT-103.High_Alarm, LIC106_Overflow_OR.IN1
LIC-106.PV_High_Alarm, LIC106_Overflow_OR.IN2
LIC106_Overflow_OR.OUT, LIC-106_OVERFLOW_IL.Bool_In
LT-102.General_Fault, LIC106_Fault_OR.IN1
XV-101.Position_Error, LIC106_Fault_OR.IN2
LIC-106_OVERFLOW_IL.Bool_Out, LIC106_Close_OR.IN1
LIC106_Fault_OR.OUT, LIC106_Close_OR.IN2
LIC106_Close_OR.OUT, LIC-106.Inhibit
LIC106_Close_OR.OUT, XV-101.Inhibit
LIC-106_OVERFLOW_IL.Bool_Out, LIC-106.Inhibit
LIC-106_OVERFLOW_IL.Bool_Out, XV-101.Inhibit
LT-107.Low_Alarm, FC-008_LOWLEVEL_IL.Bool_In
FC-008_LOWLEVEL_IL.Bool_Out, FC-008.Inhibit
FC-008_LOWLEVEL_IL.Bool_Out, PV-104.Inhibit
FIT-105.General_Fault, FC-008.Inhibit

* Parameter Data Connections *
90, LIC-106.PV_High
85, LT-103.PV_High
15, LT-107.PV_Low
12, FC-008.Deviation_Limit
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 06:32:51

### Output:
```
* Parameter Data Connections *
6.25, LT-102.Scaling_Slope
-25.0, LT-102.Scaling_Offset
TRUE, LT-102.Alarm_Enable
0.0, LT-102.PV_Low
100.0, LT-102.PV_High
9.375, FIT-105.Scaling_Slope
-37.5, FIT-105.Scaling_Offset
TRUE, FIT-105.Alarm_Enable
0.0, FIT-105.PV_Low
150.0, FIT-105.PV_High
65.0, LIC-106.SP
3.0, LIC-106.KP
1.2, LIC-106.TR
0.0, LIC-106.TD
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
100.0, XV-101.Open_Limit
0.0, XV-101.Close_Limit
T#10s, XV-101.Timeout
120.0, FC-008.SP
2.5, FC-008.KP
0.8, FC-008.TR
0.2, FC-008.TD
0.0, FC-008.MV_MIN
100.0, FC-008.MV_MAX
12.0, FC-008.Deviation_Limit
85.0, LT-103.PV_High
TRUE, LT-103.Alarm_Enable
15.0, LT-107.PV_Low
TRUE, LT-107.Alarm_Enable
100.0, PV-104.Open_Limit
0.0, PV-104.Close_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 06:33:52

### Output:
```
* Parameter Data Connections *
6.25, LT-102.Scaling_Slope
-25.0, LT-102.Scaling_Offset
TRUE, LT-102.Alarm_Enable
0.0, LT-102.PV_Low
100.0, LT-102.PV_High
9.375, FIT-105.Scaling_Slope
-37.5, FIT-105.Scaling_Offset
TRUE, FIT-105.Alarm_Enable
0.0, FIT-105.PV_Low
150.0, FIT-105.PV_High
65.0, LIC-106.SP
3.0, LIC-106.KP
1.2, LIC-106.TR
0.0, LIC-106.TD
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
0.0, LIC-106.PV_Low
90.0, LIC-106.PV_High
100.0, XV-101.Open_Limit
0.0, XV-101.Close_Limit
T#10s, XV-101.Timeout
120.0, FC-008.SP
2.5, FC-008.KP
0.8, FC-008.TR
0.2, FC-008.TD
0.0, FC-008.MV_MIN
100.0, FC-008.MV_MAX
0.0, FC-008.PV_Low
150.0, FC-008.PV_High
12.0, FC-008.Deviation_Limit
85.0, LT-103.PV_High
0.0, LT-103.PV_Low
TRUE, LT-103.Alarm_Enable
15.0, LT-107.PV_Low
100.0, LT-107.PV_High
TRUE, LT-107.Alarm_Enable
100.0, PV-104.Open_Limit
0.0, PV-104.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 06:34:34

### Output:
```
* Variables *
REAL LIC106_MV_XV101_Command
REAL FC008_MV_PV104_Command

* Data Connections *
LIC-106.XOUT, LIC106_MV_XV101_Command
FC-008.XOUT, FC008_MV_PV104_Command
```

---

## Step 8: openplc-rule-checks
**Time:** 06:34:59

### Output:
```
* Function Blocks *
ANALOG_IN LT-102
ANALOG_IN LT-103
ANALOG_IN LT-107
ANALOG_IN FIT-105
PID_BASIC LIC-106
PID_BASIC FC-008
VALVE_ELECTRIC XV-101
VALVE_ELECTRIC PV-104

* Variables *
BOOL System_RunCmd
BOOL Decanter2_Online
REAL LIC106_MV_XV101_Command
REAL FC008_MV_PV104_Command

* Functions *
GT LIC106_Overflow_GT
OR LIC106_Fault_OR
OR LIC106_Disable_OR
NOT LT102_Fault_NOT
NOT LIC106_Disable_NOT
AND LIC106_Permissives_AND
AND LIC106_AUTO_AND
LT FC8_LowLevel_LT
OR FC8_ValveFault_OR
OR FC8_Fault_OR
NOT FIT105_Fault_NOT
AND FC8_Permissives_AND1
AND FC8_Permissives_AND2
NOT FC8_Fault_NOT
NOT FC8_LowLevel_NOT
AND FC8_NotInterlocks_AND
AND FC8_AUTO_AND
MULT FC8_FaultToX0_MULT
TON StartupDelay_TON

* Data Connections *
LT-102.PV, LIC-106.PV
FIT-105.PV, FC-008.PV
LIC-106.XOUT, XV-101.Control_Signal
FC-008.XOUT, PV-104.Control_Signal
LIC-106.XOUT, LIC106_MV_XV101_Command
FC-008.XOUT, FC008_MV_PV104_Command
System_RunCmd, StartupDelay_TON.IN
LT-102.General_Fault, LT102_Fault_NOT.IN
StartupDelay_TON.Q, LIC106_Permissives_AND.IN1
LT102_Fault_NOT.OUT, LIC106_Permissives_AND.IN2
LT-103.PV, LIC106_Overflow_GT.IN1
LT-102.General_Fault, LIC106_Fault_OR.IN1
XV-101.Position_Error, LIC106_Fault_OR.IN2
LIC106_Overflow_GT.OUT, LIC106_Disable_OR.IN1
LIC106_Fault_OR.OUT, LIC106_Disable_OR.IN2
LIC106_Disable_OR.OUT, LIC106_Disable_NOT.IN
LIC106_Permissives_AND.OUT, LIC106_AUTO_AND.IN1
LIC106_Disable_NOT.OUT, LIC106_AUTO_AND.IN2
LIC106_AUTO_AND.OUT, LIC-106.AUTO
FIT-105.General_Fault, FIT105_Fault_NOT.IN
StartupDelay_TON.Q, FC8_Permissives_AND1.IN1
Decanter2_Online, FC8_Permissives_AND1.IN2
FC8_Permissives_AND1.OUT, FC8_Permissives_AND2.IN1
FIT105_Fault_NOT.OUT, FC8_Permissives_AND2.IN2
PV-104.Position_Error, FC8_ValveFault_OR.IN1
PV-104.Alarm, FC8_ValveFault_OR.IN2
FIT-105.General_Fault, FC8_Fault_OR.IN1
FC8_ValveFault_OR.OUT, FC8_Fault_OR.IN2
FC8_Fault_OR.OUT, FC8_Fault_NOT.IN
LT-107.PV, FC8_LowLevel_LT.IN1
FC8_Fault_NOT.OUT, FC8_NotInterlocks_AND.IN1
FC8_LowLevel_LT.OUT, FC8_LowLevel_NOT.IN
FC8_LowLevel_NOT.OUT, FC8_NotInterlocks_AND.IN2
FC8_Permissives_AND2.OUT, FC8_AUTO_AND.IN1
FC8_NotInterlocks_AND.OUT, FC8_AUTO_AND.IN2
FC8_AUTO_AND.OUT, FC-008.AUTO
FC8_Fault_OR.OUT, FC8_FaultToX0_MULT.IN2
FC8_FaultToX0_MULT.OUT, FC-008.X0

* Parameter Data Connections *
6.25, LT-102.Scaling_Slope
-25.0, LT-102.Scaling_Offset
TRUE, LT-102.Alarm_Enable
0.0, LT-102.PV_Low
100.0, LT-102.PV_High
6.25, LT-103.Scaling_Slope
-25.0, LT-103.Scaling_Offset
TRUE, LT-103.Alarm_Enable
0.0, LT-103.PV_Low
85.0, LT-103.PV_High
6.25, LT-107.Scaling_Slope
-25.0, LT-107.Scaling_Offset
TRUE, LT-107.Alarm_Enable
15.0, LT-107.PV_Low
100.0, LT-107.PV_High
9.375, FIT-105.Scaling_Slope
-37.5, FIT-105.Scaling_Offset
TRUE, FIT-105.Alarm_Enable
0.0, FIT-105.PV_Low
150.0, FIT-105.PV_High
65.0, LIC-106.SP
3.0, LIC-106.KP
1.2, LIC-106.TR
0.0, LIC-106.TD
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
0.0, LIC-106.PV_Low
100.0, LIC-106.PV_High
0.0, LIC-106.X0
120.0, FC-008.SP
2.5, FC-008.KP
0.8, FC-008.TR
0.2, FC-008.TD
0.0, FC-008.MV_MIN
100.0, FC-008.MV_MAX
0.0, FC-008.PV_Low
150.0, FC-008.PV_High
12.0, FC-008.Deviation_Limit
100.0, XV-101.Open_Limit
0.0, XV-101.Close_Limit
T#10s, XV-101.Timeout
100.0, PV-104.Open_Limit
0.0, PV-104.Close_Limit
T#14s, StartupDelay_TON.PT
90.0, LIC106_Overflow_GT.IN2
20.0, FC8_LowLevel_LT.IN2
100.0, FC8_FaultToX0_MULT.IN1
```

---

## Step 9: openplc-rule-checks2
**Time:** 06:37:30

### Output:
```
* Function Blocks *
ANALOG_IN LT-102
ANALOG_IN LT-103
ANALOG_IN LT-107
ANALOG_IN FIT-105
PID_BASIC LIC-106
PID_BASIC FC-008
VALVE_ELECTRIC XV-101
VALVE_ELECTRIC PV-104

* Variables *
BOOL System_RunCmd
BOOL Decanter2_Online
REAL LIC106_MV_XV101_Command
REAL FC008_MV_PV104_Command

* Functions *
GT LIC106_Overflow_GT
OR LIC106_Fault_OR
OR LIC106_Disable_OR
NOT LT102_Fault_NOT
NOT LIC106_Disable_NOT
AND LIC106_Permissives_AND
AND LIC106_AUTO_AND
LT FC8_LowLevel_LT
OR FC8_ValveFault_OR
OR FC8_Fault_OR
NOT FIT105_Fault_NOT
AND FC8_Permissives_AND1
AND FC8_Permissives_AND2
NOT FC8_Fault_NOT
NOT FC8_LowLevel_NOT
AND FC8_NotInterlocks_AND
AND FC8_AUTO_AND
MULT FC8_FaultToX0_MULT
TON StartupDelay_TON

* Data Connections *
LT-102.PV, LIC-106.PV
FIT-105.PV, FC-008.PV
LIC-106.XOUT, XV-101.Control_Signal
FC-008.XOUT, PV-104.Control_Signal
LIC-106.XOUT, LIC106_MV_XV101_Command
FC-008.XOUT, FC008_MV_PV104_Command
System_RunCmd, StartupDelay_TON.IN
LT-102.General_Fault, LT102_Fault_NOT.IN
StartupDelay_TON.Q, LIC106_Permissives_AND.IN1
LT102_Fault_NOT.OUT, LIC106_Permissives_AND.IN2
LT-103.PV, LIC106_Overflow_GT.IN1
LT-102.General_Fault, LIC106_Fault_OR.IN1
XV-101.Position_Error, LIC106_Fault_OR.IN2
LIC106_Overflow_GT.OUT, LIC106_Disable_OR.IN1
LIC106_Fault_OR.OUT, LIC106_Disable_OR.IN2
LIC106_Disable_OR.OUT, LIC106_Disable_NOT.IN
LIC106_Permissives_AND.OUT, LIC106_AUTO_AND.IN1
LIC106_Disable_NOT.OUT, LIC106_AUTO_AND.IN2
LIC106_AUTO_AND.OUT, LIC-106.AUTO
FIT-105.General_Fault, FIT105_Fault_NOT.IN
StartupDelay_TON.Q, FC8_Permissives_AND1.IN1
Decanter2_Online, FC8_Permissives_AND1.IN2
FC8_Permissives_AND1.OUT, FC8_Permissives_AND2.IN1
FIT105_Fault_NOT.OUT, FC8_Permissives_AND2.IN2
PV-104.Position_Error, FC8_ValveFault_OR.IN1
PV-104.Alarm, FC8_ValveFault_OR.IN2
FIT-105.General_Fault, FC8_Fault_OR.IN1
FC8_ValveFault_OR.OUT, FC8_Fault_OR.IN2
FC8_Fault_OR.OUT, FC8_Fault_NOT.IN
LT-107.PV, FC8_LowLevel_LT.IN1
FC8_Fault_NOT.OUT, FC8_NotInterlocks_AND.IN1
FC8_LowLevel_LT.OUT, FC8_LowLevel_NOT.IN
FC8_LowLevel_NOT.OUT, FC8_NotInterlocks_AND.IN2
FC8_Permissives_AND2.OUT, FC8_AUTO_AND.IN1
FC8_NotInterlocks_AND.OUT, FC8_AUTO_AND.IN2
FC8_AUTO_AND.OUT, FC-008.AUTO
FC8_Fault_OR.OUT, FC8_FaultToX0_MULT.IN2
FC8_FaultToX0_MULT.OUT, FC-008.X0

* Parameter Data Connections *
6.25, LT-102.Scaling_Slope
-25.0, LT-102.Scaling_Offset
TRUE, LT-102.Alarm_Enable
0.0, LT-102.PV_Low
100.0, LT-102.PV_High
6.25, LT-103.Scaling_Slope
-25.0, LT-103.Scaling_Offset
TRUE, LT-103.Alarm_Enable
0.0, LT-103.PV_Low
85.0, LT-103.PV_High
6.25, LT-107.Scaling_Slope
-25.0, LT-107.Scaling_Offset
TRUE, LT-107.Alarm_Enable
15.0, LT-107.PV_Low
100.0, LT-107.PV_High
9.375, FIT-105.Scaling_Slope
-37.5, FIT-105.Scaling_Offset
TRUE, FIT-105.Alarm_Enable
0.0, FIT-105.PV_Low
150.0, FIT-105.PV_High
65.0, LIC-106.SP
3.0, LIC-106.KP
1.2, LIC-106.TR
0.0, LIC-106.TD
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
0.0, LIC-106.PV_Low
100.0, LIC-106.PV_High
0.0, LIC-106.X0
120.0, FC-008.SP
2.5, FC-008.KP
0.8, FC-008.TR
0.2, FC-008.TD
0.0, FC-008.MV_MIN
100.0, FC-008.MV_MAX
0.0, FC-008.PV_Low
150.0, FC-008.PV_High
12.0, FC-008.Deviation_Limit
100.0, XV-101.Open_Limit
0.0, XV-101.Close_Limit
T#10s, XV-101.Timeout
100.0, PV-104.Open_Limit
0.0, PV-104.Close_Limit
T#14s, StartupDelay_TON.PT
90.0, LIC106_Overflow_GT.IN2
20.0, FC8_LowLevel_LT.IN2
100.0, FC8_FaultToX0_MULT.IN1
```

---

## Step 10: append_two_inputs
**Time:** 06:37:56

### Output:
```
* Function Blocks *
ANALOG_IN LT-102
ANALOG_IN LT-103
ANALOG_IN LT-107
ANALOG_IN FIT-105
PID_BASIC LIC-106
PID_BASIC FC-008
VALVE_ELECTRIC XV-101
VALVE_ELECTRIC PV-104

* Variables *
BOOL System_RunCmd
BOOL Decanter2_Online
REAL LIC106_MV_XV101_Command
REAL FC008_MV_PV104_Command

* Functions *
GT LIC106_Overflow_GT
OR LIC106_Fault_OR
OR LIC106_Disable_OR
NOT LT102_Fault_NOT
NOT LIC106_Disable_NOT
AND LIC106_Permissives_AND
AND LIC106_AUTO_AND
LT FC8_LowLevel_LT
OR FC8_ValveFault_OR
OR FC8_Fault_OR
OR FC8_Interlocks_OR
NOT FIT105_Fault_NOT
AND FC8_Permissives_AND1
AND FC8_Permissives_AND2
NOT FC8_Fault_NOT
AND FC8_AUTO_AND
MULT FC8_FaultToX0_MULT
TON StartupDelay_TON

* Data Connections *
LT-102.PV, LIC-106.PV
FIT-105.PV, FC-008.PV
LIC-106.XOUT, XV-101.Control_Signal
FC-008.XOUT, PV-104.Control_Signal
LIC-106.XOUT, LIC106_MV_XV101_Command
FC-008.XOUT, FC008_MV_PV104_Command
System_RunCmd, StartupDelay_TON.IN
LT-102.General_Fault, LT102_Fault_NOT.IN
StartupDelay_TON.Q, LIC106_Permissives_AND.IN1
LT102_Fault_NOT.OUT, LIC106_Permissives_AND.IN2
LT-103.PV, LIC106_Overflow_GT.IN1
LT-102.General_Fault, LIC106_Fault_OR.IN1
XV-101.Position_Error, LIC106_Fault_OR.IN2
LIC106_Overflow_GT.OUT, LIC106_Disable_OR.IN1
LIC106_Fault_OR.OUT, LIC106_Disable_OR.IN2
LIC106_Disable_OR.OUT, LIC106_Disable_NOT.IN
LIC106_Permissives_AND.OUT, LIC106_AUTO_AND.IN1
LIC106_Disable_NOT.OUT, LIC106_AUTO_AND.IN2
LIC106_AUTO_AND.OUT, LIC-106.AUTO
FIT-105.General_Fault, FIT105_Fault_NOT.IN
StartupDelay_TON.Q, FC8_Permissives_AND1.IN1
Decanter2_Online, FC8_Permissives_AND1.IN2
FC8_Permissives_AND1.OUT, FC8_Permissives_AND2.IN1
FIT105_Fault_NOT.OUT, FC8_Permissives_AND2.IN2
PV-104.Position_Error, FC8_ValveFault_OR.IN1
PV-104.Alarm, FC8_ValveFault_OR.IN2
FIT-105.General_Fault, FC8_Fault_OR.IN1
FC8_ValveFault_OR.OUT, FC8_Fault_OR.IN2
FC8_Fault_OR.OUT, FC8_Interlocks_OR.IN1
LT-107.PV, FC8_LowLevel_LT.IN1
FC8_LowLevel_LT.OUT, FC8_Interlocks_OR.IN2
FC8_Interlocks_OR.OUT, FC8_Fault_NOT.IN
FC8_Permissives_AND2.OUT, FC8_AUTO_AND.IN1
FC8_Fault_NOT.OUT, FC8_AUTO_AND.IN2
FC8_AUTO_AND.OUT, FC-008.AUTO
FC8_Fault_OR.OUT, FC8_FaultToX0_MULT.IN2
FC8_FaultToX0_MULT.OUT, FC-008.X0

* Parameter Data Connections *
6.25, LT-102.Scaling_Slope
-25.0, LT-102.Scaling_Offset
TRUE, LT-102.Alarm_Enable
0.0, LT-102.PV_Low
100.0, LT-102.PV_High
6.25, LT-103.Scaling_Slope
-25.0, LT-103.Scaling_Offset
TRUE, LT-103.Alarm_Enable
0.0, LT-103.PV_Low
85.0, LT-103.PV_High
6.25, LT-107.Scaling_Slope
-25.0, LT-107.Scaling_Offset
TRUE, LT-107.Alarm_Enable
15.0, LT-107.PV_Low
100.0, LT-107.PV_High
9.375, FIT-105.Scaling_Slope
-37.5, FIT-105.Scaling_Offset
TRUE, FIT-105.Alarm_Enable
0.0, FIT-105.PV_Low
150.0, FIT-105.PV_High
65.0, LIC-106.SP
3.0, LIC-106.KP
1.2, LIC-106.TR
0.0, LIC-106.TD
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
0.0, LIC-106.PV_Low
100.0, LIC-106.PV_High
0.0, LIC-106.X0
120.0, FC-008.SP
2.5, FC-008.KP
0.8, FC-008.TR
0.2, FC-008.TD
0.0, FC-008.MV_MIN
100.0, FC-008.MV_MAX
0.0, FC-008.PV_Low
150.0, FC-008.PV_High
12.0, FC-008.Deviation_Limit
100.0, XV-101.Open_Limit
0.0, XV-101.Close_Limit
T#10s, XV-101.Timeout
100.0, PV-104.Open_Limit
0.0, PV-104.Close_Limit
T#14s, StartupDelay_TON.PT
90.0, LIC106_Overflow_GT.IN2
20.0, FC8_LowLevel_LT.IN2
100.0, FC8_FaultToX0_MULT.IN1
```

---


