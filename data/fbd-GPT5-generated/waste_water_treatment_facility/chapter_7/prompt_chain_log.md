# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 10:50:42

## Step 1: contextgen1-sensors
**Time:** 10:50:42

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
**Time:** 10:51:17

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
**Time:** 10:51:42

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|------------------|-------------|
| Duty-Standby | 0.98 |
| PID Control | 0.32 |
| OVERRIDE | 0.18 |
| VOTING | 0.05 |
| Cascade Control | 0.04 |
| FEEDFORWARD | 0.03 |
| SPLIT RANGE | 0.03 |
| Ratio Control | 0.02 |

Selected Control Strategy: Duty-Standby
Short explanation: The narrative centers on redundant lead/lag operation with automatic switchover on fault, runtime-based alternation, and enforced minimum run times—hallmarks of a duty/standby strategy.

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
**Timestamp:** 2025-09-24 10:52:47

## Step 1: openplc-function-blocks-v2
**Time:** 10:52:47

### Output:
```
* Function Blocks *
BOOL_IN LS-601
ANALOG_IN PT-601A
ANALOG_IN PT-601B
MOTOR_ON_OFF CL-601A
MOTOR_ON_OFF CL-601B
MOTOR_ON_OFF PS-601A
MOTOR_ON_OFF PS-601B
VALVE_ELECTRIC VS-601A
VALVE_ELECTRIC VS-601B
DUTY_STANDBY CL-601_DUTY_STANDBY
DUTY_STANDBY PS-601_DUTY_STANDBY
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 10:53:33

### Output:
```
* Function Block List * 
* Function Blocks *
BOOL_IN LS-601
ANALOG_IN PT-601A
ANALOG_IN PT-601B
MOTOR_ON_OFF CL-601A
MOTOR_ON_OFF CL-601B
MOTOR_ON_OFF PS-601A
MOTOR_ON_OFF PS-601B
VALVE_ELECTRIC VS-601A
VALVE_ELECTRIC VS-601B
DUTY_STANDBY CL-601_DUTY_STANDBY
DUTY_STANDBY PS-601_DUTY_STANDBY
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 10:54:42

### Output:
```
* Functions *
EQ AlwaysTrue_EQ_EQ
OR CL_Run_OR_OR
NOT CL_NotRunning_NOT
TON CL_DutyTimer_TON
TON CL_MinRun_TON
TON CL_SwitchoverDelay_TON
OR PS_Run_OR_OR
NOT PS_NotRunning_NOT
TON PS_DutyTimer_TON
TON PS_MinRun_TON
TON PS_SwitchoverDelay_TON

* Block-to-Block Connections *
LS-601.Bool_Out, AlwaysTrue_EQ_EQ.IN1
LS-601.Bool_Out, AlwaysTrue_EQ_EQ.IN2
AlwaysTrue_EQ_EQ.OUT, CL-601_DUTY_STANDBY.Enable
AlwaysTrue_EQ_EQ.OUT, CL-601_DUTY_STANDBY.StartRequest
AlwaysTrue_EQ_EQ.OUT, CL-601_DUTY_STANDBY.AlternateEnable
AlwaysTrue_EQ_EQ.OUT, PS-601_DUTY_STANDBY.Enable
AlwaysTrue_EQ_EQ.OUT, PS-601_DUTY_STANDBY.StartRequest
AlwaysTrue_EQ_EQ.OUT, PS-601_DUTY_STANDBY.AlternateEnable
CL-601A.FB_Running, CL_Run_OR_OR.IN1
CL-601B.FB_Running, CL_Run_OR_OR.IN2
CL_Run_OR_OR.OUT, CL_DutyTimer_TON.IN
CL_Run_OR_OR.OUT, CL_MinRun_TON.IN
CL_Run_OR_OR.OUT, CL_NotRunning_NOT.IN
CL_NotRunning_NOT.OUT, CL_SwitchoverDelay_TON.IN
CL_DutyTimer_TON.Q, CL-601_DUTY_STANDBY.DutyElapsed
CL_MinRun_TON.Q, CL-601_DUTY_STANDBY.MinRunElapsed
CL_SwitchoverDelay_TON.Q, CL-601_DUTY_STANDBY.SwitchoverDelayElapsed
CL-601A.FB_Running, CL-601_DUTY_STANDBY.PumpA_RunFB
CL-601B.FB_Running, CL-601_DUTY_STANDBY.PumpB_RunFB
CL-601_DUTY_STANDBY.CmdPumpA, CL-601A.Start_Cmd
CL-601_DUTY_STANDBY.CmdPumpB, CL-601B.Start_Cmd
PS-601A.FB_Running, PS_Run_OR_OR.IN1
PS-601B.FB_Running, PS_Run_OR_OR.IN2
PS_Run_OR_OR.OUT, PS_DutyTimer_TON.IN
PS_Run_OR_OR.OUT, PS_MinRun_TON.IN
PS_Run_OR_OR.OUT, PS_NotRunning_NOT.IN
PS_NotRunning_NOT.OUT, PS_SwitchoverDelay_TON.IN
PS_DutyTimer_TON.Q, PS-601_DUTY_STANDBY.DutyElapsed
PS_MinRun_TON.Q, PS-601_DUTY_STANDBY.MinRunElapsed
PS_SwitchoverDelay_TON.Q, PS-601_DUTY_STANDBY.SwitchoverDelayElapsed
PS-601A.FB_Running, PS-601_DUTY_STANDBY.PumpA_RunFB
PS-601B.FB_Running, PS-601_DUTY_STANDBY.PumpB_RunFB
PS-601_DUTY_STANDBY.CmdPumpA, PS-601A.Start_Cmd
PS-601_DUTY_STANDBY.CmdPumpB, PS-601B.Start_Cmd
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 10:58:34

### Output:
```
* Functions * 
OR BlanketHigh_OR
OR PS601A_Inhibit_OR
OR PS601B_Inhibit_OR
OR CL601A_Inhibit_OR
OR CL601B_Inhibit_OR
OR SystemShutdown_OR

