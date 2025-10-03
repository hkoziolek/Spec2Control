# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-23 20:55:12

## Step 1: contextgen1-sensors
**Time:** 20:55:12

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
**Time:** 20:55:42

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
**Time:** 20:56:08

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
|------------------|-------------|
| Duty-Standby | 0.99 |
| PID Control | 0.30 |

Selected Control Strategy: Duty-Standby
Short explanation: Two pumps operate in duty/standby with automatic switchover based on pressure and faults, with timers and minimum runtime—this matches the Duty-Standby strategy.

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
**Timestamp:** 2025-09-23 20:56:52

## Step 1: openplc-function-blocks-v2
**Time:** 20:56:52

### Output:
```
* Function Blocks *
ANALOG_IN FI-102
ANALOG_IN PI-102
VALVE_ELECTRIC LCV-102
MOTOR_ON_OFF P-102A
MOTOR_ON_OFF P-102B
DUTY_STANDBY P-102
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 20:57:28

### Output:
```
* Function Blocks *
ANALOG_IN FI-102
ANALOG_IN PI-102
VALVE_ELECTRIC LCV-102
BOOL_IN LIC-102
MOTOR_ON_OFF P-102A
MOTOR_ON_OFF P-102B
DUTY_STANDBY P-102
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 20:58:43

### Output:
```
* Functions *
NOT HighFlowInv_NOT
OR AlwaysTrue_OR
TON LowPress10s_TON
NOT NotActive_NOT
AND ActiveALowP_AND
AND NotActiveBLowP_AND
OR A_Fault_OR
OR B_Fault_OR
TON SwitchoverDelay5s_TON
OR CmdAorB_OR
TON MinRun30m_TON
OR B_Start_OR

* Block-to-Block Connections *
FI-102.High_Alarm, HighFlowInv_NOT.IN
HighFlowInv_NOT.OUT, AlwaysTrue_OR.IN2
FI-102.High_Alarm, AlwaysTrue_OR.IN1
AlwaysTrue_OR.OUT, P-102.Enable
AlwaysTrue_OR.OUT, P-102.StartRequest
PI-102.Low_Alarm, LowPress10s_TON.IN
LowPress10s_TON.Q, SwitchoverDelay5s_TON.IN
SwitchoverDelay5s_TON.Q, P-102.SwitchoverDelayElapsed
P-102.ActiveIsA, ActiveALowP_AND.IN1
LowPress10s_TON.Q, ActiveALowP_AND.IN2
P-102.ActiveIsA, NotActive_NOT.IN
NotActive_NOT.OUT, NotActiveBLowP_AND.IN1
LowPress10s_TON.Q, NotActiveBLowP_AND.IN2
P-102A.FB_Trip, A_Fault_OR.IN1
ActiveALowP_AND.OUT, A_Fault_OR.IN2
P-102B.FB_Trip, B_Fault_OR.IN1
NotActiveBLowP_AND.OUT, B_Fault_OR.IN2
A_Fault_OR.OUT, P-102.PumpA_Fault
B_Fault_OR.OUT, P-102.PumpB_Fault
P-102A.FB_Running, P-102.PumpA_RunFB
P-102B.FB_Running, P-102.PumpB_RunFB
P-102.CmdPumpA, P-102A.Start_Cmd
P-102.CmdPumpB, B_Start_OR.IN1
FI-102.High_Alarm, B_Start_OR.IN2
B_Start_OR.OUT, P-102B.Start_Cmd
P-102.CmdPumpA, CmdAorB_OR.IN1
P-102.CmdPumpB, CmdAorB_OR.IN2
CmdAorB_OR.OUT, MinRun30m_TON.IN
MinRun30m_TON.Q, P-102.MinRunElapsed
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 21:01:58

### Output:
```
* Functions * 
OR P102A_Inhib_OR
OR P102B_Inhib_OR

* Data Connections *
PI-102.Low_Alarm, P102A_Inhib_OR.IN1
P-102A.FB_Trip, P102A_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102A_Inhib_OR.IN3
P102A_Inhib_OR.OUT, P-102A.Inhibit
PI-102.Low_Alarm, P102B_Inhib_OR.IN1
P-102B.FB_Trip, P102B_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102B_Inhib_OR.IN3
P102B_Inhib_OR.OUT, P-102B.Inhibit
P-102.Alarm_NoAvailablePump, LCV-102.Inhibit

* Parameter Data Connections *
700, FI-102.PV_High
500, FI-102.PV_Low
25, PI-102.PV_Low
TRUE, FI-102.Alarm_Enable
TRUE, PI-102.Alarm_Enable
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 21:03:34

