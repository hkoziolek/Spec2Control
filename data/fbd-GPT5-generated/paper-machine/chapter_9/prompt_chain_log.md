# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 03:21:50

## Step 1: contextgen1-sensors
**Time:** 03:21:50

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
**Time:** 03:22:18

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
**Time:** 03:22:53

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| PID Control | 0.97 |
| OVERRIDE | 0.72 |

Selected Control Strategy: PID Control
Short explanation: The narrative specifies multiple independent feedback loops using transmitters driving actuators via PID control to maintain temperature, moisture, fan speed, and tension.

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
**Timestamp:** 2025-09-24 03:23:41

## Step 1: openplc-function-blocks-v2
**Time:** 03:23:41

### Output:
```
* Function Blocks *
ANALOG_IN TT-801
ANALOG_IN TT-802
ANALOG_IN PT-801
ANALOG_IN IR-801
ANALOG_IN WT-801
MOTOR_VSD F-801
VALVE_ELECTRIC FV-801
VALVE_ELECTRIC XV-802
MOTOR_ON_OFF M-801
PID_BASIC TC-801
PID_BASIC SC-801_PID
PID_BASIC IR-801_PID
PID_BASIC WT-801_PID
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 03:25:28

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN TT-801
ANALOG_IN TT-802
ANALOG_IN PT-801
ANALOG_IN IR-801
ANALOG_IN WT-801
MOTOR_VSD F-801
MOTOR_VSD M-801
VALVE_ELECTRIC FV-801
VALVE_ELECTRIC XV-802
PID_BASIC TC-801
PID_BASIC SC-801_PID
PID_BASIC IR-801_PID
PID_BASIC WT-801_PID
BOOL_IN PT-801_Overpressure
BOOL_IN IR-801_Available
BOOL_IN XV-802_Open
BOOL_IN TT-802_InRange
BOOL_IN WT-801_InRange
BOOL_IN M-801_Running
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 03:27:08

### Output:
```
* Functions *

* Block-to-Block Connections *
TT-801.PV, SC-801_PID.PV
SC-801_PID.XOUT, FV-801.Control_Signal
TT-802.PV, TC-801.PV
TC-801.XOUT, XV-802.Control_Signal
IR-801.PV, IR-801_PID.PV
IR-801_PID.XOUT, F-801.Speed_SP
WT-801.PV, WT-801_PID.PV
WT-801_PID.XOUT, M-801.Speed_SP
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 03:27:36

