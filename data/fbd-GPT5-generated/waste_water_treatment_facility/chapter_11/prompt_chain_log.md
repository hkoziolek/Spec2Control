# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 12:03:20

## Step 1: contextgen1-sensors
**Time:** 12:03:20

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
**Time:** 12:04:11

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
**Time:** 12:04:31

### Output:
```
*** Available Control Strategies ***
| Strategy | Probability |
|----------|-------------|
| Ratio Control | 0.95 |
| PID Control | 0.85 |

Selected Control Strategy: Ratio Control
Short explanation: The dosing setpoint is derived by maintaining a fixed ratio to influent flow, with the ratio controller sending a slave setpoint to the PID loop that drives the dosing actuator.

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
**Timestamp:** 2025-09-24 12:05:17

## Step 1: openplc-function-blocks-v2
**Time:** 12:05:17

### Output:
```
* Function Blocks *
ANALOG_IN FIT-104
RATIO_CONTROL FFIC-107
PID_BASIC FIC-106
MOTOR_VSD CD-1001
VALVE_ELECTRIC PV-101
VALVE_ON_OFF XV-102
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 12:05:54

### Output:
```
* Function Blocks *
ANALOG_IN FIT-104
RATIO_CONTROL FFIC-107
PID_BASIC FIC-106
MOTOR_VSD CD-1001
VALVE_ELECTRIC PV-101
VALVE_ON_OFF XV-102
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 12:06:44

### Output:
```
* Functions *

* Block-to-Block Connections *
FIT-104.PV, FFIC-107.PrimaryPV
FFIC-107.SlaveSP, FIC-106.SP
CD-1001.FB_ActualSpeed, FIC-106.PV
FIC-106.XOUT, CD-1001.Speed_SP
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 12:08:02

### Output:
```
* Functions *
NOT XV102NotOpen_NOT
OR PV101Fault_OR
OR PumpFaults_OR
OR CD1001_Inhibit_OR
OR FFIC107_Inhibit_OR

* Data Connections *
FIT-104.Low_Alarm, FFIC107_Inhibit_OR.IN1
FIT-104.General_Fault, FFIC107_Inhibit_OR.IN2
PumpFaults_OR.OUT, FFIC107_Inhibit_OR.IN3
FFIC107_Inhibit_OR.OUT, FFIC-107.Inhibit
XV-102.FB_Opened, XV102NotOpen_NOT.IN
XV102NotOpen_NOT.OUT, CD1001_Inhibit_OR.IN1
PV-101.Alarm, PV101Fault_OR.IN1
PV-101.Position_Error, PV101Fault_OR.IN2
PV101Fault_OR.OUT, CD1001_Inhibit_OR.IN2
XV-102.Alarm_Position_Error, CD1001_Inhibit_OR.IN3
XV-102.Alarm_General, CD1001_Inhibit_OR.IN4
CD1001_Inhibit_OR.OUT, CD-1001.Inhibit
CD-1001.FB_Fault, PumpFaults_OR.IN1
CD-1001.Alarm_Comm_Fail, PumpFaults_OR.IN2
CD-1001.Alarm_Speed_Deviation, PumpFaults_OR.IN3

* Parameter Data Connections *
5000, FIT-104.PV_High
100, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 12:11:06

### Output:
```
* Parameter Data Connections *
6.25, FIT-104.Scaling_Slope
-25.0, FIT-104.Scaling_Offset
100.0, FIT-104.PV_High
0.0, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
2.5, FFIC-107.RatioSP
3.0, FIC-106.Deviation_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 12:13:45

### Output:
```
* Parameter Data Connections *
312.5, FIT-104.Scaling_Slope
-1250.0, FIT-104.Scaling_Offset
5000.0, FIT-104.PV_High
100.0, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
2.5, FFIC-107.RatioSP
0.0, FFIC-107.MV_MIN
15000.0, FFIC-107.MV_MAX
0.0, FFIC-107.Bias
500.0, FFIC-107.ManOut
3.0, FIC-106.Deviation_Limit
0.0, FIC-106.MV_MIN
100.0, FIC-106.MV_MAX
100.0, FIC-106.PV_High
0.0, FIC-106.PV_Low
100.0, PV-101.Open_Limit
0.0, PV-101.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 12:16:22

### Output:
```
* Variables *
REAL FIT104_InfluentFlow_PV
REAL FFIC107_ChemDose_SlaveSP
REAL FFIC107_ActiveRatio

