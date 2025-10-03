# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-23 22:17:16

## Step 1: contextgen1-sensors
**Time:** 22:17:16

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
Output,DI_Out,BOOL,Debounced and stable digital output.
Output,Fault_State,BOOL,Indicates a fault in the input signal (e.g. wiring fault).
```

---

## Step 2: contextgen1-actuators
**Time:** 22:18:26

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
**Time:** 22:18:41

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability Needed |
|------------------|------------------------------|
| PID Control | 0.98 |
| OVERRIDE | 0.55 |
| VOTING | 0.15 |
| Cascade Control | 0.08 |
| Duty-Standby | 0.05 |
| FEEDFORWARD | 0.05 |
| SPLIT RANGE | 0.05 |
| Ratio Control | 0.04 |

Selected Control Strategy: PID Control
Short explanation: Multiple independent PID loops regulate flow, pressure, and temperature with alarms, interlocks, anti-windup, and bumpless transfer.

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
**Timestamp:** 2025-09-23 22:19:42

## Step 1: openplc-function-blocks-v2
**Time:** 22:19:42

### Output:
```
* Function Blocks *
DIGITAL_IN ESD-501
PID_BASIC FC-103
ANALOG_IN FT-103
VALVE_ELECTRIC FV-103
PID_BASIC PC-501
ANALOG_IN PT-501
ANALOG_IN PT-502
PID_BASIC TC-501
ANALOG_IN TT-101
VALVE_ELECTRIC TV-501
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 22:20:09

### Output:
```
* Function Block List * 
* Function Blocks *
DIGITAL_IN ESD-501
PID_BASIC FC-103
ANALOG_IN FT-103
VALVE_ELECTRIC FV-103
PID_BASIC PC-501
ANALOG_IN PT-501
ANALOG_IN PT-502
PID_BASIC TC-501
ANALOG_IN TT-101
VALVE_ELECTRIC TV-501
BOOL_IN ILK-PT-501-HI
BOOL_IN ILK-TT-101-HI
BOOL_IN PERM-PT-502-OK
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 22:20:57

### Output:
```
* Functions *

* Block-to-Block Connections *
FT-103.PV, FC-103.PV
FC-103.XOUT, FV-103.Control_Signal
TT-101.PV, TC-501.PV
TC-501.XOUT, TV-501.Control_Signal
PT-501.PV, PC-501.PV
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 22:21:35

### Output:
```
* Functions * 
OR FC103_ESD_TT_OR
OR FC103_Pressure_OR
OR FC103_Fault_OR
OR TV501_ESD_TTfault_OR
OR TV501_Perm_OR
NOT PT502_Permissive_NOT
NOT ESD_OK_NOT
NOT FT103_OK_NOT
NOT TT101_OK_NOT
AND FC103_AutoEnable_AND
AND TC501_AutoEnable_AND

* Data Connections *
PT-501.High_Alarm, ILK-PT-501-HI.Bool_In
ILK-PT-501-HI.Bool_Out, FC103_Pressure_OR.IN1
TT-101.High_Alarm, ILK-TT-101-HI.Bool_In
ILK-TT-101-HI.Bool_Out, FC103_ESD_TT_OR.IN2
ESD-501.DI_Out, FC103_ESD_TT_OR.IN1
FC103_ESD_TT_OR.OUT, FC103_Pressure_OR.IN2
FT-103.General_Fault, FC103_Fault_OR.IN1
FC103_Pressure_OR.OUT, FC103_Fault_OR.IN2
FC103_Fault_OR.OUT, FC-103.Inhibit
FC103_Fault_OR.OUT, FV-103.Inhibit
ESD-501.DI_Out, ESD_OK_NOT.IN
ESD_OK_NOT.OUT, FC103_AutoEnable_AND.IN1
FT-103.General_Fault, FT103_OK_NOT.IN
FT103_OK_NOT.OUT, FC103_AutoEnable_AND.IN2
FC103_AutoEnable_AND.OUT, FC-103.AUTO
TT-101.General_Fault, TT101_OK_NOT.IN
ESD_OK_NOT.OUT, TC501_AutoEnable_AND.IN1
TT101_OK_NOT.OUT, TC501_AutoEnable_AND.IN2
TC501_AutoEnable_AND.OUT, TC-501.AUTO
PT-502.High_Alarm, PERM-PT-502-OK.Bool_In
PERM-PT-502-OK.Bool_Out, PT502_Permissive_NOT.IN
ESD-501.DI_Out, TV501_ESD_TTfault_OR.IN1
TT-101.General_Fault, TV501_ESD_TTfault_OR.IN2
PT502_Permissive_NOT.OUT, TV501_Perm_OR.IN1
TV501_ESD_TTfault_OR.OUT, TV501_Perm_OR.IN2
TV501_Perm_OR.OUT, TV-501.Inhibit

* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
1600, FC-103.PV_High
400, FC-103.PV_Low
410, TT-101.PV_High
290, TT-101.PV_Low
415, TC-501.PV_High
290, TC-501.PV_Low
50, PT-501.PV_High
10, PT-502.PV_High
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 22:23:34

### Output:
```
* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
125, FT-103.Scaling_Slope
-500, FT-103.Scaling_Offset
TRUE, FT-103.Alarm_Enable
415, TT-101.PV_High
290, TT-101.PV_Low
TRUE, TT-101.Alarm_Enable
1.8, FC-103.KP
0.5, FC-103.TR
0.1, FC-103.TD
0, FC-103.MV_MIN
100, FC-103.MV_MAX
1600, FC-103.PV_High
400, FC-103.PV_Low
375, TC-501.SP
2.5, TC-501.KP
0.8, TC-501.TR
0.2, TC-501.TD
0, TC-501.MV_MIN
100, TC-501.MV_MAX
415, TC-501.PV_High
290, TC-501.PV_Low
100, FV-103.Open_Limit
0, FV-103.Close_Limit
100, TV-501.Open_Limit
0, TV-501.Close_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 22:24:24

