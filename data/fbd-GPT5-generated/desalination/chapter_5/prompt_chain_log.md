# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-23 23:44:08

## Step 1: contextgen1-sensors
**Time:** 23:44:08

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
**Time:** 23:44:40

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
**Time:** 23:45:17

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| PID Control | 0.95 |
| OVERRIDE | 0.65 |
| Duty-Standby | 0.45 |

Selected Control Strategy: PID Control
Short explanation: The narrative primarily describes a single-loop PID regulating flow via the metering pump using FT-301 as PV and an adjustable SP.

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
**Timestamp:** 2025-09-23 23:45:51

## Step 1: openplc-function-blocks-v2
**Time:** 23:45:51

### Output:
```
* Function Blocks *
BOOL_IN ANK-301
DIGITAL_IN FAH-301
DIGITAL_IN FAL-301
PID_BASIC FIC-301
ANALOG_IN FT-301
VALVE_ELECTRIC FV-301
DIGITAL_IN LAL-301
ANALOG_IN LT-301
DIGITAL_IN PAH-103
DIGITAL_IN PFA-301
DIGITAL_IN TAH-101
MOTOR_VSD UMP-301A
VALVE_ON_OFF XV-107
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 23:46:28

### Output:
```
* Function Block List * 
* Function Blocks *
BOOL_IN ANK-301
DIGITAL_IN FAH-301
DIGITAL_IN FAL-301
PID_BASIC FIC-301
ANALOG_IN FT-301
VALVE_ELECTRIC FV-301
DIGITAL_IN LAL-301
ANALOG_IN LT-301
DIGITAL_IN PAH-103
DIGITAL_IN PFA-301
DIGITAL_IN TAH-101
MOTOR_VSD UMP-301A
MOTOR_VSD UMP-301B
VALVE_ON_OFF XV-107
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 23:47:20

### Output:
```
* Functions *
GE DetectHighSaturation_GE
LE DetectLowSaturation_LE
OR CombineSaturation_OR
TON DeviationPersistTimer_TON
NOT NotDevPersist_NOT
OR PIDInhibit_OR

* Block-to-Block Connections *
FT-301.PV, FIC-301.PV
FIC-301.XOUT, FV-301.Control_Signal
FV-301.Feedback_Pos, FIC-301.X0
FIC-301.Deviation_Alarm, DeviationPersistTimer_TON.IN
DeviationPersistTimer_TON.Q, NotDevPersist_NOT.IN
NotDevPersist_NOT.Q, PIDInhibit_OR.IN1
FIC-301.XOUT, DetectHighSaturation_GE.IN1
DetectHighSaturation_GE.Q, CombineSaturation_OR.IN1
FIC-301.XOUT, DetectLowSaturation_LE.IN1
DetectLowSaturation_LE.Q, CombineSaturation_OR.IN2
CombineSaturation_OR.Q, PIDInhibit_OR.IN2
PIDInhibit_OR.Q, FIC-301.Inhibit
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 23:48:39

### Output:
```
* Functions * 
NOT NotPumpAReady_NOT
NOT NotPumpBReady_NOT
AND NoPumpAvailable_AND
NOT NotXV107Open_NOT
OR PumpInhibit_OR
OR ValveTrip_OR

* Data Connections *
UMP-301A.FB_Ready, NotPumpAReady_NOT.IN
UMP-301B.FB_Ready, NotPumpBReady_NOT.IN
NotPumpAReady_NOT.OUT, NoPumpAvailable_AND.IN1
NotPumpBReady_NOT.OUT, NoPumpAvailable_AND.IN2
XV-107.FB_Opened, NotXV107Open_NOT.IN
LAL-301.DI_Out, PumpInhibit_OR.IN1
LT-301.Low_Alarm, PumpInhibit_OR.IN2
ANK-301.Bool_Out, PumpInhibit_OR.IN3
NotXV107Open_NOT.OUT, PumpInhibit_OR.IN4
NoPumpAvailable_AND.OUT, PumpInhibit_OR.IN5
PumpInhibit_OR.OUT, UMP-301A.Inhibit
PumpInhibit_OR.OUT, UMP-301B.Inhibit
PAH-103.DI_Out, ValveTrip_OR.IN1
TAH-101.DI_Out, ValveTrip_OR.IN2
LAL-301.DI_Out, ValveTrip_OR.IN3
ANK-301.Bool_Out, ValveTrip_OR.IN4
ValveTrip_OR.OUT, FV-301.Inhibit

* Parameter Data Connections *
48, FT-301.PV_High
8, FT-301.PV_Low
20, LT-301.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 23:51:13

