# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 00:33:15

## Step 1: contextgen1-sensors
**Time:** 00:33:15

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
**Time:** 00:33:46

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
```

---

## Step 3: contextgen1-strategies
**Time:** 00:34:05

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
| PID Control | 0.99 |
| Cascade Control | 0.08 |
| Duty-Standby | 0.05 |
| VOTING | 0.02 |
| FEEDFORWARD | 0.03 |
| OVERRIDE | 0.55 |
| SPLIT RANGE | 0.02 |
| Ratio Control | 0.02 |

Selected Control Strategy: PID Control 
Short explanation: Two independent single-loop reverse-acting PIDs (FIC-101 and FIC-102) directly control a valve and a pump to maintain specified flow setpoints.

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
**Timestamp:** 2025-09-24 00:35:05

## Step 1: openplc-function-blocks-v2
**Time:** 00:35:05

### Output:
```
* Function Blocks *
ANALOG_IN FT-102
ANALOG_IN FT-104
ANALOG_IN LI-101
PID_BASIC FIC-101
PID_BASIC FIC-102
VALVE_ELECTRIC FV-103
MOTOR_VSD P-001
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 00:35:29

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN FT-102
ANALOG_IN FT-104
ANALOG_IN LI-101
PID_BASIC FIC-101
PID_BASIC FIC-102
VALVE_ELECTRIC FV-103
MOTOR_VSD P-001
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 00:35:57

### Output:
```
* Functions *

* Block-to-Block Connections *
FT-102.PV, FIC-101.PV
FIC-101.XOUT, FV-103.Control_Signal
FT-104.PV, FIC-102.PV
FIC-102.XOUT, P-001.Speed_SP
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 00:36:10

### Output:
```
* Functions * 
OR LevelTrip_OR
OR FIC101Inhibit_OR
OR FIC102Inhibit_OR

* Data Connections *
LI-101.Low_Alarm, LevelTrip_OR.IN1
LI-101.High_Alarm, LevelTrip_OR.IN2
LevelTrip_OR.OUT, FIC101Inhibit_OR.IN1
FT-102.General_Fault, FIC101Inhibit_OR.IN2
LevelTrip_OR.OUT, FIC102Inhibit_OR.IN1
FT-104.General_Fault, FIC102Inhibit_OR.IN2
FIC101Inhibit_OR.OUT, FIC-101.Inhibit
FIC102Inhibit_OR.OUT, FIC-102.Inhibit
LI-101.General_Fault, P-001.Inhibit
LI-101.General_Fault, FV-103.Inhibit

* Parameter Data Connections *
20, LI-101.PV_Low
90, LI-101.PV_High
10, FIC-101.Deviation_Limit
8, FIC-102.Deviation_Limit
0, FIC-101.X0
0, FIC-102.X0
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 00:37:36

### Output:
```
* Parameter Data Connections *
50.0, FIC-101.SP
45.0, FIC-102.SP
2.0, FIC-101.KP
2.0, FIC-102.KP
1.0, FIC-101.TR
1.0, FIC-102.TR
0.1, FIC-101.TD
0.1, FIC-102.TD
0.0, FIC-101.MV_MIN
0.0, FIC-102.MV_MIN
100.0, FIC-101.MV_MAX
100.0, FIC-102.MV_MAX
0.0, FIC-101.X0
0.0, FIC-102.X0
TRUE, FIC-101.AUTO
TRUE, FIC-102.AUTO
6.25, FT-102.Scaling_Slope
-25.0, FT-102.Scaling_Offset
6.25, FT-104.Scaling_Slope
-25.0, FT-104.Scaling_Offset
10.0, FIC-101.Deviation_Limit
8.0, FIC-102.Deviation_Limit
100.0, FV-103.Open_Limit
0.0, FV-103.Close_Limit
20.0, LI-101.PV_Low
90.0, LI-101.PV_High
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 00:38:13

### Output:
```
* Parameter Data Connections *
50.0, FIC-101.SP
45.0, FIC-102.SP
2.0, FIC-101.KP
2.0, FIC-102.KP
1.0, FIC-101.TR
1.0, FIC-102.TR
0.1, FIC-101.TD
0.1, FIC-102.TD
0.0, FIC-101.MV_MIN
0.0, FIC-102.MV_MIN
100.0, FIC-101.MV_MAX
100.0, FIC-102.MV_MAX
0.0, FIC-101.X0
0.0, FIC-102.X0
TRUE, FIC-101.AUTO
TRUE, FIC-102.AUTO
6.25, FT-102.Scaling_Slope
-25.0, FT-102.Scaling_Offset
6.25, FT-104.Scaling_Slope
-25.0, FT-104.Scaling_Offset
10.0, FIC-101.Deviation_Limit
8.0, FIC-102.Deviation_Limit
100.0, FV-103.Open_Limit
0.0, FV-103.Close_Limit
20.0, LI-101.PV_Low
90.0, LI-101.PV_High
TRUE, LI-101.Alarm_Enable
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 00:39:44

