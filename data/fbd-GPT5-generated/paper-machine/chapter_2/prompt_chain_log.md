# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 02:02:11

## Step 1: contextgen1-sensors
**Time:** 02:02:11

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
**Time:** 02:02:57

### Output:
```
MOTOR_VSD
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of motor's purpose.
Input,Start_Cmd,BOOL,Command to start the VSD.
Input,Stop_Cmd,BOOL,Command to stop the VSD.
Input,Speed_SP,REAL,Desired speed setpoint (e.g., 0-100%).
Input,Accel_Ramp,TIME,Acceleration ramp time.
Input,Decel_Ramp,TIME,Deceleration ramp time.
Input,Inhibit,BOOL,Inhibits starting the motor and can receive alarm signals.
Output,Speed_Out,REAL,Analog output to VSD for speed command.
Output,FB_Running,BOOL,Feedback from VSD indicating it is running.
Output,FB_Fault,BOOL,Feedback from VSD indicating a fault.
Output,FB_Ready,BOOL,Feedback from VSD indicating it is ready to run.
Output,FB_ActualSpeed,REAL,Actual motor speed feedback from VSD.
Output,Alarm_Speed_Deviation,BOOL,Indicates a significant difference between commanded and actual speed.
Output,Alarm_Comm_Fail,BOOL,Indicates communication failure with VSD.

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
**Time:** 02:03:45

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
|------------------|-----------------------|
| PID Control | 0.95 |
| OVERRIDE | 0.70 |
| Split Range | 0.15 |
| Cascade Control | 0.10 |
| Feedforward | 0.05 |
| VOTING | 0.02 |
| Duty-Standby | 0.01 |
| Ratio Control | 0.01 |

Selected Control Strategy: PID Control 
Short explanation: The narrative describes a single-loop flow control using LT-101 feeding FC-101 to modulate the final actuator, with alarms, permissives, and anti-windup, which fits a standard PID control architecture.

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
**Timestamp:** 2025-09-24 02:04:19

## Step 1: openplc-function-blocks-v2
**Time:** 02:04:19

### Output:
```
* Function Blocks *
ANALOG_IN LT-101
PID_BASIC FC-101
MOTOR_VSD M-102
VALVE_ELECTRIC FV-106
VALVE_ELECTRIC LV-103
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-104
VALVE_ON_OFF XV-105
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 02:04:51

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN LT-101
PID_BASIC FC-101
MOTOR_VSD M-102
VALVE_ELECTRIC FV-106
VALVE_ELECTRIC LV-103
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-104
VALVE_ON_OFF XV-105
BOOL_IN ILK-FC-101-XV-102-OPEN
BOOL_IN ILK-FC-101-XV-104-OPEN
BOOL_IN ILK-FC-101-LT-101-VALID
BOOL_IN PERM-M-102-LV-103-LEVEL-ABOVE-20
BOOL_IN PERM-M-102-XV-105-CLOSED
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 02:05:43

### Output:
```
* Functions *

* Block-to-Block Connections *
LT-101.PV, FC-101.PV
FC-101.XOUT, FV-106.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 02:06:01

### Output:
```
* Functions * 
LT101Valid_NOT
FC101ValvesOpen_AND
FC101Interlock_AND
FC101Inhibit_NOT
FC101Fault_OR
M102Permissive_AND
M102PermissiveInhibit_NOT
M102Inhibit_OR