* Data Connections *
LS-601.Bool_Out, BlanketHigh_OR.IN1
LS-601.Alarm_Active, BlanketHigh_OR.IN2
BlanketHigh_OR.OUT, CL601A_Inhibit_OR.IN1
CL-601A.FB_Trip, CL601A_Inhibit_OR.IN2
CL601A_Inhibit_OR.OUT, CL-601A.Inhibit
BlanketHigh_OR.OUT, CL601B_Inhibit_OR.IN1
CL-601B.FB_Trip, CL601B_Inhibit_OR.IN2
CL601B_Inhibit_OR.OUT, CL-601B.Inhibit
PT-601A.Low_Alarm, PS601A_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PS601A_Inhibit_OR.IN2
PS601A_Inhibit_OR.OUT, PS-601A.Inhibit
PT-601B.Low_Alarm, PS601B_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PS601B_Inhibit_OR.IN2
PS601B_Inhibit_OR.OUT, PS-601B.Inhibit
BlanketHigh_OR.OUT, SystemShutdown_OR.IN1
PT-601A.Low_Alarm, SystemShutdown_OR.IN2
PT-601B.Low_Alarm, SystemShutdown_OR.IN3
SystemShutdown_OR.OUT, CL-601_DUTY_STANDBY.Inhibit
SystemShutdown_OR.OUT, PS-601_DUTY_STANDBY.Inhibit
LS-601.Bool_Out, CL-601A.Inhibit
LS-601.Bool_Out, CL-601B.Inhibit
LS-601.Bool_Out, PS-601A.Inhibit
LS-601.Bool_Out, PS-601B.Inhibit
LS-601.Bool_Out, CL-601_DUTY_STANDBY.Inhibit
LS-601.Bool_Out, PS-601_DUTY_STANDBY.Inhibit

* Parameter Data Connections *
25, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
TRUE, LS-601.Alarm_OnTrue
FALSE, LS-601.Alarm_OnFalse
TRUE, LS-601.Latch_Enable
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 11:00:20

### Output:
```
* Parameter Data Connections *
T#72H, CL_DutyTimer_TON.PT
T#30M, CL_MinRun_TON.PT
T#10S, CL_SwitchoverDelay_TON.PT
T#72H, PS_DutyTimer_TON.PT
T#30M, PS_MinRun_TON.PT
T#10S, PS_SwitchoverDelay_TON.PT
T#5S, CL-601A.Start_Delay
T#5S, CL-601B.Start_Delay
T#5S, PS-601A.Start_Delay
T#5S, PS-601B.Start_Delay
T#30M, CL-601A.MinRunTime
T#30M, CL-601B.MinRunTime
T#30M, PS-601A.MinRunTime
T#30M, PS-601B.MinRunTime
25.0, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25.0, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 11:01:38

### Output:
```
* Parameter Data Connections *
T#72H, CL_DutyTimer_TON.PT
T#30M, CL_MinRun_TON.PT
T#10S, CL_SwitchoverDelay_TON.PT
T#72H, PS_DutyTimer_TON.PT
T#30M, PS_MinRun_TON.PT
T#10S, PS_SwitchoverDelay_TON.PT
T#5S, CL-601A.Start_Delay
T#5S, CL-601B.Start_Delay
T#5S, PS-601A.Start_Delay
T#5S, PS-601B.Start_Delay
T#30M, CL-601A.MinRunTime
T#30M, CL-601B.MinRunTime
T#30M, PS-601A.MinRunTime
T#30M, PS-601B.MinRunTime
25.0, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25.0, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
TRUE, LS-601.Alarm_OnTrue
FALSE, LS-601.Alarm_OnFalse
TRUE, LS-601.Latch_Enable
100.0, VS-601A.Open_Limit
0.0, VS-601A.Close_Limit
100.0, VS-601B.Open_Limit
0.0, VS-601B.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 11:03:21

