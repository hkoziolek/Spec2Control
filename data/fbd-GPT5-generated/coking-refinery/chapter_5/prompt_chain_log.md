# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-23 22:01:25

## Step 1: contextgen1-sensors
**Time:** 22:01:25

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
**Time:** 22:02:12

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
```

---

## Step 3: contextgen1-strategies
**Time:** 22:02:34

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|---|---|
| PID Control | 0.98 |
| OVERRIDE | 0.72 |
| Duty-Standby | 0.35 |

Selected Control Strategy: PID Control 
Short explanation: The core requirement is a single-loop temperature control (TC-401) using TIT-101 to modulate FV-401, which is directly implemented by a standard PID control strategy.

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
**Timestamp:** 2025-09-23 22:03:51

## Step 1: openplc-function-blocks-v2
**Time:** 22:03:51

### Output:
```
* Function Blocks *
ANALOG_IN FT-401A
VALVE_ELECTRIC FV-401
MOTOR_ON_OFF P-401A
MOTOR_ON_OFF P-401B
PID_BASIC PC-401
ANALOG_IN PT-402
ANALOG_IN PT-403
PID_BASIC TC-401
ANALOG_IN TIT-101
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 22:04:22

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN FT-401A
DIGITAL_IN FT-401B
VALVE_ELECTRIC FV-401
MOTOR_ON_OFF P-401A
MOTOR_ON_OFF P-401B
PID_BASIC PC-401
ANALOG_IN PT-402
ANALOG_IN PT-403
PID_BASIC TC-401
ANALOG_IN TIT-101
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 22:05:13

### Output:
```
* Functions *

* Block-to-Block Connections *
TIT-101.PV, TC-401.PV
TC-401.XOUT, FV-401.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 22:06:02

### Output:
```
* Functions * 
FuelGasPressOutOfRange_OR
FuelGasPressOK_NOT
DraftOutOfRange_OR
DraftOK_NOT
PumpsRunning_OR
FlowPermissive_AND
ProcessPermissive_AND
Permissive1_AND
FinalPermissive_AND
BaseInhibit_NOT
InhibitWithHighTrip_OR
FinalInhibit_OR

* Data Connections *
PC-401.PV_High_Alarm, FuelGasPressOutOfRange_OR.IN1
PC-401.PV_Low_Alarm, FuelGasPressOutOfRange_OR.IN2
FuelGasPressOutOfRange_OR.OUT, FuelGasPressOK_NOT.IN
PT-402.High_Alarm, DraftOutOfRange_OR.IN1
PT-402.Low_Alarm, DraftOutOfRange_OR.IN2
DraftOutOfRange_OR.OUT, DraftOK_NOT.IN
P-401A.FB_Running, PumpsRunning_OR.IN1
P-401B.FB_Running, PumpsRunning_OR.IN2
PumpsRunning_OR.OUT, FlowPermissive_AND.IN1
PT-403.High_Alarm, FlowPermissive_AND.IN2
FuelGasPressOK_NOT.OUT, ProcessPermissive_AND.IN1
DraftOK_NOT.OUT, ProcessPermissive_AND.IN2
ProcessPermissive_AND.OUT, Permissive1_AND.IN1
FlowPermissive_AND.OUT, Permissive1_AND.IN2
Permissive1_AND.OUT, FinalPermissive_AND.IN1
FT-401B.DI_Out, FinalPermissive_AND.IN2
FinalPermissive_AND.OUT, BaseInhibit_NOT.IN
BaseInhibit_NOT.OUT, InhibitWithHighTrip_OR.IN1
TIT-101.High_Alarm, InhibitWithHighTrip_OR.IN2
InhibitWithHighTrip_OR.OUT, FinalInhibit_OR.IN1
TIT-101.General_Fault, FinalInhibit_OR.IN2
FinalInhibit_OR.OUT, FV-401.Inhibit
FinalInhibit_OR.OUT, TC-401.Inhibit

* Parameter Data Connections *
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
8.0, PT-403.PV_High
550, TIT-101.PV_High
510, TC-401.PV_High
480, TC-401.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 22:10:01