* Data Connections *
XV-102.FB_Opened, ILK-FC-101-XV-102-OPEN.Bool_In
XV-104.FB_Opened, ILK-FC-101-XV-104-OPEN.Bool_In
LT-101.General_Fault, LT101Valid_NOT.IN
LT101Valid_NOT.OUT, ILK-FC-101-LT-101-VALID.Bool_In
ILK-FC-101-XV-102-OPEN.Bool_Out, FC101ValvesOpen_AND.IN1
ILK-FC-101-XV-104-OPEN.Bool_Out, FC101ValvesOpen_AND.IN2
FC101ValvesOpen_AND.OUT, FC101Interlock_AND.IN1
ILK-FC-101-LT-101-VALID.Bool_Out, FC101Interlock_AND.IN2
FC101Interlock_AND.OUT, FC101Inhibit_NOT.IN
FC101Inhibit_NOT.OUT, FC101Fault_OR.IN1
M-102.FB_Fault, FC101Fault_OR.IN2
FC101Fault_OR.OUT, FC-101.Inhibit
XV-105.FB_Closed, PERM-M-102-XV-105-CLOSED.Bool_In
PERM-M-102-LV-103-LEVEL-ABOVE-20.Bool_Out, M102Permissive_AND.IN1
PERM-M-102-XV-105-CLOSED.Bool_Out, M102Permissive_AND.IN2
M102Permissive_AND.OUT, M102PermissiveInhibit_NOT.IN
M102PermissiveInhibit_NOT.OUT, M102Inhibit_OR.IN1
LT-101.General_Fault, M102Inhibit_OR.IN2
M-102.FB_Fault, M102Inhibit_OR.IN3
M102Inhibit_OR.OUT, M-102.Inhibit
M-102.FB_Fault, XV-102.Inhibit
M-102.FB_Fault, XV-104.Inhibit
LT-101.General_Fault, FV-106.Inhibit

* Parameter Data Connections *
380, LT-101.PV_High
20, LT-101.PV_Low
380, FC-101.PV_High
20, FC-101.PV_Low
25, FC-101.Deviation_Limit
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 02:07:27

### Output:
```
* Parameter Data Connections *
25.0, LT-101.Scaling_Slope
-100.0, LT-101.Scaling_Offset
TRUE, LT-101.Alarm_Enable
380.0, LT-101.PV_High
20.0, LT-101.PV_Low
250.0, FC-101.SP
0.0, FC-101.MV_MIN
100.0, FC-101.MV_MAX
3.0, FC-101.KP
1.2, FC-101.TR
0.3, FC-101.TD
380.0, FC-101.PV_High
20.0, FC-101.PV_Low
25.0, FC-101.Deviation_Limit
T#5s, FV-106.Timeout
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
FALSE, FV-106.Manual_Mode
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 02:08:24

### Output:
```
* Parameter Data Connections *
25.0, LT-101.Scaling_Slope
-100.0, LT-101.Scaling_Offset
TRUE, LT-101.Alarm_Enable
380.0, LT-101.PV_High
20.0, LT-101.PV_Low
250.0, FC-101.SP
0.0, FC-101.MV_MIN
100.0, FC-101.MV_MAX
3.0, FC-101.KP
1.2, FC-101.TR
0.3, FC-101.TD
380.0, FC-101.PV_High
20.0, FC-101.PV_Low
25.0, FC-101.Deviation_Limit
T#5s, FV-106.Timeout
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
FALSE, FV-106.Manual_Mode
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 02:09:25

### Output:
```
* Variables *
REAL LT101_Flow_PV_m3ph
REAL FC101_MV_Percent

* Data Connections *
LT-101.PV, LT101_Flow_PV_m3ph
FC-101.XOUT, FC101_MV_Percent
```

---

## Step 8: openplc-rule-checks
**Time:** 02:10:04