### Output:
```
* Parameter Data Connections *
3.125, FT-301.Scaling_Slope
-12.5, FT-301.Scaling_Offset
48.0, FT-301.PV_High
8.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
30.0, FIC-301.SP
1.8, FIC-301.KP
0.5, FIC-301.TR
0.05, FIC-301.TD
5.0, FIC-301.MV_MIN
95.0, FIC-301.MV_MAX
0.5, FIC-301.Deviation_Limit
48.0, FIC-301.PV_High
8.0, FIC-301.PV_Low
TRUE, FIC-301.AUTO
100.0, FV-301.Open_Limit
0.0, FV-301.Close_Limit
FALSE, FV-301.Manual_Mode
95.0, DetectHighSaturation_GE.IN2
5.0, DetectLowSaturation_LE.IN2
T#23s, DeviationPersistTimer_TON.PT
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 23:52:26

### Output:
```
* Parameter Data Connections *
3.125, FT-301.Scaling_Slope
-12.5, FT-301.Scaling_Offset
48.0, FT-301.PV_High
8.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
30.0, FIC-301.SP
1.8, FIC-301.KP
0.5, FIC-301.TR
0.05, FIC-301.TD
5.0, FIC-301.MV_MIN
95.0, FIC-301.MV_MAX
0.3, FIC-301.Deviation_Limit
48.0, FIC-301.PV_High
8.0, FIC-301.PV_Low
TRUE, FIC-301.AUTO
100.0, FV-301.Open_Limit
0.0, FV-301.Close_Limit
FALSE, FV-301.Manual_Mode
95.0, DetectHighSaturation_GE.IN2
5.0, DetectLowSaturation_LE.IN2
T#23s, DeviationPersistTimer_TON.PT
20.0, LT-301.PV_Low
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 23:53:30

### Output:
```
* Variables *
REAL CHLOR-PUMP-301AB_Stroke_CMD

* Data Connections *
FIC-301.XOUT, CHLOR-PUMP-301AB_Stroke_CMD
```

---

## Step 8: openplc-rule-checks
**Time:** 23:54:11

### Output:
```
* Function Blocks *
BOOL_IN ANK-301
DIGITAL_IN FAH-301
DIGITAL_IN FAL-301
PID_BASIC FIC-301
ANALOG_IN FT-301
VALVE_ELECTRIC FV-301
DIGITAL_IN LAL-301
ANALOG_IN LT-301
DIGITAL_IN PAH-103
DIGITAL_IN PFA-301
DIGITAL_IN TAH-101
MOTOR_VSD UMP-301A
MOTOR_VSD UMP-301B
VALVE_ON_OFF XV-107

* Variables *
REAL CHLOR-PUMP-301AB_Stroke_CMD

* Functions *
GE DetectHighSaturation_GE
LE DetectLowSaturation_LE
OR CombineSaturation_OR
TON DeviationPersistTimer_TON
NOT NotDevPersist_NOT
OR PIDInhibit_OR
NOT NotPumpAReady_NOT
NOT NotPumpBReady_NOT
AND NoPumpAvailable_AND
NOT NotXV107Open_NOT
OR PumpInhibit_OR
OR ValveTrip_OR

* Data Connections *
FT-301.PV, FIC-301.PV
FIC-301.XOUT, FV-301.Control_Signal
FV-301.Feedback_Pos, FIC-301.X0
FIC-301.Deviation_Alarm, DeviationPersistTimer_TON.IN
DeviationPersistTimer_TON.Q, NotDevPersist_NOT.IN
NotDevPersist_NOT.OUT, PIDInhibit_OR.IN1
FIC-301.XOUT, DetectHighSaturation_GE.IN1
DetectHighSaturation_GE.Q, CombineSaturation_OR.IN1
FIC-301.XOUT, DetectLowSaturation_LE.IN1
DetectLowSaturation_LE.Q, CombineSaturation_OR.IN2
CombineSaturation_OR.OUT, PIDInhibit_OR.IN2
PIDInhibit_OR.OUT, FIC-301.Inhibit
UMP-301A.FB_Ready, NotPumpAReady_NOT.IN
UMP-301B.FB_Ready, NotPumpBReady_NOT.IN
NotPumpAReady_NOT.OUT, NoPumpAvailable_AND.IN1
NotPumpBReady_NOT.OUT, NoPumpAvailable_AND.IN2
XV-107.FB_Opened, NotXV107Open_NOT.IN
LAL-301.DI_Out, PumpInhibit_OR.IN1
LT-301.Low_Alarm, PumpInhibit_OR.IN2
ANK-301.Bool_Out, PumpInhibit_OR.IN3
NotXV107Open_NOT.OUT, PumpInhibit_OR.IN4
NoPumpAvailable_AND.OUT, PumpInhibit_OR.IN5
PumpInhibit_OR.OUT, UMP-301A.Inhibit
PumpInhibit_OR.OUT, UMP-301B.Inhibit
PAH-103.DI_Out, ValveTrip_OR.IN1
TAH-101.DI_Out, ValveTrip_OR.IN2
LAL-301.DI_Out, ValveTrip_OR.IN3
ANK-301.Bool_Out, ValveTrip_OR.IN4
ValveTrip_OR.OUT, FV-301.Inhibit
FIC-301.XOUT, CHLOR-PUMP-301AB_Stroke_CMD

* Parameter Data Connections *
3.125, FT-301.Scaling_Slope
-12.5, FT-301.Scaling_Offset
48.0, FT-301.PV_High
8.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
30.0, FIC-301.SP
1.8, FIC-301.KP
0.5, FIC-301.TR
0.05, FIC-301.TD
5.0, FIC-301.MV_MIN
95.0, FIC-301.MV_MAX
0.3, FIC-301.Deviation_Limit
48.0, FIC-301.PV_High
8.0, FIC-301.PV_Low
TRUE, FIC-301.AUTO
100.0, FV-301.Open_Limit
0.0, FV-301.Close_Limit
FALSE, FV-301.Manual_Mode
95.0, DetectHighSaturation_GE.IN2
5.0, DetectLowSaturation_LE.IN2
T#23s, DeviationPersistTimer_TON.PT
20.0, LT-301.PV_Low
```

