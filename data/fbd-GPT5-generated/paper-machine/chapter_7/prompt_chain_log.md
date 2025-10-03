# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 03:00:16

## Step 1: contextgen1-sensors
**Time:** 03:00:16

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
**Time:** 03:00:39

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
**Time:** 03:00:57

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|------------------|-------------|
| Ratio Control | 0.98 |
| PID Control | 0.95 |
| OVERRIDE | 0.65 |

Selected Control Strategy: Ratio Control
Short explanation: The narrative centers on maintaining a defined dilution water-to-slurry consistency ratio, with the ratio controller generating the slave setpoint for a downstream flow PID, matching the Ratio Control strategy.

** Description ** 
The system includes two flow transmitters, a ratio controller, (optionally) a slave PID controller, and a control valve. Each flow transmitter provides an analog input to the ratio controller. The ratio controller maintains a predefined ratio between the two flows by sending a slave setpoint to the PID Controller. Multiplications are handled inside the controller and need no additional logic. If no slave PID controller is specified, the ratio controller directly drives the control valve and sends the slave setpoint to it.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.PV, RATIO_CONTROL.PrimaryPV
ANALOG_IN2.PV, RATIO_CONTROL.SecondaryPV
<specified ratio>, RATIO_CONTROL.RatioSP
RATIO_CONTROL.SlaveSP, PID_BASIC.SP
PID_BASIC.XOUT, VALVE_ELECTRIC.Control_Signal

*** Available Function Block Types ***
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
**Timestamp:** 2025-09-24 03:01:35

## Step 1: openplc-function-blocks-v2
**Time:** 03:01:35

### Output:
```
* Function Blocks *
ANALOG_IN CT-601
ANALOG_IN FT-601
ANALOG_IN PIT-601
ANALOG_IN VT-601
PID_BASIC FIC-601
RATIO_CONTROL FFIC-601
VALVE_ELECTRIC FV-601
MOTOR_ON_OFF P-601
BOOL_IN FS-601
DIGITAL_IN ALM-601
DIGITAL_IN ALM-602
DIGITAL_IN ALM-603
DIGITAL_IN ALM-604
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 03:02:24

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN CT-601
ANALOG_IN FT-601
ANALOG_IN PIT-601
ANALOG_IN VT-601
PID_BASIC FIC-601
RATIO_CONTROL FFIC-601
VALVE_ELECTRIC FV-601
MOTOR_ON_OFF P-601
BOOL_IN FS-601
BOOL_IN P-601-RUN
BOOL_IN PIT-601-OK
BOOL_IN VT-601-OK
DIGITAL_IN ALM-601
DIGITAL_IN ALM-602
DIGITAL_IN ALM-603
DIGITAL_IN ALM-604
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 03:03:16

### Output:
```
* Functions *

* Block-to-Block Connections *
CT-601.PV, FFIC-601.PrimaryPV
FT-601.PV, FFIC-601.SecondaryPV
FFIC-601.SlaveSP, FIC-601.SP
FT-601.PV, FIC-601.PV
FIC-601.XOUT, FV-601.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 03:03:52

### Output:
```
* Functions * 
AND RatioPermissive_AND
NOT PIT601_OK_NOT
NOT VT601_OK_NOT
NOT RatioPermissive_NOT
OR RatioInhibit_OR
OR FICInhibit_OR
OR ValveInhibit_OR
OR FlowRangeAlarm_OR

* Data Connections *
PIT-601.Low_Alarm, PIT601_OK_NOT.IN
PIT601_OK_NOT.OUT, PIT-601-OK.Bool_In
VT-601.Low_Alarm, VT601_OK_NOT.IN
VT601_OK_NOT.OUT, VT-601-OK.Bool_In
P-601-RUN.Bool_Out, RatioPermissive_AND.IN1
FS-601.Bool_Out, RatioPermissive_AND.IN2
PIT-601-OK.Bool_Out, RatioPermissive_AND.IN3
VT-601-OK.Bool_Out, RatioPermissive_AND.IN4
RatioPermissive_AND.OUT, RatioPermissive_NOT.IN
RatioPermissive_NOT.OUT, RatioInhibit_OR.IN1
ALM-602.DI_Out, RatioInhibit_OR.IN2
RatioInhibit_OR.OUT, FFIC-601.Inhibit
RatioPermissive_NOT.OUT, FICInhibit_OR.IN1
ALM-603.DI_Out, FICInhibit_OR.IN2
FICInhibit_OR.OUT, FIC-601.Inhibit
RatioPermissive_NOT.OUT, ValveInhibit_OR.IN1
ALM-603.DI_Out, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-601.Inhibit
FIC-601.PV_High_Alarm, FlowRangeAlarm_OR.IN1
FIC-601.PV_Low_Alarm, FlowRangeAlarm_OR.IN2
FlowRangeAlarm_OR.OUT, ALM-601.DI_Raw
CT-601.General_Fault, ALM-602.DI_Raw
FT-601.General_Fault, ALM-603.DI_Raw
FIC-601.Deviation_Alarm, ALM-604.DI_Raw

* Parameter Data Connections *
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
0, FT-601.PV_Low
500, FT-601.PV_High
300, PIT-601.PV_Low
30, VT-601.PV_Low
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
T#10s, ALM-604.DebounceTime
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 03:06:10

### Output:
```
* Parameter Data Connections *
2.5, FFIC-601.RatioSP
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
T#2s, FFIC-601.TrimTi
TRUE, CT-601.Alarm_Enable
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
TRUE, FT-601.Alarm_Enable
0, FT-601.PV_Low
500, FT-601.PV_High
TRUE, PIT-601.Alarm_Enable
300, PIT-601.PV_Low
TRUE, VT-601.Alarm_Enable
30, VT-601.PV_Low
20, FV-601.Manual_Position
20, FIC-601.X0
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 03:07:18

