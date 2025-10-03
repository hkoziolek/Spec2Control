# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 02:49:04

## Step 1: contextgen1-sensors
**Time:** 02:49:04

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
**Time:** 02:49:24

### Output:
```
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
**Time:** 02:49:41

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
| PID Control | 0.98 |
| OVERRIDE | 0.55 |

Selected Control Strategy: PID Control 
Short explanation: Two independent feedback loops (SEL and dilution consistency) use measured analog signals to drive actuators via PID controllers, fitting the standard PID Control architecture.

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
**Timestamp:** 2025-09-24 02:50:21

## Step 1: openplc-function-blocks-v2
**Time:** 02:50:21

### Output:
```
* Function Blocks *
ANALOG_IN CT-501
PID_BASIC FC-502
VALVE_ELECTRIC FV-502
ANALOG_IN LT-501
MOTOR_ON_OFF M-501
ANALOG_IN PT-502
PID_BASIC SELC-501
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 02:50:50

### Output:
```
* Function Blocks *
ANALOG_IN CT-501
ANALOG_IN LT-501
ANALOG_IN PT-502
ANALOG_IN PG-501
ANALOG_IN SEL-501
PID_BASIC FC-502
PID_BASIC SELC-501
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC PGA-501
MOTOR_ON_OFF M-501
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 02:52:41

### Output:
```
* Functions *

* Block-to-Block Connections *
CT-501.PV, FC-502.PV
FC-502.XOUT, FV-502.Control_Signal
SEL-501.PV, SELC-501.PV
SELC-501.XOUT, PGA-501.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 02:53:09

### Output:
```
* Functions * 
OR PG_Alarms_OR
NOT PG_OK_NOT
AND SELC_Permissive_AND
NOT SELC_Inhibit_NOT
NOT Level_OK_NOT
OR Pressure_OOR_OR
NOT Press_OK_NOT
AND FC_Permissive_AND
NOT FC_Inhibit_NOT
OR FC_FinalInhibit_OR

* Data Connections *
PG-501.High_Alarm, PG_Alarms_OR.IN1
PG-501.Low_Alarm, PG_Alarms_OR.IN2
PG_Alarms_OR.OUT, PG_OK_NOT.IN
M-501.FB_Running, SELC_Permissive_AND.IN1
PG_OK_NOT.OUT, SELC_Permissive_AND.IN2
SELC_Permissive_AND.OUT, SELC_Inhibit_NOT.IN
SELC_Inhibit_NOT.OUT, SELC-501.Inhibit
SELC_Inhibit_NOT.OUT, PGA-501.Inhibit
PG_Alarms_OR.OUT, M-501.Inhibit
LT-501.Low_Alarm, Level_OK_NOT.IN
PT-502.High_Alarm, Pressure_OOR_OR.IN1
PT-502.Low_Alarm, Pressure_OOR_OR.IN2
Pressure_OOR_OR.OUT, Press_OK_NOT.IN
Level_OK_NOT.OUT, FC_Permissive_AND.IN1
Press_OK_NOT.OUT, FC_Permissive_AND.IN2
FC_Permissive_AND.OUT, FC_Inhibit_NOT.IN
FC_Inhibit_NOT.OUT, FC_FinalInhibit_OR.IN1
CT-501.General_Fault, FC_FinalInhibit_OR.IN2
FC_FinalInhibit_OR.OUT, FC-502.Inhibit
FC_FinalInhibit_OR.OUT, FV-502.Inhibit

* Parameter Data Connections *
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
600, PT-502.PV_High
300, PT-502.PV_Low
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
20, LT-501.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 02:54:11

### Output:
```
* Parameter Data Connections *
0.1875, CT-501.Scaling_Slope
1.25, CT-501.Scaling_Offset
TRUE, CT-501.Alarm_Enable
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
0.0625, SEL-501.Scaling_Slope
-0.05, SEL-501.Scaling_Offset
TRUE, SEL-501.Alarm_Enable
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
TRUE, PT-502.Alarm_Enable
600.0, PT-502.PV_High
300.0, PT-502.PV_Low
TRUE, PG-501.Alarm_Enable
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
TRUE, LT-501.Alarm_Enable
20.0, LT-501.PV_Low
3.0, FC-502.SP
0.0, FC-502.MV_MIN
100.0, FC-502.MV_MAX
2.2, FC-502.KP
0.7, FC-502.TR
0.0, FC-502.TD
4.0, FC-502.PV_High
2.0, FC-502.PV_Low
0.0, SELC-501.MV_MIN
100.0, SELC-501.MV_MAX
1.8, SELC-501.KP
0.5, SELC-501.TR
0.1, SELC-501.TD
1.1, SELC-501.PV_High
0.3, SELC-501.PV_Low
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
100.0, PGA-501.Open_Limit
0.0, PGA-501.Close_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 02:55:00

