# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 11:48:56

## Step 1: contextgen1-sensors
**Time:** 11:48:56

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
**Time:** 11:49:36

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
**Time:** 11:49:59

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|------------------|-------------|
| Duty-Standby     | 0.99        |

Selected Control Strategy: Duty-Standby
Short explanation: The narrative requires redundant pump control with automatic switchover on failure, alternation based on runtime, minimum run-time enforcement, and delay timers, which aligns directly with the Duty-Standby strategy.

** Description **
The system includes two identical actuators (e.g., pumps), runtime monitors, and a control logic unit. One actuator operates as the duty unit, while the other remains in standby. The control logic monitors runtime or fault conditions and switches to the standby actuator either if the duty cycle has expired or if one pump becomes faulty. Multiple timers can be involved.
** Intended Block-to-Block Connections Types **
MOTOR_ON_OFF1.FB_Running, DUTY_STANDBY.PumpA_RunFB
MOTOR_ON_OFF2.FB_Running, DUTY_STANDBY.PumpB_RunFB
<defined time for duty-standby cycle>,TON1.PT
TON1.Q, DUTY_STANDBY.DutyElapsed
DUTY_STANDBY.CmdPumpA, MOTOR_ON_OFF1.StartCmd
DUTY_STANDBY.CmdPumpB, MOTOR_ON_OFF2.StartCmd

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
```

---


# Prompt Chain: openplc-function-block-chain-v3.txt
**Timestamp:** 2025-09-24 11:51:09

## Step 1: openplc-function-blocks-v2
**Time:** 11:51:09

### Output:
```
* Function Blocks *
ANALOG_IN FT-901
ANALOG_IN LS-901
MOTOR_ON_OFF P-901A
MOTOR_ON_OFF P-901B
VALVE_ON_OFF XV-102
DUTY_STANDBY P-901_DUTY_STANDBY
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 11:51:38

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN FT-901
ANALOG_IN LS-901
MOTOR_ON_OFF P-901A
MOTOR_ON_OFF P-901B
VALVE_ON_OFF XV-102
DUTY_STANDBY P-901_DUTY_STANDBY
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 11:52:35