### Output:
```
* Functions * 
OR SC-801_SteamInhibit_OR
OR IR-801_SignalFault_OR
NOT IR-801_Available_NOT
NOT IR-801_NotAvailable_NOT
OR TT-802_OutOfRange_OR
NOT TT-802_InRange_NOT
AND HoodControlPermissive_AND
NOT HoodControlNotPermissive_NOT
OR XV-802_Inhibit_OR
OR WT-801_OutOfRange_OR
NOT WT-801_InRange_NOT
AND TensionPermissive_AND
NOT TensionNotPermissive_NOT

* Data Connections *
PT-801.High_Alarm, PT-801_Overpressure.Bool_In
PT-801_Overpressure.Bool_Out, SC-801_SteamInhibit_OR.IN1
PT-801.Low_Alarm, SC-801_SteamInhibit_OR.IN2
TT-801.High_Alarm, SC-801_SteamInhibit_OR.IN3
SC-801_SteamInhibit_OR.OUT, FV-801.Inhibit
SC-801_SteamInhibit_OR.OUT, SC-801_PID.Inhibit
IR-801.General_Fault, IR-801_SignalFault_OR.IN1
IR-801.Low_Alarm, IR-801_SignalFault_OR.IN2
IR-801.High_Alarm, IR-801_SignalFault_OR.IN3
IR-801_SignalFault_OR.OUT, IR-801_Available_NOT.IN
IR-801_Available_NOT.OUT, IR-801_Available.Bool_In
IR-801_Available.Bool_Out, IR-801_NotAvailable_NOT.IN
IR-801_NotAvailable_NOT.OUT, F-801.Inhibit
IR-801_NotAvailable_NOT.OUT, IR-801_PID.Inhibit
TT-802.High_Alarm, TT-802_OutOfRange_OR.IN1
TT-802.Low_Alarm, TT-802_OutOfRange_OR.IN2
TT-802_OutOfRange_OR.OUT, TT-802_InRange_NOT.IN
TT-802_InRange_NOT.OUT, TT-802_InRange.Bool_In
XV-802_Open.Bool_Out, HoodControlPermissive_AND.IN1
TT-802_InRange.Bool_Out, HoodControlPermissive_AND.IN2
HoodControlPermissive_AND.OUT, HoodControlNotPermissive_NOT.IN
HoodControlNotPermissive_NOT.OUT, TC-801.Inhibit
HoodControlNotPermissive_NOT.OUT, XV-802_Inhibit_OR.IN1
TC-801.PV_High_Alarm, XV-802_Inhibit_OR.IN2
XV-802_Inhibit_OR.OUT, XV-802.Inhibit
WT-801.High_Alarm, WT-801_OutOfRange_OR.IN1
WT-801.Low_Alarm, WT-801_OutOfRange_OR.IN2
WT-801_OutOfRange_OR.OUT, WT-801_InRange_NOT.IN
WT-801_InRange_NOT.OUT, WT-801_InRange.Bool_In
M-801.FB_Running, M-801_Running.Bool_In
M-801_Running.Bool_Out, TensionPermissive_AND.IN1
WT-801_InRange.Bool_Out, TensionPermissive_AND.IN2
TensionPermissive_AND.OUT, TensionNotPermissive_NOT.IN
TensionNotPermissive_NOT.OUT, WT-801_PID.Inhibit
WT-801_OutOfRange_OR.OUT, M-801.Inhibit

* Parameter Data Connections *
125, TT-801.PV_High
0, TT-801.PV_Low
900, PT-801.PV_High
600, PT-801.PV_Low
120, TT-802.PV_High
50, TT-802.PV_Low
10, IR-801.PV_High
0, IR-801.PV_Low
450, WT-801.PV_High
50, WT-801.PV_Low
125, SC-801_PID.PV_High
0, SC-801_PID.PV_Low
95, TC-801.PV_High
50, TC-801.PV_Low
5.0, IR-801_PID.PV_High
0, IR-801_PID.PV_Low
400, WT-801_PID.PV_High
50, WT-801_PID.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 03:29:19

### Output:
```
* Parameter Data Connections *
9.375, TT-801.Scaling_Slope
-37.5, TT-801.Scaling_Offset
125, TT-801.PV_High
TRUE, TT-801.Alarm_Enable
4.375, TT-802.Scaling_Slope
32.5, TT-802.Scaling_Offset
95, TT-802.PV_High
TRUE, TT-802.Alarm_Enable
0.625, IR-801.Scaling_Slope
-2.5, IR-801.Scaling_Offset
5.0, IR-801.PV_High
TRUE, IR-801.Alarm_Enable
31.25, WT-801.Scaling_Slope
-125, WT-801.Scaling_Offset
400, WT-801.PV_High
50, WT-801.PV_Low
TRUE, WT-801.Alarm_Enable
900, PT-801.PV_High
600, PT-801.PV_Low
TRUE, PT-801.Alarm_Enable
115, SC-801_PID.SP
3.0, SC-801_PID.KP
0.5, SC-801_PID.TR
0.1, SC-801_PID.TD
0, SC-801_PID.MV_MIN
100, SC-801_PID.MV_MAX
TRUE, SC-801_PID.AUTO
85, TC-801.SP
2.5, TC-801.KP
0.8, TC-801.TR
0.2, TC-801.TD
10, TC-801.MV_MIN
90, TC-801.MV_MAX
TRUE, TC-801.AUTO
4.5, IR-801_PID.SP
1.8, IR-801_PID.KP
0.6, IR-801_PID.TR
0.05, IR-801_PID.TD
0, IR-801_PID.MV_MIN
100, IR-801_PID.MV_MAX
0.2, IR-801_PID.Deviation_Limit
TRUE, IR-801_PID.AUTO
250, WT-801_PID.SP
4.0, WT-801_PID.KP
1.0, WT-801_PID.TR
0.3, WT-801_PID.TD
0, WT-801_PID.MV_MIN
100, WT-801_PID.MV_MAX
TRUE, WT-801_PID.AUTO
400, WT-801_PID.PV_High
50, WT-801_PID.PV_Low
100, FV-801.Open_Limit
0, FV-801.Close_Limit
FALSE, FV-801.Manual_Mode
90, XV-802.Open_Limit
10, XV-802.Close_Limit
FALSE, XV-802.Manual_Mode
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 03:30:10

