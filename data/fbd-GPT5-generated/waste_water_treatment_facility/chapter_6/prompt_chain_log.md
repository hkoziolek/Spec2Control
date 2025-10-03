# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 10:39:04

## Step 1: contextgen1-sensors
**Time:** 10:39:04

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
**Time:** 10:39:34

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
**Time:** 10:40:13

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|------------------|-------------|
| Ratio Control | 0.98 |
| PID Control | 0.95 |

Selected Control Strategy: Ratio Control 
Short explanation: The narrative specifies FFIC-102 computing an airflow setpoint as Influent Flow × 2.0 with clamping and bias, sending the slave setpoint to FIC-103, which modulates FV-102—this matches the Ratio Control strategy with a slave PID.

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
**Timestamp:** 2025-09-24 10:40:57

## Step 1: openplc-function-blocks-v2
**Time:** 10:40:57

### Output:
```
* Function Blocks *
MOTOR_ON_OFF B-501A
MOTOR_ON_OFF B-501B
RATIO_CONTROL FFIC-102
PID_BASIC FIC-101
PID_BASIC FIC-103
VALVE_ELECTRIC FV-102
MOTOR_ON_OFF MX-501
ANALOG_IN PT-501
VALVE_ON_OFF XV-105
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 10:41:21

### Output:
```
* Function Blocks *
MOTOR_ON_OFF B-501A
MOTOR_ON_OFF B-501B
RATIO_CONTROL FFIC-102
PID_BASIC FIC-101
PID_BASIC FIC-103
VALVE_ELECTRIC FV-102
MOTOR_ON_OFF MX-501
ANALOG_IN PT-501
VALVE_ON_OFF XV-105
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 10:42:04

### Output:
```
* Functions *

* Block-to-Block Connections *
FFIC-102.SlaveSP, FIC-103.SP
FIC-103.XOUT, FV-102.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 10:42:37

### Output:
```
* Functions * 
BlowersRunning_OR
NotBlowersRunning_NOT
MixerNotRunning_NOT
RatioInhibit_OR
XV105NotOpen_NOT
ValveInhibit_OR

* Data Connections *
BlowersRunning_OR.IN1, B-501A.FB_Running
BlowersRunning_OR.IN2, B-501B.FB_Running
NotBlowersRunning_NOT.IN, BlowersRunning_OR.OUT
MixerNotRunning_NOT.IN, MX-501.FB_Running
RatioInhibit_OR.IN1, NotBlowersRunning_NOT.OUT
RatioInhibit_OR.IN2, PT-501.Low_Alarm
RatioInhibit_OR.IN3, MixerNotRunning_NOT.OUT
RatioInhibit_OR.IN4, FIC-101.PV_Low_Alarm
RatioInhibit_OR.IN5, B-501A.FB_Trip
RatioInhibit_OR.IN6, B-501B.FB_Trip
RatioInhibit_OR.IN7, PT-501.General_Fault
RatioInhibit_OR.OUT, FFIC-102.Inhibit
XV105NotOpen_NOT.IN, XV-105.FB_Opened
ValveInhibit_OR.IN1, XV105NotOpen_NOT.OUT
ValveInhibit_OR.IN2, FIC-101.PV_Low_Alarm
ValveInhibit_OR.OUT, FV-102.Inhibit

* Parameter Data Connections *
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
100, FIC-101.PV_Low
5000, FIC-101.PV_High
10, FIC-103.Deviation_Limit
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 10:44:11

### Output:
```
* Parameter Data Connections *
TRUE, FFIC-102.Auto
2.0, FFIC-102.RatioSP
0.0, FFIC-102.Bias
0.0, FFIC-102.MV_MIN
12500.0, FFIC-102.MV_MAX
TRUE, FIC-103.AUTO
10.0, FIC-103.Deviation_Limit
5000.0, FIC-101.PV_High
100.0, FIC-101.PV_Low
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 10:46:04

### Output:
```
* Parameter Data Connections *
TRUE, FFIC-102.Auto
2.0, FFIC-102.RatioSP
0.0, FFIC-102.Bias
0.0, FFIC-102.MV_MIN
12500.0, FFIC-102.MV_MAX
TRUE, FIC-103.AUTO
0.0, FIC-103.MV_MIN
100.0, FIC-103.MV_MAX
10.0, FIC-103.Deviation_Limit
5000.0, FIC-101.PV_High
100.0, FIC-101.PV_Low
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
0.0, FV-102.Close_Limit
100.0, FV-102.Open_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 10:47:07