### Output:
```
* Parameter Data Connections *
495.0, TC-401.SP
0.0, TC-401.MV_MIN
100.0, TC-401.MV_MAX
3.2, TC-401.KP
0.9, TC-401.TR
0.3, TC-401.TD
2.0, TC-401.Deviation_Limit
510.0, TIT-101.PV_High
480.0, TIT-101.PV_Low
TRUE, TIT-101.Alarm_Enable
9.375, TIT-101.Scaling_Slope
362.5, TIT-101.Scaling_Offset
100.0, FV-401.Open_Limit
0.0, FV-401.Close_Limit
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
TRUE, PT-402.Alarm_Enable
8.0, PT-403.PV_Low
TRUE, PT-403.Alarm_Enable
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 22:11:04

### Output:
```
* Parameter Data Connections *
495.0, TC-401.SP
0.0, TC-401.MV_MIN
100.0, TC-401.MV_MAX
3.2, TC-401.KP
0.9, TC-401.TR
0.3, TC-401.TD
2.0, TC-401.Deviation_Limit
510.0, TC-401.PV_High
480.0, TC-401.PV_Low
TRUE, TIT-101.Alarm_Enable
9.375, TIT-101.Scaling_Slope
362.5, TIT-101.Scaling_Offset
550.0, TIT-101.PV_High
480.0, TIT-101.PV_Low
100.0, FV-401.Open_Limit
0.0, FV-401.Close_Limit
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
TRUE, PT-402.Alarm_Enable
8.0, PT-403.PV_High
0.0, PT-403.PV_Low
TRUE, PT-403.Alarm_Enable
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 22:12:18

### Output:
```
* Variables *
REAL TIT-101_FurnaceOutletTemp_PV
REAL TC-401_MV_To_FV-401
REAL PT-402_FurnaceDraftPressure_PV
REAL PT-403_DischargePressure_PV
REAL FT-401A_FlowRate_PV

* Data Connections *
TIT-101.PV, TIT-101_FurnaceOutletTemp_PV
TC-401.XOUT, TC-401_MV_To_FV-401
PT-402.PV, PT-402_FurnaceDraftPressure_PV
PT-403.PV, PT-403_DischargePressure_PV
FT-401A.PV, FT-401A_FlowRate_PV
```

---

## Step 8: openplc-rule-checks
**Time:** 22:13:14