### Output:
```
* Parameter Data Connections *
0.1875, CT-501.Scaling_Slope
1.25, CT-501.Scaling_Offset
TRUE, CT-501.Alarm_Enable
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
0.0625, SEL-501.Scaling_Slope
-0.05, SEL-501.Scaling_Offset
TRUE, SEL-501.Alarm_Enable
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
TRUE, PT-502.Alarm_Enable
600.0, PT-502.PV_High
300.0, PT-502.PV_Low
TRUE, PG-501.Alarm_Enable
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
TRUE, LT-501.Alarm_Enable
100.0, LT-501.PV_High
20.0, LT-501.PV_Low
3.0, FC-502.SP
0.0, FC-502.MV_MIN
100.0, FC-502.MV_MAX
2.2, FC-502.KP
0.7, FC-502.TR
0.0, FC-502.TD
4.0, FC-502.PV_High
2.0, FC-502.PV_Low
0.0, SELC-501.MV_MIN
100.0, SELC-501.MV_MAX
1.8, SELC-501.KP
0.5, SELC-501.TR
0.1, SELC-501.TD
1.1, SELC-501.PV_High
0.3, SELC-501.PV_Low
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
100.0, PGA-501.Open_Limit
0.0, PGA-501.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 02:56:11

### Output:
```
* Variables *
REAL SELC_501_MV_Percent
REAL FC_502_MV_Percent

* Data Connections *
SELC-501.XOUT, SELC_501_MV_Percent
FC-502.XOUT, FC_502_MV_Percent
```

---

## Step 8: openplc-rule-checks
**Time:** 02:56:37

### Output:
```
* Function Blocks *
ANALOG_IN CT-501
ANALOG_IN LT-501
ANALOG_IN PT-502
ANALOG_IN PG-501
ANALOG_IN SEL-501
PID_BASIC FC-502
PID_BASIC SELC-501
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC PGA-501
MOTOR_ON_OFF M-501

* Variables *
REAL SELC_501_MV_Percent
REAL FC_502_MV_Percent

* Functions *
OR PG_Alarms_OR
NOT PG_OK_NOT
AND SELC_Permissive_AND
NOT SELC_Inhibit_NOT
NOT Level_OK_NOT
OR Pressure_OOR_OR
NOT Press_OK_NOT
AND FC_Permissive_AND
NOT FC_Inhibit_NOT
OR FC_FinalInhibit_OR

* Data Connections *
CT-501.PV, FC-502.PV
FC-502.XOUT, FV-502.Control_Signal
SEL-501.PV, SELC-501.PV
SELC-501.XOUT, PGA-501.Control_Signal
PG-501.High_Alarm, PG_Alarms_OR.IN1
PG-501.Low_Alarm, PG_Alarms_OR.IN2
PG_Alarms_OR.OUT, PG_OK_NOT.IN
M-501.FB_Running, SELC_Permissive_AND.IN1
PG_OK_NOT.OUT, SELC_Permissive_AND.IN2
SELC_Permissive_AND.OUT, SELC_Inhibit_NOT.IN
SELC_Inhibit_NOT.OUT, SELC-501.Inhibit
SELC_Inhibit_NOT.OUT, PGA-501.Inhibit
PG_Alarms_OR.OUT, M-501.Inhibit
LT-501.Low_Alarm, Level_OK_NOT.IN
PT-502.High_Alarm, Pressure_OOR_OR.IN1
PT-502.Low_Alarm, Pressure_OOR_OR.IN2
Pressure_OOR_OR.OUT, Press_OK_NOT.IN
Level_OK_NOT.OUT, FC_Permissive_AND.IN1
Press_OK_NOT.OUT, FC_Permissive_AND.IN2
FC_Permissive_AND.OUT, FC_Inhibit_NOT.IN
FC_Inhibit_NOT.OUT, FC_FinalInhibit_OR.IN1
CT-501.General_Fault, FC_FinalInhibit_OR.IN2
FC_FinalInhibit_OR.OUT, FC-502.Inhibit
FC_FinalInhibit_OR.OUT, FV-502.Inhibit
SELC-501.XOUT, SELC_501_MV_Percent
FC-502.XOUT, FC_502_MV_Percent