### Output:
```
* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
125, FT-103.Scaling_Slope
-500, FT-103.Scaling_Offset
TRUE, FT-103.Alarm_Enable
410, TT-101.PV_High
290, TT-101.PV_Low
TRUE, TT-101.Alarm_Enable
1.8, FC-103.KP
0.5, FC-103.TR
0.1, FC-103.TD
0, FC-103.MV_MIN
100, FC-103.MV_MAX
1600, FC-103.PV_High
400, FC-103.PV_Low
375, TC-501.SP
2.5, TC-501.KP
0.8, TC-501.TR
0.2, TC-501.TD
0, TC-501.MV_MIN
100, TC-501.MV_MAX
415, TC-501.PV_High
290, TC-501.PV_Low
100, FV-103.Open_Limit
0, FV-103.Close_Limit
100, TV-501.Open_Limit
0, TV-501.Close_Limit
50, PT-501.PV_High
TRUE, PT-501.Alarm_Enable
10, PT-502.PV_High
TRUE, PT-502.Alarm_Enable
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 22:26:18

### Output:
```
* Variables *
REAL FT103_H2Flow_PV
REAL FC103_MV_to_FV103
REAL TT101_ReactorOutletTemp_PV
REAL TC501_MV_to_TV501
REAL PT501_ReactorPressure_PV
REAL PT502_ReactorInletPressure_PV

* Data Connections *
FT-103.PV, FT103_H2Flow_PV
FC-103.XOUT, FC103_MV_to_FV103
TT-101.PV, TT101_ReactorOutletTemp_PV
TC-501.XOUT, TC501_MV_to_TV501
PT-501.PV, PT501_ReactorPressure_PV
PT-502.PV, PT502_ReactorInletPressure_PV
```

---

## Step 8: openplc-rule-checks
**Time:** 22:27:00

### Output:
```
* Function Blocks *
DIGITAL_IN ESD-501
PID_BASIC FC-103
ANALOG_IN FT-103
VALVE_ELECTRIC FV-103
PID_BASIC PC-501
ANALOG_IN PT-501
ANALOG_IN PT-502
PID_BASIC TC-501
ANALOG_IN TT-101
VALVE_ELECTRIC TV-501

* Variables *
REAL FC103_SP_Operator
REAL FC103_SP_Reduced
REAL TC501_SP_Fixed
REAL FT103_H2Flow_PV
REAL FC103_MV_to_FV103
REAL TT101_ReactorOutletTemp_PV
REAL TC501_MV_to_TV501
REAL PT501_ReactorPressure_PV
REAL PT502_ReactorInletPressure_PV

* Functions *
OR FC103_Disable_OR
OR FV103_Manual_OR
AND FC103_AutoEnable_AND
NOT ESD_OK_NOT
NOT FT103_OK_NOT
OR TV501_Manual_OR
AND TC501_AutoEnable_AND
NOT TT101_OK_NOT
TON TV501_OpenDelay_TON
NOT PT502_Permissive_NOT
OR TV501_PermissiveFail_OR
OR TV501_Inhibit_OR
MULT FC103_SP_Reduce_MULT