### Output:
```
* Function Blocks *
ANALOG_IN FT-401A
VALVE_ELECTRIC FV-401
MOTOR_ON_OFF P-401A
MOTOR_ON_OFF P-401B
PID_BASIC PC-401
ANALOG_IN PT-402
ANALOG_IN PT-403
PID_BASIC TC-401
ANALOG_IN TIT-101

* Variables *
REAL TIT_101_FurnaceOutletTemp_PV
REAL TC_401_MV_To_FV_401
REAL PT_402_FurnaceDraftPressure_PV
REAL PT_403_DischargePressure_PV
REAL FT_401A_FlowRate_PV
REAL FuelGasPressure_PV
BOOL Flame_OK
BOOL TempHighAlarm_3s
BOOL TempLowAlarm_3s
BOOL TC401_AutoCmd
REAL TC401_ManualBias
BOOL Valve_ManualMode
REAL Valve_ManualPos

* Functions *
OR FuelGasPressOutOfRange_OR
NOT FuelGasPressOK_NOT
OR DraftOutOfRange_OR
NOT DraftOK_NOT
OR PumpsRunning_OR
AND FlowPermissive_AND
AND ProcessPermissive_AND
AND Permissive1_AND
AND FinalPermissive_AND
NOT PermissiveNot_NOT
TON FuelFlowInterlockDelay_TON
OR InhibitWithHighTrip_OR
OR FinalInhibit_OR
TON TempHighAlarmDelay_TON
TON TempLowAlarmDelay_TON

* Data Connections * 
TIT-101.PV, TC-401.PV
TC-401.XOUT, FV-401.Control_Signal
PC-401.PV_High_Alarm, FuelGasPressOutOfRange_OR.IN1
PC-401.PV_Low_Alarm, FuelGasPressOutOfRange_OR.IN2
FuelGasPressOutOfRange_OR.OUT, FuelGasPressOK_NOT.IN
PT-402.High_Alarm, DraftOutOfRange_OR.IN1
PT-402.Low_Alarm, DraftOutOfRange_OR.IN2
DraftOutOfRange_OR.OUT, DraftOK_NOT.IN
P-401A.FB_Running, PumpsRunning_OR.IN1
P-401B.FB_Running, PumpsRunning_OR.IN2
PumpsRunning_OR.OUT, FlowPermissive_AND.IN1
PT-403.High_Alarm, FlowPermissive_AND.IN2
FuelGasPressOK_NOT.OUT, ProcessPermissive_AND.IN1
DraftOK_NOT.OUT, ProcessPermissive_AND.IN2
ProcessPermissive_AND.OUT, Permissive1_AND.IN1
FlowPermissive_AND.OUT, Permissive1_AND.IN2
Permissive1_AND.OUT, FinalPermissive_AND.IN1
Flame_OK, FinalPermissive_AND.IN2
FinalPermissive_AND.OUT, PermissiveNot_NOT.IN
PermissiveNot_NOT.OUT, FuelFlowInterlockDelay_TON.IN
FuelFlowInterlockDelay_TON.Q, InhibitWithHighTrip_OR.IN1
TIT-101.High_Alarm, InhibitWithHighTrip_OR.IN2
InhibitWithHighTrip_OR.OUT, FinalInhibit_OR.IN1
TIT-101.General_Fault, FinalInhibit_OR.IN2
FinalInhibit_OR.OUT, FV-401.Inhibit
FinalInhibit_OR.OUT, TC-401.Inhibit
TIT-101.High_Alarm, TempHighAlarmDelay_TON.IN
TIT-101.Low_Alarm, TempLowAlarmDelay_TON.IN
TempHighAlarmDelay_TON.Q, TempHighAlarm_3s
TempLowAlarmDelay_TON.Q, TempLowAlarm_3s
TIT-101.PV, TIT_101_FurnaceOutletTemp_PV
TC-401.XOUT, TC_401_MV_To_FV_401
PT-402.PV, PT_402_FurnaceDraftPressure_PV
PT-403.PV, PT_403_DischargePressure_PV
FT-401A.PV, FT_401A_FlowRate_PV
FuelGasPressure_PV, PC-401.PV
TC401_AutoCmd, TC-401.AUTO
TC401_ManualBias, TC-401.X0
Valve_ManualMode, FV-401.Manual_Mode
Valve_ManualPos, FV-401.Manual_Position

* Parameter Data Connections *
495.0, TC-401.SP
0.0, TC-401.MV_MIN
100.0, TC-401.MV_MAX
3.2, TC-401.KP
0.9, TC-401.TR
0.3, TC-401.TD
2.0, TC-401.Deviation_Limit
510.0, TC-401.PV_High
480.0, TC-401.PV_Low
TRUE, TIT-101.Alarm_Enable
9.375, TIT-101.Scaling_Slope
362.5, TIT-101.Scaling_Offset
550.0, TIT-101.PV_High
480.0, TIT-101.PV_Low
TRUE, PT-402.Alarm_Enable
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
TRUE, PT-403.Alarm_Enable
8.0, PT-403.PV_High
0.0, PT-403.PV_Low
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
100.0, FV-401.Open_Limit
0.0, FV-401.Close_Limit
T#10s, FV-401.Timeout
T#5s, FuelFlowInterlockDelay_TON.PT
T#3s, TempHighAlarmDelay_TON.PT
T#3s, TempLowAlarmDelay_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 22:15:57

### Output:
```
* Function Blocks *
ANALOG_IN FT-401A
VALVE_ELECTRIC FV-401
MOTOR_ON_OFF P-401A
MOTOR_ON_OFF P-401B
PID_BASIC PC-401
ANALOG_IN PT-402
ANALOG_IN PT-403
PID_BASIC TC-401
ANALOG_IN TIT-101

* Variables *
REAL TIT_101_FurnaceOutletTemp_PV
REAL TC_401_MV_To_FV_401
REAL PT_402_FurnaceDraftPressure_PV
REAL PT_403_DischargePressure_PV
REAL FT_401A_FlowRate_PV
REAL FuelGasPressure_PV
BOOL Flame_OK
BOOL TempHighAlarm_3s
BOOL TempLowAlarm_3s
BOOL TC401_AutoCmd
REAL TC401_ManualBias
BOOL Valve_ManualMode
REAL Valve_ManualPos

* Functions *
OR FuelGasPressOutOfRange_OR
NOT FuelGasPressOK_NOT
OR DraftOutOfRange_OR
NOT DraftOK_NOT
OR PumpsRunning_OR
AND FlowPermissive_AND
AND ProcessPermissive_AND
AND Permissive1_AND
AND FinalPermissive_AND
NOT PermissiveNot_NOT
TON FuelFlowInterlockDelay_TON
OR InhibitWithHighTrip_OR
OR FinalInhibit_OR
TON TempHighAlarmDelay_TON
TON TempLowAlarmDelay_TON