### Output:
```
* Functions *
GT LevelAbove60_GT
LT LevelBelow40_LT
GT LevelAbove85_GT
NOT LevelAbove60_NOT
RS StartRequest_RS
AND SelectedA_AND
NOT ActiveIsA_NOT
AND SelectedB_AND
OR SelectedRun_OR
TON DutyPeriod_TON
TON MinRun_TON
LT FTBelow15_LT
AND PumpA_Fail_AND
TON PumpA_Fail_TON
AND PumpB_Fail_AND
TON PumpB_Fail_TON
OR FailAny_OR
TON SwitchoverDelay_TON
OR StartA_OR
NOT StartA_NOT
OR StartB_OR
NOT StartB_NOT
OR AlwaysTrue_OR

* Block-to-Block Connections *
LS-901.PV, LevelAbove60_GT.IN1
60.0, LevelAbove60_GT.IN2
LS-901.PV, LevelBelow40_LT.IN1
40.0, LevelBelow40_LT.IN2
LS-901.PV, LevelAbove85_GT.IN1
85.0, LevelAbove85_GT.IN2
LevelAbove60_GT.Q, LevelAbove60_NOT.IN
LevelAbove60_GT.Q, StartRequest_RS.S
LevelBelow40_LT.Q, StartRequest_RS.R
P-901_DUTY_STANDBY.ActiveIsA, SelectedA_AND.IN1
P-901A.FB_Running, SelectedA_AND.IN2
P-901_DUTY_STANDBY.ActiveIsA, ActiveIsA_NOT.IN
ActiveIsA_NOT.Q, SelectedB_AND.IN1
P-901B.FB_Running, SelectedB_AND.IN2
SelectedA_AND.Q, SelectedRun_OR.IN1
SelectedB_AND.Q, SelectedRun_OR.IN2
SelectedRun_OR.Q, DutyPeriod_TON.IN
T#48h, DutyPeriod_TON.PT
DutyPeriod_TON.Q, P-901_DUTY_STANDBY.DutyElapsed
SelectedRun_OR.Q, MinRun_TON.IN
T#30m, MinRun_TON.PT
MinRun_TON.Q, P-901_DUTY_STANDBY.MinRunElapsed
FT-901.PV, FTBelow15_LT.IN1
15.0, FTBelow15_LT.IN2
P-901A.FB_Running, PumpA_Fail_AND.IN1
FTBelow15_LT.Q, PumpA_Fail_AND.IN2
PumpA_Fail_AND.Q, PumpA_Fail_TON.IN
T#10s, PumpA_Fail_TON.PT
PumpA_Fail_TON.Q, P-901_DUTY_STANDBY.PumpA_Fault
P-901B.FB_Running, PumpB_Fail_AND.IN1
FTBelow15_LT.Q, PumpB_Fail_AND.IN2
PumpB_Fail_AND.Q, PumpB_Fail_TON.IN
T#10s, PumpB_Fail_TON.PT
PumpB_Fail_TON.Q, P-901_DUTY_STANDBY.PumpB_Fault
PumpA_Fail_TON.Q, FailAny_OR.IN1
PumpB_Fail_TON.Q, FailAny_OR.IN2
FailAny_OR.Q, SwitchoverDelay_TON.IN
T#5s, SwitchoverDelay_TON.PT
SwitchoverDelay_TON.Q, P-901_DUTY_STANDBY.SwitchoverDelayElapsed
StartRequest_RS.Q, P-901_DUTY_STANDBY.StartRequest
LevelAbove60_NOT.Q, AlwaysTrue_OR.IN1
LevelAbove60_GT.Q, AlwaysTrue_OR.IN2
AlwaysTrue_OR.Q, P-901_DUTY_STANDBY.Enable
AlwaysTrue_OR.Q, P-901_DUTY_STANDBY.AlternateEnable
P-901_DUTY_STANDBY.CmdPumpA, StartA_OR.IN1
LevelAbove85_GT.Q, StartA_OR.IN2
StartA_OR.Q, StartA_NOT.IN
StartA_OR.Q, P-901A.Start_Cmd
StartA_NOT.Q, P-901A.Stop_Cmd
P-901_DUTY_STANDBY.CmdPumpB, StartB_OR.IN1
LevelAbove85_GT.Q, StartB_OR.IN2
StartB_OR.Q, StartB_NOT.IN
StartB_OR.Q, P-901B.Start_Cmd
StartB_NOT.Q, P-901B.Stop_Cmd
P-901A.FB_Running, P-901_DUTY_STANDBY.PumpA_RunFB
P-901B.FB_Running, P-901_DUTY_STANDBY.PumpB_RunFB
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 11:54:32

### Output:
```
* Functions *
AND PumpA_FlowFail_AND
AND PumpB_FlowFail_AND
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR

* Data Connections *
P-901A.FB_Running, PumpA_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpA_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpA_Inhibit_OR.IN1
PumpA_FlowFail_AND.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, P-901A.Inhibit
P-901B.FB_Running, PumpB_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpB_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpB_Inhibit_OR.IN1
PumpB_FlowFail_AND.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, P-901B.Inhibit
P-901_DUTY_STANDBY.Alarm_NoAvailablePump, XV-102.Inhibit

* Parameter Data Connections *
40, LS-901.PV_Low
90, LS-901.PV_High
15, FT-901.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 11:55:44