### Output:
```
* Parameter Data Connections *
9.375, TT-801.Scaling_Slope
-37.5, TT-801.Scaling_Offset
125, TT-801.PV_High
0, TT-801.PV_Low
TRUE, TT-801.Alarm_Enable
4.375, TT-802.Scaling_Slope
32.5, TT-802.Scaling_Offset
120, TT-802.PV_High
50, TT-802.PV_Low
TRUE, TT-802.Alarm_Enable
0.625, IR-801.Scaling_Slope
-2.5, IR-801.Scaling_Offset
5.0, IR-801.PV_High
0, IR-801.PV_Low
TRUE, IR-801.Alarm_Enable
31.25, WT-801.Scaling_Slope
-125, WT-801.Scaling_Offset
450, WT-801.PV_High
50, WT-801.PV_Low
TRUE, WT-801.Alarm_Enable
900, PT-801.PV_High
600, PT-801.PV_Low
TRUE, PT-801.Alarm_Enable
115, SC-801_PID.SP
3.0, SC-801_PID.KP
0.5, SC-801_PID.TR
0.1, SC-801_PID.TD
0, SC-801_PID.MV_MIN
100, SC-801_PID.MV_MAX
125, SC-801_PID.PV_High
0, SC-801_PID.PV_Low
TRUE, SC-801_PID.AUTO
85, TC-801.SP
2.5, TC-801.KP
0.8, TC-801.TR
0.2, TC-801.TD
10, TC-801.MV_MIN
90, TC-801.MV_MAX
95, TC-801.PV_High
50, TC-801.PV_Low
TRUE, TC-801.AUTO
4.5, IR-801_PID.SP
1.8, IR-801_PID.KP
0.6, IR-801_PID.TR
0.05, IR-801_PID.TD
0, IR-801_PID.MV_MIN
100, IR-801_PID.MV_MAX
0.2, IR-801_PID.Deviation_Limit
5.0, IR-801_PID.PV_High
0, IR-801_PID.PV_Low
TRUE, IR-801_PID.AUTO
250, WT-801_PID.SP
4.0, WT-801_PID.KP
1.0, WT-801_PID.TR
0.3, WT-801_PID.TD
0, WT-801_PID.MV_MIN
100, WT-801_PID.MV_MAX
400, WT-801_PID.PV_High
50, WT-801_PID.PV_Low
TRUE, WT-801_PID.AUTO
100, FV-801.Open_Limit
0, FV-801.Close_Limit
FALSE, FV-801.Manual_Mode
90, XV-802.Open_Limit
10, XV-802.Close_Limit
FALSE, XV-802.Manual_Mode
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 03:30:50

### Output:
```
* Variables *
REAL F801_VFD_Speed_Cmd_Pct
REAL FV801_SteamFlow_ValvePos_Cmd_Pct
REAL XV802_HoodDamper_Pos_Cmd_Pct
REAL M801_Drive_Torque_Cmd_Pct

* Data Connections *
F-801.Speed_Out, F801_VFD_Speed_Cmd_Pct
FV-801.Valve_Position, FV801_SteamFlow_ValvePos_Cmd_Pct
XV-802.Valve_Position, XV802_HoodDamper_Pos_Cmd_Pct
M-801.Speed_Out, M801_Drive_Torque_Cmd_Pct
```

---

## Step 8: openplc-rule-checks
**Time:** 03:31:15

### Output:
```
* Function Blocks *
ANALOG_IN TT-801
ANALOG_IN TT-802
ANALOG_IN PT-801
ANALOG_IN IR-801
ANALOG_IN WT-801
MOTOR_VSD F-801
MOTOR_VSD M-801
VALVE_ELECTRIC FV-801
VALVE_ELECTRIC XV-802
PID_BASIC TC-801
PID_BASIC SC-801_LOOP
PID_BASIC IR-801_LOOP
PID_BASIC WT-801_LOOP
BOOL_IN PT-801_Overpressure
BOOL_IN IR-801_Available
BOOL_IN XV-802_Open
BOOL_IN TT-802_InRange
BOOL_IN WT-801_InRange
BOOL_IN M-801_Running

* Variables *
REAL F801_VFD_Speed_Cmd_Pct
REAL FV801_SteamFlow_ValvePos_Cmd_Pct
REAL XV802_HoodDamper_Pos_Cmd_Pct
REAL M801_Drive_Torque_Cmd_Pct

* Functions *
OR SC-801_SteamInhibit_OR
OR IR-801_SignalFault_OR
NOT IR-801_Available_NOT
NOT IR-801_NotAvailable_NOT
OR TT-802_OutOfRange_OR
NOT TT-802_InRange_NOT
AND HoodControlPermissive_AND
NOT HoodControlNotPermissive_NOT
OR XV-802_Inhibit_OR
OR WT-801_OutOfRange_OR
NOT WT-801_InRange_NOT
AND TensionPermissive_AND
NOT TensionNotPermissive_NOT
GT XV-802_Open_GT