### Output:
```
* Parameter Data Connections *
2.5, FFIC-601.RatioSP
T#2s, FFIC-601.TrimTi
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
TRUE, CT-601.Alarm_Enable
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
TRUE, FT-601.Alarm_Enable
0, FT-601.PV_Low
500, FT-601.PV_High
TRUE, PIT-601.Alarm_Enable
300, PIT-601.PV_Low
TRUE, VT-601.Alarm_Enable
30, VT-601.PV_Low
10, FIC-601.PV_Low
500, FIC-601.PV_High
20, FV-601.Manual_Position
20, FIC-601.X0
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 03:08:16

### Output:
```
* Variables *
REAL FT601_Flow_SP

* Data Connections *
FFIC-601.SlaveSP, FT601_Flow_SP
```

---

## Step 8: openplc-rule-checks
**Time:** 03:09:01

### Output:
```
* Function Blocks *
ANALOG_IN CT-601
ANALOG_IN FT-601
ANALOG_IN PIT-601
ANALOG_IN VT-601
PID_BASIC FIC-601
RATIO_CONTROL FFIC-601
VALVE_ELECTRIC FV-601
MOTOR_ON_OFF P-601
BOOL_IN FS-601
BOOL_IN P-601-RUN
BOOL_IN PIT-601-OK
BOOL_IN VT-601-OK
DIGITAL_IN ALM-601
DIGITAL_IN ALM-602
DIGITAL_IN ALM-603
DIGITAL_IN ALM-604

* Variables *
REAL FT601_Flow_SP
REAL Ratio_Bias

* Functions *
AND RatioPermissive_AND
NOT PIT601_OK_NOT
NOT VT601_OK_NOT
NOT RatioPermissive_NOT
OR RatioInhibit_OR
OR FICInhibit_OR
OR ValveInhibit_OR
OR FlowRangeAlarm_OR
NOT RatioAuto_NOT

* Data Connections * 
CT-601.PV, FFIC-601.PrimaryPV
FT-601.PV, FFIC-601.SecondaryPV
FFIC-601.SlaveSP, FIC-601.SP
FT-601.PV, FIC-601.PV
FIC-601.XOUT, FV-601.Control_Signal
PIT-601.Low_Alarm, PIT601_OK_NOT.IN
PIT601_OK_NOT.OUT, PIT-601-OK.Bool_In
VT-601.Low_Alarm, VT601_OK_NOT.IN
VT601_OK_NOT.OUT, VT-601-OK.Bool_In
P-601.FB_Running, P-601-RUN.Bool_In
P-601-RUN.Bool_Out, RatioPermissive_AND.IN1
FS-601.Bool_Out, RatioPermissive_AND.IN2
PIT-601-OK.Bool_Out, RatioPermissive_AND.IN3
VT-601-OK.Bool_Out, RatioPermissive_AND.IN4
RatioPermissive_AND.OUT, RatioPermissive_NOT.IN
RatioPermissive_NOT.OUT, RatioInhibit_OR.IN1
ALM-602.DI_Out, RatioInhibit_OR.IN2
RatioInhibit_OR.OUT, FFIC-601.Inhibit
RatioInhibit_OR.OUT, FV-601.Manual_Mode
RatioInhibit_OR.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-601.Auto
RatioAuto_NOT.OUT, FIC-601.AUTO
RatioPermissive_NOT.OUT, FICInhibit_OR.IN1
ALM-603.DI_Out, FICInhibit_OR.IN2
FICInhibit_OR.OUT, FIC-601.Inhibit
RatioPermissive_NOT.OUT, ValveInhibit_OR.IN1
ALM-603.DI_Out, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-601.Inhibit
FIC-601.PV_High_Alarm, FlowRangeAlarm_OR.IN1
FIC-601.PV_Low_Alarm, FlowRangeAlarm_OR.IN2
FlowRangeAlarm_OR.OUT, ALM-601.DI_Raw
CT-601.General_Fault, ALM-602.DI_Raw
FT-601.General_Fault, ALM-603.DI_Raw
FIC-601.Deviation_Alarm, ALM-604.DI_Raw
FFIC-601.SlaveSP, FT601_Flow_SP
Ratio_Bias, FFIC-601.Bias