### Output:
```
* Parameter Data Connections *
60.0, LevelAbove60_GT.IN2
40.0, LevelBelow40_LT.IN2
85.0, LevelAbove85_GT.IN2
15.0, FTBelow15_LT.IN2
T#48h, DutyPeriod_TON.PT
T#30m, MinRun_TON.PT
T#10s, PumpA_Fail_TON.PT
T#10s, PumpB_Fail_TON.PT
T#5s, SwitchoverDelay_TON.PT
90.0, LS-901.PV_High
TRUE, LS-901.Alarm_Enable
15.0, FT-901.PV_Low
TRUE, FT-901.Alarm_Enable
T#30m, P-901A.MinRunTime
T#30m, P-901B.MinRunTime
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 11:56:41

### Output:
```
* Parameter Data Connections *
60.0, LevelAbove60_GT.IN2
40.0, LevelBelow40_LT.IN2
85.0, LevelAbove85_GT.IN2
15.0, FTBelow15_LT.IN2
T#48h, DutyPeriod_TON.PT
T#30m, MinRun_TON.PT
T#10s, PumpA_Fail_TON.PT
T#10s, PumpB_Fail_TON.PT
T#5s, SwitchoverDelay_TON.PT
40.0, LS-901.PV_Low
90.0, LS-901.PV_High
TRUE, LS-901.Alarm_Enable
15.0, FT-901.PV_Low
TRUE, FT-901.Alarm_Enable
T#30m, P-901A.MinRunTime
T#30m, P-901B.MinRunTime
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 11:57:47

### Output:
```
* Variables *
REAL FT-901_Flow_PV
REAL LS-901_Level_PV
BOOL P-901A_MotorStartOut
BOOL P-901B_MotorStartOut
BOOL XV-102_CloseOut

* Data Connections *
FT-901.PV, FT-901_Flow_PV
LS-901.PV, LS-901_Level_PV
P-901A.Motor_Start_Out, P-901A_MotorStartOut
P-901B.Motor_Start_Out, P-901B_MotorStartOut
XV-102.Valve_Close_Out, XV-102_CloseOut
```

---

## Step 8: openplc-rule-checks
**Time:** 11:58:32