* Data Connections * 
TT-801.PV, SC-801_LOOP.PV
SC-801_LOOP.XOUT, FV-801.Control_Signal
TT-802.PV, TC-801.PV
TC-801.XOUT, XV-802.Control_Signal
IR-801.PV, IR-801_LOOP.PV
IR-801_LOOP.XOUT, F-801.Speed_SP
WT-801.PV, WT-801_LOOP.PV
WT-801_LOOP.XOUT, M-801.Speed_SP
PT-801.High_Alarm, PT-801_Overpressure.Bool_In
PT-801_Overpressure.Bool_Out, SC-801_SteamInhibit_OR.IN1
PT-801.Low_Alarm, SC-801_SteamInhibit_OR.IN2
TT-801.High_Alarm, SC-801_SteamInhibit_OR.IN3
SC-801_SteamInhibit_OR.OUT, FV-801.Inhibit
SC-801_SteamInhibit_OR.OUT, SC-801_LOOP.Inhibit
IR-801.General_Fault, IR-801_SignalFault_OR.IN1
IR-801.Low_Alarm, IR-801_SignalFault_OR.IN2
IR-801.High_Alarm, IR-801_SignalFault_OR.IN3
IR-801_SignalFault_OR.OUT, IR-801_Available_NOT.IN
IR-801_Available_NOT.OUT, IR-801_Available.Bool_In
IR-801_Available.Bool_Out, IR-801_NotAvailable_NOT.IN
IR-801_NotAvailable_NOT.OUT, F-801.Inhibit
IR-801_NotAvailable_NOT.OUT, IR-801_LOOP.Inhibit
TT-802.High_Alarm, TT-802_OutOfRange_OR.IN1
TT-802.Low_Alarm, TT-802_OutOfRange_OR.IN2
TT-802_OutOfRange_OR.OUT, TT-802_InRange_NOT.IN
TT-802_InRange_NOT.OUT, TT-802_InRange.Bool_In
XV-802.Feedback_Pos, XV-802_Open_GT.IN1
XV-802_Open_GT.OUT, XV-802_Open.Bool_In
XV-802_Open.Bool_Out, HoodControlPermissive_AND.IN1
TT-802_InRange.Bool_Out, HoodControlPermissive_AND.IN2
HoodControlPermissive_AND.OUT, HoodControlNotPermissive_NOT.IN
HoodControlNotPermissive_NOT.OUT, TC-801.Inhibit
HoodControlNotPermissive_NOT.OUT, XV-802_Inhibit_OR.IN1
TC-801.PV_High_Alarm, XV-802_Inhibit_OR.IN2
XV-802_Inhibit_OR.OUT, XV-802.Inhibit
WT-801.High_Alarm, WT-801_OutOfRange_OR.IN1
WT-801.Low_Alarm, WT-801_OutOfRange_OR.IN2
WT-801_OutOfRange_OR.OUT, WT-801_InRange_NOT.IN
WT-801_InRange_NOT.OUT, WT-801_InRange.Bool_In
M-801.FB_Running, M-801_Running.Bool_In
M-801_Running.Bool_Out, TensionPermissive_AND.IN1
WT-801_InRange.Bool_Out, TensionPermissive_AND.IN2
TensionPermissive_AND.OUT, TensionNotPermissive_NOT.IN
TensionNotPermissive_NOT.OUT, WT-801_LOOP.Inhibit
WT-801_OutOfRange_OR.OUT, M-801.Inhibit
F-801.Speed_Out, F801_VFD_Speed_Cmd_Pct
FV-801.Valve_Position, FV801_SteamFlow_ValvePos_Cmd_Pct
XV-802.Valve_Position, XV802_HoodDamper_Pos_Cmd_Pct
M-801.Speed_Out, M801_Drive_Torque_Cmd_Pct