### Output:
```
* Variables *
REAL PT_601A_DischargePressure_PV
REAL PT_601B_DischargePressure_PV
BOOL LS_601_BlanketLevelSwitchStatus
BOOL CL_601A_Running
BOOL CL_601B_Running
BOOL PS_601A_Running
BOOL PS_601B_Running
REAL VS_601A_Feedback_Position_Pct
REAL VS_601B_Feedback_Position_Pct
BOOL CL_601_ActiveIsA
BOOL PS_601_ActiveIsA
BOOL CL_601A_RunCmd
BOOL CL_601B_RunCmd
BOOL PS_601A_RunCmd
BOOL PS_601B_RunCmd

* Data Connections *
PT-601A.PV, PT_601A_DischargePressure_PV
PT-601B.PV, PT_601B_DischargePressure_PV
LS-601.Bool_Out, LS_601_BlanketLevelSwitchStatus
CL-601A.FB_Running, CL_601A_Running
CL-601B.FB_Running, CL_601B_Running
PS-601A.FB_Running, PS_601A_Running
PS-601B.FB_Running, PS_601B_Running
VS-601A.Feedback_Pos, VS_601A_Feedback_Position_Pct
VS-601B.Feedback_Pos, VS_601B_Feedback_Position_Pct
CL-601_DUTY_STANDBY.ActiveIsA, CL_601_ActiveIsA
PS-601_DUTY_STANDBY.ActiveIsA, PS_601_ActiveIsA
CL-601_DUTY_STANDBY.CmdPumpA, CL_601A_RunCmd
CL-601_DUTY_STANDBY.CmdPumpB, CL_601B_RunCmd
PS-601_DUTY_STANDBY.CmdPumpA, PS_601A_RunCmd
PS-601_DUTY_STANDBY.CmdPumpB, PS_601B_RunCmd
```

---

## Step 8: openplc-rule-checks
**Time:** 11:05:58