### Output:
```
* Variables *
REAL FFIC-102_AirflowSP_for_FIC-103
REAL PT-501_AirHeaderPressure_PV
BOOL B-501A_Running_FB
BOOL B-501B_Running_FB
BOOL MX-501_Running_FB
BOOL XV-105_Open_FB

* Data Connections *
FFIC-102.SlaveSP, FFIC-102_AirflowSP_for_FIC-103
PT-501.PV, PT-501_AirHeaderPressure_PV
B-501A.FB_Running, B-501A_Running_FB
B-501B.FB_Running, B-501B_Running_FB
MX-501.FB_Running, MX-501_Running_FB
XV-105.FB_Opened, XV-105_Open_FB
```

---

## Step 8: openplc-rule-checks
**Time:** 10:48:09

### Output:
```
* Function Blocks *
MOTOR_ON_OFF B-501A
MOTOR_ON_OFF B-501B
RATIO_CONTROL FFIC-102
PID_BASIC FIC-101
PID_BASIC FIC-103
VALVE_ELECTRIC FV-102
MOTOR_ON_OFF MX-501
ANALOG_IN PT-501
VALVE_ON_OFF XV-105

* Variables *
REAL FFIC-102_AirflowSP_for_FIC-103
REAL PT-501_AirHeaderPressure_PV
BOOL B-501A_Running_FB
BOOL B-501B_Running_FB
BOOL MX-501_Running_FB
BOOL XV-105_Open_FB
BOOL AirflowDeviationAlarm
BOOL LowFlowAlarm

* Functions *
OR BlowersRunning_OR
NOT NotBlowersRunning_NOT
NOT MixerNotRunning_NOT
OR RatioInhibit_OR
NOT XV105NotOpen_NOT
OR ValveInhibit_OR
TON AirflowDevAlarmDelay_TON
TON LowFlowAlarmDelay_TON

* Data Connections *
FIC-101.PV, FFIC-102.PrimaryPV
FIC-103.PV, FFIC-102.SecondaryPV
FFIC-102.SlaveSP, FIC-103.SP
FIC-103.XOUT, FV-102.Control_Signal
BlowersRunning_OR.IN1, B-501A.FB_Running
BlowersRunning_OR.IN2, B-501B.FB_Running
NotBlowersRunning_NOT.IN, BlowersRunning_OR.OUT
MixerNotRunning_NOT.IN, MX-501.FB_Running
RatioInhibit_OR.IN1, NotBlowersRunning_NOT.OUT
RatioInhibit_OR.IN2, PT-501.Low_Alarm
RatioInhibit_OR.IN3, MixerNotRunning_NOT.OUT
RatioInhibit_OR.IN4, FIC-101.PV_Low_Alarm
RatioInhibit_OR.IN5, B-501A.FB_Trip
RatioInhibit_OR.IN6, B-501B.FB_Trip
RatioInhibit_OR.IN7, PT-501.General_Fault
RatioInhibit_OR.OUT, FFIC-102.Inhibit
XV105NotOpen_NOT.IN, XV-105.FB_Opened
ValveInhibit_OR.IN1, XV105NotOpen_NOT.OUT
ValveInhibit_OR.IN2, FIC-101.PV_Low_Alarm
ValveInhibit_OR.OUT, FV-102.Inhibit
FIC-103.Deviation_Alarm, AirflowDevAlarmDelay_TON.IN
AirflowDevAlarmDelay_TON.Q, AirflowDeviationAlarm
FIC-101.PV_Low_Alarm, LowFlowAlarmDelay_TON.IN
LowFlowAlarmDelay_TON.Q, LowFlowAlarm
FFIC-102.SlaveSP, FFIC-102_AirflowSP_for_FIC-103
PT-501.PV, PT-501_AirHeaderPressure_PV
B-501A.FB_Running, B-501A_Running_FB
B-501B.FB_Running, B-501B_Running_FB
MX-501.FB_Running, MX-501_Running_FB
XV-105.FB_Opened, XV-105_Open_FB

* Parameter Data Connections *
TRUE, FFIC-102.Auto
2.0, FFIC-102.RatioSP
0.0, FFIC-102.Bias
0.0, FFIC-102.MV_MIN
12500.0, FFIC-102.MV_MAX
TRUE, FIC-103.AUTO
0.0, FIC-103.MV_MIN
100.0, FIC-103.MV_MAX
10.0, FIC-103.Deviation_Limit
5000.0, FIC-101.PV_High
100.0, FIC-101.PV_Low
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
0.0, FV-102.Close_Limit
100.0, FV-102.Open_Limit
T#30s, AirflowDevAlarmDelay_TON.PT
T#5m, LowFlowAlarmDelay_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 10:49:46

### Output:
```
* Function Blocks *
MOTOR_ON_OFF B-501A
MOTOR_ON_OFF B-501B
RATIO_CONTROL FFIC-102
PID_BASIC FIC-101
PID_BASIC FIC-103
VALVE_ELECTRIC FV-102
MOTOR_ON_OFF MX-501
ANALOG_IN PT-501
VALVE_ON_OFF XV-105