* Parameter Data Connections *
2.5, FFIC-601.RatioSP
T#2s, FFIC-601.TrimTi
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
TRUE, CT-601.Alarm_Enable
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
TRUE, FT-601.Alarm_Enable
0, FT-601.PV_Low
500, FT-601.PV_High
TRUE, PIT-601.Alarm_Enable
300, PIT-601.PV_Low
TRUE, VT-601.Alarm_Enable
30, VT-601.PV_Low
10, FIC-601.PV_Low
500, FIC-601.PV_High
20, FV-601.Manual_Position
20, FIC-601.X0
```

---

## Step 9: openplc-rule-checks2
**Time:** 03:10:41

### Output:
```
* Function Blocks *
ANALOG_IN CT-601
ANALOG_IN FT-601
ANALOG_IN PIT-601
ANALOG_IN VT-601
PID_BASIC FIC-601
RATIO_CONTROL FFIC-601
VALVE_ELECTRIC FV-601
MOTOR_ON_OFF P-601
BOOL_IN FS-601
BOOL_IN P-601-RUN
BOOL_IN PIT-601-OK
BOOL_IN VT-601-OK
DIGITAL_IN ALM-601
DIGITAL_IN ALM-602
DIGITAL_IN ALM-603
DIGITAL_IN ALM-604

* Variables *
REAL FT601_Flow_SP
REAL Ratio_Bias

* Functions *
AND RatioPermissive_AND
NOT PIT601_OK_NOT
NOT VT601_OK_NOT
NOT RatioPermissive_NOT
OR RatioInhibit_OR
OR FICInhibit_OR
OR ValveInhibit_OR
OR FlowRangeAlarm_OR
NOT RatioAuto_NOT

* Data Connections * 
CT-601.PV, FFIC-601.PrimaryPV
FT-601.PV, FFIC-601.SecondaryPV
FFIC-601.SlaveSP, FIC-601.SP
FT-601.PV, FIC-601.PV
FIC-601.XOUT, FV-601.Control_Signal
PIT-601.Low_Alarm, PIT601_OK_NOT.IN
PIT601_OK_NOT.OUT, PIT-601-OK.Bool_In
VT-601.Low_Alarm, VT601_OK_NOT.IN
VT601_OK_NOT.OUT, VT-601-OK.Bool_In
P-601.FB_Running, P-601-RUN.Bool_In
P-601-RUN.Bool_Out, RatioPermissive_AND.IN1
FS-601.Bool_Out, RatioPermissive_AND.IN2
PIT-601-OK.Bool_Out, RatioPermissive_AND.IN3
VT-601-OK.Bool_Out, RatioPermissive_AND.IN4
RatioPermissive_AND.OUT, RatioPermissive_NOT.IN
RatioPermissive_NOT.OUT, RatioInhibit_OR.IN1
ALM-602.DI_Out, RatioInhibit_OR.IN2
RatioInhibit_OR.OUT, FFIC-601.Inhibit
RatioInhibit_OR.OUT, FV-601.Manual_Mode
RatioInhibit_OR.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-601.Auto
RatioAuto_NOT.OUT, FIC-601.AUTO
RatioPermissive_NOT.OUT, FICInhibit_OR.IN1
ALM-603.DI_Out, FICInhibit_OR.IN2
FICInhibit_OR.OUT, FIC-601.Inhibit
RatioPermissive_NOT.OUT, ValveInhibit_OR.IN1
ALM-603.DI_Out, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-601.Inhibit
FIC-601.PV_High_Alarm, FlowRangeAlarm_OR.IN1
FIC-601.PV_Low_Alarm, FlowRangeAlarm_OR.IN2
FlowRangeAlarm_OR.OUT, ALM-601.DI_Raw
CT-601.General_Fault, ALM-602.DI_Raw
FT-601.General_Fault, ALM-603.DI_Raw
FIC-601.Deviation_Alarm, ALM-604.DI_Raw
FFIC-601.SlaveSP, FT601_Flow_SP
Ratio_Bias, FFIC-601.Bias