### Output:
```
* Function Blocks *
BOOL_IN LS-601
ANALOG_IN PT-601A
ANALOG_IN PT-601B
MOTOR_ON_OFF CL-601A
MOTOR_ON_OFF CL-601B
MOTOR_ON_OFF PS-601A
MOTOR_ON_OFF PS-601B
VALVE_ELECTRIC VS-601A
VALVE_ELECTRIC VS-601B
DUTY_STANDBY CL-601_DUTY_STANDBY
DUTY_STANDBY PS-601_DUTY_STANDBY

* Variables *
REAL PT_601A_DischargePressure_PV
REAL PT_601B_DischargePressure_PV
BOOL LS_601_BlanketLevelSwitchStatus
BOOL CL_601A_Running
BOOL CL_601B_Running
BOOL PS_601A_Running
BOOL PS_601B_Running
REAL VS_601A_Feedback_Position_Pct
REAL VS_601B_Feedback_Position_Pct
BOOL CL_601_ActiveIsA
BOOL PS_601_ActiveIsA
BOOL CL_601A_RunCmd
BOOL CL_601B_RunCmd
BOOL PS_601A_RunCmd
BOOL PS_601B_RunCmd

* Functions *
EQ AutoEnable_EQ
OR ClarifierRun_OR
NOT ClarifierNotRunning_NOT
TON ClarifierDuty_TON
TON ClarifierMinRun_TON
TON ClarifierSwitchoverDelay_TON
OR PumpRun_OR
NOT PumpNotRunning_NOT
TON PumpDuty_TON
TON PumpMinRun_TON
TON PumpSwitchoverDelay_TON
OR BlanketHigh_OR
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR
OR ClarifierA_Inhibit_OR
OR ClarifierB_Inhibit_OR
OR SystemShutdown_OR
OR ClarifierFaultA_OR
OR ClarifierFaultB_OR
OR PumpFaultA_OR
OR PumpFaultB_OR

* Data Connections * 
LS-601.Bool_Out, AutoEnable_EQ.IN1
LS-601.Bool_Out, AutoEnable_EQ.IN2
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.AlternateEnable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.AlternateEnable
CL-601A.FB_Running, ClarifierRun_OR.IN1
CL-601B.FB_Running, ClarifierRun_OR.IN2
ClarifierRun_OR.OUT, ClarifierDuty_TON.IN
ClarifierRun_OR.OUT, ClarifierMinRun_TON.IN
ClarifierRun_OR.OUT, ClarifierNotRunning_NOT.IN
ClarifierNotRunning_NOT.OUT, ClarifierSwitchoverDelay_TON.IN
ClarifierDuty_TON.Q, CL-601_DUTY_STANDBY.DutyElapsed
ClarifierMinRun_TON.Q, CL-601_DUTY_STANDBY.MinRunElapsed
ClarifierSwitchoverDelay_TON.Q, CL-601_DUTY_STANDBY.SwitchoverDelayElapsed
CL-601A.FB_Running, CL-601_DUTY_STANDBY.PumpA_RunFB
CL-601B.FB_Running, CL-601_DUTY_STANDBY.PumpB_RunFB
CL-601_DUTY_STANDBY.CmdPumpA, CL-601A.Start_Cmd
CL-601_DUTY_STANDBY.CmdPumpB, CL-601B.Start_Cmd
PS-601A.FB_Running, PumpRun_OR.IN1
PS-601B.FB_Running, PumpRun_OR.IN2
PumpRun_OR.OUT, PumpDuty_TON.IN
PumpRun_OR.OUT, PumpMinRun_TON.IN
PumpRun_OR.OUT, PumpNotRunning_NOT.IN
PumpNotRunning_NOT.OUT, PumpSwitchoverDelay_TON.IN
PumpDuty_TON.Q, PS-601_DUTY_STANDBY.DutyElapsed
PumpMinRun_TON.Q, PS-601_DUTY_STANDBY.MinRunElapsed
PumpSwitchoverDelay_TON.Q, PS-601_DUTY_STANDBY.SwitchoverDelayElapsed
PS-601A.FB_Running, PS-601_DUTY_STANDBY.PumpA_RunFB
PS-601B.FB_Running, PS-601_DUTY_STANDBY.PumpB_RunFB
PS-601_DUTY_STANDBY.CmdPumpA, PS-601A.Start_Cmd
PS-601_DUTY_STANDBY.CmdPumpB, PS-601B.Start_Cmd
LS-601.Bool_Out, BlanketHigh_OR.IN1
LS-601.Alarm_Active, BlanketHigh_OR.IN2
BlanketHigh_OR.OUT, ClarifierA_Inhibit_OR.IN1
CL-601A.FB_Trip, ClarifierA_Inhibit_OR.IN2
ClarifierA_Inhibit_OR.OUT, CL-601A.Inhibit
BlanketHigh_OR.OUT, ClarifierB_Inhibit_OR.IN1
CL-601B.FB_Trip, ClarifierB_Inhibit_OR.IN2
ClarifierB_Inhibit_OR.OUT, CL-601B.Inhibit
PT-601A.Low_Alarm, PumpA_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, PS-601A.Inhibit
PT-601B.Low_Alarm, PumpB_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, PS-601B.Inhibit
BlanketHigh_OR.OUT, SystemShutdown_OR.IN1
PT-601A.Low_Alarm, SystemShutdown_OR.IN2
PT-601B.Low_Alarm, SystemShutdown_OR.IN3
SystemShutdown_OR.OUT, CL-601_DUTY_STANDBY.Inhibit
SystemShutdown_OR.OUT, PS-601_DUTY_STANDBY.Inhibit
CL-601A.FB_Trip, ClarifierFaultA_OR.IN1
BlanketHigh_OR.OUT, ClarifierFaultA_OR.IN2
ClarifierFaultA_OR.OUT, CL-601_DUTY_STANDBY.PumpA_Fault
CL-601B.FB_Trip, ClarifierFaultB_OR.IN1
BlanketHigh_OR.OUT, ClarifierFaultB_OR.IN2
ClarifierFaultB_OR.OUT, CL-601_DUTY_STANDBY.PumpB_Fault
PS-601A.FB_Trip, PumpFaultA_OR.IN1
PT-601A.Low_Alarm, PumpFaultA_OR.IN2
PumpFaultA_OR.OUT, PS-601_DUTY_STANDBY.PumpA_Fault
PS-601B.FB_Trip, PumpFaultB_OR.IN1
PT-601B.Low_Alarm, PumpFaultB_OR.IN2
PumpFaultB_OR.OUT, PS-601_DUTY_STANDBY.PumpB_Fault
PT-601A.PV, PT_601A_DischargePressure_PV
PT-601B.PV, PT_601B_DischargePressure_PV
LS-601.Bool_Out, LS_601_BlanketLevelSwitchStatus
CL-601A.FB_Running, CL_601A_Running
CL-601B.FB_Running, CL_601B_Running
PS-601A.FB_Running, PS_601A_Running
PS-601B.FB_Running, PS_601B_Running
VS-601A.Feedback_Pos, VS_601A_Feedback_Position_Pct
VS-601B.Feedback_Pos, VS_601B_Feedback_Position_Pct
CL-601_DUTY_STANDBY.ActiveIsA, CL_601_ActiveIsA
PS-601_DUTY_STANDBY.ActiveIsA, PS_601_ActiveIsA
CL-601_DUTY_STANDBY.CmdPumpA, CL_601A_RunCmd
CL-601_DUTY_STANDBY.CmdPumpB, CL_601B_RunCmd
PS-601_DUTY_STANDBY.CmdPumpA, PS_601A_RunCmd
PS-601_DUTY_STANDBY.CmdPumpB, PS_601B_RunCmd

* Parameter Data Connections *
T#72H, ClarifierDuty_TON.PT
T#30M, ClarifierMinRun_TON.PT
T#10S, ClarifierSwitchoverDelay_TON.PT
T#72H, PumpDuty_TON.PT
T#30M, PumpMinRun_TON.PT
T#10S, PumpSwitchoverDelay_TON.PT
T#5S, CL-601A.Start_Delay
T#5S, CL-601B.Start_Delay
T#5S, PS-601A.Start_Delay
T#5S, PS-601B.Start_Delay
T#30M, CL-601A.MinRunTime
T#30M, CL-601B.MinRunTime
T#30M, PS-601A.MinRunTime
T#30M, PS-601B.MinRunTime
25.0, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25.0, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
TRUE, LS-601.Alarm_OnTrue
FALSE, LS-601.Alarm_OnFalse
TRUE, LS-601.Latch_Enable
100.0, VS-601A.Open_Limit
0.0, VS-601A.Close_Limit
100.0, VS-601B.Open_Limit
0.0, VS-601B.Close_Limit
```