### Output:
```
* Function Blocks *
ANALOG_IN FT-901
ANALOG_IN LS-901
MOTOR_ON_OFF P-901A
MOTOR_ON_OFF P-901B
VALVE_ON_OFF XV-102
DUTY_STANDBY P-901_DS

* Variables *
REAL FT-901_Flow_PV
REAL LS-901_Level_PV
BOOL P-901A_MotorStartOut
BOOL P-901B_MotorStartOut
BOOL XV-102_CloseOut

* Functions *
GT LevelAbove60_GT
LT LevelBelow40_LT
GT LevelAbove85_GT
NOT LevelAbove60_NOT
RS StartRequest_RS
AND SelectedA_AND
NOT ActiveIsA_NOT
AND SelectedB_AND
OR SelectedRun_OR
TON DutyPeriod_TON
TON MinRun_TON
LT FTBelow15_LT
AND PumpA_Fail_AND
TON PumpA_Fail_TON
AND PumpB_Fail_AND
TON PumpB_Fail_TON
OR FailAny_OR
TON SwitchoverDelay_TON
OR StartA_OR
NOT StartA_NOT
OR StartB_OR
NOT StartB_NOT
OR AlwaysTrue_OR
AND PumpA_FlowFail_AND
AND PumpB_FlowFail_AND
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR

* Data Connections * 
LS-901.PV, LevelAbove60_GT.IN1
LS-901.PV, LevelBelow40_LT.IN1
LS-901.PV, LevelAbove85_GT.IN1
LevelAbove60_GT.OUT, LevelAbove60_NOT.IN
LevelAbove60_GT.OUT, StartRequest_RS.S
LevelBelow40_LT.OUT, StartRequest_RS.R
P-901_DS.ActiveIsA, SelectedA_AND.IN1
P-901A.FB_Running, SelectedA_AND.IN2
P-901_DS.ActiveIsA, ActiveIsA_NOT.IN
ActiveIsA_NOT.OUT, SelectedB_AND.IN1
P-901B.FB_Running, SelectedB_AND.IN2
SelectedA_AND.OUT, SelectedRun_OR.IN1
SelectedB_AND.OUT, SelectedRun_OR.IN2
SelectedRun_OR.OUT, DutyPeriod_TON.IN
DutyPeriod_TON.Q, P-901_DS.DutyElapsed
SelectedRun_OR.OUT, MinRun_TON.IN
MinRun_TON.Q, P-901_DS.MinRunElapsed
FT-901.PV, FTBelow15_LT.IN1
P-901A.FB_Running, PumpA_Fail_AND.IN1
FTBelow15_LT.OUT, PumpA_Fail_AND.IN2
PumpA_Fail_AND.OUT, PumpA_Fail_TON.IN
PumpA_Fail_TON.Q, P-901_DS.PumpA_Fault
P-901B.FB_Running, PumpB_Fail_AND.IN1
FTBelow15_LT.OUT, PumpB_Fail_AND.IN2
PumpB_Fail_AND.OUT, PumpB_Fail_TON.IN
PumpB_Fail_TON.Q, P-901_DS.PumpB_Fault
PumpA_Fail_TON.Q, FailAny_OR.IN1
PumpB_Fail_TON.Q, FailAny_OR.IN2
FailAny_OR.OUT, SwitchoverDelay_TON.IN
SwitchoverDelay_TON.Q, P-901_DS.SwitchoverDelayElapsed
StartRequest_RS.Q, P-901_DS.StartRequest
LevelAbove60_NOT.OUT, AlwaysTrue_OR.IN1
LevelAbove60_GT.OUT, AlwaysTrue_OR.IN2
AlwaysTrue_OR.OUT, P-901_DS.Enable
AlwaysTrue_OR.OUT, P-901_DS.AlternateEnable
P-901_DS.CmdPumpA, StartA_OR.IN1
LevelAbove85_GT.OUT, StartA_OR.IN2
StartA_OR.OUT, StartA_NOT.IN
StartA_OR.OUT, P-901A.Start_Cmd
StartA_NOT.OUT, P-901A.Stop_Cmd
P-901_DS.CmdPumpB, StartB_OR.IN1
LevelAbove85_GT.OUT, StartB_OR.IN2
StartB_OR.OUT, StartB_NOT.IN
StartB_OR.OUT, P-901B.Start_Cmd
StartB_NOT.OUT, P-901B.Stop_Cmd
P-901A.FB_Running, P-901_DS.PumpA_RunFB
P-901B.FB_Running, P-901_DS.PumpB_RunFB
P-901A.FB_Running, PumpA_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpA_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpA_Inhibit_OR.IN1
PumpA_FlowFail_AND.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, P-901A.Inhibit
P-901B.FB_Running, PumpB_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpB_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpB_Inhibit_OR.IN1
PumpB_FlowFail_AND.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, P-901B.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Close_Cmd
FT-901.PV, FT-901_Flow_PV
LS-901.PV, LS-901_Level_PV
P-901A.Motor_Start_Out, P-901A_MotorStartOut
P-901B.Motor_Start_Out, P-901B_MotorStartOut
XV-102.Valve_Close_Out, XV-102_CloseOut

* Parameter Data Connections *
60.0, LevelAbove60_GT.IN2
40.0, LevelBelow40_LT.IN2
85.0, LevelAbove85_GT.IN2
15.0, FTBelow15_LT.IN2
T#48h, DutyPeriod_TON.PT
T#30m, MinRun_TON.PT
T#10s, PumpA_Fail_TON.PT
T#10s, PumpB_Fail_TON.PT
T#5s, SwitchoverDelay_TON.PT
40.0, LS-901.PV_Low
90.0, LS-901.PV_High
TRUE, LS-901.Alarm_Enable
15.0, FT-901.PV_Low
TRUE, FT-901.Alarm_Enable
T#30m, P-901A.MinRunTime
T#30m, P-901B.MinRunTime
```