### Output:
```
* Variables *
REAL FV103_ControlSignal_From_FIC101
REAL P001_SpeedCmd_From_FIC102

* Data Connections *
FIC-101.XOUT, FV103_ControlSignal_From_FIC101
FIC-102.XOUT, P001_SpeedCmd_From_FIC102
```

---

## Step 8: openplc-rule-checks
**Time:** 00:40:11

### Output:
```
* Function Blocks *
ANALOG_IN FT-102
ANALOG_IN FT-104
ANALOG_IN LI-101
PID_BASIC FIC-101
PID_BASIC FIC-102
VALVE_ELECTRIC FV-103
MOTOR_VSD P-001

* Variables *
REAL FV103_ControlSignal_From_FIC101
REAL P001_SpeedCmd_From_FIC102
BOOL LevelTrip
BOOL PumpStartPermissive
BOOL ValveOpenPermit
BOOL FT102_FlowAbove10
BOOL FlowValid_DelayOK
BOOL ValveOpenFB_OK
BOOL FIC101_DeviationAlarm_15s
BOOL FIC102_DeviationAlarm_15s

* Functions *
OR LevelTripOR
NOT LevelTripNOT
OR FIC101InhibitOR
OR FIC102InhibitOR
GT FT102_GT_10GPM
TON FT102_Flow_Valid_TON
AND ValveOpenPermitAND
NOT ValveOpenPermitNOT
OR ValveInhibitOR1
OR ValveInhibitOR2
GE LI101_GE_25PCT
GE FV103_FB_GE_90PCT
AND PumpStartPermissiveAND
NOT PumpStartPermissiveNOT
OR PumpInhibitOR
TON FIC101_DevAlarm_TON
TON FIC102_DevAlarm_TON

* Data Connections *
FT-102.PV, FIC-101.PV
FIC-101.XOUT, FV-103.Control_Signal
FT-104.PV, FIC-102.PV
FIC-102.XOUT, P-001.Speed_SP
FIC-101.XOUT, FV103_ControlSignal_From_FIC101
FIC-102.XOUT, P001_SpeedCmd_From_FIC102
LI-101.Low_Alarm, LevelTripOR.IN1
LI-101.High_Alarm, LevelTripOR.IN2
LevelTripOR.OUT, LevelTrip
LevelTrip, LevelTripNOT.IN
LevelTripNOT.OUT, FIC-101.AUTO
LevelTripNOT.OUT, FIC-102.AUTO
LevelTrip, FIC101InhibitOR.IN1
FT-102.General_Fault, FIC101InhibitOR.IN2
FIC101InhibitOR.OUT, FIC-101.Inhibit
LevelTrip, FIC102InhibitOR.IN1
FT-104.General_Fault, FIC102InhibitOR.IN2
FIC102InhibitOR.OUT, FIC-102.Inhibit
LI-101.PV, LI101_GE_25PCT.IN1
LI101_GE_25PCT.OUT, PumpStartPermissiveAND.IN1
FV-103.Feedback_Pos, FV103_FB_GE_90PCT.IN1
FV103_FB_GE_90PCT.OUT, PumpStartPermissiveAND.IN2
PumpStartPermissiveAND.OUT, PumpStartPermissive
PumpStartPermissive, PumpStartPermissiveNOT.IN
PumpStartPermissiveNOT.OUT, PumpInhibitOR.IN1
LI-101.General_Fault, PumpInhibitOR.IN2
PumpInhibitOR.OUT, P-001.Inhibit
FT-102.PV, FT102_GT_10GPM.IN1
FT102_GT_10GPM.OUT, FT102_Flow_Valid_TON.IN
FT102_Flow_Valid_TON.Q, FlowValid_DelayOK
P-001.FB_Running, ValveOpenPermitAND.IN1
FlowValid_DelayOK, ValveOpenPermitAND.IN2
ValveOpenPermitAND.OUT, ValveOpenPermit
ValveOpenPermit, ValveOpenPermitNOT.IN
ValveOpenPermitNOT.OUT, ValveInhibitOR1.IN1
LevelTrip, ValveInhibitOR1.IN2
ValveInhibitOR1.OUT, ValveInhibitOR2.IN1
LI-101.General_Fault, ValveInhibitOR2.IN2
ValveInhibitOR2.OUT, FV-103.Inhibit
FIC-101.Deviation_Alarm, FIC101_DevAlarm_TON.IN
FIC101_DevAlarm_TON.Q, FIC101_DeviationAlarm_15s
FIC-102.Deviation_Alarm, FIC102_DevAlarm_TON.IN
FIC102_DevAlarm_TON.Q, FIC102_DeviationAlarm_15s

* Parameter Data Connections *
50.0, FIC-101.SP
45.0, FIC-102.SP
2.0, FIC-101.KP
2.0, FIC-102.KP
1.0, FIC-101.TR
1.0, FIC-102.TR
0.1, FIC-101.TD
0.1, FIC-102.TD
0.0, FIC-101.MV_MIN
0.0, FIC-102.MV_MIN
100.0, FIC-101.MV_MAX
100.0, FIC-102.MV_MAX
0.0, FIC-101.X0
0.0, FIC-102.X0
6.25, FT-102.Scaling_Slope
-25.0, FT-102.Scaling_Offset
6.25, FT-104.Scaling_Slope
-25.0, FT-104.Scaling_Offset
10.0, FIC-101.Deviation_Limit
8.0, FIC-102.Deviation_Limit
100.0, FV-103.Open_Limit
0.0, FV-103.Close_Limit
20.0, LI-101.PV_Low
90.0, LI-101.PV_High
TRUE, LI-101.Alarm_Enable
T#8s, FT102_Flow_Valid_TON.PT
T#15s, FIC101_DevAlarm_TON.PT
T#15s, FIC102_DevAlarm_TON.PT
25.0, LI101_GE_25PCT.IN2
90.0, FV103_FB_GE_90PCT.IN2
10.0, FT102_GT_10GPM.IN2
```