---

## Step 9: openplc-rule-checks2
**Time:** 11:08:43

### Output:
```
* Function Blocks *
BOOL_IN LS-601
ANALOG_IN PT-601A
ANALOG_IN PT-601B
MOTOR_ON_OFF CL-601A
MOTOR_ON_OFF CL-601B
MOTOR_ON_OFF PS-601A
MOTOR_ON_OFF PS-601B
VALVE_ELECTRIC VS-601A
VALVE_ELECTRIC VS-601B
DUTY_STANDBY CL-601_DUTY_STANDBY
DUTY_STANDBY PS-601_DUTY_STANDBY

* Variables *
REAL PT_601A_DischargePressure_PV
REAL PT_601B_DischargePressure_PV
BOOL LS_601_BlanketLevelSwitchStatus
BOOL CL_601A_Running
BOOL CL_601B_Running
BOOL PS_601A_Running
BOOL PS_601B_Running
REAL VS_601A_Feedback_Position_Pct
REAL VS_601B_Feedback_Position_Pct
BOOL CL_601_ActiveIsA
BOOL PS_601_ActiveIsA
BOOL CL_601A_RunCmd
BOOL CL_601B_RunCmd
BOOL PS_601A_RunCmd
BOOL PS_601B_RunCmd

* Functions *
EQ AutoEnable_EQ
OR ClarifierRun_OR
NOT ClarifierNotRunning_NOT
TON ClarifierDuty_TON
TON ClarifierMinRun_TON
TON ClarifierSwitchoverDelay_TON
OR PumpRun_OR
NOT PumpNotRunning_NOT
TON PumpDuty_TON
TON PumpMinRun_TON
TON PumpSwitchoverDelay_TON
OR BlanketHigh_OR
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR
OR ClarifierA_Inhibit_OR
OR ClarifierB_Inhibit_OR
OR SystemShutdown_OR
OR ClarifierFaultA_OR
OR ClarifierFaultB_OR
OR PumpFaultA_OR
OR PumpFaultB_OR

* Data Connections * 
LS-601.Bool_Out, AutoEnable_EQ.IN1
LS-601.Bool_Out, AutoEnable_EQ.IN2
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.AlternateEnable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.AlternateEnable
CL-601A.FB_Running, ClarifierRun_OR.IN1
CL-601B.FB_Running, ClarifierRun_OR.IN2
ClarifierRun_OR.OUT, ClarifierDuty_TON.IN
ClarifierRun_OR.OUT, ClarifierMinRun_TON.IN
ClarifierRun_OR.OUT, ClarifierNotRunning_NOT.IN
ClarifierNotRunning_NOT.OUT, ClarifierSwitchoverDelay_TON.IN
ClarifierDuty_TON.Q, CL-601_DUTY_STANDBY.DutyElapsed
ClarifierMinRun_TON.Q, CL-601_DUTY_STANDBY.MinRunElapsed
ClarifierSwitchoverDelay_TON.Q, CL-601_DUTY_STANDBY.SwitchoverDelayElapsed
CL-601A.FB_Running, CL-601_DUTY_STANDBY.PumpA_RunFB
CL-601B.FB_Running, CL-601_DUTY_STANDBY.PumpB_RunFB
CL-601_DUTY_STANDBY.CmdPumpA, CL-601A.Start_Cmd
CL-601_DUTY_STANDBY.CmdPumpB, CL-601B.Start_Cmd
PS-601A.FB_Running, PumpRun_OR.IN1
PS-601B.FB_Running, PumpRun_OR.IN2
PumpRun_OR.OUT, PumpDuty_TON.IN
PumpRun_OR.OUT, PumpMinRun_TON.IN
PumpRun_OR.OUT, PumpNotRunning_NOT.IN
PumpNotRunning_NOT.OUT, PumpSwitchoverDelay_TON.IN
PumpDuty_TON.Q, PS-601_DUTY_STANDBY.DutyElapsed
PumpMinRun_TON.Q, PS-601_DUTY_STANDBY.MinRunElapsed
PumpSwitchoverDelay_TON.Q, PS-601_DUTY_STANDBY.SwitchoverDelayElapsed
PS-601A.FB_Running, PS-601_DUTY_STANDBY.PumpA_RunFB
PS-601B.FB_Running, PS-601_DUTY_STANDBY.PumpB_RunFB
PS-601_DUTY_STANDBY.CmdPumpA, PS-601A.Start_Cmd
PS-601_DUTY_STANDBY.CmdPumpB, PS-601B.Start_Cmd
LS-601.Bool_Out, BlanketHigh_OR.IN1
LS-601.Alarm_Active, BlanketHigh_OR.IN2
BlanketHigh_OR.OUT, ClarifierA_Inhibit_OR.IN1
CL-601A.FB_Trip, ClarifierA_Inhibit_OR.IN2
ClarifierA_Inhibit_OR.OUT, CL-601A.Inhibit
BlanketHigh_OR.OUT, ClarifierB_Inhibit_OR.IN1
CL-601B.FB_Trip, ClarifierB_Inhibit_OR.IN2
ClarifierB_Inhibit_OR.OUT, CL-601B.Inhibit
PT-601A.Low_Alarm, PumpA_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, PS-601A.Inhibit
PT-601B.Low_Alarm, PumpB_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, PS-601B.Inhibit
BlanketHigh_OR.OUT, SystemShutdown_OR.IN1
PT-601A.Low_Alarm, SystemShutdown_OR.IN2
PT-601B.Low_Alarm, SystemShutdown_OR.IN3
SystemShutdown_OR.OUT, CL-601_DUTY_STANDBY.Inhibit
SystemShutdown_OR.OUT, PS-601_DUTY_STANDBY.Inhibit
CL-601A.FB_Trip, ClarifierFaultA_OR.IN1
BlanketHigh_OR.OUT, ClarifierFaultA_OR.IN2
ClarifierFaultA_OR.OUT, CL-601_DUTY_STANDBY.PumpA_Fault
CL-601B.FB_Trip, ClarifierFaultB_OR.IN1
BlanketHigh_OR.OUT, ClarifierFaultB_OR.IN2
ClarifierFaultB_OR.OUT, CL-601_DUTY_STANDBY.PumpB_Fault
PS-601A.FB_Trip, PumpFaultA_OR.IN1
PT-601A.Low_Alarm, PumpFaultA_OR.IN2
PumpFaultA_OR.OUT, PS-601_DUTY_STANDBY.PumpA_Fault
PS-601B.FB_Trip, PumpFaultB_OR.IN1
PT-601B.Low_Alarm, PumpFaultB_OR.IN2
PumpFaultB_OR.OUT, PS-601_DUTY_STANDBY.PumpB_Fault
PT-601A.PV, PT_601A_DischargePressure_PV
PT-601B.PV, PT_601B_DischargePressure_PV
LS-601.Bool_Out, LS_601_BlanketLevelSwitchStatus
CL-601A.FB_Running, CL_601A_Running
CL-601B.FB_Running, CL_601B_Running
PS-601A.FB_Running, PS_601A_Running
PS-601B.FB_Running, PS_601B_Running
VS-601A.Feedback_Pos, VS_601A_Feedback_Position_Pct
VS-601B.Feedback_Pos, VS_601B_Feedback_Position_Pct
CL-601_DUTY_STANDBY.ActiveIsA, CL_601_ActiveIsA
PS-601_DUTY_STANDBY.ActiveIsA, PS_601_ActiveIsA
CL-601_DUTY_STANDBY.CmdPumpA, CL_601A_RunCmd
CL-601_DUTY_STANDBY.CmdPumpB, CL_601B_RunCmd
PS-601_DUTY_STANDBY.CmdPumpA, PS_601A_RunCmd
PS-601_DUTY_STANDBY.CmdPumpB, PS_601B_RunCmd

* Parameter Data Connections *
T#72H, ClarifierDuty_TON.PT
T#30M, ClarifierMinRun_TON.PT
T#10S, ClarifierSwitchoverDelay_TON.PT
T#72H, PumpDuty_TON.PT
T#30M, PumpMinRun_TON.PT
T#10S, PumpSwitchoverDelay_TON.PT
T#5S, CL-601A.Start_Delay
T#5S, CL-601B.Start_Delay
T#5S, PS-601A.Start_Delay
T#5S, PS-601B.Start_Delay
T#30M, CL-601A.MinRunTime
T#30M, CL-601B.MinRunTime
T#30M, PS-601A.MinRunTime
T#30M, PS-601B.MinRunTime
25.0, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25.0, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
TRUE, LS-601.Alarm_OnTrue
FALSE, LS-601.Alarm_OnFalse
TRUE, LS-601.Latch_Enable
100.0, VS-601A.Open_Limit
0.0, VS-601A.Close_Limit
100.0, VS-601B.Open_Limit
0.0, VS-601B.Close_Limit
```