* Data Connections *
FIT-104.PV, FIT104_InfluentFlow_PV
FFIC-107.SlaveSP, FFIC107_ChemDose_SlaveSP
FFIC-107.ActiveRatio, FFIC107_ActiveRatio
```

---

## Step 8: openplc-rule-checks
**Time:** 12:17:37

### Output:
```
* Function Blocks *
ANALOG_IN FIT-104
RATIO_CONTROL FFIC-107
PID_BASIC FIC-106
MOTOR_VSD CD-1001
VALVE_ELECTRIC PV-101
VALVE_ON_OFF XV-102

* Variables *
REAL FIT104_InfluentFlow_PV
REAL FFIC107_ChemDose_SlaveSP
REAL FFIC107_ActiveRatio

* Functions *
NOT XV102_NotOpen
OR PV101_Faults
OR Pump_Faults
OR CD1001_Inhibit
OR FFIC107_Inhibit

* Data Connections * 
FIT-104.PV, FFIC-107.PrimaryPV
CD-1001.FB_ActualSpeed, FFIC-107.SecondaryPV
FFIC-107.SlaveSP, FIC-106.SP
CD-1001.FB_ActualSpeed, FIC-106.PV
FIC-106.XOUT, CD-1001.Speed_SP
FIT-104.Low_Alarm, FFIC107_Inhibit.IN1
FIT-104.General_Fault, FFIC107_Inhibit.IN2
Pump_Faults.OUT, FFIC107_Inhibit.IN3
FFIC107_Inhibit.OUT, FFIC-107.Inhibit
XV-102.FB_Opened, XV102_NotOpen.IN
XV102_NotOpen.OUT, CD1001_Inhibit.IN1
PV-101.Alarm, PV101_Faults.IN1
PV-101.Position_Error, PV101_Faults.IN2
PV101_Faults.OUT, CD1001_Inhibit.IN2
XV-102.Alarm_Position_Error, CD1001_Inhibit.IN3
XV-102.Alarm_General, CD1001_Inhibit.IN4
CD1001_Inhibit.OUT, CD-1001.Inhibit
CD-1001.FB_Fault, Pump_Faults.IN1
CD-1001.Alarm_Comm_Fail, Pump_Faults.IN2
CD-1001.Alarm_Speed_Deviation, Pump_Faults.IN3
FIT-104.PV, FIT104_InfluentFlow_PV
FFIC-107.SlaveSP, FFIC107_ChemDose_SlaveSP
FFIC-107.ActiveRatio, FFIC107_ActiveRatio

* Parameter Data Connections *
"Influent Flow FIT-104", FIT-104.Name
"Influent flow transmitter 0-5000 L/min for ratio control", FIT-104.Description
312.5, FIT-104.Scaling_Slope
-1250.0, FIT-104.Scaling_Offset
5000.0, FIT-104.PV_High
100.0, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
"Chemical Ratio Controller FFIC-107", FFIC-107.Name
"Maintains chemical-to-influent ratio 2.5:1 with bias and limits", FFIC-107.Description
TRUE, FFIC-107.Auto
2.5, FFIC-107.RatioSP
0.0, FFIC-107.Bias
0.0, FFIC-107.TrimKp
T#0s, FFIC-107.TrimTi
0.0, FFIC-107.MV_MIN
15000.0, FFIC-107.MV_MAX
"Chemical Dosing PID FIC-106", FIC-106.Name
"Controls pump speed to meet ratio setpoint", FIC-106.Description
TRUE, FIC-106.AUTO
0.0, FIC-106.MV_MIN
100.0, FIC-106.MV_MAX
0.0, FIC-106.X0
1.0, FIC-106.KP
10.0, FIC-106.TR
0.0, FIC-106.TD
100.0, FIC-106.PV_High
0.0, FIC-106.PV_Low
3.0, FIC-106.Deviation_Limit
"Chemical Dosing Pump CD-1001", CD-1001.Name
"Variable speed chemical dosing pump", CD-1001.Description
T#2s, CD-1001.Accel_Ramp
T#2s, CD-1001.Decel_Ramp
"Pressure Control Valve PV-101", PV-101.Name
"Maintains minimum pressure in dosing header", PV-101.Description
100.0, PV-101.Open_Limit
0.0, PV-101.Close_Limit
T#5s, PV-101.Timeout
"Shut-off Valve XV-102", XV-102.Name
"Enables or disables chemical dosing flow path", XV-102.Description
T#5s, XV-102.Timeout
```

---

## Step 9: openplc-rule-checks2
**Time:** 12:22:55

### Output:
```
* Function Blocks *
ANALOG_IN FIT-104
RATIO_CONTROL FFIC-107
PID_BASIC FIC-106
MOTOR_VSD CD-1001
VALVE_ELECTRIC PV-101
VALVE_ON_OFF XV-102