* Parameter Data Connections *
0.1875, CT-501.Scaling_Slope
1.25, CT-501.Scaling_Offset
TRUE, CT-501.Alarm_Enable
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
TRUE, PT-502.Alarm_Enable
600.0, PT-502.PV_High
300.0, PT-502.PV_Low
TRUE, PG-501.Alarm_Enable
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
0.0625, SEL-501.Scaling_Slope
-0.05, SEL-501.Scaling_Offset
TRUE, SEL-501.Alarm_Enable
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
TRUE, LT-501.Alarm_Enable
100.0, LT-501.PV_High
20.0, LT-501.PV_Low
TRUE, FC-502.AUTO
3.0, FC-502.SP
0.0, FC-502.MV_MIN
100.0, FC-502.MV_MAX
2.2, FC-502.KP
0.7, FC-502.TR
0.0, FC-502.TD
4.0, FC-502.PV_High
2.0, FC-502.PV_Low
TRUE, SELC-501.AUTO
0.7, SELC-501.SP
0.0, SELC-501.MV_MIN
100.0, SELC-501.MV_MAX
1.8, SELC-501.KP
0.5, SELC-501.TR
0.1, SELC-501.TD
1.1, SELC-501.PV_High
0.3, SELC-501.PV_Low
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
100.0, PGA-501.Open_Limit
0.0, PGA-501.Close_Limit
```

---

## Step 9: openplc-rule-checks2
**Time:** 02:58:47

### Output:
```
* Function Blocks *
ANALOG_IN CT-501
ANALOG_IN LT-501
ANALOG_IN PT-502
ANALOG_IN PG-501
ANALOG_IN SEL-501
PID_BASIC FC-502
PID_BASIC SELC-501
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC PGA-501
MOTOR_ON_OFF M-501

* Variables *
REAL SELC_501_MV_Percent
REAL FC_502_MV_Percent

* Functions *
OR PG_Alarms_OR
NOT PG_OK_NOT
AND SELC_Permissive_AND
NOT SELC_Inhibit_NOT
NOT Level_OK_NOT
OR Pressure_OOR_OR
NOT Press_OK_NOT
AND FC_Permissive_AND
NOT FC_Inhibit_NOT
OR FC_FinalInhibit_OR

* Data Connections *
CT-501.PV, FC-502.PV
FC-502.XOUT, FV-502.Control_Signal
SEL-501.PV, SELC-501.PV
SELC-501.XOUT, PGA-501.Control_Signal
PG-501.High_Alarm, PG_Alarms_OR.IN1
PG-501.Low_Alarm, PG_Alarms_OR.IN2
PG_Alarms_OR.OUT, PG_OK_NOT.IN
M-501.FB_Running, SELC_Permissive_AND.IN1
PG_OK_NOT.OUT, SELC_Permissive_AND.IN2
SELC_Permissive_AND.OUT, SELC_Inhibit_NOT.IN
SELC_Inhibit_NOT.OUT, SELC-501.Inhibit
SELC_Inhibit_NOT.OUT, PGA-501.Inhibit
PG_Alarms_OR.OUT, M-501.Inhibit
LT-501.Low_Alarm, Level_OK_NOT.IN
PT-502.High_Alarm, Pressure_OOR_OR.IN1
PT-502.Low_Alarm, Pressure_OOR_OR.IN2
Pressure_OOR_OR.OUT, Press_OK_NOT.IN
Level_OK_NOT.OUT, FC_Permissive_AND.IN1
Press_OK_NOT.OUT, FC_Permissive_AND.IN2
FC_Permissive_AND.OUT, FC_Inhibit_NOT.IN
FC_Inhibit_NOT.OUT, FC_FinalInhibit_OR.IN1
CT-501.General_Fault, FC_FinalInhibit_OR.IN2
FC_FinalInhibit_OR.OUT, FC-502.Inhibit
FC_FinalInhibit_OR.OUT, FV-502.Inhibit
SELC-501.XOUT, SELC_501_MV_Percent
FC-502.XOUT, FC_502_MV_Percent