---

## Step 9: openplc-rule-checks2
**Time:** 12:01:17

### Output:
```
* Function Blocks *
ANALOG_IN FT-901
ANALOG_IN LS-901
MOTOR_ON_OFF P-901A
MOTOR_ON_OFF P-901B
VALVE_ON_OFF XV-102
DUTY_STANDBY P-901_DS

* Variables *
REAL FT-901_Flow_PV
REAL LS-901_Level_PV
BOOL P-901A_MotorStartOut
BOOL P-901B_MotorStartOut
BOOL XV-102_CloseOut

* Functions *
GT LevelAbove60_GT
LT LevelBelow40_LT
GT LevelAbove85_GT
NOT LevelAbove60_NOT
RS StartRequest_RS
AND SelectedA_AND
NOT ActiveIsA_NOT
AND SelectedB_AND
OR SelectedRun_OR
TON DutyPeriod_TON
TON MinRun_TON
LT FTBelow15_LT
AND PumpA_Fail_AND
TON PumpA_Fail_TON
AND PumpB_Fail_AND
TON PumpB_Fail_TON
OR FailAny_OR
TON SwitchoverDelay_TON
OR StartA_OR
NOT StartA_NOT
OR StartB_OR
NOT StartB_NOT
OR AlwaysTrue_OR
AND PumpA_FlowFail_AND
AND PumpB_FlowFail_AND
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR

* Data Connections * 
LS-901.PV, LevelAbove60_GT.IN1
LS-901.PV, LevelBelow40_LT.IN1
LS-901.PV, LevelAbove85_GT.IN1
LevelAbove60_GT.OUT, LevelAbove60_NOT.IN
LevelAbove60_GT.OUT, StartRequest_RS.S
LevelBelow40_LT.OUT, StartRequest_RS.R
P-901_DS.ActiveIsA, SelectedA_AND.IN1
P-901A.FB_Running, SelectedA_AND.IN2
P-901_DS.ActiveIsA, ActiveIsA_NOT.IN
ActiveIsA_NOT.OUT, SelectedB_AND.IN1
P-901B.FB_Running, SelectedB_AND.IN2
SelectedA_AND.OUT, SelectedRun_OR.IN1
SelectedB_AND.OUT, SelectedRun_OR.IN2
SelectedRun_OR.OUT, DutyPeriod_TON.IN
DutyPeriod_TON.Q, P-901_DS.DutyElapsed
SelectedRun_OR.OUT, MinRun_TON.IN
MinRun_TON.Q, P-901_DS.MinRunElapsed
FT-901.PV, FTBelow15_LT.IN1
P-901A.FB_Running, PumpA_Fail_AND.IN1
FTBelow15_LT.OUT, PumpA_Fail_AND.IN2
PumpA_Fail_AND.OUT, PumpA_Fail_TON.IN
PumpA_Fail_TON.Q, P-901_DS.PumpA_Fault
P-901B.FB_Running, PumpB_Fail_AND.IN1
FTBelow15_LT.OUT, PumpB_Fail_AND.IN2
PumpB_Fail_AND.OUT, PumpB_Fail_TON.IN
PumpB_Fail_TON.Q, P-901_DS.PumpB_Fault
PumpA_Fail_TON.Q, FailAny_OR.IN1
PumpB_Fail_TON.Q, FailAny_OR.IN2
FailAny_OR.OUT, SwitchoverDelay_TON.IN
SwitchoverDelay_TON.Q, P-901_DS.SwitchoverDelayElapsed
StartRequest_RS.Q, P-901_DS.StartRequest
LevelAbove60_NOT.OUT, AlwaysTrue_OR.IN1
LevelAbove60_GT.OUT, AlwaysTrue_OR.IN2
AlwaysTrue_OR.OUT, P-901_DS.Enable
AlwaysTrue_OR.OUT, P-901_DS.AlternateEnable
P-901_DS.CmdPumpA, StartA_OR.IN1
LevelAbove85_GT.OUT, StartA_OR.IN2
StartA_OR.OUT, StartA_NOT.IN
StartA_OR.OUT, P-901A.Start_Cmd
StartA_NOT.OUT, P-901A.Stop_Cmd
P-901_DS.CmdPumpB, StartB_OR.IN1
LevelAbove85_GT.OUT, StartB_OR.IN2
StartB_OR.OUT, StartB_NOT.IN
StartB_OR.OUT, P-901B.Start_Cmd
StartB_NOT.OUT, P-901B.Stop_Cmd
P-901A.FB_Running, P-901_DS.PumpA_RunFB
P-901B.FB_Running, P-901_DS.PumpB_RunFB
P-901A.FB_Running, PumpA_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpA_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpA_Inhibit_OR.IN1
PumpA_FlowFail_AND.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, P-901A.Inhibit
P-901B.FB_Running, PumpB_FlowFail_AND.IN1
FT-901.Low_Alarm, PumpB_FlowFail_AND.IN2
LS-901.Low_Alarm, PumpB_Inhibit_OR.IN1
PumpB_FlowFail_AND.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, P-901B.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Close_Cmd
FT-901.PV, FT-901_Flow_PV
LS-901.PV, LS-901_Level_PV
P-901A.Motor_Start_Out, P-901A_MotorStartOut
P-901B.Motor_Start_Out, P-901B_MotorStartOut
XV-102.Valve_Close_Out, XV-102_CloseOut

* Parameter Data Connections *
60.0, LevelAbove60_GT.IN2
40.0, LevelBelow40_LT.IN2
85.0, LevelAbove85_GT.IN2
15.0, FTBelow15_LT.IN2
T#48h, DutyPeriod_TON.PT
T#30m, MinRun_TON.PT
T#10s, PumpA_Fail_TON.PT
T#10s, PumpB_Fail_TON.PT
T#5s, SwitchoverDelay_TON.PT
40.0, LS-901.PV_Low
90.0, LS-901.PV_High
TRUE, LS-901.Alarm_Enable
15.0, FT-901.PV_Low
TRUE, FT-901.Alarm_Enable
T#30m, P-901A.MinRunTime
T#30m, P-901B.MinRunTime
```