* Parameter Data Connections *
9.375, TT-801.Scaling_Slope
-37.5, TT-801.Scaling_Offset
125, TT-801.PV_High
0, TT-801.PV_Low
TRUE, TT-801.Alarm_Enable
4.375, TT-802.Scaling_Slope
32.5, TT-802.Scaling_Offset
120, TT-802.PV_High
50, TT-802.PV_Low
TRUE, TT-802.Alarm_Enable
0.625, IR-801.Scaling_Slope
-2.5, IR-801.Scaling_Offset
5.0, IR-801.PV_High
0, IR-801.PV_Low
TRUE, IR-801.Alarm_Enable
31.25, WT-801.Scaling_Slope
-125, WT-801.Scaling_Offset
450, WT-801.PV_High
50, WT-801.PV_Low
TRUE, WT-801.Alarm_Enable
900, PT-801.PV_High
600, PT-801.PV_Low
TRUE, PT-801.Alarm_Enable
115, SC-801_LOOP.SP
3.0, SC-801_LOOP.KP
0.5, SC-801_LOOP.TR
0.1, SC-801_LOOP.TD
0, SC-801_LOOP.MV_MIN
100, SC-801_LOOP.MV_MAX
125, SC-801_LOOP.PV_High
0, SC-801_LOOP.PV_Low
TRUE, SC-801_LOOP.AUTO
85, TC-801.SP
2.5, TC-801.KP
0.8, TC-801.TR
0.2, TC-801.TD
10, TC-801.MV_MIN
90, TC-801.MV_MAX
95, TC-801.PV_High
50, TC-801.PV_Low
TRUE, TC-801.AUTO
4.5, IR-801_LOOP.SP
1.8, IR-801_LOOP.KP
0.6, IR-801_LOOP.TR
0.05, IR-801_LOOP.TD
0, IR-801_LOOP.MV_MIN
100, IR-801_LOOP.MV_MAX
0.2, IR-801_LOOP.Deviation_Limit
5.0, IR-801_LOOP.PV_High
0, IR-801_LOOP.PV_Low
TRUE, IR-801_LOOP.AUTO
250, WT-801_LOOP.SP
4.0, WT-801_LOOP.KP
1.0, WT-801_LOOP.TR
0.3, WT-801_LOOP.TD
0, WT-801_LOOP.MV_MIN
100, WT-801_LOOP.MV_MAX
400, WT-801_LOOP.PV_High
50, WT-801_LOOP.PV_Low
TRUE, WT-801_LOOP.AUTO
100, FV-801.Open_Limit
0, FV-801.Close_Limit
FALSE, FV-801.Manual_Mode
90, XV-802.Open_Limit
10, XV-802.Close_Limit
FALSE, XV-802.Manual_Mode
20, XV-802_Open_GT.IN2
```

---

## Step 9: openplc-rule-checks2
**Time:** 03:32:49

### Output:
```
* Function Blocks *
ANALOG_IN TT-801
ANALOG_IN TT-802
ANALOG_IN PT-801
ANALOG_IN IR-801
ANALOG_IN WT-801
MOTOR_VSD F-801
MOTOR_VSD M-801
VALVE_ELECTRIC FV-801
VALVE_ELECTRIC XV-802
PID_BASIC TC-801
PID_BASIC SC-801_LOOP
PID_BASIC IR-801_LOOP
PID_BASIC WT-801_LOOP
BOOL_IN PT-801_Overpressure
BOOL_IN IR-801_Available
BOOL_IN XV-802_Open
BOOL_IN TT-802_InRange
BOOL_IN WT-801_InRange
BOOL_IN M-801_Running

* Variables *
REAL F801_VFD_Speed_Cmd_Pct
REAL FV801_SteamFlow_ValvePos_Cmd_Pct
REAL XV802_HoodDamper_Pos_Cmd_Pct
REAL M801_Drive_Torque_Cmd_Pct

* Functions *
OR SC-801_SteamInhibit_OR
OR IR-801_SignalFault_OR
NOT IR-801_Available_NOT
NOT IR-801_NotAvailable_NOT
OR TT-802_OutOfRange_OR
NOT TT-802_InRange_NOT
AND HoodControlPermissive_AND
NOT HoodControlNotPermissive_NOT
OR XV-802_Inhibit_OR
OR WT-801_OutOfRange_OR
NOT WT-801_InRange_NOT
AND TensionPermissive_AND
NOT TensionNotPermissive_NOT
GT XV-802_Open_GT