### Output:
```
* Function Blocks *
ANALOG_IN LT-101
PID_BASIC FC-101
MOTOR_VSD M-102
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-104
VALVE_ON_OFF XV-105
BOOL_IN ILK-FC-101-XV-102-OPEN
BOOL_IN ILK-FC-101-XV-104-OPEN
BOOL_IN ILK-FC-101-LT-101-VALID
BOOL_IN PERM-M-102-LEVEL-ABOVE-20
BOOL_IN PERM-M-102-XV-105-CLOSED

* Variables *
REAL LT101_Flow_PV_m3ph
REAL FC101_MV_Percent
BOOL HopperLevel_Above20

* Functions *
NOT LT101Valid_NOT
AND FC101ValvesOpen_AND
AND FC101Interlock_AND
NOT FC101Inhibit_NOT
OR FC101Fault_OR
AND M102Permissive_AND
NOT M102Permissive_NOT
OR M102Fault_OR
OR M102Inhibit_OR
NOT M102AllowedRun_NOT
AND M102Start_AND
TON M102RestartDelay_TON

* Data Connections * 
LT-101.PV, FC-101.PV
FC-101.XOUT, M-102.Speed_SP
XV-102.FB_Opened, ILK-FC-101-XV-102-OPEN.Bool_In
XV-104.FB_Opened, ILK-FC-101-XV-104-OPEN.Bool_In
LT-101.General_Fault, LT101Valid_NOT.IN
LT101Valid_NOT.OUT, ILK-FC-101-LT-101-VALID.Bool_In
ILK-FC-101-XV-102-OPEN.Bool_Out, FC101ValvesOpen_AND.IN1
ILK-FC-101-XV-104-OPEN.Bool_Out, FC101ValvesOpen_AND.IN2
FC101ValvesOpen_AND.OUT, FC101Interlock_AND.IN1
ILK-FC-101-LT-101-VALID.Bool_Out, FC101Interlock_AND.IN2
FC101Interlock_AND.OUT, FC-101.AUTO
FC101Interlock_AND.OUT, FC101Inhibit_NOT.IN
FC101Inhibit_NOT.OUT, FC101Fault_OR.IN1
M-102.FB_Fault, FC101Fault_OR.IN2
FC101Fault_OR.OUT, FC-101.Inhibit
XV-105.FB_Closed, PERM-M-102-XV-105-CLOSED.Bool_In
HopperLevel_Above20, PERM-M-102-LEVEL-ABOVE-20.Bool_In
PERM-M-102-LEVEL-ABOVE-20.Bool_Out, M102Permissive_AND.IN1
PERM-M-102-XV-105-CLOSED.Bool_Out, M102Permissive_AND.IN2
M102Permissive_AND.OUT, M102Permissive_NOT.IN
M102Permissive_NOT.OUT, M102Inhibit_OR.IN1
LT-101.General_Fault, M102Fault_OR.IN1
M-102.FB_Fault, M102Fault_OR.IN2
M102Fault_OR.OUT, M102Inhibit_OR.IN2
M102Inhibit_OR.OUT, M-102.Inhibit
M102Inhibit_OR.OUT, M-102.Stop_Cmd
M102Inhibit_OR.OUT, M102AllowedRun_NOT.IN
M102AllowedRun_NOT.OUT, M102RestartDelay_TON.IN
M102AllowedRun_NOT.OUT, M102Start_AND.IN1
M102RestartDelay_TON.Q, M102Start_AND.IN2
M102Start_AND.OUT, M-102.Start_Cmd
M-102.FB_Fault, XV-102.Inhibit
M-102.FB_Fault, XV-104.Inhibit
LT-101.General_Fault, FV-106.Inhibit
LT-101.PV, LT101_Flow_PV_m3ph
FC-101.XOUT, FC101_MV_Percent

* Parameter Data Connections *
25.0, LT-101.Scaling_Slope
-100.0, LT-101.Scaling_Offset
TRUE, LT-101.Alarm_Enable
380.0, LT-101.PV_High
20.0, LT-101.PV_Low
250.0, FC-101.SP
0.0, FC-101.MV_MIN
100.0, FC-101.MV_MAX
0.0, FC-101.X0
3.0, FC-101.KP
1.2, FC-101.TR
0.3, FC-101.TD
380.0, FC-101.PV_High
20.0, FC-101.PV_Low
25.0, FC-101.Deviation_Limit
T#5s, M-102.Accel_Ramp
T#5s, M-102.Decel_Ramp
T#5s, FV-106.Timeout
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
TRUE, FV-106.Manual_Mode
0.0, FV-106.Manual_Position
T#60s, M102RestartDelay_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 02:12:51

### Output:
```
* Function Blocks *
ANALOG_IN LT-101
PID_BASIC FC-101
MOTOR_VSD M-102
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-104
VALVE_ON_OFF XV-105
BOOL_IN ILK-FC-101-XV-102-OPEN
BOOL_IN ILK-FC-101-XV-104-OPEN
BOOL_IN ILK-FC-101-LT-101-VALID
BOOL_IN PERM-M-102-LEVEL-ABOVE-20
BOOL_IN PERM-M-102-XV-105-CLOSED
TON M102RestartDelay_TON

* Variables *
REAL LT101_Flow_PV_m3ph
REAL FC101_MV_Percent
BOOL HopperLevel_Above20

* Functions *
NOT LT101Valid_NOT
AND FC101ValvesOpen_AND
AND FC101Interlock_AND
NOT FC101Inhibit_NOT
OR FC101Fault_OR
AND M102Permissive_AND
NOT M102Permissive_NOT
OR M102Fault_OR
OR M102Inhibit_OR
NOT M102AllowedRun_NOT
AND M102Start_AND