---

## Step 10: append_two_inputs
**Time:** 12:01:46

### Output:
```
* Function Blocks *
ANALOG_IN FT-901
ANALOG_IN LS-901
MOTOR_ON_OFF P-901A
MOTOR_ON_OFF P-901B
VALVE_ON_OFF XV-102
DUTY_STANDBY P-901_DS

* Variables *
REAL FT-901_Flow_PV
REAL LS-901_Level_PV
BOOL P-901A_MotorStartOut
BOOL P-901B_MotorStartOut
BOOL XV-102_CloseOut

* Functions *
GT LevelAbove60_GT
LT LevelBelow40_LT
GT LevelAbove85_GT
RS StartRequest_RS
AND SelectedA_AND
NOT ActiveIsA_NOT
AND SelectedB_AND
OR SelectedRun_OR
TON DutyPeriod_TON
TON MinRun_TON
AND PumpA_Fail_AND
TON PumpA_Fail_TON
AND PumpB_Fail_AND
TON PumpB_Fail_TON
OR FailAny_OR
TON SwitchoverDelay_TON
OR StartA_OR
NOT StartA_NOT
OR StartB_OR
NOT StartB_NOT
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR

* Data Connections * 
LS-901.PV, LevelAbove60_GT.IN1
LS-901.PV, LevelBelow40_LT.IN1
LS-901.PV, LevelAbove85_GT.IN1
LevelAbove60_GT.OUT, StartRequest_RS.S
LevelBelow40_LT.OUT, StartRequest_RS.R
P-901_DS.ActiveIsA, SelectedA_AND.IN1
P-901A.FB_Running, SelectedA_AND.IN2
P-901_DS.ActiveIsA, ActiveIsA_NOT.IN
ActiveIsA_NOT.OUT, SelectedB_AND.IN1
P-901B.FB_Running, SelectedB_AND.IN2
SelectedA_AND.OUT, SelectedRun_OR.IN1
SelectedB_AND.OUT, SelectedRun_OR.IN2
SelectedRun_OR.OUT, DutyPeriod_TON.IN
DutyPeriod_TON.Q, P-901_DS.DutyElapsed
SelectedRun_OR.OUT, MinRun_TON.IN
MinRun_TON.Q, P-901_DS.MinRunElapsed
P-901A.FB_Running, PumpA_Fail_AND.IN1
FT-901.Low_Alarm, PumpA_Fail_AND.IN2
PumpA_Fail_AND.OUT, PumpA_Fail_TON.IN
PumpA_Fail_TON.Q, P-901_DS.PumpA_Fault
P-901B.FB_Running, PumpB_Fail_AND.IN1
FT-901.Low_Alarm, PumpB_Fail_AND.IN2
PumpB_Fail_AND.OUT, PumpB_Fail_TON.IN
PumpB_Fail_TON.Q, P-901_DS.PumpB_Fault
PumpA_Fail_TON.Q, FailAny_OR.IN1
PumpB_Fail_TON.Q, FailAny_OR.IN2
FailAny_OR.OUT, SwitchoverDelay_TON.IN
SwitchoverDelay_TON.Q, P-901_DS.SwitchoverDelayElapsed
StartRequest_RS.Q, P-901_DS.StartRequest
P-901_DS.CmdPumpA, StartA_OR.IN1
LevelAbove85_GT.OUT, StartA_OR.IN2
StartA_OR.OUT, StartA_NOT.IN
StartA_OR.OUT, P-901A.Start_Cmd
StartA_NOT.OUT, P-901A.Stop_Cmd
P-901_DS.CmdPumpB, StartB_OR.IN1
LevelAbove85_GT.OUT, StartB_OR.IN2
StartB_OR.OUT, StartB_NOT.IN
StartB_OR.OUT, P-901B.Start_Cmd
StartB_NOT.OUT, P-901B.Stop_Cmd
P-901A.FB_Running, P-901_DS.PumpA_RunFB
P-901B.FB_Running, P-901_DS.PumpB_RunFB
LS-901.Low_Alarm, PumpA_Inhibit_OR.IN1
PumpA_Fail_AND.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, P-901A.Inhibit
LS-901.Low_Alarm, PumpB_Inhibit_OR.IN1
PumpB_Fail_AND.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, P-901B.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Inhibit
P-901_DS.Alarm_NoAvailablePump, XV-102.Close_Cmd
FT-901.PV, FT-901_Flow_PV
LS-901.PV, LS-901_Level_PV
P-901A.Motor_Start_Out, P-901A_MotorStartOut
P-901B.Motor_Start_Out, P-901B_MotorStartOut
XV-102.Valve_Close_Out, XV-102_CloseOut

* Parameter Data Connections *
60.0, LevelAbove60_GT.IN2
40.0, LevelBelow40_LT.IN2
85.0, LevelAbove85_GT.IN2
T#48h, DutyPeriod_TON.PT
T#30m, MinRun_TON.PT
T#10s, PumpA_Fail_TON.PT
T#10s, PumpB_Fail_TON.PT
T#5s, SwitchoverDelay_TON.PT
40.0, LS-901.PV_Low
90.0, LS-901.PV_High
TRUE, LS-901.Alarm_Enable
15.0, FT-901.PV_Low
TRUE, FT-901.Alarm_Enable
T#30m, P-901A.MinRunTime
T#30m, P-901B.MinRunTime
TRUE, P-901_DS.Enable
TRUE, P-901_DS.AlternateEnable
```

---