* Data Connections * 
TT-801.PV, SC-801_LOOP.PV
SC-801_LOOP.XOUT, FV-801.Control_Signal
TT-802.PV, TC-801.PV
TC-801.XOUT, XV-802.Control_Signal
IR-801.PV, IR-801_LOOP.PV
IR-801_LOOP.XOUT, F-801.Speed_SP
WT-801.PV, WT-801_LOOP.PV
WT-801_LOOP.XOUT, M-801.Speed_SP
PT-801.High_Alarm, PT-801_Overpressure.Bool_In
PT-801_Overpressure.Bool_Out, SC-801_SteamInhibit_OR.IN1
PT-801.Low_Alarm, SC-801_SteamInhibit_OR.IN2
TT-801.High_Alarm, SC-801_SteamInhibit_OR.IN3
SC-801_SteamInhibit_OR.OUT, FV-801.Inhibit
SC-801_SteamInhibit_OR.OUT, SC-801_LOOP.Inhibit
IR-801.General_Fault, IR-801_SignalFault_OR.IN1
IR-801.Low_Alarm, IR-801_SignalFault_OR.IN2
IR-801.High_Alarm, IR-801_SignalFault_OR.IN3
IR-801_SignalFault_OR.OUT, IR-801_Available_NOT.IN
IR-801_Available_NOT.OUT, IR-801_Available.Bool_In
IR-801_Available.Bool_Out, IR-801_NotAvailable_NOT.IN
IR-801_NotAvailable_NOT.OUT, F-801.Inhibit
IR-801_NotAvailable_NOT.OUT, IR-801_LOOP.Inhibit
TT-802.High_Alarm, TT-802_OutOfRange_OR.IN1
TT-802.Low_Alarm, TT-802_OutOfRange_OR.IN2
TT-802_OutOfRange_OR.OUT, TT-802_InRange_NOT.IN
TT-802_InRange_NOT.OUT, TT-802_InRange.Bool_In
XV-802.Feedback_Pos, XV-802_Open_GT.IN1
XV-802_Open_GT.OUT, XV-802_Open.Bool_In
XV-802_Open.Bool_Out, HoodControlPermissive_AND.IN1
TT-802_InRange.Bool_Out, HoodControlPermissive_AND.IN2
HoodControlPermissive_AND.OUT, HoodControlNotPermissive_NOT.IN
HoodControlNotPermissive_NOT.OUT, TC-801.Inhibit
HoodControlNotPermissive_NOT.OUT, XV-802_Inhibit_OR.IN1
TC-801.PV_High_Alarm, XV-802_Inhibit_OR.IN2
XV-802_Inhibit_OR.OUT, XV-802.Inhibit
WT-801.High_Alarm, WT-801_OutOfRange_OR.IN1
WT-801.Low_Alarm, WT-801_OutOfRange_OR.IN2
WT-801_OutOfRange_OR.OUT, WT-801_InRange_NOT.IN
WT-801_InRange_NOT.OUT, WT-801_InRange.Bool_In
M-801.FB_Running, M-801_Running.Bool_In
M-801_Running.Bool_Out, TensionPermissive_AND.IN1
WT-801_InRange.Bool_Out, TensionPermissive_AND.IN2
TensionPermissive_AND.OUT, TensionNotPermissive_NOT.IN
TensionNotPermissive_NOT.OUT, WT-801_LOOP.Inhibit
WT-801_OutOfRange_OR.OUT, M-801.Inhibit
F-801.Speed_Out, F801_VFD_Speed_Cmd_Pct
FV-801.Valve_Position, FV801_SteamFlow_ValvePos_Cmd_Pct
XV-802.Valve_Position, XV802_HoodDamper_Pos_Cmd_Pct
M-801.Speed_Out, M801_Drive_Torque_Cmd_Pct