* Parameter Data Connections *
0.1875, CT-501.Scaling_Slope
1.25, CT-501.Scaling_Offset
TRUE, CT-501.Alarm_Enable
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
TRUE, PT-502.Alarm_Enable
600.0, PT-502.PV_High
300.0, PT-502.PV_Low
TRUE, PG-501.Alarm_Enable
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
0.0625, SEL-501.Scaling_Slope
-0.05, SEL-501.Scaling_Offset
TRUE, SEL-501.Alarm_Enable
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
TRUE, LT-501.Alarm_Enable
100.0, LT-501.PV_High
20.0, LT-501.PV_Low
TRUE, FC-502.AUTO
3.0, FC-502.SP
0.0, FC-502.MV_MIN
100.0, FC-502.MV_MAX
2.2, FC-502.KP
0.7, FC-502.TR
0.0, FC-502.TD
4.0, FC-502.PV_High
2.0, FC-502.PV_Low
TRUE, SELC-501.AUTO
0.7, SELC-501.SP
0.0, SELC-501.MV_MIN
100.0, SELC-501.MV_MAX
1.8, SELC-501.KP
0.5, SELC-501.TR
0.1, SELC-501.TD
1.1, SELC-501.PV_High
0.3, SELC-501.PV_Low
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
100.0, PGA-501.Open_Limit
0.0, PGA-501.Close_Limit
```

---

## Step 10: append_two_inputs
**Time:** 02:59:05

### Output:
```
* Function Blocks *
ANALOG_IN CT-501
ANALOG_IN LT-501
ANALOG_IN PT-502
ANALOG_IN PG-501
ANALOG_IN SEL-501
PID_BASIC FC-502
PID_BASIC SELC-501
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC PGA-501
MOTOR_ON_OFF M-501

* Variables *
REAL SELC_501_MV_Percent
REAL FC_502_MV_Percent

* Functions *
OR PG_Alarms_OR
OR Pressure_OOR_OR
OR FC_FinalInhibit_OR
NOT M_Run_NOT
OR FC_Inhibit_OR1
OR SELC_FinalInhibit_OR

* Data Connections *
CT-501.PV, FC-502.PV
FC-502.XOUT, FV-502.Control_Signal
SEL-501.PV, SELC-501.PV
SELC-501.XOUT, PGA-501.Control_Signal
PG-501.High_Alarm, PG_Alarms_OR.IN1
PG-501.Low_Alarm, PG_Alarms_OR.IN2
M-501.FB_Running, M_Run_NOT.IN
M_Run_NOT.OUT, SELC_FinalInhibit_OR.IN1
PG_Alarms_OR.OUT, SELC_FinalInhibit_OR.IN2
SELC_FinalInhibit_OR.OUT, SELC-501.Inhibit
SELC_FinalInhibit_OR.OUT, PGA-501.Inhibit
PG_Alarms_OR.OUT, M-501.Inhibit
PT-502.High_Alarm, Pressure_OOR_OR.IN1
PT-502.Low_Alarm, Pressure_OOR_OR.IN2
LT-501.Low_Alarm, FC_Inhibit_OR1.IN1
Pressure_OOR_OR.OUT, FC_Inhibit_OR1.IN2
FC_Inhibit_OR1.OUT, FC_FinalInhibit_OR.IN1
CT-501.General_Fault, FC_FinalInhibit_OR.IN2
FC_FinalInhibit_OR.OUT, FC-502.Inhibit
FC_FinalInhibit_OR.OUT, FV-502.Inhibit
SELC-501.XOUT, SELC_501_MV_Percent
FC-502.XOUT, FC_502_MV_Percent

* Parameter Data Connections *
0.1875, CT-501.Scaling_Slope
1.25, CT-501.Scaling_Offset
TRUE, CT-501.Alarm_Enable
4.0, CT-501.PV_High
2.0, CT-501.PV_Low
TRUE, PT-502.Alarm_Enable
600.0, PT-502.PV_High
300.0, PT-502.PV_Low
TRUE, PG-501.Alarm_Enable
5.0, PG-501.PV_High
0.5, PG-501.PV_Low
0.0625, SEL-501.Scaling_Slope
-0.05, SEL-501.Scaling_Offset
TRUE, SEL-501.Alarm_Enable
1.1, SEL-501.PV_High
0.3, SEL-501.PV_Low
TRUE, LT-501.Alarm_Enable
100.0, LT-501.PV_High
20.0, LT-501.PV_Low
TRUE, FC-502.AUTO
3.0, FC-502.SP
0.0, FC-502.MV_MIN
100.0, FC-502.MV_MAX
2.2, FC-502.KP
0.7, FC-502.TR
0.0, FC-502.TD
4.0, FC-502.PV_High
2.0, FC-502.PV_Low
TRUE, SELC-501.AUTO
0.7, SELC-501.SP
0.0, SELC-501.MV_MIN
100.0, SELC-501.MV_MAX
1.8, SELC-501.KP
0.5, SELC-501.TR
0.1, SELC-501.TD
1.1, SELC-501.PV_High
0.3, SELC-501.PV_Low
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
100.0, PGA-501.Open_Limit
0.0, PGA-501.Close_Limit
```

---