### Output:
```
* Parameter Data Connections *
700.0, FI-102.PV_High
TRUE, FI-102.Alarm_Enable
25.0, PI-102.PV_Low
TRUE, PI-102.Alarm_Enable
T#10s, LowPress10s_TON.PT
T#5s, SwitchoverDelay5s_TON.PT
T#30m, MinRun30m_TON.PT
T#30m, P-102A.MinRunTime
T#30m, P-102B.MinRunTime
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 21:04:42

### Output:
```
* Parameter Data Connections *
500.0, FI-102.PV_Low
700.0, FI-102.PV_High
TRUE, FI-102.Alarm_Enable
25.0, PI-102.PV_Low
TRUE, PI-102.Alarm_Enable
T#10s, LowPress10s_TON.PT
T#5s, SwitchoverDelay5s_TON.PT
T#30m, MinRun30m_TON.PT
T#30m, P-102A.MinRunTime
T#30m, P-102B.MinRunTime
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 21:06:07

### Output:
```
* Variables *
REAL FI102_FlowRate_PV
REAL PI102_Pressure_PV
BOOL LIC102_Level_StartPermissive
BOOL P102_ActiveIsA_Status

* Data Connections *
FI-102.PV, FI102_FlowRate_PV
PI-102.PV, PI102_Pressure_PV
LIC-102.Bool_Out, LIC102_Level_StartPermissive
P-102.ActiveIsA, P102_ActiveIsA_Status
```

---

## Step 8: openplc-rule-checks
**Time:** 21:07:41

### Output:
```
* Function Blocks *
ANALOG_IN FI-102
ANALOG_IN PI-102
VALVE_ELECTRIC LCV-102
BOOL_IN LIC-102
MOTOR_ON_OFF P-102A
MOTOR_ON_OFF P-102B
DUTY_STANDBY P-102

* Variables *
REAL FI102_FlowRate_PV
REAL PI102_Pressure_PV
BOOL LIC102_Level_StartPermissive
BOOL P102_ActiveIsA_Status

* Functions *
NOT NotActive_NOT
AND ActiveALowP_AND
AND NotActiveBLowP_AND
OR A_Fault_OR
OR B_Fault_OR
TON LowPress10s_TON
TON SwitchoverDelay5s_TON
OR CmdAorB_OR
TON MinRun30m_TON
OR B_Start_OR
OR P102A_Inhib_OR
OR P102B_Inhib_OR

* Data Connections *
LIC-102.Bool_Out, P-102.Enable
LIC-102.Bool_Out, P-102.StartRequest
PI-102.Low_Alarm, LowPress10s_TON.IN
LowPress10s_TON.Q, SwitchoverDelay5s_TON.IN
SwitchoverDelay5s_TON.Q, P-102.SwitchoverDelayElapsed
P-102.ActiveIsA, ActiveALowP_AND.IN1
LowPress10s_TON.Q, ActiveALowP_AND.IN2
P-102.ActiveIsA, NotActive_NOT.IN
NotActive_NOT.OUT, NotActiveBLowP_AND.IN1
LowPress10s_TON.Q, NotActiveBLowP_AND.IN2
P-102A.FB_Trip, A_Fault_OR.IN1
ActiveALowP_AND.OUT, A_Fault_OR.IN2
P-102B.FB_Trip, B_Fault_OR.IN1
NotActiveBLowP_AND.OUT, B_Fault_OR.IN2
A_Fault_OR.OUT, P-102.PumpA_Fault
B_Fault_OR.OUT, P-102.PumpB_Fault
P-102A.FB_Running, P-102.PumpA_RunFB
P-102B.FB_Running, P-102.PumpB_RunFB
P-102.CmdPumpA, P-102A.Start_Cmd
P-102.CmdPumpB, B_Start_OR.IN1
FI-102.High_Alarm, B_Start_OR.IN2
B_Start_OR.OUT, P-102B.Start_Cmd
P-102.CmdPumpA, CmdAorB_OR.IN1
P-102.CmdPumpB, CmdAorB_OR.IN2
CmdAorB_OR.OUT, MinRun30m_TON.IN
MinRun30m_TON.Q, P-102.MinRunElapsed
PI-102.Low_Alarm, P102A_Inhib_OR.IN1
P-102A.FB_Trip, P102A_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102A_Inhib_OR.IN3
P102A_Inhib_OR.OUT, P-102A.Inhibit
PI-102.Low_Alarm, P102B_Inhib_OR.IN1
P-102B.FB_Trip, P102B_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102B_Inhib_OR.IN3
P102B_Inhib_OR.OUT, P-102B.Inhibit
P-102.Alarm_NoAvailablePump, LCV-102.Inhibit
FI-102.PV, FI102_FlowRate_PV
PI-102.PV, PI102_Pressure_PV
LIC-102.Bool_Out, LIC102_Level_StartPermissive
P-102.ActiveIsA, P102_ActiveIsA_Status

* Parameter Data Connections *
700.0, FI-102.PV_High
500.0, FI-102.PV_Low
TRUE, FI-102.Alarm_Enable
25.0, PI-102.PV_Low
TRUE, PI-102.Alarm_Enable
T#10s, LowPress10s_TON.PT
T#5s, SwitchoverDelay5s_TON.PT
T#30m, MinRun30m_TON.PT
T#30m, P-102A.MinRunTime
T#30m, P-102B.MinRunTime
```