* Variables *
REAL FIT104_InfluentFlow_PV
REAL FFIC107_ChemDose_SlaveSP
REAL FFIC107_ActiveRatio

* Functions *
NOT XV102_NotOpen
OR PV101_Faults
OR Pump_Faults
OR CD1001_Inhibit
OR FFIC107_Inhibit

* Data Connections * 
FIT-104.PV, FFIC-107.PrimaryPV
CD-1001.FB_ActualSpeed, FFIC-107.SecondaryPV
FFIC-107.SlaveSP, FIC-106.SP
CD-1001.FB_ActualSpeed, FIC-106.PV
FIC-106.XOUT, CD-1001.Speed_SP
FIT-104.Low_Alarm, FFIC107_Inhibit.IN1
FIT-104.General_Fault, FFIC107_Inhibit.IN2
Pump_Faults.OUT, FFIC107_Inhibit.IN3
FFIC107_Inhibit.OUT, FFIC-107.Inhibit
XV-102.FB_Opened, XV102_NotOpen.IN
XV102_NotOpen.OUT, CD1001_Inhibit.IN1
PV-101.Alarm, PV101_Faults.IN1
PV-101.Position_Error, PV101_Faults.IN2
PV101_Faults.OUT, CD1001_Inhibit.IN2
XV-102.Alarm_Position_Error, CD1001_Inhibit.IN3
XV-102.Alarm_General, CD1001_Inhibit.IN4
CD1001_Inhibit.OUT, CD-1001.Inhibit
CD-1001.FB_Fault, Pump_Faults.IN1
CD-1001.Alarm_Comm_Fail, Pump_Faults.IN2
CD-1001.Alarm_Speed_Deviation, Pump_Faults.IN3
FIT-104.PV, FIT104_InfluentFlow_PV
FFIC-107.SlaveSP, FFIC107_ChemDose_SlaveSP
FFIC-107.ActiveRatio, FFIC107_ActiveRatio

* Parameter Data Connections *
"Influent Flow FIT-104", FIT-104.Name
312.5, FIT-104.Scaling_Slope
-1250.0, FIT-104.Scaling_Offset
5000.0, FIT-104.PV_High
100.0, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
"Chemical Ratio Controller FFIC-107", FFIC-107.Name
TRUE, FFIC-107.Auto
2.5, FFIC-107.RatioSP
0.0, FFIC-107.Bias
0.0, FFIC-107.TrimKp
T#0s, FFIC-107.TrimTi
0.0, FFIC-107.MV_MIN
15000.0, FFIC-107.MV_MAX
"Chemical Dosing PID FIC-106", FIC-106.Name
TRUE, FIC-106.AUTO
0.0, FIC-106.MV_MIN
100.0, FIC-106.MV_MAX
0.0, FIC-106.X0
1.0, FIC-106.KP
10.0, FIC-106.TR
0.0, FIC-106.TD
100.0, FIC-106.PV_High
0.0, FIC-106.PV_Low
3.0, FIC-106.Deviation_Limit
"Chemical Dosing Pump CD-1001", CD-1001.Name
T#2s, CD-1001.Accel_Ramp
T#2s, CD-1001.Decel_Ramp
"Pressure Control Valve PV-101", PV-101.Name
100.0, PV-101.Open_Limit
0.0, PV-101.Close_Limit
T#5s, PV-101.Timeout
"Shut-off Valve XV-102", XV-102.Name
T#5s, XV-102.Timeout
```

---

## Step 10: append_two_inputs
**Time:** 12:24:06

### Output:
```
* Function Blocks *
ANALOG_IN FIT-104
RATIO_CONTROL FFIC-107
PID_BASIC FIC-106
MOTOR_VSD CD-1001
VALVE_ELECTRIC PV-101
VALVE_ON_OFF XV-102