* Parameter Data Connections *
9.375, TT-801.Scaling_Slope
-37.5, TT-801.Scaling_Offset
125, TT-801.PV_High
0, TT-801.PV_Low
TRUE, TT-801.Alarm_Enable
4.375, TT-802.Scaling_Slope
32.5, TT-802.Scaling_Offset
120, TT-802.PV_High
50, TT-802.PV_Low
TRUE, TT-802.Alarm_Enable
0.625, IR-801.Scaling_Slope
-2.5, IR-801.Scaling_Offset
5.0, IR-801.PV_High
0, IR-801.PV_Low
TRUE, IR-801.Alarm_Enable
31.25, WT-801.Scaling_Slope
-125, WT-801.Scaling_Offset
450, WT-801.PV_High
50, WT-801.PV_Low
TRUE, WT-801.Alarm_Enable
900, PT-801.PV_High
600, PT-801.PV_Low
TRUE, PT-801.Alarm_Enable
115, SC-801_LOOP.SP
3.0, SC-801_LOOP.KP
0.5, SC-801_LOOP.TR
0.1, SC-801_LOOP.TD
0, SC-801_LOOP.MV_MIN
100, SC-801_LOOP.MV_MAX
125, SC-801_LOOP.PV_High
0, SC-801_LOOP.PV_Low
TRUE, SC-801_LOOP.AUTO
85, TC-801.SP
2.5, TC-801.KP
0.8, TC-801.TR
0.2, TC-801.TD
10, TC-801.MV_MIN
90, TC-801.MV_MAX
95, TC-801.PV_High
50, TC-801.PV_Low
TRUE, TC-801.AUTO
4.5, IR-801_LOOP.SP
1.8, IR-801_LOOP.KP
0.6, IR-801_LOOP.TR
0.05, IR-801_LOOP.TD
0, IR-801_LOOP.MV_MIN
100, IR-801_LOOP.MV_MAX
0.2, IR-801_LOOP.Deviation_Limit
5.0, IR-801_LOOP.PV_High
0, IR-801_LOOP.PV_Low
TRUE, IR-801_LOOP.AUTO
250, WT-801_LOOP.SP
4.0, WT-801_LOOP.KP
1.0, WT-801_LOOP.TR
0.3, WT-801_LOOP.TD
0, WT-801_LOOP.MV_MIN
100, WT-801_LOOP.MV_MAX
400, WT-801_LOOP.PV_High
50, WT-801_LOOP.PV_Low
TRUE, WT-801_LOOP.AUTO
100, FV-801.Open_Limit
0, FV-801.Close_Limit
FALSE, FV-801.Manual_Mode
90, XV-802.Open_Limit
10, XV-802.Close_Limit
FALSE, XV-802.Manual_Mode
20, XV-802_Open_GT.IN2
```

---

## Step 10: append_two_inputs
**Time:** 03:33:15

### Output:
```
* Function Blocks *
ANALOG_IN TT-801
ANALOG_IN TT-802
ANALOG_IN PT-801
ANALOG_IN IR-801
ANALOG_IN WT-801
MOTOR_VSD F-801
MOTOR_VSD M-801
VALVE_ELECTRIC FV-801
VALVE_ELECTRIC XV-802
PID_BASIC TC-801
PID_BASIC SC-801_LOOP
PID_BASIC IR-801_LOOP
PID_BASIC WT-801_LOOP
BOOL_IN PT-801_Overpressure
BOOL_IN IR-801_Available
BOOL_IN XV-802_Open
BOOL_IN TT-802_InRange
BOOL_IN WT-801_InRange
BOOL_IN M-801_Running

* Variables *
REAL F801_VFD_Speed_Cmd_Pct
REAL FV801_SteamFlow_ValvePos_Cmd_Pct
REAL XV802_HoodDamper_Pos_Cmd_Pct
REAL M801_Drive_Torque_Cmd_Pct

* Functions *
OR SC-801_SteamInhibit_OR
OR IR-801_SignalFault_OR
NOT IR-801_Available_NOT
OR TT-802_OutOfRange_OR
NOT TT-802_InRange_NOT
AND HoodControlPermissive_AND
NOT HoodControlNotPermissive_NOT
OR XV-802_Inhibit_OR
OR WT-801_OutOfRange_OR
NOT WT-801_InRange_NOT
AND TensionPermissive_AND
NOT TensionNotPermissive_NOT
GT XV-802_Open_GT

* Data Connections * 
TT-801.PV, SC-801_LOOP.PV
SC-801_LOOP.XOUT, FV-801.Control_Signal
TT-802.PV, TC-801.PV
TC-801.XOUT, XV-802.Control_Signal
IR-801.PV, IR-801_LOOP.PV
IR-801_LOOP.XOUT, F-801.Speed_SP
WT-801.PV, WT-801_LOOP.PV
WT-801_LOOP.XOUT, M-801.Speed_SP
PT-801.High_Alarm, PT-801_Overpressure.Bool_In
PT-801_Overpressure.Bool_Out, SC-801_SteamInhibit_OR.IN1
PT-801.Low_Alarm, SC-801_SteamInhibit_OR.IN2
TT-801.High_Alarm, SC-801_SteamInhibit_OR.IN3
SC-801_SteamInhibit_OR.OUT, FV-801.Inhibit
SC-801_SteamInhibit_OR.OUT, SC-801_LOOP.Inhibit
IR-801.General_Fault, IR-801_SignalFault_OR.IN1
IR-801.Low_Alarm, IR-801_SignalFault_OR.IN2
IR-801.High_Alarm, IR-801_SignalFault_OR.IN3
IR-801_SignalFault_OR.OUT, IR-801_Available_NOT.IN
IR-801_Available_NOT.OUT, IR-801_Available.Bool_In
IR-801_SignalFault_OR.OUT, F-801.Inhibit
IR-801_SignalFault_OR.OUT, IR-801_LOOP.Inhibit
TT-802.High_Alarm, TT-802_OutOfRange_OR.IN1
TT-802.Low_Alarm, TT-802_OutOfRange_OR.IN2
TT-802_OutOfRange_OR.OUT, TT-802_InRange_NOT.IN
TT-802_InRange_NOT.OUT, TT-802_InRange.Bool_In
XV-802.Feedback_Pos, XV-802_Open_GT.IN1
XV-802_Open_GT.OUT, XV-802_Open.Bool_In
XV-802_Open.Bool_Out, HoodControlPermissive_AND.IN1
TT-802_InRange.Bool_Out, HoodControlPermissive_AND.IN2
HoodControlPermissive_AND.OUT, HoodControlNotPermissive_NOT.IN
HoodControlNotPermissive_NOT.OUT, TC-801.Inhibit
HoodControlNotPermissive_NOT.OUT, XV-802_Inhibit_OR.IN1
TC-801.PV_High_Alarm, XV-802_Inhibit_OR.IN2
XV-802_Inhibit_OR.OUT, XV-802.Inhibit
WT-801.High_Alarm, WT-801_OutOfRange_OR.IN1
WT-801.Low_Alarm, WT-801_OutOfRange_OR.IN2
WT-801_OutOfRange_OR.OUT, WT-801_InRange_NOT.IN
WT-801_InRange_NOT.OUT, WT-801_InRange.Bool_In
M-801.FB_Running, M-801_Running.Bool_In
M-801_Running.Bool_Out, TensionPermissive_AND.IN1
WT-801_InRange.Bool_Out, TensionPermissive_AND.IN2
TensionPermissive_AND.OUT, TensionNotPermissive_NOT.IN
TensionNotPermissive_NOT.OUT, WT-801_LOOP.Inhibit
WT-801_OutOfRange_OR.OUT, M-801.Inhibit
F-801.Speed_Out, F801_VFD_Speed_Cmd_Pct
FV-801.Valve_Position, FV801_SteamFlow_ValvePos_Cmd_Pct
XV-802.Valve_Position, XV802_HoodDamper_Pos_Cmd_Pct
M-801.Speed_Out, M801_Drive_Torque_Cmd_Pct