---

## Step 9: openplc-rule-checks2
**Time:** 21:09:35

### Output:
```
* Function Blocks *
ANALOG_IN FI-102
ANALOG_IN PI-102
VALVE_ELECTRIC LCV-102
BOOL_IN LIC-102
MOTOR_ON_OFF P-102A
MOTOR_ON_OFF P-102B
DUTY_STANDBY P-102

* Variables *
REAL FI102_FlowRate_PV
REAL PI102_Pressure_PV
BOOL LIC102_Level_StartPermissive
BOOL P102_ActiveIsA_Status

* Functions *
NOT NotActive_NOT
AND ActiveALowP_AND
AND NotActiveBLowP_AND
OR A_Fault_OR
OR B_Fault_OR
TON LowPress10s_TON
TON SwitchoverDelay5s_TON
OR CmdAorB_OR
TON MinRun30m_TON
OR B_Start_OR
OR P102A_Inhib_OR
OR P102B_Inhib_OR

* Data Connections *
LIC-102.Bool_Out, P-102.Enable
LIC-102.Bool_Out, P-102.StartRequest
PI-102.Low_Alarm, LowPress10s_TON.IN
LowPress10s_TON.Q, SwitchoverDelay5s_TON.IN
SwitchoverDelay5s_TON.Q, P-102.SwitchoverDelayElapsed
P-102.ActiveIsA, ActiveALowP_AND.IN1
LowPress10s_TON.Q, ActiveALowP_AND.IN2
P-102.ActiveIsA, NotActive_NOT.IN
NotActive_NOT.OUT, NotActiveBLowP_AND.IN1
LowPress10s_TON.Q, NotActiveBLowP_AND.IN2
P-102A.FB_Trip, A_Fault_OR.IN1
ActiveALowP_AND.OUT, A_Fault_OR.IN2
P-102B.FB_Trip, B_Fault_OR.IN1
NotActiveBLowP_AND.OUT, B_Fault_OR.IN2
A_Fault_OR.OUT, P-102.PumpA_Fault
B_Fault_OR.OUT, P-102.PumpB_Fault
P-102A.FB_Running, P-102.PumpA_RunFB
P-102B.FB_Running, P-102.PumpB_RunFB
P-102.CmdPumpA, P-102A.Start_Cmd
P-102.CmdPumpB, B_Start_OR.IN1
FI-102.High_Alarm, B_Start_OR.IN2
B_Start_OR.OUT, P-102B.Start_Cmd
P-102.CmdPumpA, CmdAorB_OR.IN1
P-102.CmdPumpB, CmdAorB_OR.IN2
CmdAorB_OR.OUT, MinRun30m_TON.IN
MinRun30m_TON.Q, P-102.MinRunElapsed
PI-102.Low_Alarm, P102A_Inhib_OR.IN1
P-102A.FB_Trip, P102A_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102A_Inhib_OR.IN3
P102A_Inhib_OR.OUT, P-102A.Inhibit
PI-102.Low_Alarm, P102B_Inhib_OR.IN1
P-102B.FB_Trip, P102B_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102B_Inhib_OR.IN3
P102B_Inhib_OR.OUT, P-102B.Inhibit
P-102.Alarm_NoAvailablePump, LCV-102.Inhibit
FI-102.PV, FI102_FlowRate_PV
PI-102.PV, PI102_Pressure_PV
LIC-102.Bool_Out, LIC102_Level_StartPermissive
P-102.ActiveIsA, P102_ActiveIsA_Status

* Parameter Data Connections *
700.0, FI-102.PV_High
500.0, FI-102.PV_Low
TRUE, FI-102.Alarm_Enable
25.0, PI-102.PV_Low
TRUE, PI-102.Alarm_Enable
T#10s, LowPress10s_TON.PT
T#5s, SwitchoverDelay5s_TON.PT
T#30m, MinRun30m_TON.PT
T#30m, P-102A.MinRunTime
T#30m, P-102B.MinRunTime
```