---

## Step 9: openplc-rule-checks2
**Time:** 00:42:04

### Output:
```
* Function Blocks *
ANALOG_IN FT-102
ANALOG_IN FT-104
ANALOG_IN LI-101
PID_BASIC FIC-101
PID_BASIC FIC-102
VALVE_ELECTRIC FV-103
MOTOR_VSD P-001
TON FT102_Flow_Valid_TON
TON FIC101_DevAlarm_TON
TON FIC102_DevAlarm_TON

* Variables *
REAL FV103_ControlSignal_From_FIC101
REAL P001_SpeedCmd_From_FIC102
BOOL LevelTrip
BOOL PumpStartPermissive
BOOL ValveOpenPermit
BOOL FT102_FlowAbove10
BOOL FlowValid_DelayOK
BOOL ValveOpenFB_OK
BOOL FIC101_DeviationAlarm_15s
BOOL FIC102_DeviationAlarm_15s

* Functions *
OR LevelTripOR
NOT LevelTripNOT
OR FIC101InhibitOR
OR FIC102InhibitOR
GT FT102_GT_10GPM
AND ValveOpenPermitAND
NOT ValveOpenPermitNOT
OR ValveInhibitOR1
OR ValveInhibitOR2
GE LI101_GE_25PCT
GE FV103_FB_GE_90PCT
AND PumpStartPermissiveAND
NOT PumpStartPermissiveNOT
OR PumpInhibitOR

* Data Connections *
FT-102.PV, FIC-101.PV
FIC-101.XOUT, FV-103.Control_Signal
FT-104.PV, FIC-102.PV
FIC-102.XOUT, P-001.Speed_SP
FIC-101.XOUT, FV103_ControlSignal_From_FIC101
FIC-102.XOUT, P001_SpeedCmd_From_FIC102
LI-101.Low_Alarm, LevelTripOR.IN1
LI-101.High_Alarm, LevelTripOR.IN2
LevelTripOR.OUT, LevelTrip
LevelTrip, LevelTripNOT.IN
LevelTripNOT.OUT, FIC-101.AUTO
LevelTripNOT.OUT, FIC-102.AUTO
LevelTrip, FIC101InhibitOR.IN1
FT-102.General_Fault, FIC101InhibitOR.IN2
FIC101InhibitOR.OUT, FIC-101.Inhibit
LevelTrip, FIC102InhibitOR.IN1
FT-104.General_Fault, FIC102InhibitOR.IN2
FIC102InhibitOR.OUT, FIC-102.Inhibit
LI-101.PV, LI101_GE_25PCT.IN1
LI101_GE_25PCT.OUT, PumpStartPermissiveAND.IN1
FV-103.Feedback_Pos, FV103_FB_GE_90PCT.IN1
FV103_FB_GE_90PCT.OUT, PumpStartPermissiveAND.IN2
PumpStartPermissiveAND.OUT, PumpStartPermissive
PumpStartPermissive, PumpStartPermissiveNOT.IN
PumpStartPermissiveNOT.OUT, PumpInhibitOR.IN1
LI-101.General_Fault, PumpInhibitOR.IN2
PumpInhibitOR.OUT, P-001.Inhibit
FT-102.PV, FT102_GT_10GPM.IN1
FT102_GT_10GPM.OUT, FT102_Flow_Valid_TON.IN
FT102_Flow_Valid_TON.Q, FlowValid_DelayOK
P-001.FB_Running, ValveOpenPermitAND.IN1
FlowValid_DelayOK, ValveOpenPermitAND.IN2
ValveOpenPermitAND.OUT, ValveOpenPermit
ValveOpenPermit, ValveOpenPermitNOT.IN
ValveOpenPermitNOT.OUT, ValveInhibitOR1.IN1
LevelTrip, ValveInhibitOR1.IN2
ValveInhibitOR1.OUT, ValveInhibitOR2.IN1
LI-101.General_Fault, ValveInhibitOR2.IN2
ValveInhibitOR2.OUT, FV-103.Inhibit
FIC-101.Deviation_Alarm, FIC101_DevAlarm_TON.IN
FIC101_DevAlarm_TON.Q, FIC101_DeviationAlarm_15s
FIC-102.Deviation_Alarm, FIC102_DevAlarm_TON.IN
FIC102_DevAlarm_TON.Q, FIC102_DeviationAlarm_15s

* Parameter Data Connections *
50.0, FIC-101.SP
45.0, FIC-102.SP
2.0, FIC-101.KP
2.0, FIC-102.KP
1.0, FIC-101.TR
1.0, FIC-102.TR
0.1, FIC-101.TD
0.1, FIC-102.TD
0.0, FIC-101.MV_MIN
0.0, FIC-102.MV_MIN
100.0, FIC-101.MV_MAX
100.0, FIC-102.MV_MAX
0.0, FIC-101.X0
0.0, FIC-102.X0
6.25, FT-102.Scaling_Slope
-25.0, FT-102.Scaling_Offset
6.25, FT-104.Scaling_Slope
-25.0, FT-104.Scaling_Offset
10.0, FIC-101.Deviation_Limit
8.0, FIC-102.Deviation_Limit
100.0, FV-103.Open_Limit
0.0, FV-103.Close_Limit
20.0, LI-101.PV_Low
90.0, LI-101.PV_High
TRUE, LI-101.Alarm_Enable
T#8s, FT102_Flow_Valid_TON.PT
T#15s, FIC101_DevAlarm_TON.PT
T#15s, FIC102_DevAlarm_TON.PT
25.0, LI101_GE_25PCT.IN2
90.0, FV103_FB_GE_90PCT.IN2
10.0, FT102_GT_10GPM.IN2
```