* Variables *
REAL FFIC-102_AirflowSP_for_FIC-103
REAL PT-501_AirHeaderPressure_PV
BOOL B-501A_Running_FB
BOOL B-501B_Running_FB
BOOL MX-501_Running_FB
BOOL XV-105_Open_FB
BOOL AirflowDeviationAlarm
BOOL LowFlowAlarm

* Functions *
OR BlowersRunning_OR
NOT NotBlowersRunning_NOT
NOT MixerNotRunning_NOT
OR RatioInhibit_OR
NOT XV105NotOpen_NOT
OR ValveInhibit_OR
TON AirflowDevAlarmDelay_TON
TON LowFlowAlarmDelay_TON

* Data Connections *
FIC-101.PV, FFIC-102.PrimaryPV
FIC-103.PV, FFIC-102.SecondaryPV
FFIC-102.SlaveSP, FIC-103.SP
FIC-103.XOUT, FV-102.Control_Signal
BlowersRunning_OR.IN1, B-501A.FB_Running
BlowersRunning_OR.IN2, B-501B.FB_Running
NotBlowersRunning_NOT.IN, BlowersRunning_OR.OUT
MixerNotRunning_NOT.IN, MX-501.FB_Running
RatioInhibit_OR.IN1, NotBlowersRunning_NOT.OUT
RatioInhibit_OR.IN2, PT-501.Low_Alarm
RatioInhibit_OR.IN3, MixerNotRunning_NOT.OUT
RatioInhibit_OR.IN4, FIC-101.PV_Low_Alarm
RatioInhibit_OR.IN5, B-501A.FB_Trip
RatioInhibit_OR.IN6, B-501B.FB_Trip
RatioInhibit_OR.IN7, PT-501.General_Fault
RatioInhibit_OR.OUT, FFIC-102.Inhibit
XV105NotOpen_NOT.IN, XV-105.FB_Opened
ValveInhibit_OR.IN1, XV105NotOpen_NOT.OUT
ValveInhibit_OR.IN2, FIC-101.PV_Low_Alarm
ValveInhibit_OR.OUT, FV-102.Inhibit
FIC-103.Deviation_Alarm, AirflowDevAlarmDelay_TON.IN
AirflowDevAlarmDelay_TON.Q, AirflowDeviationAlarm
FIC-101.PV_Low_Alarm, LowFlowAlarmDelay_TON.IN
LowFlowAlarmDelay_TON.Q, LowFlowAlarm
FFIC-102.SlaveSP, FFIC-102_AirflowSP_for_FIC-103
PT-501.PV, PT-501_AirHeaderPressure_PV
B-501A.FB_Running, B-501A_Running_FB
B-501B.FB_Running, B-501B_Running_FB
MX-501.FB_Running, MX-501_Running_FB
XV-105.FB_Opened, XV-105_Open_FB

* Parameter Data Connections *
TRUE, FFIC-102.Auto
2.0, FFIC-102.RatioSP
0.0, FFIC-102.Bias
0.0, FFIC-102.MV_MIN
12500.0, FFIC-102.MV_MAX
TRUE, FIC-103.AUTO
0.0, FIC-103.MV_MIN
100.0, FIC-103.MV_MAX
10.0, FIC-103.Deviation_Limit
5000.0, FIC-101.PV_High
100.0, FIC-101.PV_Low
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
0.0, FV-102.Close_Limit
100.0, FV-102.Open_Limit
T#30s, AirflowDevAlarmDelay_TON.PT
T#5m, LowFlowAlarmDelay_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 10:50:07