* Data Connections * 
TIT-101.PV, TC-401.PV
TC-401.XOUT, FV-401.Control_Signal
PC-401.PV_High_Alarm, FuelGasPressOutOfRange_OR.IN1
PC-401.PV_Low_Alarm, FuelGasPressOutOfRange_OR.IN2
FuelGasPressOutOfRange_OR.OUT, FuelGasPressOK_NOT.IN
PT-402.High_Alarm, DraftOutOfRange_OR.IN1
PT-402.Low_Alarm, DraftOutOfRange_OR.IN2
DraftOutOfRange_OR.OUT, DraftOK_NOT.IN
P-401A.FB_Running, PumpsRunning_OR.IN1
P-401B.FB_Running, PumpsRunning_OR.IN2
PumpsRunning_OR.OUT, FlowPermissive_AND.IN1
PT-403.High_Alarm, FlowPermissive_AND.IN2
FuelGasPressOK_NOT.OUT, ProcessPermissive_AND.IN1
DraftOK_NOT.OUT, ProcessPermissive_AND.IN2
ProcessPermissive_AND.OUT, Permissive1_AND.IN1
FlowPermissive_AND.OUT, Permissive1_AND.IN2
Permissive1_AND.OUT, FinalPermissive_AND.IN1
Flame_OK, FinalPermissive_AND.IN2
FinalPermissive_AND.OUT, PermissiveNot_NOT.IN
PermissiveNot_NOT.OUT, FuelFlowInterlockDelay_TON.IN
FuelFlowInterlockDelay_TON.Q, InhibitWithHighTrip_OR.IN1
TIT-101.High_Alarm, InhibitWithHighTrip_OR.IN2
InhibitWithHighTrip_OR.OUT, FinalInhibit_OR.IN1
TIT-101.General_Fault, FinalInhibit_OR.IN2
FinalInhibit_OR.OUT, FV-401.Inhibit
FinalInhibit_OR.OUT, TC-401.Inhibit
TIT-101.High_Alarm, TempHighAlarmDelay_TON.IN
TIT-101.Low_Alarm, TempLowAlarmDelay_TON.IN
TempHighAlarmDelay_TON.Q, TempHighAlarm_3s
TempLowAlarmDelay_TON.Q, TempLowAlarm_3s
TIT-101.PV, TIT_101_FurnaceOutletTemp_PV
TC-401.XOUT, TC_401_MV_To_FV_401
PT-402.PV, PT_402_FurnaceDraftPressure_PV
PT-403.PV, PT_403_DischargePressure_PV
FT-401A.PV, FT_401A_FlowRate_PV
FuelGasPressure_PV, PC-401.PV
TC401_AutoCmd, TC-401.AUTO
TC401_ManualBias, TC-401.X0
Valve_ManualMode, FV-401.Manual_Mode
Valve_ManualPos, FV-401.Manual_Position

* Parameter Data Connections *
495.0, TC-401.SP
0.0, TC-401.MV_MIN
100.0, TC-401.MV_MAX
3.2, TC-401.KP
0.9, TC-401.TR
0.3, TC-401.TD
2.0, TC-401.Deviation_Limit
510.0, TC-401.PV_High
480.0, TC-401.PV_Low
TRUE, TIT-101.Alarm_Enable
9.375, TIT-101.Scaling_Slope
362.5, TIT-101.Scaling_Offset
550.0, TIT-101.PV_High
480.0, TIT-101.PV_Low
TRUE, PT-402.Alarm_Enable
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
TRUE, PT-403.Alarm_Enable
8.0, PT-403.PV_High
0.0, PT-403.PV_Low
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
100.0, FV-401.Open_Limit
0.0, FV-401.Close_Limit
T#10s, FV-401.Timeout
T#5s, FuelFlowInterlockDelay_TON.PT
T#3s, TempHighAlarmDelay_TON.PT
T#3s, TempLowAlarmDelay_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 22:16:27

