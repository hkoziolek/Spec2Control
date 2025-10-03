# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 05:25:58

## Step 1: contextgen1-sensors
**Time:** 05:25:58

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
**Time:** 05:26:22

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
**Time:** 05:27:06

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| PID Control | 0.98 |
| OVERRIDE | 0.74 |

Selected Control Strategy: PID Control
Short explanation: The core of the narrative is two independent PID loops (temperature TIC-101 and level LIC-106) driving final elements based on process variables and setpoints; other logic augments but PID is fundamental.

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
**Timestamp:** 2025-09-24 05:28:05

## Step 1: openplc-function-blocks-v2
**Time:** 05:28:05

### Output:
```
* Function Blocks *
ANALOG_IN TIT-103
ANALOG_IN LT-105
PID_BASIC TIC-101
PID_BASIC LIC-106
PID_BASIC FC-004
VALVE_ELECTRIC XV-102
VALVE_ELECTRIC LV-104
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 05:28:30

### Output:
```
* Function Blocks *
ANALOG_IN TIT-103
ANALOG_IN LT-105
PID_BASIC TIC-101
PID_BASIC LIC-106
PID_BASIC FC-004
VALVE_ELECTRIC XV-102
VALVE_ELECTRIC LV-104
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 05:29:18

### Output:
```
* Functions *

* Block-to-Block Connections *
TIT-103.PV, TIC-101.PV
TIC-101.XOUT, XV-102.Control_Signal
LT-105.PV, LIC-106.PV
LIC-106.XOUT, LV-104.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 05:29:53

### Output:
```
* Functions * 
OR TIC101_Inhibit_OR
OR LIC106_Inhibit_OR

* Data Connections *
XV-102.Position_Error, TIC101_Inhibit_OR.IN1
TIT-103.High_Alarm, TIC101_Inhibit_OR.IN2
FC-004.PV_Low_Alarm, TIC101_Inhibit_OR.IN3
TIT-103.General_Fault, TIC101_Inhibit_OR.IN4
TIC101_Inhibit_OR.OUT, TIC-101.Inhibit
LV-104.Position_Error, LIC106_Inhibit_OR.IN1
LT-105.General_Fault, LIC106_Inhibit_OR.IN2
XV-102.Alarm, LIC106_Inhibit_OR.IN3
LIC106_Inhibit_OR.OUT, LIC-106.Inhibit
TIT-103.High_Alarm, XV-102.Inhibit
LT-105.High_Alarm, LV-104.Inhibit

* Parameter Data Connections *
200, TIT-103.PV_High
160, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
80, LT-105.PV_High
20, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
T#5s, XV-102.Timeout
10, FC-004.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 05:31:39

### Output:
```
* Parameter Data Connections *
200.0, TIT-103.PV_High
160.0, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
15.625, TIT-103.Scaling_Slope
-62.5, TIT-103.Scaling_Offset
80.0, LT-105.PV_High
20.0, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
6.25, LT-105.Scaling_Slope
-25.0, LT-105.Scaling_Offset
180.0, TIC-101.SP
0.0, TIC-101.MV_MIN
100.0, TIC-101.MV_MAX
3.0, TIC-101.KP
1.2, TIC-101.TR
0.1, TIC-101.TD
200.0, TIC-101.PV_High
160.0, TIC-101.PV_Low
50.0, LIC-106.SP
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
2.5, LIC-106.KP
0.9, LIC-106.TR
0.0, LIC-106.TD
80.0, LIC-106.PV_High
20.0, LIC-106.PV_Low
100.0, XV-102.Open_Limit
0.0, XV-102.Close_Limit
T#5s, XV-102.Timeout
100.0, LV-104.Open_Limit
0.0, LV-104.Close_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 05:33:07

### Output:
```
* Parameter Data Connections *
200.0, TIT-103.PV_High
160.0, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
15.625, TIT-103.Scaling_Slope
-62.5, TIT-103.Scaling_Offset
80.0, LT-105.PV_High
20.0, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
6.25, LT-105.Scaling_Slope
-25.0, LT-105.Scaling_Offset
180.0, TIC-101.SP
0.0, TIC-101.MV_MIN
100.0, TIC-101.MV_MAX
3.0, TIC-101.KP
1.2, TIC-101.TR
0.1, TIC-101.TD
200.0, TIC-101.PV_High
160.0, TIC-101.PV_Low
50.0, LIC-106.SP
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
2.5, LIC-106.KP
0.9, LIC-106.TR
0.0, LIC-106.TD
80.0, LIC-106.PV_High
20.0, LIC-106.PV_Low
100.0, XV-102.Open_Limit
0.0, XV-102.Close_Limit
T#5s, XV-102.Timeout
100.0, LV-104.Open_Limit
0.0, LV-104.Close_Limit
10.0, FC-004.PV_Low
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 05:35:09