* Parameter Data Connections *
9.375, TT-801.Scaling_Slope
-37.5, TT-801.Scaling_Offset
125, TT-801.PV_High
0, TT-801.PV_Low
TRUE, TT-801.Alarm_Enable
4.375, TT-802.Scaling_Slope
32.5, TT-802.Scaling_Offset
120, TT-802.PV_High
50, TT-802.PV_Low
TRUE, TT-802.Alarm_Enable
0.625, IR-801.Scaling_Slope
-2.5, IR-801.Scaling_Offset
5.0, IR-801.PV_High
0, IR-801.PV_Low
TRUE, IR-801.Alarm_Enable
31.25, WT-801.Scaling_Slope
-125, WT-801.Scaling_Offset
450, WT-801.PV_High
50, WT-801.PV_Low
TRUE, WT-801.Alarm_Enable
900, PT-801.PV_High
600, PT-801.PV_Low
TRUE, PT-801.Alarm_Enable
115, SC-801_LOOP.SP
3.0, SC-801_LOOP.KP
0.5, SC-801_LOOP.TR
0.1, SC-801_LOOP.TD
0, SC-801_LOOP.MV_MIN
100, SC-801_LOOP.MV_MAX
125, SC-801_LOOP.PV_High
0, SC-801_LOOP.PV_Low
TRUE, SC-801_LOOP.AUTO
85, TC-801.SP
2.5, TC-801.KP
0.8, TC-801.TR
0.2, TC-801.TD
10, TC-801.MV_MIN
90, TC-801.MV_MAX
95, TC-801.PV_High
50, TC-801.PV_Low
TRUE, TC-801.AUTO
4.5, IR-801_LOOP.SP
1.8, IR-801_LOOP.KP
0.6, IR-801_LOOP.TR
0.05, IR-801_LOOP.TD
0, IR-801_LOOP.MV_MIN
100, IR-801_LOOP.MV_MAX
0.2, IR-801_LOOP.Deviation_Limit
5.0, IR-801_LOOP.PV_High
0, IR-801_LOOP.PV_Low
TRUE, IR-801_LOOP.AUTO
250, WT-801_LOOP.SP
4.0, WT-801_LOOP.KP
1.0, WT-801_LOOP.TR
0.3, WT-801_LOOP.TD
0, WT-801_LOOP.MV_MIN
100, WT-801_LOOP.MV_MAX
400, WT-801_LOOP.PV_High
50, WT-801_LOOP.PV_Low
TRUE, WT-801_LOOP.AUTO
100, FV-801.Open_Limit
0, FV-801.Close_Limit
FALSE, FV-801.Manual_Mode
90, XV-802.Open_Limit
10, XV-802.Close_Limit
FALSE, XV-802.Manual_Mode
20, XV-802_Open_GT.IN2
```

---