* Parameter Data Connections *
2.5, FFIC-601.RatioSP
T#2s, FFIC-601.TrimTi
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
TRUE, CT-601.Alarm_Enable
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
TRUE, FT-601.Alarm_Enable
0, FT-601.PV_Low
500, FT-601.PV_High
TRUE, PIT-601.Alarm_Enable
300, PIT-601.PV_Low
TRUE, VT-601.Alarm_Enable
30, VT-601.PV_Low
10, FIC-601.PV_Low
500, FIC-601.PV_High
20, FV-601.Manual_Position
20, FIC-601.X0
```

---

## Step 10: append_two_inputs
**Time:** 03:11:01

### Output:
```
* Function Blocks *
ANALOG_IN CT-601
ANALOG_IN FT-601
ANALOG_IN PIT-601
ANALOG_IN VT-601
PID_BASIC FIC-601
RATIO_CONTROL FFIC-601
VALVE_ELECTRIC FV-601
MOTOR_ON_OFF P-601
BOOL_IN FS-601
BOOL_IN P-601-RUN
BOOL_IN PIT-601-OK
BOOL_IN VT-601-OK
DIGITAL_IN ALM-601
DIGITAL_IN ALM-602
DIGITAL_IN ALM-603
DIGITAL_IN ALM-604

* Variables *
REAL FT601_Flow_SP
REAL Ratio_Bias

* Functions *
AND RatioPermissive_AND
NOT PIT601_OK_NOT
NOT VT601_OK_NOT
NOT RatioPermissive_NOT
OR RatioInhibit_OR
OR FICInhibit_OR
OR FlowRangeAlarm_OR
NOT RatioAuto_NOT

* Data Connections * 
CT-601.PV, FFIC-601.PrimaryPV
FT-601.PV, FFIC-601.SecondaryPV
FFIC-601.SlaveSP, FIC-601.SP
FT-601.PV, FIC-601.PV
FIC-601.XOUT, FV-601.Control_Signal
PIT-601.Low_Alarm, PIT601_OK_NOT.IN
PIT601_OK_NOT.OUT, PIT-601-OK.Bool_In
VT-601.Low_Alarm, VT601_OK_NOT.IN
VT601_OK_NOT.OUT, VT-601-OK.Bool_In
P-601.FB_Running, P-601-RUN.Bool_In
P-601-RUN.Bool_Out, RatioPermissive_AND.IN1
FS-601.Bool_Out, RatioPermissive_AND.IN2
PIT-601-OK.Bool_Out, RatioPermissive_AND.IN3
VT-601-OK.Bool_Out, RatioPermissive_AND.IN4
RatioPermissive_AND.OUT, RatioPermissive_NOT.IN
RatioPermissive_NOT.OUT, RatioInhibit_OR.IN1
ALM-602.DI_Out, RatioInhibit_OR.IN2
RatioInhibit_OR.OUT, FFIC-601.Inhibit
RatioInhibit_OR.OUT, FV-601.Manual_Mode
RatioInhibit_OR.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-601.Auto
RatioAuto_NOT.OUT, FIC-601.AUTO
RatioPermissive_NOT.OUT, FICInhibit_OR.IN1
ALM-603.DI_Out, FICInhibit_OR.IN2
FICInhibit_OR.OUT, FIC-601.Inhibit
FICInhibit_OR.OUT, FV-601.Inhibit
FIC-601.PV_High_Alarm, FlowRangeAlarm_OR.IN1
FIC-601.PV_Low_Alarm, FlowRangeAlarm_OR.IN2
FlowRangeAlarm_OR.OUT, ALM-601.DI_Raw
CT-601.General_Fault, ALM-602.DI_Raw
FT-601.General_Fault, ALM-603.DI_Raw
FIC-601.Deviation_Alarm, ALM-604.DI_Raw
FFIC-601.SlaveSP, FT601_Flow_SP
Ratio_Bias, FFIC-601.Bias

* Parameter Data Connections *
2.5, FFIC-601.RatioSP
T#2s, FFIC-601.TrimTi
10, FFIC-601.MV_MIN
500, FFIC-601.MV_MAX
TRUE, CT-601.Alarm_Enable
0.5, CT-601.PV_Low
3.0, CT-601.PV_High
TRUE, FT-601.Alarm_Enable
0, FT-601.PV_Low
500, FT-601.PV_High
TRUE, PIT-601.Alarm_Enable
300, PIT-601.PV_Low
TRUE, VT-601.Alarm_Enable
30, VT-601.PV_Low
10, FIC-601.PV_Low
500, FIC-601.PV_High
20, FV-601.Manual_Position
20, FIC-601.X0
```

---