### Output:
```
* Variables *
REAL TIT103_PV_Temperature
REAL LT105_Level_PV
REAL TIC101_MV_to_XV102
REAL LIC106_MV_to_LV104

* Data Connections *
TIT-103.PV, TIT103_PV_Temperature
LT-105.PV, LT105_Level_PV
TIC-101.XOUT, TIC101_MV_to_XV102
LIC-106.XOUT, LIC106_MV_to_LV104
```

---

## Step 8: openplc-rule-checks
**Time:** 05:35:54

### Output:
```
* Function Blocks *
ANALOG_IN TIT-103
ANALOG_IN LT-105
ANALOG_IN FC-004
PID_BASIC TIC-101
PID_BASIC LIC-106
VALVE_ELECTRIC XV-102
VALVE_ELECTRIC LV-104

* Variables *
REAL TIT103_PV_Temperature
REAL LT105_Level_PV
REAL TIC101_MV_to_XV102
REAL LIC106_MV_to_LV104

* Functions *
OR TIC101_Inhibit_OR
OR LIC106_Inhibit_OR
GT FC004_Above10_GT
AND TIC101_Enable_AND
AND LIC106_Enable_AND
NOT XV102_PosErr_NOT
NOT XV102_Alarm_NOT
NOT LV104_PosErr_NOT
OR XV102_ForceClose_OR
OR LV104_ForceClose_OR
TON TIC101_StartDelay_TON
TON LIC106_StartDelay_TON

* Data Connections *
TIT-103.PV, TIC-101.PV
TIC-101.XOUT, XV-102.Control_Signal
LT-105.PV, LIC-106.PV
LIC-106.XOUT, LV-104.Control_Signal
XV-102.Position_Error, TIC101_Inhibit_OR.IN1
TIT-103.High_Alarm, TIC101_Inhibit_OR.IN2
FC-004.Low_Alarm, TIC101_Inhibit_OR.IN3
TIT-103.General_Fault, TIC101_Inhibit_OR.IN4
TIC101_Inhibit_OR.OUT, TIC-101.Inhibit
LV-104.Position_Error, LIC106_Inhibit_OR.IN1
LT-105.General_Fault, LIC106_Inhibit_OR.IN2
XV-102.Alarm, LIC106_Inhibit_OR.IN3
LIC106_Inhibit_OR.OUT, LIC-106.Inhibit
TIT-103.High_Alarm, XV-102.Inhibit
LT-105.High_Alarm, LV-104.Inhibit
FC-004.PV, FC004_Above10_GT.IN1
FC004_Above10_GT.OUT, TIC101_StartDelay_TON.IN
TIC101_StartDelay_TON.Q, TIC101_Enable_AND.IN1
XV-102.Position_Error, XV102_PosErr_NOT.IN
XV102_PosErr_NOT.OUT, TIC101_Enable_AND.IN2
TIC101_Enable_AND.OUT, TIC-101.AUTO
TIC-101.AUTO, LIC106_StartDelay_TON.IN
XV-102.Alarm, XV102_Alarm_NOT.IN
XV102_Alarm_NOT.OUT, LIC106_Enable_AND.IN1
LIC106_StartDelay_TON.Q, LIC106_Enable_AND.IN2
LV-104.Position_Error, LV104_PosErr_NOT.IN
LV104_PosErr_NOT.OUT, LIC106_Enable_AND.IN3
LIC106_Enable_AND.OUT, LIC-106.AUTO
TIT-103.High_Alarm, XV102_ForceClose_OR.IN1
FALSE, XV102_ForceClose_OR.IN2
XV102_ForceClose_OR.OUT, XV-102.Manual_Mode
LT-105.High_Alarm, LV104_ForceClose_OR.IN1
FALSE, LV104_ForceClose_OR.IN2
LV104_ForceClose_OR.OUT, LV-104.Manual_Mode
TIT-103.PV, TIT103_PV_Temperature
LT-105.PV, LT105_Level_PV
TIC-101.XOUT, TIC101_MV_to_XV102
LIC-106.XOUT, LIC106_MV_to_LV104

* Parameter Data Connections *
200.0, TIT-103.PV_High
160.0, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
15.625, TIT-103.Scaling_Slope
-62.5, TIT-103.Scaling_Offset
80.0, LT-105.PV_High
20.0, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
6.25, LT-105.Scaling_Slope
-25.0, LT-105.Scaling_Offset
10.0, FC-004.PV_Low
TRUE, FC-004.Alarm_Enable
180.0, TIC-101.SP
0.0, TIC-101.MV_MIN
100.0, TIC-101.MV_MAX
3.0, TIC-101.KP
1.2, TIC-101.TR
0.1, TIC-101.TD
200.0, TIC-101.PV_High
160.0, TIC-101.PV_Low
50.0, LIC-106.SP
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
2.5, LIC-106.KP
0.9, LIC-106.TR
0.0, LIC-106.TD
80.0, LIC-106.PV_High
20.0, LIC-106.PV_Low
100.0, XV-102.Open_Limit
0.0, XV-102.Close_Limit
T#5s, XV-102.Timeout
0.0, XV-102.Manual_Position
100.0, LV-104.Open_Limit
0.0, LV-104.Close_Limit
0.0, LV-104.Manual_Position
T#21s, TIC101_StartDelay_TON.PT
T#15s, LIC106_StartDelay_TON.PT
10.0, FC004_Above10_GT.IN2
```