---

## Step 9: openplc-rule-checks2
**Time:** 23:55:27

### Output:
```
* Function Blocks *
BOOL_IN ANK-301
DIGITAL_IN FAH-301
DIGITAL_IN FAL-301
PID_BASIC FIC-301
ANALOG_IN FT-301
VALVE_ELECTRIC FV-301
DIGITAL_IN LAL-301
ANALOG_IN LT-301
DIGITAL_IN PAH-103
DIGITAL_IN PFA-301
DIGITAL_IN TAH-101
MOTOR_VSD UMP-301A
MOTOR_VSD UMP-301B
VALVE_ON_OFF XV-107

* Variables *
REAL CHLOR-PUMP-301AB_Stroke_CMD

* Functions *
GE DetectHighSaturation_GE
LE DetectLowSaturation_LE
OR CombineSaturation_OR
TON DeviationPersistTimer_TON
NOT NotDevPersist_NOT
OR PIDInhibit_OR
NOT NotPumpAReady_NOT
NOT NotPumpBReady_NOT
AND NoPumpAvailable_AND
NOT NotXV107Open_NOT
OR PumpInhibit_OR
OR ValveTrip_OR

* Data Connections *
FT-301.PV, FIC-301.PV
FIC-301.XOUT, FV-301.Control_Signal
FV-301.Feedback_Pos, FIC-301.X0
FIC-301.Deviation_Alarm, DeviationPersistTimer_TON.IN
DeviationPersistTimer_TON.Q, NotDevPersist_NOT.IN
NotDevPersist_NOT.OUT, PIDInhibit_OR.IN1
FIC-301.XOUT, DetectHighSaturation_GE.IN1
DetectHighSaturation_GE.Q, CombineSaturation_OR.IN1
FIC-301.XOUT, DetectLowSaturation_LE.IN1
DetectLowSaturation_LE.Q, CombineSaturation_OR.IN2
CombineSaturation_OR.OUT, PIDInhibit_OR.IN2
PIDInhibit_OR.OUT, FIC-301.Inhibit
UMP-301A.FB_Ready, NotPumpAReady_NOT.IN
UMP-301B.FB_Ready, NotPumpBReady_NOT.IN
NotPumpAReady_NOT.OUT, NoPumpAvailable_AND.IN1
NotPumpBReady_NOT.OUT, NoPumpAvailable_AND.IN2
XV-107.FB_Opened, NotXV107Open_NOT.IN
LAL-301.DI_Out, PumpInhibit_OR.IN1
LT-301.Low_Alarm, PumpInhibit_OR.IN2
ANK-301.Bool_Out, PumpInhibit_OR.IN3
NotXV107Open_NOT.OUT, PumpInhibit_OR.IN4
NoPumpAvailable_AND.OUT, PumpInhibit_OR.IN5
PumpInhibit_OR.OUT, UMP-301A.Inhibit
PumpInhibit_OR.OUT, UMP-301B.Inhibit
PAH-103.DI_Out, ValveTrip_OR.IN1
TAH-101.DI_Out, ValveTrip_OR.IN2
LAL-301.DI_Out, ValveTrip_OR.IN3
ANK-301.Bool_Out, ValveTrip_OR.IN4
ValveTrip_OR.OUT, FV-301.Inhibit
FIC-301.XOUT, CHLOR-PUMP-301AB_Stroke_CMD

* Parameter Data Connections *
3.125, FT-301.Scaling_Slope
-12.5, FT-301.Scaling_Offset
48.0, FT-301.PV_High
8.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
30.0, FIC-301.SP
1.8, FIC-301.KP
0.5, FIC-301.TR
0.05, FIC-301.TD
5.0, FIC-301.MV_MIN
95.0, FIC-301.MV_MAX
0.3, FIC-301.Deviation_Limit
48.0, FIC-301.PV_High
8.0, FIC-301.PV_Low
TRUE, FIC-301.AUTO
100.0, FV-301.Open_Limit
0.0, FV-301.Close_Limit
FALSE, FV-301.Manual_Mode
95.0, DetectHighSaturation_GE.IN2
5.0, DetectLowSaturation_LE.IN2
T#23s, DeviationPersistTimer_TON.PT
20.0, LT-301.PV_Low
```