* Data Connections * 
FT-103.PV, FC-103.PV
FC-103.XOUT, FV-103.Control_Signal
TT-101.PV, TC-501.PV
TC-501.XOUT, TV-501.Control_Signal
PT-501.PV, PC-501.PV
ESD-501.DI_Out, ESD_OK_NOT.IN
FT-103.General_Fault, FT103_OK_NOT.IN
TT-101.General_Fault, TT101_OK_NOT.IN
ESD_OK_NOT.OUT, FC103_AutoEnable_AND.IN1
FT103_OK_NOT.OUT, FC103_AutoEnable_AND.IN2
FC103_AutoEnable_AND.OUT, FC-103.AUTO
ESD_OK_NOT.OUT, TC501_AutoEnable_AND.IN1
TT101_OK_NOT.OUT, TC501_AutoEnable_AND.IN2
TC501_AutoEnable_AND.OUT, TC-501.AUTO
ESD-501.DI_Out, FC103_Disable_OR.IN1
TT-101.High_Alarm, FC103_Disable_OR.IN2
FC103_Disable_OR.OUT, FC-103.Inhibit
FC103_Disable_OR.OUT, FV-103.Inhibit
ESD-501.DI_Out, FV103_Manual_OR.IN1
TT-101.High_Alarm, FV103_Manual_OR.IN2
FV103_Manual_OR.OUT, FV-103.Manual_Mode
ESD-501.DI_Out, TV501_Manual_OR.IN1
TT-101.General_Fault, TV501_Manual_OR.IN2
TV501_Manual_OR.OUT, TV-501.Manual_Mode
PT-502.High_Alarm, TV501_OpenDelay_TON.IN
TV501_OpenDelay_TON.Q, PT502_Permissive_NOT.IN
PT502_Permissive_NOT.OUT, TV501_PermissiveFail_OR.IN1
ESD-501.DI_Out, TV501_PermissiveFail_OR.IN2
TV501_PermissiveFail_OR.OUT, TV501_Inhibit_OR.IN1
TT-101.General_Fault, TV501_Inhibit_OR.IN2
TV501_Inhibit_OR.OUT, TV-501.Inhibit
FC103_SP_Operator, FC103_SP_Reduce_MULT.IN1
0.5, FC103_SP_Reduce_MULT.IN2
FC103_SP_Reduce_MULT.OUT, FC-103.SP
FT-103.PV, FT103_H2Flow_PV
FC-103.XOUT, FC103_MV_to_FV103
TT-101.PV, TT101_ReactorOutletTemp_PV
TC-501.XOUT, TC501_MV_to_TV501
PT-501.PV, PT501_ReactorPressure_PV
PT-502.PV, PT502_ReactorInletPressure_PV

* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
125, FT-103.Scaling_Slope
-500, FT-103.Scaling_Offset
TRUE, FT-103.Alarm_Enable
1.8, FC-103.KP
0.5, FC-103.TR
0.1, FC-103.TD
0, FC-103.MV_MIN
100, FC-103.MV_MAX
1600, FC-103.PV_High
400, FC-103.PV_Low
20, FC-103.Deviation_Limit
375, TC-501.SP
2.5, TC-501.KP
0.8, TC-501.TR
0.2, TC-501.TD
0, TC-501.MV_MIN
100, TC-501.MV_MAX
415, TC-501.PV_High
290, TC-501.PV_Low
1, TC-501.Deviation_Limit
50, PT-501.PV_High
TRUE, PT-501.Alarm_Enable
10, PT-502.PV_High
TRUE, PT-502.Alarm_Enable
100, FV-103.Open_Limit
0, FV-103.Close_Limit
0, FV-103.Manual_Position
100, TV-501.Open_Limit
0, TV-501.Close_Limit
100, TV-501.Manual_Position
T#15s, TV501_OpenDelay_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 22:28:56