---

## Step 10: append_two_inputs
**Time:** 11:09:14

### Output:
```
* Function Blocks *
BOOL_IN LS-601
ANALOG_IN PT-601A
ANALOG_IN PT-601B
MOTOR_ON_OFF CL-601A
MOTOR_ON_OFF CL-601B
MOTOR_ON_OFF PS-601A
MOTOR_ON_OFF PS-601B
VALVE_ELECTRIC VS-601A
VALVE_ELECTRIC VS-601B
DUTY_STANDBY CL-601_DUTY_STANDBY
DUTY_STANDBY PS-601_DUTY_STANDBY

* Variables *
REAL PT_601A_DischargePressure_PV
REAL PT_601B_DischargePressure_PV
BOOL LS_601_BlanketLevelSwitchStatus
BOOL CL_601A_Running
BOOL CL_601B_Running
BOOL PS_601A_Running
BOOL PS_601B_Running
REAL VS_601A_Feedback_Position_Pct
REAL VS_601B_Feedback_Position_Pct
BOOL CL_601_ActiveIsA
BOOL PS_601_ActiveIsA
BOOL CL_601A_RunCmd
BOOL CL_601B_RunCmd
BOOL PS_601A_RunCmd
BOOL PS_601B_RunCmd

* Functions *
OR ClarifierRun_OR
NOT ClarifierNotRunning_NOT
TON ClarifierDuty_TON
TON ClarifierMinRun_TON
TON ClarifierSwitchoverDelay_TON
OR PumpRun_OR
NOT PumpNotRunning_NOT
TON PumpDuty_TON
TON PumpMinRun_TON
TON PumpSwitchoverDelay_TON
OR BlanketHigh_OR
OR PumpA_Inhibit_OR
OR PumpB_Inhibit_OR
OR ClarifierA_Inhibit_OR
OR ClarifierB_Inhibit_OR
OR SystemShutdown_OR
OR PumpFaultA_OR
OR PumpFaultB_OR

* Data Connections * 
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, CL-601_DUTY_STANDBY.AlternateEnable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.Enable
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.StartRequest
AutoEnable_EQ.OUT, PS-601_DUTY_STANDBY.AlternateEnable
CL-601A.FB_Running, ClarifierRun_OR.IN1
CL-601B.FB_Running, ClarifierRun_OR.IN2
ClarifierRun_OR.OUT, ClarifierDuty_TON.IN
ClarifierRun_OR.OUT, ClarifierMinRun_TON.IN
ClarifierRun_OR.OUT, ClarifierNotRunning_NOT.IN
ClarifierNotRunning_NOT.OUT, ClarifierSwitchoverDelay_TON.IN
ClarifierDuty_TON.Q, CL-601_DUTY_STANDBY.DutyElapsed
ClarifierMinRun_TON.Q, CL-601_DUTY_STANDBY.MinRunElapsed
ClarifierSwitchoverDelay_TON.Q, CL-601_DUTY_STANDBY.SwitchoverDelayElapsed
CL-601A.FB_Running, CL-601_DUTY_STANDBY.PumpA_RunFB
CL-601B.FB_Running, CL-601_DUTY_STANDBY.PumpB_RunFB
CL-601_DUTY_STANDBY.CmdPumpA, CL-601A.Start_Cmd
CL-601_DUTY_STANDBY.CmdPumpB, CL-601B.Start_Cmd
PS-601A.FB_Running, PumpRun_OR.IN1
PS-601B.FB_Running, PumpRun_OR.IN2
PumpRun_OR.OUT, PumpDuty_TON.IN
PumpRun_OR.OUT, PumpMinRun_TON.IN
PumpRun_OR.OUT, PumpNotRunning_NOT.IN
PumpNotRunning_NOT.OUT, PumpSwitchoverDelay_TON.IN
PumpDuty_TON.Q, PS-601_DUTY_STANDBY.DutyElapsed
PumpMinRun_TON.Q, PS-601_DUTY_STANDBY.MinRunElapsed
PumpSwitchoverDelay_TON.Q, PS-601_DUTY_STANDBY.SwitchoverDelayElapsed
PS-601A.FB_Running, PS-601_DUTY_STANDBY.PumpA_RunFB
PS-601B.FB_Running, PS-601_DUTY_STANDBY.PumpB_RunFB
PS-601_DUTY_STANDBY.CmdPumpA, PS-601A.Start_Cmd
PS-601_DUTY_STANDBY.CmdPumpB, PS-601B.Start_Cmd
LS-601.Bool_Out, BlanketHigh_OR.IN1
LS-601.Alarm_Active, BlanketHigh_OR.IN2
BlanketHigh_OR.OUT, ClarifierA_Inhibit_OR.IN1
CL-601A.FB_Trip, ClarifierA_Inhibit_OR.IN2
ClarifierA_Inhibit_OR.OUT, CL-601A.Inhibit
ClarifierA_Inhibit_OR.OUT, CL-601_DUTY_STANDBY.PumpA_Fault
BlanketHigh_OR.OUT, ClarifierB_Inhibit_OR.IN1
CL-601B.FB_Trip, ClarifierB_Inhibit_OR.IN2
ClarifierB_Inhibit_OR.OUT, CL-601B.Inhibit
ClarifierB_Inhibit_OR.OUT, CL-601_DUTY_STANDBY.PumpB_Fault
PT-601A.Low_Alarm, PumpA_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpA_Inhibit_OR.IN2
PumpA_Inhibit_OR.OUT, PS-601A.Inhibit
PT-601B.Low_Alarm, PumpB_Inhibit_OR.IN1
BlanketHigh_OR.OUT, PumpB_Inhibit_OR.IN2
PumpB_Inhibit_OR.OUT, PS-601B.Inhibit
BlanketHigh_OR.OUT, SystemShutdown_OR.IN1
PT-601A.Low_Alarm, SystemShutdown_OR.IN2
PT-601B.Low_Alarm, SystemShutdown_OR.IN3
SystemShutdown_OR.OUT, CL-601_DUTY_STANDBY.Inhibit
SystemShutdown_OR.OUT, PS-601_DUTY_STANDBY.Inhibit
PS-601A.FB_Trip, PumpFaultA_OR.IN1
PT-601A.Low_Alarm, PumpFaultA_OR.IN2
PumpFaultA_OR.OUT, PS-601_DUTY_STANDBY.PumpA_Fault
PS-601B.FB_Trip, PumpFaultB_OR.IN1
PT-601B.Low_Alarm, PumpFaultB_OR.IN2
PumpFaultB_OR.OUT, PS-601_DUTY_STANDBY.PumpB_Fault
PT-601A.PV, PT_601A_DischargePressure_PV
PT-601B.PV, PT_601B_DischargePressure_PV
LS-601.Bool_Out, LS_601_BlanketLevelSwitchStatus
CL-601A.FB_Running, CL_601A_Running
CL-601B.FB_Running, CL_601B_Running
PS-601A.FB_Running, PS_601A_Running
PS-601B.FB_Running, PS_601B_Running
VS-601A.Feedback_Pos, VS_601A_Feedback_Position_Pct
VS-601B.Feedback_Pos, VS_601B_Feedback_Position_Pct
CL-601_DUTY_STANDBY.ActiveIsA, CL_601_ActiveIsA
PS-601_DUTY_STANDBY.ActiveIsA, PS_601_ActiveIsA
CL-601_DUTY_STANDBY.CmdPumpA, CL_601A_RunCmd
CL-601_DUTY_STANDBY.CmdPumpB, CL_601B_RunCmd
PS-601_DUTY_STANDBY.CmdPumpA, PS_601A_RunCmd
PS-601_DUTY_STANDBY.CmdPumpB, PS_601B_RunCmd

* Parameter Data Connections *
T#72H, ClarifierDuty_TON.PT
T#30M, ClarifierMinRun_TON.PT
T#10S, ClarifierSwitchoverDelay_TON.PT
T#72H, PumpDuty_TON.PT
T#30M, PumpMinRun_TON.PT
T#10S, PumpSwitchoverDelay_TON.PT
T#5S, CL-601A.Start_Delay
T#5S, CL-601B.Start_Delay
T#5S, PS-601A.Start_Delay
T#5S, PS-601B.Start_Delay
T#30M, CL-601A.MinRunTime
T#30M, CL-601B.MinRunTime
T#30M, PS-601A.MinRunTime
T#30M, PS-601B.MinRunTime
25.0, PT-601A.PV_Low
TRUE, PT-601A.Alarm_Enable
25.0, PT-601B.PV_Low
TRUE, PT-601B.Alarm_Enable
TRUE, LS-601.Alarm_OnTrue
FALSE, LS-601.Alarm_OnFalse
TRUE, LS-601.Latch_Enable
100.0, VS-601A.Open_Limit
0.0, VS-601A.Close_Limit
100.0, VS-601B.Open_Limit
0.0, VS-601B.Close_Limit
TRUE, CL-601_DUTY_STANDBY.Enable
TRUE, CL-601_DUTY_STANDBY.StartRequest
TRUE, CL-601_DUTY_STANDBY.AlternateEnable
TRUE, PS-601_DUTY_STANDBY.Enable
TRUE, PS-601_DUTY_STANDBY.StartRequest
TRUE, PS-601_DUTY_STANDBY.AlternateEnable
```

---