---

## Step 9: openplc-rule-checks2
**Time:** 05:40:10

### Output:
```
* Function Blocks *
ANALOG_IN TIT-103
ANALOG_IN LT-105
ANALOG_IN FC-004
PID_BASIC TIC-101
PID_BASIC LIC-106
VALVE_ELECTRIC XV-102
VALVE_ELECTRIC LV-104

* Variables *
REAL TIT103_PV_Temperature
REAL LT105_Level_PV
REAL TIC101_MV_to_XV102
REAL LIC106_MV_to_LV104

* Functions *
OR TIC101_Inhibit_OR
OR LIC106_Inhibit_OR
GT FC004_Above10_GT
AND TIC101_Enable_AND
AND LIC106_Enable_AND
NOT XV102_PosErr_NOT
NOT XV102_Alarm_NOT
NOT LV104_PosErr_NOT
OR XV102_ForceClose_OR
OR LV104_ForceClose_OR
TON TIC101_StartDelay_TON
TON LIC106_StartDelay_TON

* Data Connections *
TIT-103.PV, TIC-101.PV
TIC-101.XOUT, XV-102.Control_Signal
LT-105.PV, LIC-106.PV
LIC-106.XOUT, LV-104.Control_Signal
XV-102.Position_Error, TIC101_Inhibit_OR.IN1
TIT-103.High_Alarm, TIC101_Inhibit_OR.IN2
FC-004.Low_Alarm, TIC101_Inhibit_OR.IN3
TIT-103.General_Fault, TIC101_Inhibit_OR.IN4
TIC101_Inhibit_OR.OUT, TIC-101.Inhibit
LV-104.Position_Error, LIC106_Inhibit_OR.IN1
LT-105.General_Fault, LIC106_Inhibit_OR.IN2
XV-102.Alarm, LIC106_Inhibit_OR.IN3
LIC106_Inhibit_OR.OUT, LIC-106.Inhibit
TIT-103.High_Alarm, XV-102.Inhibit
LT-105.High_Alarm, LV-104.Inhibit
FC-004.PV, FC004_Above10_GT.IN1
FC004_Above10_GT.OUT, TIC101_StartDelay_TON.IN
TIC101_StartDelay_TON.Q, TIC101_Enable_AND.IN1
XV-102.Position_Error, XV102_PosErr_NOT.IN
XV102_PosErr_NOT.OUT, TIC101_Enable_AND.IN2
TIC101_Enable_AND.OUT, TIC-101.AUTO
TIC-101.AUTO, LIC106_StartDelay_TON.IN
XV-102.Alarm, XV102_Alarm_NOT.IN
XV102_Alarm_NOT.OUT, LIC106_Enable_AND.IN1
LIC106_StartDelay_TON.Q, LIC106_Enable_AND.IN2
LV-104.Position_Error, LV104_PosErr_NOT.IN
LV104_PosErr_NOT.OUT, LIC106_Enable_AND.IN3
LIC106_Enable_AND.OUT, LIC-106.AUTO
TIT-103.High_Alarm, XV102_ForceClose_OR.IN1
FALSE, XV102_ForceClose_OR.IN2
XV102_ForceClose_OR.OUT, XV-102.Manual_Mode
LT-105.High_Alarm, LV104_ForceClose_OR.IN1
FALSE, LV104_ForceClose_OR.IN2
LV104_ForceClose_OR.OUT, LV-104.Manual_Mode
TIT-103.PV, TIT103_PV_Temperature
LT-105.PV, LT105_Level_PV
TIC-101.XOUT, TIC101_MV_to_XV102
LIC-106.XOUT, LIC106_MV_to_LV104

* Parameter Data Connections *
200.0, TIT-103.PV_High
160.0, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
15.625, TIT-103.Scaling_Slope
-62.5, TIT-103.Scaling_Offset
80.0, LT-105.PV_High
20.0, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
6.25, LT-105.Scaling_Slope
-25.0, LT-105.Scaling_Offset
10.0, FC-004.PV_Low
TRUE, FC-004.Alarm_Enable
180.0, TIC-101.SP
0.0, TIC-101.MV_MIN
100.0, TIC-101.MV_MAX
3.0, TIC-101.KP
1.2, TIC-101.TR
0.1, TIC-101.TD
200.0, TIC-101.PV_High
160.0, TIC-101.PV_Low
50.0, LIC-106.SP
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
2.5, LIC-106.KP
0.9, LIC-106.TR
0.0, LIC-106.TD
80.0, LIC-106.PV_High
20.0, LIC-106.PV_Low
100.0, XV-102.Open_Limit
0.0, XV-102.Close_Limit
T#5s, XV-102.Timeout
0.0, XV-102.Manual_Position
100.0, LV-104.Open_Limit
0.0, LV-104.Close_Limit
0.0, LV-104.Manual_Position
T#21s, TIC101_StartDelay_TON.PT
T#15s, LIC106_StartDelay_TON.PT
10.0, FC004_Above10_GT.IN2
```