---

## Step 10: append_two_inputs
**Time:** 00:42:40

### Output:
```
* Function Blocks *
ANALOG_IN FT-102
ANALOG_IN FT-104
ANALOG_IN LI-101
PID_BASIC FIC-101
PID_BASIC FIC-102
VALVE_ELECTRIC FV-103
MOTOR_VSD P-001
TON FT102_Flow_Valid_TON
TON FIC101_DevAlarm_TON
TON FIC102_DevAlarm_TON

* Variables *
REAL FV103_ControlSignal_From_FIC101
REAL P001_SpeedCmd_From_FIC102
BOOL LevelTrip
BOOL PumpStartPermissive
BOOL ValveOpenPermit
BOOL FT102_FlowAbove10
BOOL FlowValid_DelayOK
BOOL ValveOpenFB_OK
BOOL FIC101_DeviationAlarm_15s
BOOL FIC102_DeviationAlarm_15s

* Functions *
OR LevelTripOR
NOT LevelTripNOT
OR FIC101InhibitOR
OR FIC102InhibitOR
GT FT102_GT_10GPM
AND ValveOpenPermitAND
NOT ValveOpenPermitNOT
OR ValveInhibitOR1
OR ValveInhibitOR2
GE LI101_GE_25PCT
GE FV103_FB_GE_90PCT
AND PumpStartPermissiveAND
NOT PumpStartPermissiveNOT
OR PumpInhibitOR

* Data Connections *
FT-102.PV, FIC-101.PV
FIC-101.XOUT, FV-103.Control_Signal
FT-104.PV, FIC-102.PV
FIC-102.XOUT, P-001.Speed_SP
FIC-101.XOUT, FV103_ControlSignal_From_FIC101
FIC-102.XOUT, P001_SpeedCmd_From_FIC102
LI-101.Low_Alarm, LevelTripOR.IN1
LI-101.High_Alarm, LevelTripOR.IN2
LevelTripOR.OUT, LevelTrip
LevelTrip, LevelTripNOT.IN
LevelTripNOT.OUT, FIC-101.AUTO
LevelTripNOT.OUT, FIC-102.AUTO
LevelTrip, FIC101InhibitOR.IN1
FT-102.General_Fault, FIC101InhibitOR.IN2
FIC101InhibitOR.OUT, FIC-101.Inhibit
LevelTrip, FIC102InhibitOR.IN1
FT-104.General_Fault, FIC102InhibitOR.IN2
FIC102InhibitOR.OUT, FIC-102.Inhibit
LI-101.PV, LI101_GE_25PCT.IN1
LI101_GE_25PCT.OUT, PumpStartPermissiveAND.IN1
FV-103.Feedback_Pos, FV103_FB_GE_90PCT.IN1
FV103_FB_GE_90PCT.OUT, PumpStartPermissiveAND.IN2
PumpStartPermissiveAND.OUT, PumpStartPermissive
PumpStartPermissive, PumpStartPermissiveNOT.IN
PumpStartPermissiveNOT.OUT, PumpInhibitOR.IN1
LI-101.General_Fault, PumpInhibitOR.IN2
PumpInhibitOR.OUT, P-001.Inhibit
FT-102.PV, FT102_GT_10GPM.IN1
FT102_GT_10GPM.OUT, FT102_Flow_Valid_TON.IN
FT102_Flow_Valid_TON.Q, FlowValid_DelayOK
P-001.FB_Running, ValveOpenPermitAND.IN1
FlowValid_DelayOK, ValveOpenPermitAND.IN2
ValveOpenPermitAND.OUT, ValveOpenPermit
ValveOpenPermit, ValveOpenPermitNOT.IN
ValveOpenPermitNOT.OUT, ValveInhibitOR1.IN1
LevelTrip, ValveInhibitOR1.IN2
ValveInhibitOR1.OUT, ValveInhibitOR2.IN1
LI-101.General_Fault, ValveInhibitOR2.IN2
ValveInhibitOR2.OUT, FV-103.Inhibit
FIC-101.Deviation_Alarm, FIC101_DevAlarm_TON.IN
FIC101_DevAlarm_TON.Q, FIC101_DeviationAlarm_15s
FIC-102.Deviation_Alarm, FIC102_DevAlarm_TON.IN
FIC102_DevAlarm_TON.Q, FIC102_DeviationAlarm_15s

* Parameter Data Connections *
50.0, FIC-101.SP
45.0, FIC-102.SP
2.0, FIC-101.KP
2.0, FIC-102.KP
1.0, FIC-101.TR
1.0, FIC-102.TR
0.1, FIC-101.TD
0.1, FIC-102.TD
0.0, FIC-101.MV_MIN
0.0, FIC-102.MV_MIN
100.0, FIC-101.MV_MAX
100.0, FIC-102.MV_MAX
0.0, FIC-101.X0
0.0, FIC-102.X0
6.25, FT-102.Scaling_Slope
-25.0, FT-102.Scaling_Offset
6.25, FT-104.Scaling_Slope
-25.0, FT-104.Scaling_Offset
10.0, FIC-101.Deviation_Limit
8.0, FIC-102.Deviation_Limit
100.0, FV-103.Open_Limit
0.0, FV-103.Close_Limit
20.0, LI-101.PV_Low
90.0, LI-101.PV_High
TRUE, LI-101.Alarm_Enable
T#8s, FT102_Flow_Valid_TON.PT
T#15s, FIC101_DevAlarm_TON.PT
T#15s, FIC102_DevAlarm_TON.PT
25.0, LI101_GE_25PCT.IN2
90.0, FV103_FB_GE_90PCT.IN2
10.0, FT102_GT_10GPM.IN2
```

---