---

## Step 10: append_two_inputs
**Time:** 21:10:06

### Output:
```
* Function Blocks *
ANALOG_IN FI-102
ANALOG_IN PI-102
VALVE_ELECTRIC LCV-102
BOOL_IN LIC-102
MOTOR_ON_OFF P-102A
MOTOR_ON_OFF P-102B
DUTY_STANDBY P-102

* Variables *
REAL FI102_FlowRate_PV
REAL PI102_Pressure_PV
BOOL LIC102_Level_StartPermissive
BOOL P102_ActiveIsA_Status

* Functions *
NOT NotActive_NOT
AND ActiveALowP_AND
AND NotActiveBLowP_AND
OR A_Fault_OR
OR B_Fault_OR
TON LowPress10s_TON
TON SwitchoverDelay5s_TON
OR CmdAorB_OR
TON MinRun30m_TON
OR B_Start_OR
OR P102A_Inhib_OR
OR P102B_Inhib_OR

* Data Connections *
LIC-102.Bool_Out, P-102.Enable
LIC-102.Bool_Out, P-102.StartRequest
PI-102.Low_Alarm, LowPress10s_TON.IN
LowPress10s_TON.Q, SwitchoverDelay5s_TON.IN
SwitchoverDelay5s_TON.Q, P-102.SwitchoverDelayElapsed
P-102.ActiveIsA, ActiveALowP_AND.IN1
LowPress10s_TON.Q, ActiveALowP_AND.IN2
P-102.ActiveIsA, NotActive_NOT.IN
NotActive_NOT.OUT, NotActiveBLowP_AND.IN1
LowPress10s_TON.Q, NotActiveBLowP_AND.IN2
P-102A.FB_Trip, A_Fault_OR.IN1
ActiveALowP_AND.OUT, A_Fault_OR.IN2
P-102B.FB_Trip, B_Fault_OR.IN1
NotActiveBLowP_AND.OUT, B_Fault_OR.IN2
A_Fault_OR.OUT, P-102.PumpA_Fault
B_Fault_OR.OUT, P-102.PumpB_Fault
P-102A.FB_Running, P-102.PumpA_RunFB
P-102B.FB_Running, P-102.PumpB_RunFB
P-102.CmdPumpA, P-102A.Start_Cmd
P-102.CmdPumpB, B_Start_OR.IN1
FI-102.High_Alarm, B_Start_OR.IN2
B_Start_OR.OUT, P-102B.Start_Cmd
P-102.CmdPumpA, CmdAorB_OR.IN1
P-102.CmdPumpB, CmdAorB_OR.IN2
CmdAorB_OR.OUT, MinRun30m_TON.IN
MinRun30m_TON.Q, P-102.MinRunElapsed
PI-102.Low_Alarm, P102A_Inhib_OR.IN1
P-102A.FB_Trip, P102A_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102A_Inhib_OR.IN3
P102A_Inhib_OR.OUT, P-102A.Inhibit
PI-102.Low_Alarm, P102B_Inhib_OR.IN1
P-102B.FB_Trip, P102B_Inhib_OR.IN2
P-102.Alarm_NoAvailablePump, P102B_Inhib_OR.IN3
P102B_Inhib_OR.OUT, P-102B.Inhibit
P-102.Alarm_NoAvailablePump, LCV-102.Inhibit
FI-102.PV, FI102_FlowRate_PV
PI-102.PV, PI102_Pressure_PV
LIC-102.Bool_Out, LIC102_Level_StartPermissive
P-102.ActiveIsA, P102_ActiveIsA_Status

* Parameter Data Connections *
700.0, FI-102.PV_High
500.0, FI-102.PV_Low
TRUE, FI-102.Alarm_Enable
25.0, PI-102.PV_Low
TRUE, PI-102.Alarm_Enable
T#10s, LowPress10s_TON.PT
T#5s, SwitchoverDelay5s_TON.PT
T#30m, MinRun30m_TON.PT
T#30m, P-102A.MinRunTime
T#30m, P-102B.MinRunTime
```

---