---

## Step 10: append_two_inputs
**Time:** 05:40:48

### Output:
```
* Function Blocks *
ANALOG_IN TIT-103
ANALOG_IN LT-105
ANALOG_IN FC-004
PID_BASIC TIC-101
PID_BASIC LIC-106
VALVE_ELECTRIC XV-102
VALVE_ELECTRIC LV-104

* Variables *
REAL TIT103_PV_Temperature
REAL LT105_Level_PV
REAL TIC101_MV_to_XV102
REAL LIC106_MV_to_LV104

* Functions *
OR TIC101_Inhibit_OR
OR LIC106_Inhibit_OR
GT FC004_Above10_GT
AND TIC101_Enable_AND
AND LIC106_Enable_AND
NOT XV102_PosErr_NOT
NOT XV102_Alarm_NOT
NOT LV104_PosErr_NOT
TON TIC101_StartDelay_TON
TON LIC106_StartDelay_TON

* Data Connections *
TIT-103.PV, TIC-101.PV
TIC-101.XOUT, XV-102.Control_Signal
LT-105.PV, LIC-106.PV
LIC-106.XOUT, LV-104.Control_Signal
XV-102.Position_Error, TIC101_Inhibit_OR.IN1
TIT-103.High_Alarm, TIC101_Inhibit_OR.IN2
FC-004.Low_Alarm, TIC101_Inhibit_OR.IN3
TIT-103.General_Fault, TIC101_Inhibit_OR.IN4
TIC101_Inhibit_OR.OUT, TIC-101.Inhibit
LV-104.Position_Error, LIC106_Inhibit_OR.IN1
LT-105.General_Fault, LIC106_Inhibit_OR.IN2
XV-102.Alarm, LIC106_Inhibit_OR.IN3
LIC106_Inhibit_OR.OUT, LIC-106.Inhibit
TIT-103.High_Alarm, XV-102.Inhibit
LT-105.High_Alarm, LV-104.Inhibit
FC-004.PV, FC004_Above10_GT.IN1
FC004_Above10_GT.OUT, TIC101_StartDelay_TON.IN
TIC101_StartDelay_TON.Q, TIC101_Enable_AND.IN1
XV-102.Position_Error, XV102_PosErr_NOT.IN
XV102_PosErr_NOT.OUT, TIC101_Enable_AND.IN2
TIC101_Enable_AND.OUT, TIC-101.AUTO
TIC-101.AUTO, LIC106_StartDelay_TON.IN
XV-102.Alarm, XV102_Alarm_NOT.IN
XV102_Alarm_NOT.OUT, LIC106_Enable_AND.IN1
LIC106_StartDelay_TON.Q, LIC106_Enable_AND.IN2
LV-104.Position_Error, LV104_PosErr_NOT.IN
LV104_PosErr_NOT.OUT, LIC106_Enable_AND.IN3
LIC106_Enable_AND.OUT, LIC-106.AUTO
TIT-103.High_Alarm, XV-102.Manual_Mode
LT-105.High_Alarm, LV-104.Manual_Mode
TIT-103.PV, TIT103_PV_Temperature
LT-105.PV, LT105_Level_PV
TIC-101.XOUT, TIC101_MV_to_XV102
LIC-106.XOUT, LIC106_MV_to_LV104

* Parameter Data Connections *
200.0, TIT-103.PV_High
160.0, TIT-103.PV_Low
TRUE, TIT-103.Alarm_Enable
15.625, TIT-103.Scaling_Slope
-62.5, TIT-103.Scaling_Offset
80.0, LT-105.PV_High
20.0, LT-105.PV_Low
TRUE, LT-105.Alarm_Enable
6.25, LT-105.Scaling_Slope
-25.0, LT-105.Scaling_Offset
10.0, FC-004.PV_Low
TRUE, FC-004.Alarm_Enable
180.0, TIC-101.SP
0.0, TIC-101.MV_MIN
100.0, TIC-101.MV_MAX
3.0, TIC-101.KP
1.2, TIC-101.TR
0.1, TIC-101.TD
200.0, TIC-101.PV_High
160.0, TIC-101.PV_Low
50.0, LIC-106.SP
0.0, LIC-106.MV_MIN
100.0, LIC-106.MV_MAX
2.5, LIC-106.KP
0.9, LIC-106.TR
0.0, LIC-106.TD
80.0, LIC-106.PV_High
20.0, LIC-106.PV_Low
100.0, XV-102.Open_Limit
0.0, XV-102.Close_Limit
T#5s, XV-102.Timeout
0.0, XV-102.Manual_Position
100.0, LV-104.Open_Limit
0.0, LV-104.Close_Limit
0.0, LV-104.Manual_Position
T#21s, TIC101_StartDelay_TON.PT
T#15s, LIC106_StartDelay_TON.PT
10.0, FC004_Above10_GT.IN2
```

---