* Data Connections * 
LT-101.PV, FC-101.PV
FC-101.XOUT, M-102.Speed_SP
XV-102.FB_Opened, ILK-FC-101-XV-102-OPEN.Bool_In
XV-104.FB_Opened, ILK-FC-101-XV-104-OPEN.Bool_In
LT-101.General_Fault, LT101Valid_NOT.IN
LT101Valid_NOT.OUT, ILK-FC-101-LT-101-VALID.Bool_In
ILK-FC-101-XV-102-OPEN.Bool_Out, FC101ValvesOpen_AND.IN1
ILK-FC-101-XV-104-OPEN.Bool_Out, FC101ValvesOpen_AND.IN2
FC101ValvesOpen_AND.OUT, FC101Interlock_AND.IN1
ILK-FC-101-LT-101-VALID.Bool_Out, FC101Interlock_AND.IN2
FC101Interlock_AND.OUT, FC-101.AUTO
FC101Interlock_AND.OUT, FC101Inhibit_NOT.IN
FC101Inhibit_NOT.OUT, FC101Fault_OR.IN1
M-102.FB_Fault, FC101Fault_OR.IN2
FC101Fault_OR.OUT, FC-101.Inhibit
XV-105.FB_Closed, PERM-M-102-XV-105-CLOSED.Bool_In
HopperLevel_Above20, PERM-M-102-LEVEL-ABOVE-20.Bool_In
PERM-M-102-LEVEL-ABOVE-20.Bool_Out, M102Permissive_AND.IN1
PERM-M-102-XV-105-CLOSED.Bool_Out, M102Permissive_AND.IN2
M102Permissive_AND.OUT, M102Permissive_NOT.IN
M102Permissive_NOT.OUT, M102Inhibit_OR.IN1
LT-101.General_Fault, M102Fault_OR.IN1
M-102.FB_Fault, M102Fault_OR.IN2
M102Fault_OR.OUT, M102Inhibit_OR.IN2
M102Inhibit_OR.OUT, M-102.Inhibit
M102Inhibit_OR.OUT, M-102.Stop_Cmd
M102Inhibit_OR.OUT, M102AllowedRun_NOT.IN
M102AllowedRun_NOT.OUT, M102RestartDelay_TON.IN
M102AllowedRun_NOT.OUT, M102Start_AND.IN1
M102RestartDelay_TON.Q, M102Start_AND.IN2
M102Start_AND.OUT, M-102.Start_Cmd
M-102.FB_Fault, XV-102.Inhibit
M-102.FB_Fault, XV-104.Inhibit
LT-101.General_Fault, FV-106.Inhibit
LT-101.PV, LT101_Flow_PV_m3ph
FC-101.XOUT, FC101_MV_Percent

* Parameter Data Connections *
25.0, LT-101.Scaling_Slope
-100.0, LT-101.Scaling_Offset
TRUE, LT-101.Alarm_Enable
380.0, LT-101.PV_High
20.0, LT-101.PV_Low
250.0, FC-101.SP
0.0, FC-101.MV_MIN
100.0, FC-101.MV_MAX
0.0, FC-101.X0
3.0, FC-101.KP
1.2, FC-101.TR
0.3, FC-101.TD
380.0, FC-101.PV_High
20.0, FC-101.PV_Low
25.0, FC-101.Deviation_Limit
T#5s, M-102.Accel_Ramp
T#5s, M-102.Decel_Ramp
T#5s, FV-106.Timeout
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
TRUE, FV-106.Manual_Mode
0.0, FV-106.Manual_Position
T#60s, M102RestartDelay_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 02:13:14