### Output:
```
* Function Blocks *
MOTOR_ON_OFF B-501A
MOTOR_ON_OFF B-501B
RATIO_CONTROL FFIC-102
PID_BASIC FIC-101
PID_BASIC FIC-103
VALVE_ELECTRIC FV-102
MOTOR_ON_OFF MX-501
ANALOG_IN PT-501
VALVE_ON_OFF XV-105

* Variables *
REAL FFIC-102_AirflowSP_for_FIC-103
REAL PT-501_AirHeaderPressure_PV
BOOL B-501A_Running_FB
BOOL B-501B_Running_FB
BOOL MX-501_Running_FB
BOOL XV-105_Open_FB
BOOL AirflowDeviationAlarm
BOOL LowFlowAlarm

* Functions *
OR BlowersRunning_OR
NOT NotBlowersRunning_NOT
NOT MixerNotRunning_NOT
OR RatioInhibit_OR
NOT XV105NotOpen_NOT
OR ValveInhibit_OR
TON AirflowDevAlarmDelay_TON
TON LowFlowAlarmDelay_TON

* Data Connections *
FIC-101.PV, FFIC-102.PrimaryPV
FIC-103.PV, FFIC-102.SecondaryPV
FFIC-102.SlaveSP, FIC-103.SP
FIC-103.XOUT, FV-102.Control_Signal
BlowersRunning_OR.IN1, B-501A.FB_Running
BlowersRunning_OR.IN2, B-501B.FB_Running
NotBlowersRunning_NOT.IN, BlowersRunning_OR.OUT
MixerNotRunning_NOT.IN, MX-501.FB_Running
RatioInhibit_OR.IN1, NotBlowersRunning_NOT.OUT
RatioInhibit_OR.IN2, PT-501.Low_Alarm
RatioInhibit_OR.IN3, MixerNotRunning_NOT.OUT
RatioInhibit_OR.IN4, FIC-101.PV_Low_Alarm
RatioInhibit_OR.IN5, B-501A.FB_Trip
RatioInhibit_OR.IN6, B-501B.FB_Trip
RatioInhibit_OR.IN7, PT-501.General_Fault
RatioInhibit_OR.OUT, FFIC-102.Inhibit
XV105NotOpen_NOT.IN, XV-105.FB_Opened
ValveInhibit_OR.IN1, XV105NotOpen_NOT.OUT
ValveInhibit_OR.IN2, FIC-101.PV_Low_Alarm
ValveInhibit_OR.OUT, FV-102.Inhibit
FIC-103.Deviation_Alarm, AirflowDevAlarmDelay_TON.IN
AirflowDevAlarmDelay_TON.Q, AirflowDeviationAlarm
FIC-101.PV_Low_Alarm, LowFlowAlarmDelay_TON.IN
LowFlowAlarmDelay_TON.Q, LowFlowAlarm
FFIC-102.SlaveSP, FFIC-102_AirflowSP_for_FIC-103
PT-501.PV, PT-501_AirHeaderPressure_PV
B-501A.FB_Running, B-501A_Running_FB
B-501B.FB_Running, B-501B_Running_FB
MX-501.FB_Running, MX-501_Running_FB
XV-105.FB_Opened, XV-105_Open_FB

* Parameter Data Connections *
TRUE, FFIC-102.Auto
2.0, FFIC-102.RatioSP
0.0, FFIC-102.Bias
0.0, FFIC-102.MV_MIN
12500.0, FFIC-102.MV_MAX
TRUE, FIC-103.AUTO
0.0, FIC-103.MV_MIN
100.0, FIC-103.MV_MAX
10.0, FIC-103.Deviation_Limit
5000.0, FIC-101.PV_High
100.0, FIC-101.PV_Low
3.0, PT-501.PV_Low
TRUE, PT-501.Alarm_Enable
0.0, FV-102.Close_Limit
100.0, FV-102.Open_Limit
T#30s, AirflowDevAlarmDelay_TON.PT
T#5m, LowFlowAlarmDelay_TON.PT
```

---