* Variables *
REAL FIT104_InfluentFlow_PV
REAL FFIC107_ChemDose_SlaveSP
REAL FFIC107_ActiveRatio

* Functions *
NOT XV102_NotOpen
OR CD1001_Inhibit
OR FFIC107_Inhibit

* Data Connections * 
FIT-104.PV, FFIC-107.PrimaryPV
CD-1001.FB_ActualSpeed, FFIC-107.SecondaryPV
FFIC-107.SlaveSP, FIC-106.SP
CD-1001.FB_ActualSpeed, FIC-106.PV
FIC-106.XOUT, CD-1001.Speed_SP
FIT-104.Low_Alarm, FFIC107_Inhibit.IN1
FIT-104.General_Fault, FFIC107_Inhibit.IN2
CD-1001.FB_Fault, FFIC107_Inhibit.IN3
CD-1001.Alarm_Comm_Fail, FFIC107_Inhibit.IN4
CD-1001.Alarm_Speed_Deviation, FFIC107_Inhibit.IN5
FFIC107_Inhibit.OUT, FFIC-107.Inhibit
XV-102.FB_Opened, XV102_NotOpen.IN
XV102_NotOpen.OUT, CD1001_Inhibit.IN1
PV-101.Alarm, CD1001_Inhibit.IN2
PV-101.Position_Error, CD1001_Inhibit.IN5
XV-102.Alarm_Position_Error, CD1001_Inhibit.IN3
XV-102.Alarm_General, CD1001_Inhibit.IN4
CD1001_Inhibit.OUT, CD-1001.Inhibit
FIT-104.PV, FIT104_InfluentFlow_PV
FFIC-107.SlaveSP, FFIC107_ChemDose_SlaveSP
FFIC-107.ActiveRatio, FFIC107_ActiveRatio

* Parameter Data Connections *
"Influent Flow FIT-104", FIT-104.Name
312.5, FIT-104.Scaling_Slope
-1250.0, FIT-104.Scaling_Offset
5000.0, FIT-104.PV_High
100.0, FIT-104.PV_Low
TRUE, FIT-104.Alarm_Enable
"Chemical Ratio Controller FFIC-107", FFIC-107.Name
TRUE, FFIC-107.Auto
2.5, FFIC-107.RatioSP
0.0, FFIC-107.Bias
0.0, FFIC-107.TrimKp
T#0s, FFIC-107.TrimTi
0.0, FFIC-107.MV_MIN
15000.0, FFIC-107.MV_MAX
"Chemical Dosing PID FIC-106", FIC-106.Name
TRUE, FIC-106.AUTO
0.0, FIC-106.MV_MIN
100.0, FIC-106.MV_MAX
0.0, FIC-106.X0
1.0, FIC-106.KP
10.0, FIC-106.TR
0.0, FIC-106.TD
100.0, FIC-106.PV_High
0.0, FIC-106.PV_Low
3.0, FIC-106.Deviation_Limit
"Chemical Dosing Pump CD-1001", CD-1001.Name
T#2s, CD-1001.Accel_Ramp
T#2s, CD-1001.Decel_Ramp
"Pressure Control Valve PV-101", PV-101.Name
100.0, PV-101.Open_Limit
0.0, PV-101.Close_Limit
T#5s, PV-101.Timeout
"Shut-off Valve XV-102", XV-102.Name
T#5s, XV-102.Timeout
```

---