### Output:
```
* Function Blocks *
ANALOG_IN LT-101
PID_BASIC FC-101
MOTOR_VSD M-102
VALVE_ELECTRIC FV-106
VALVE_ON_OFF XV-102
VALVE_ON_OFF XV-104
VALVE_ON_OFF XV-105
BOOL_IN ILK-FC-101-XV-102-OPEN
BOOL_IN ILK-FC-101-XV-104-OPEN
BOOL_IN ILK-FC-101-LT-101-VALID
BOOL_IN PERM-M-102-LEVEL-ABOVE-20
BOOL_IN PERM-M-102-XV-105-CLOSED
TON M102RestartDelay_TON

* Variables *
REAL LT101_Flow_PV_m3ph
REAL FC101_MV_Percent
BOOL HopperLevel_Above20

* Functions *
NOT LT101Valid_NOT
AND FC101ValvesOpen_AND
AND FC101Interlock_AND
NOT FC101Inhibit_NOT
OR FC101Fault_OR
AND M102Permissive_AND
NOT M102Permissive_NOT
OR M102Fault_OR
OR M102Inhibit_OR
NOT M102AllowedRun_NOT
AND M102Start_AND

* Data Connections * 
LT-101.PV, FC-101.PV
FC-101.XOUT, M-102.Speed_SP
XV-102.FB_Opened, ILK-FC-101-XV-102-OPEN.Bool_In
XV-104.FB_Opened, ILK-FC-101-XV-104-OPEN.Bool_In
LT-101.General_Fault, LT101Valid_NOT.IN
LT101Valid_NOT.OUT, ILK-FC-101-LT-101-VALID.Bool_In
ILK-FC-101-XV-102-OPEN.Bool_Out, FC101ValvesOpen_AND.IN1
ILK-FC-101-XV-104-OPEN.Bool_Out, FC101ValvesOpen_AND.IN2
FC101ValvesOpen_AND.OUT, FC101Interlock_AND.IN1
ILK-FC-101-LT-101-VALID.Bool_Out, FC101Interlock_AND.IN2
FC101Interlock_AND.OUT, FC-101.AUTO
FC101Interlock_AND.OUT, FC101Inhibit_NOT.IN
FC101Inhibit_NOT.OUT, FC101Fault_OR.IN1
M-102.FB_Fault, FC101Fault_OR.IN2
FC101Fault_OR.OUT, FC-101.Inhibit
XV-105.FB_Closed, PERM-M-102-XV-105-CLOSED.Bool_In
HopperLevel_Above20, PERM-M-102-LEVEL-ABOVE-20.Bool_In
PERM-M-102-LEVEL-ABOVE-20.Bool_Out, M102Permissive_AND.IN1
PERM-M-102-XV-105-CLOSED.Bool_Out, M102Permissive_AND.IN2
M102Permissive_AND.OUT, M102Permissive_NOT.IN
M102Permissive_NOT.OUT, M102Inhibit_OR.IN1
LT-101.General_Fault, M102Fault_OR.IN1
M-102.FB_Fault, M102Fault_OR.IN2
M102Fault_OR.OUT, M102Inhibit_OR.IN2
M102Inhibit_OR.OUT, M-102.Inhibit
M102Inhibit_OR.OUT, M-102.Stop_Cmd
M102Inhibit_OR.OUT, M102AllowedRun_NOT.IN
M102AllowedRun_NOT.OUT, M102RestartDelay_TON.IN
M102AllowedRun_NOT.OUT, M102Start_AND.IN1
M102RestartDelay_TON.Q, M102Start_AND.IN2
M102Start_AND.OUT, M-102.Start_Cmd
M-102.FB_Fault, XV-102.Inhibit
M-102.FB_Fault, XV-104.Inhibit
LT-101.General_Fault, FV-106.Inhibit
LT-101.PV, LT101_Flow_PV_m3ph
FC-101.XOUT, FC101_MV_Percent

* Parameter Data Connections *
25.0, LT-101.Scaling_Slope
-100.0, LT-101.Scaling_Offset
TRUE, LT-101.Alarm_Enable
380.0, LT-101.PV_High
20.0, LT-101.PV_Low
250.0, FC-101.SP
0.0, FC-101.MV_MIN
100.0, FC-101.MV_MAX
0.0, FC-101.X0
3.0, FC-101.KP
1.2, FC-101.TR
0.3, FC-101.TD
380.0, FC-101.PV_High
20.0, FC-101.PV_Low
25.0, FC-101.Deviation_Limit
T#5s, M-102.Accel_Ramp
T#5s, M-102.Decel_Ramp
T#5s, FV-106.Timeout
100.0, FV-106.Open_Limit
0.0, FV-106.Close_Limit
TRUE, FV-106.Manual_Mode
0.0, FV-106.Manual_Position
T#60s, M102RestartDelay_TON.PT
```

---