### Output:
```
* Function Blocks *
DIGITAL_IN ESD-501
PID_BASIC FC-103
ANALOG_IN FT-103
VALVE_ELECTRIC FV-103
PID_BASIC PC-501
ANALOG_IN PT-501
ANALOG_IN PT-502
PID_BASIC TC-501
ANALOG_IN TT-101
VALVE_ELECTRIC TV-501

* Variables *
REAL FC103_SP_Operator
REAL FC103_SP_Reduced
REAL TC501_SP_Fixed
REAL FT103_H2Flow_PV
REAL FC103_MV_to_FV103
REAL TT101_ReactorOutletTemp_PV
REAL TC501_MV_to_TV501
REAL PT501_ReactorPressure_PV
REAL PT502_ReactorInletPressure_PV

* Functions *
OR FC103_Disable_OR
OR FV103_Manual_OR
AND FC103_AutoEnable_AND
NOT ESD_OK_NOT
NOT FT103_OK_NOT
OR TV501_Manual_OR
AND TC501_AutoEnable_AND
NOT TT101_OK_NOT
TON TV501_OpenDelay_TON
NOT PT502_Permissive_NOT
OR TV501_PermissiveFail_OR
OR TV501_Inhibit_OR
MULT FC103_SP_Reduce_MULT

* Data Connections * 
FT-103.PV, FC-103.PV
FC-103.XOUT, FV-103.Control_Signal
TT-101.PV, TC-501.PV
TC-501.XOUT, TV-501.Control_Signal
PT-501.PV, PC-501.PV
ESD-501.DI_Out, ESD_OK_NOT.IN
FT-103.General_Fault, FT103_OK_NOT.IN
TT-101.General_Fault, TT101_OK_NOT.IN
ESD_OK_NOT.OUT, FC103_AutoEnable_AND.IN1
FT103_OK_NOT.OUT, FC103_AutoEnable_AND.IN2
FC103_AutoEnable_AND.OUT, FC-103.AUTO
ESD_OK_NOT.OUT, TC501_AutoEnable_AND.IN1
TT101_OK_NOT.OUT, TC501_AutoEnable_AND.IN2
TC501_AutoEnable_AND.OUT, TC-501.AUTO
ESD-501.DI_Out, FC103_Disable_OR.IN1
TT-101.High_Alarm, FC103_Disable_OR.IN2
FC103_Disable_OR.OUT, FC-103.Inhibit
FC103_Disable_OR.OUT, FV-103.Inhibit
ESD-501.DI_Out, FV103_Manual_OR.IN1
TT-101.High_Alarm, FV103_Manual_OR.IN2
FV103_Manual_OR.OUT, FV-103.Manual_Mode
ESD-501.DI_Out, TV501_Manual_OR.IN1
TT-101.General_Fault, TV501_Manual_OR.IN2
TV501_Manual_OR.OUT, TV-501.Manual_Mode
PT-502.High_Alarm, TV501_OpenDelay_TON.IN
TV501_OpenDelay_TON.Q, PT502_Permissive_NOT.IN
PT502_Permissive_NOT.OUT, TV501_PermissiveFail_OR.IN1
ESD-501.DI_Out, TV501_PermissiveFail_OR.IN2
TV501_PermissiveFail_OR.OUT, TV501_Inhibit_OR.IN1
TT-101.General_Fault, TV501_Inhibit_OR.IN2
TV501_Inhibit_OR.OUT, TV-501.Inhibit
FC103_SP_Operator, FC103_SP_Reduce_MULT.IN1
0.5, FC103_SP_Reduce_MULT.IN2
FC103_SP_Reduce_MULT.OUT, FC-103.SP
FT-103.PV, FT103_H2Flow_PV
FC-103.XOUT, FC103_MV_to_FV103
TT-101.PV, TT101_ReactorOutletTemp_PV
TC-501.XOUT, TC501_MV_to_TV501
PT-501.PV, PT501_ReactorPressure_PV
PT-502.PV, PT502_ReactorInletPressure_PV

* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
125, FT-103.Scaling_Slope
-500, FT-103.Scaling_Offset
TRUE, FT-103.Alarm_Enable
1.8, FC-103.KP
0.5, FC-103.TR
0.1, FC-103.TD
0, FC-103.MV_MIN
100, FC-103.MV_MAX
1600, FC-103.PV_High
400, FC-103.PV_Low
20, FC-103.Deviation_Limit
375, TC-501.SP
2.5, TC-501.KP
0.8, TC-501.TR
0.2, TC-501.TD
0, TC-501.MV_MIN
100, TC-501.MV_MAX
415, TC-501.PV_High
290, TC-501.PV_Low
1, TC-501.Deviation_Limit
50, PT-501.PV_High
TRUE, PT-501.Alarm_Enable
10, PT-502.PV_High
TRUE, PT-502.Alarm_Enable
100, FV-103.Open_Limit
0, FV-103.Close_Limit
0, FV-103.Manual_Position
100, TV-501.Open_Limit
0, TV-501.Close_Limit
100, TV-501.Manual_Position
T#15s, TV501_OpenDelay_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 22:29:27

### Output:
```
* Function Blocks *
DIGITAL_IN ESD-501
PID_BASIC FC-103
ANALOG_IN FT-103
VALVE_ELECTRIC FV-103
PID_BASIC PC-501
ANALOG_IN PT-501
ANALOG_IN PT-502
PID_BASIC TC-501
ANALOG_IN TT-101
VALVE_ELECTRIC TV-501