---

## Step 10: append_two_inputs
**Time:** 23:55:55

### Output:
```
* Function Blocks *
BOOL_IN ANK-301
DIGITAL_IN FAH-301
DIGITAL_IN FAL-301
PID_BASIC FIC-301
ANALOG_IN FT-301
VALVE_ELECTRIC FV-301
DIGITAL_IN LAL-301
ANALOG_IN LT-301
DIGITAL_IN PAH-103
DIGITAL_IN PFA-301
DIGITAL_IN TAH-101
MOTOR_VSD UMP-301A
MOTOR_VSD UMP-301B
VALVE_ON_OFF XV-107

* Variables *
REAL CHLOR-PUMP-301AB_Stroke_CMD

* Functions *
GE DetectHighSaturation_GE
LE DetectLowSaturation_LE
TON DeviationPersistTimer_TON
NOT NotDevPersist_NOT
OR PIDInhibit_OR
OR AnyPumpReady_OR
NOT NoPumpAvailable_NOT
NOT NotXV107Open_NOT
OR PumpInhibit_OR
OR ValveTrip_OR

* Data Connections *
FT-301.PV, FIC-301.PV
FIC-301.XOUT, FV-301.Control_Signal
FV-301.Feedback_Pos, FIC-301.X0
FIC-301.Deviation_Alarm, DeviationPersistTimer_TON.IN
DeviationPersistTimer_TON.Q, NotDevPersist_NOT.IN
NotDevPersist_NOT.OUT, PIDInhibit_OR.IN1
FIC-301.XOUT, DetectHighSaturation_GE.IN1
DetectHighSaturation_GE.Q, PIDInhibit_OR.IN2
FIC-301.XOUT, DetectLowSaturation_LE.IN1
DetectLowSaturation_LE.Q, PIDInhibit_OR.IN3
PIDInhibit_OR.OUT, FIC-301.Inhibit
UMP-301A.FB_Ready, AnyPumpReady_OR.IN1
UMP-301B.FB_Ready, AnyPumpReady_OR.IN2
AnyPumpReady_OR.OUT, NoPumpAvailable_NOT.IN
XV-107.FB_Opened, NotXV107Open_NOT.IN
LAL-301.DI_Out, PumpInhibit_OR.IN1
LT-301.Low_Alarm, PumpInhibit_OR.IN2
ANK-301.Bool_Out, PumpInhibit_OR.IN3
NotXV107Open_NOT.OUT, PumpInhibit_OR.IN4
NoPumpAvailable_NOT.OUT, PumpInhibit_OR.IN5
PumpInhibit_OR.OUT, UMP-301A.Inhibit
PumpInhibit_OR.OUT, UMP-301B.Inhibit
PAH-103.DI_Out, ValveTrip_OR.IN1
TAH-101.DI_Out, ValveTrip_OR.IN2
LAL-301.DI_Out, ValveTrip_OR.IN3
ANK-301.Bool_Out, ValveTrip_OR.IN4
ValveTrip_OR.OUT, FV-301.Inhibit
FIC-301.XOUT, CHLOR-PUMP-301AB_Stroke_CMD

* Parameter Data Connections *
3.125, FT-301.Scaling_Slope
-12.5, FT-301.Scaling_Offset
48.0, FT-301.PV_High
8.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
30.0, FIC-301.SP
1.8, FIC-301.KP
0.5, FIC-301.TR
0.05, FIC-301.TD
5.0, FIC-301.MV_MIN
95.0, FIC-301.MV_MAX
0.3, FIC-301.Deviation_Limit
48.0, FIC-301.PV_High
8.0, FIC-301.PV_Low
TRUE, FIC-301.AUTO
100.0, FV-301.Open_Limit
0.0, FV-301.Close_Limit
FALSE, FV-301.Manual_Mode
95.0, DetectHighSaturation_GE.IN2
5.0, DetectLowSaturation_LE.IN2
T#23s, DeviationPersistTimer_TON.PT
20.0, LT-301.PV_Low
```

---