### Output:
```
* Function Blocks *
ANALOG_IN FT-401A
VALVE_ELECTRIC FV-401
MOTOR_ON_OFF P-401A
MOTOR_ON_OFF P-401B
PID_BASIC PC-401
ANALOG_IN PT-402
ANALOG_IN PT-403
PID_BASIC TC-401
ANALOG_IN TIT-101

* Variables *
REAL TIT_101_FurnaceOutletTemp_PV
REAL TC_401_MV_To_FV_401
REAL PT_402_FurnaceDraftPressure_PV
REAL PT_403_DischargePressure_PV
REAL FT_401A_FlowRate_PV
REAL FuelGasPressure_PV
BOOL Flame_OK
BOOL TempHighAlarm_3s
BOOL TempLowAlarm_3s
BOOL TC401_AutoCmd
REAL TC401_ManualBias
BOOL Valve_ManualMode
REAL Valve_ManualPos

* Functions *
OR FuelGasPressOutOfRange_OR
NOT FuelGasPressOK_NOT
OR DraftOutOfRange_OR
NOT DraftOK_NOT
OR PumpsRunning_OR
AND FlowPermissive_AND
AND ProcessPermissive_AND
AND Permissive1_AND
AND FinalPermissive_AND
NOT PermissiveNot_NOT
TON FuelFlowInterlockDelay_TON
OR InhibitWithHighTrip_OR
OR FinalInhibit_OR
TON TempHighAlarmDelay_TON
TON TempLowAlarmDelay_TON

* Data Connections * 
TIT-101.PV, TC-401.PV
TC-401.XOUT, FV-401.Control_Signal
PC-401.PV_High_Alarm, FuelGasPressOutOfRange_OR.IN1
PC-401.PV_Low_Alarm, FuelGasPressOutOfRange_OR.IN2
FuelGasPressOutOfRange_OR.OUT, FuelGasPressOK_NOT.IN
PT-402.High_Alarm, DraftOutOfRange_OR.IN1
PT-402.Low_Alarm, DraftOutOfRange_OR.IN2
DraftOutOfRange_OR.OUT, DraftOK_NOT.IN
P-401A.FB_Running, PumpsRunning_OR.IN1
P-401B.FB_Running, PumpsRunning_OR.IN2
PumpsRunning_OR.OUT, FlowPermissive_AND.IN1
PT-403.High_Alarm, FlowPermissive_AND.IN2
FuelGasPressOK_NOT.OUT, ProcessPermissive_AND.IN1
DraftOK_NOT.OUT, ProcessPermissive_AND.IN2
ProcessPermissive_AND.OUT, Permissive1_AND.IN1
FlowPermissive_AND.OUT, Permissive1_AND.IN2
Permissive1_AND.OUT, FinalPermissive_AND.IN1
Flame_OK, FinalPermissive_AND.IN2
FinalPermissive_AND.OUT, PermissiveNot_NOT.IN
PermissiveNot_NOT.OUT, FuelFlowInterlockDelay_TON.IN
FuelFlowInterlockDelay_TON.Q, InhibitWithHighTrip_OR.IN1
TIT-101.High_Alarm, InhibitWithHighTrip_OR.IN2
InhibitWithHighTrip_OR.OUT, FinalInhibit_OR.IN1
TIT-101.General_Fault, FinalInhibit_OR.IN2
FinalInhibit_OR.OUT, FV-401.Inhibit
FinalInhibit_OR.OUT, TC-401.Inhibit
TIT-101.High_Alarm, TempHighAlarmDelay_TON.IN
TIT-101.Low_Alarm, TempLowAlarmDelay_TON.IN
TempHighAlarmDelay_TON.Q, TempHighAlarm_3s
TempLowAlarmDelay_TON.Q, TempLowAlarm_3s
TIT-101.PV, TIT_101_FurnaceOutletTemp_PV
TC-401.XOUT, TC_401_MV_To_FV_401
PT-402.PV, PT_402_FurnaceDraftPressure_PV
PT-403.PV, PT_403_DischargePressure_PV
FT-401A.PV, FT_401A_FlowRate_PV
FuelGasPressure_PV, PC-401.PV
TC401_AutoCmd, TC-401.AUTO
TC401_ManualBias, TC-401.X0
Valve_ManualMode, FV-401.Manual_Mode
Valve_ManualPos, FV-401.Manual_Position

* Parameter Data Connections *
495.0, TC-401.SP
0.0, TC-401.MV_MIN
100.0, TC-401.MV_MAX
3.2, TC-401.KP
0.9, TC-401.TR
0.3, TC-401.TD
2.0, TC-401.Deviation_Limit
510.0, TC-401.PV_High
480.0, TC-401.PV_Low
TRUE, TIT-101.Alarm_Enable
9.375, TIT-101.Scaling_Slope
362.5, TIT-101.Scaling_Offset
550.0, TIT-101.PV_High
480.0, TIT-101.PV_Low
TRUE, PT-402.Alarm_Enable
-0.1, PT-402.PV_High
-0.5, PT-402.PV_Low
TRUE, PT-403.Alarm_Enable
8.0, PT-403.PV_High
0.0, PT-403.PV_Low
4.0, PC-401.PV_High
2.5, PC-401.PV_Low
100.0, FV-401.Open_Limit
0.0, FV-401.Close_Limit
T#10s, FV-401.Timeout
T#5s, FuelFlowInterlockDelay_TON.PT
T#3s, TempHighAlarmDelay_TON.PT
T#3s, TempLowAlarmDelay_TON.PT
```

---