* Variables *
REAL FC103_SP_Operator
REAL FC103_SP_Reduced
REAL TC501_SP_Fixed
REAL FT103_H2Flow_PV
REAL FC103_MV_to_FV103
REAL TT101_ReactorOutletTemp_PV
REAL TC501_MV_to_TV501
REAL PT501_ReactorPressure_PV
REAL PT502_ReactorInletPressure_PV

* Functions *
OR FC103_Disable_OR
AND FC103_AutoEnable_AND
NOT ESD_OK_NOT
NOT FT103_OK_NOT
AND TC501_AutoEnable_AND
NOT TT101_OK_NOT
TON TV501_OpenDelay_TON
NOT PT502_Permissive_NOT
OR TV501_Inhibit_OR
MULT FC103_SP_Reduce_MULT
OR TV501_Base_OR

* Data Connections * 
FT-103.PV, FC-103.PV
FC-103.XOUT, FV-103.Control_Signal
TT-101.PV, TC-501.PV
TC-501.XOUT, TV-501.Control_Signal
PT-501.PV, PC-501.PV
ESD-501.DI_Out, ESD_OK_NOT.IN
FT-103.General_Fault, FT103_OK_NOT.IN
TT-101.General_Fault, TT1 01_OK_NOT.IN
ESD_OK_NOT.OUT, FC103_AutoEnable_AND.IN1
FT103_OK_NOT.OUT, FC103_AutoEnable_AND.IN2
FC103_AutoEnable_AND.OUT, FC-103.AUTO
ESD_OK_NOT.OUT, TC501_AutoEnable_AND.IN1
TT101_OK_NOT.OUT, TC501_AutoEnable_AND.IN2
TC501_AutoEnable_AND.OUT, TC-501.AUTO
ESD-501.DI_Out, FC103_Disable_OR.IN1
TT-101.High_Alarm, FC103_Disable_OR.IN2
FC103_Disable_OR.OUT, FC-103.Inhibit
FC103_Disable_OR.OUT, FV-103.Inhibit
FC103_Disable_OR.OUT, FV-103.Manual_Mode
ESD-501.DI_Out, TV501_Base_OR.IN1
TT-101.General_Fault, TV501_Base_OR.IN2
TV501_Base_OR.OUT, TV-501.Manual_Mode
PT-502.High_Alarm, TV501_OpenDelay_TON.IN
TV501_OpenDelay_TON.Q, PT502_Permissive_NOT.IN
TV501_Base_OR.OUT, TV501_Inhibit_OR.IN1
PT502_Permissive_NOT.OUT, TV501_Inhibit_OR.IN2
TV501_Inhibit_OR.OUT, TV-501.Inhibit
FC103_SP_Operator, FC103_SP_Reduce_MULT.IN1
FC103_SP_Reduce_MULT.OUT, FC-103.SP
FT-103.PV, FT103_H2Flow_PV
FC-103.XOUT, FC103_MV_to_FV103
TT-101.PV, TT101_ReactorOutletTemp_PV
TC-501.XOUT, TC501_MV_to_TV501
PT-501.PV, PT501_ReactorPressure_PV
PT-502.PV, PT502_ReactorInletPressure_PV

* Parameter Data Connections *
1600, FT-103.PV_High
400, FT-103.PV_Low
125, FT-103.Scaling_Slope
-500, FT-103.Scaling_Offset
TRUE, FT-103.Alarm_Enable
1.8, FC-103.KP
0.5, FC-103.TR
0.1, FC-103.TD
0, FC-103.MV_MIN
100, FC-103.MV_MAX
1600, FC-103.PV_High
400, FC-103.PV_Low
20, FC-103.Deviation_Limit
375, TC-501.SP
2.5, TC-501.KP
0.8, TC-501.TR
0.2, TC-501.TD
0, TC-501.MV_MIN
100, TC-501.MV_MAX
415, TC-501.PV_High
290, TC-501.PV_Low
1, TC-501.Deviation_Limit
50, PT-501.PV_High
TRUE, PT-501.Alarm_Enable
10, PT-502.PV_High
TRUE, PT-502.Alarm_Enable
100, FV-103.Open_Limit
0, FV-103.Close_Limit
0, FV-103.Manual_Position
100, TV-501.Open_Limit
0, TV-501.Close_Limit
100, TV-501.Manual_Position
T#15s, TV501_OpenDelay_TON.PT
0.5, FC103_SP_Reduce_MULT.IN2
```

---


