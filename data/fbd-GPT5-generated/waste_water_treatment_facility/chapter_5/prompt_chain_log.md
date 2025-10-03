# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 10:26:10

## Step 1: contextgen1-sensors
**Time:** 10:26:10

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
```

---

## Step 2: contextgen1-actuators
**Time:** 10:26:32

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
```

---

## Step 3: contextgen1-strategies
**Time:** 10:27:02

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| PID Control | 0.98 |
| OVERRIDE | 0.30 |

Selected Control Strategy: PID Control 
Short explanation: Two independent PID loops (pH and alkalinity) directly modulate the chemical dosing pump CD-401 to maintain setpoints, matching the narrative’s core control behavior.

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
**Timestamp:** 2025-09-24 10:28:11

## Step 1: openplc-function-blocks-v2
**Time:** 10:28:11

### Output:
```
* Function Blocks *
ANALOG_IN AC-401
MOTOR_VSD CD-401
ANALOG_IN FT-101
ANALOG_IN LT-401
ANALOG_IN PH-401
PID_BASIC PIC-401
PID_BASIC PIC-402
ANALOG_IN TS-401
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 10:28:34

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN AC-401
MOTOR_VSD CD-401
ANALOG_IN FT-101
ANALOG_IN LT-401
ANALOG_IN PH-401
PID_BASIC PIC-401
PID_BASIC PIC-402
ANALOG_IN TS-401
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 10:29:21

### Output:
```
* Functions *
GT Compare_PID_Outputs_GT
SEL Select_Max_MV_SEL

* Block-to-Block Connections *
PH-401.PV, PIC-401.PV
AC-401.PV, PIC-402.PV
PIC-401.XOUT, Compare_PID_Outputs_GT.IN1
PIC-402.XOUT, Compare_PID_Outputs_GT.IN2
Compare_PID_Outputs_GT.OUT, Select_Max_MV_SEL.G
PIC-402.XOUT, Select_Max_MV_SEL.IN0
PIC-401.XOUT, Select_Max_MV_SEL.IN1
Select_Max_MV_SEL.OUT, CD-401.Speed_SP
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 10:31:01

### Output:
```
* Functions * 
OR pHTrip_OR
OR AlkTrip_OR
OR SensorFaults_OR
OR FlowFault_OR
OR LevelTrip_OR
OR CD401_Inhibit_OR

* Data Connections *
PH-401.High_Alarm, pHTrip_OR.IN1
PH-401.Low_Alarm, pHTrip_OR.IN2
AC-401.High_Alarm, AlkTrip_OR.IN1
AC-401.Low_Alarm, AlkTrip_OR.IN2
PH-401.General_Fault, SensorFaults_OR.IN1
AC-401.General_Fault, SensorFaults_OR.IN2
FT-101.Low_Alarm, FlowFault_OR.IN1
FT-101.General_Fault, FlowFault_OR.IN2
LT-401.Low_Alarm, LevelTrip_OR.IN1
TS-401.Low_Alarm, LevelTrip_OR.IN2
pHTrip_OR.OUT, CD401_Inhibit_OR.IN1
AlkTrip_OR.OUT, CD401_Inhibit_OR.IN2
FlowFault_OR.OUT, CD401_Inhibit_OR.IN3
LevelTrip_OR.OUT, CD401_Inhibit_OR.IN4
SensorFaults_OR.OUT, CD401_Inhibit_OR.IN5
CD401_Inhibit_OR.OUT, CD-401.Inhibit
SensorFaults_OR.OUT, PIC-401.Inhibit
SensorFaults_OR.OUT, PIC-402.Inhibit

* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
300, AC-401.PV_High
50, AC-401.PV_Low
50, FT-101.PV_Low
20, LT-401.PV_Low
10, TS-401.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 10:32:35

### Output:
```
* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
TRUE, PH-401.Alarm_Enable
0.875, PH-401.Scaling_Slope
-3.5, PH-401.Scaling_Offset
300.0, AC-401.PV_High
50.0, AC-401.PV_Low
TRUE, AC-401.Alarm_Enable
31.25, AC-401.Scaling_Slope
-125.0, AC-401.Scaling_Offset
10.0, LT-401.PV_Low
TRUE, LT-401.Alarm_Enable
6.25, LT-401.Scaling_Slope
-25.0, LT-401.Scaling_Offset
7.0, PIC-401.SP
2.0, PIC-401.KP
1.0, PIC-401.TR
0.2, PIC-401.TD
0.0, PIC-401.MV_MIN
100.0, PIC-401.MV_MAX
8.0, PIC-401.PV_High
6.0, PIC-401.PV_Low
0.1, PIC-401.Deviation_Limit
150.0, PIC-402.SP
1.5, PIC-402.KP
0.8, PIC-402.TR
0.1, PIC-402.TD
0.0, PIC-402.MV_MIN
75.0, PIC-402.MV_MAX
300.0, PIC-402.PV_High
50.0, PIC-402.PV_Low
5.0, PIC-402.Deviation_Limit
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 10:33:41

### Output:
```
* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
TRUE, PH-401.Alarm_Enable
0.875, PH-401.Scaling_Slope
-3.5, PH-401.Scaling_Offset
300.0, AC-401.PV_High
50.0, AC-401.PV_Low
TRUE, AC-401.Alarm_Enable
31.25, AC-401.Scaling_Slope
-125.0, AC-401.Scaling_Offset
50.0, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
20.0, LT-401.PV_Low
TRUE, LT-401.Alarm_Enable
6.25, LT-401.Scaling_Slope
-25.0, LT-401.Scaling_Offset
10.0, TS-401.PV_Low
TRUE, TS-401.Alarm_Enable
7.0, PIC-401.SP
2.0, PIC-401.KP
1.0, PIC-401.TR
0.2, PIC-401.TD
0.0, PIC-401.MV_MIN
100.0, PIC-401.MV_MAX
8.0, PIC-401.PV_High
6.0, PIC-401.PV_Low
0.1, PIC-401.Deviation_Limit
150.0, PIC-402.SP
1.5, PIC-402.KP
0.8, PIC-402.TR
0.1, PIC-402.TD
0.0, PIC-402.MV_MIN
75.0, PIC-402.MV_MAX
300.0, PIC-402.PV_High
50.0, PIC-402.PV_Low
5.0, PIC-402.Deviation_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 10:34:55

### Output:
```
* Variables *
REAL PH_401_pH_PV
REAL AC_401_Alkalinity_PV
REAL FT_101_InfluentFlow_PV
REAL LT_401_TankLevel_PV
REAL TS_401_Temperature_PV
REAL PIC_401_pH_MV_Percent
REAL PIC_402_Alkalinity_MV_Percent

* Data Connections *
PH-401.PV, PH_401_pH_PV
AC-401.PV, AC_401_Alkalinity_PV
FT-101.PV, FT_101_InfluentFlow_PV
LT-401.PV, LT_401_TankLevel_PV
TS-401.PV, TS_401_Temperature_PV
PIC-401.XOUT, PIC_401_pH_MV_Percent
PIC-402.XOUT, PIC_402_Alkalinity_MV_Percent
```

---

## Step 8: openplc-rule-checks
**Time:** 10:36:13

### Output:
```
* Function Blocks *
ANALOG_IN AC-401
MOTOR_VSD CD-401
ANALOG_IN FT-101
ANALOG_IN LT-401
ANALOG_IN PH-401
PID_BASIC PIC-401
PID_BASIC PIC-402
ANALOG_IN TS-401

* Variables *
REAL PH_401_pH_PV
REAL AC_401_Alkalinity_PV
REAL FT_101_InfluentFlow_PV
REAL LT_401_TankLevel_PV
REAL TS_401_Temperature_PV
REAL PIC_401_pH_MV_Percent
REAL PIC_402_Alkalinity_MV_Percent

* Functions *
GT Compare_PID_Outputs_GT
SEL Select_Max_MV_SEL
OR pHTrip_OR
OR AlkTrip_OR
OR SensorFaults_OR
OR FlowFault_OR
OR LevelTrip_OR
OR CD401_Inhibit_OR

* Data Connections * 
PH-401.PV, PIC-401.PV
AC-401.PV, PIC-402.PV
PIC-401.XOUT, Compare_PID_Outputs_GT.IN1
PIC-402.XOUT, Compare_PID_Outputs_GT.IN2
Compare_PID_Outputs_GT.OUT, Select_Max_MV_SEL.G
PIC-402.XOUT, Select_Max_MV_SEL.IN0
PIC-401.XOUT, Select_Max_MV_SEL.IN1
Select_Max_MV_SEL.OUT, CD-401.Speed_SP
PH-401.High_Alarm, pHTrip_OR.IN1
PH-401.Low_Alarm, pHTrip_OR.IN2
AC-401.High_Alarm, AlkTrip_OR.IN1
AC-401.Low_Alarm, AlkTrip_OR.IN2
PH-401.General_Fault, SensorFaults_OR.IN1
AC-401.General_Fault, SensorFaults_OR.IN2
FT-101.Low_Alarm, FlowFault_OR.IN1
FT-101.General_Fault, FlowFault_OR.IN2
LT-401.Low_Alarm, LevelTrip_OR.IN1
TS-401.Low_Alarm, LevelTrip_OR.IN2
pHTrip_OR.OUT, CD401_Inhibit_OR.IN1
AlkTrip_OR.OUT, CD401_Inhibit_OR.IN2
FlowFault_OR.OUT, CD401_Inhibit_OR.IN3
LevelTrip_OR.OUT, CD401_Inhibit_OR.IN4
SensorFaults_OR.OUT, CD401_Inhibit_OR.IN5
CD401_Inhibit_OR.OUT, CD-401.Inhibit
SensorFaults_OR.OUT, PIC-401.Inhibit
SensorFaults_OR.OUT, PIC-402.Inhibit
PH-401.PV, PH_401_pH_PV
AC-401.PV, AC_401_Alkalinity_PV
FT-101.PV, FT_101_InfluentFlow_PV
LT-401.PV, LT_401_TankLevel_PV
TS-401.PV, TS_401_Temperature_PV
PIC-401.XOUT, PIC_401_pH_MV_Percent
PIC-402.XOUT, PIC_402_Alkalinity_MV_Percent

* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
TRUE, PH-401.Alarm_Enable
0.875, PH-401.Scaling_Slope
-3.5, PH-401.Scaling_Offset
300.0, AC-401.PV_High
50.0, AC-401.PV_Low
TRUE, AC-401.Alarm_Enable
31.25, AC-401.Scaling_Slope
-125.0, AC-401.Scaling_Offset
50.0, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
20.0, LT-401.PV_Low
TRUE, LT-401.Alarm_Enable
6.25, LT-401.Scaling_Slope
-25.0, LT-401.Scaling_Offset
10.0, TS-401.PV_Low
TRUE, TS-401.Alarm_Enable
7.0, PIC-401.SP
2.0, PIC-401.KP
1.0, PIC-401.TR
0.2, PIC-401.TD
0.0, PIC-401.MV_MIN
100.0, PIC-401.MV_MAX
8.0, PIC-401.PV_High
6.0, PIC-401.PV_Low
0.1, PIC-401.Deviation_Limit
TRUE, PIC-401.AUTO
150.0, PIC-402.SP
1.5, PIC-402.KP
0.8, PIC-402.TR
0.1, PIC-402.TD
0.0, PIC-402.MV_MIN
75.0, PIC-402.MV_MAX
300.0, PIC-402.PV_High
50.0, PIC-402.PV_Low
5.0, PIC-402.Deviation_Limit
TRUE, PIC-402.AUTO
```

---

## Step 9: openplc-rule-checks2
**Time:** 10:37:39

### Output:
```
* Function Blocks *
ANALOG_IN AC-401
MOTOR_VSD CD-401
ANALOG_IN FT-101
ANALOG_IN LT-401
ANALOG_IN PH-401
PID_BASIC PIC-401
PID_BASIC PIC-402
ANALOG_IN TS-401

* Variables *
REAL PH_401_pH_PV
REAL AC_401_Alkalinity_PV
REAL FT_101_InfluentFlow_PV
REAL LT_401_TankLevel_PV
REAL TS_401_Temperature_PV
REAL PIC_401_pH_MV_Percent
REAL PIC_402_Alkalinity_MV_Percent

* Functions *
GT Compare_PID_Outputs_GT
SEL Select_Max_MV_SEL
OR pHTrip_OR
OR AlkTrip_OR
OR SensorFaults_OR
OR FlowFault_OR
OR LevelTrip_OR
OR CD401_Inhibit_OR

* Data Connections * 
PH-401.PV, PIC-401.PV
AC-401.PV, PIC-402.PV
PIC-401.XOUT, Compare_PID_Outputs_GT.IN1
PIC-402.XOUT, Compare_PID_Outputs_GT.IN2
Compare_PID_Outputs_GT.OUT, Select_Max_MV_SEL.G
PIC-402.XOUT, Select_Max_MV_SEL.IN0
PIC-401.XOUT, Select_Max_MV_SEL.IN1
Select_Max_MV_SEL.OUT, CD-401.Speed_SP
PH-401.High_Alarm, pHTrip_OR.IN1
PH-401.Low_Alarm, pHTrip_OR.IN2
AC-401.High_Alarm, AlkTrip_OR.IN1
AC-401.Low_Alarm, AlkTrip_OR.IN2
PH-401.General_Fault, SensorFaults_OR.IN1
AC-401.General_Fault, SensorFaults_OR.IN2
FT-101.Low_Alarm, FlowFault_OR.IN1
FT-101.General_Fault, FlowFault_OR.IN2
LT-401.Low_Alarm, LevelTrip_OR.IN1
TS-401.Low_Alarm, LevelTrip_OR.IN2
pHTrip_OR.OUT, CD401_Inhibit_OR.IN1
AlkTrip_OR.OUT, CD401_Inhibit_OR.IN2
FlowFault_OR.OUT, CD401_Inhibit_OR.IN3
LevelTrip_OR.OUT, CD401_Inhibit_OR.IN4
SensorFaults_OR.OUT, CD401_Inhibit_OR.IN5
CD401_Inhibit_OR.OUT, CD-401.Inhibit
SensorFaults_OR.OUT, PIC-401.Inhibit
SensorFaults_OR.OUT, PIC-402.Inhibit
PH-401.PV, PH_401_pH_PV
AC-401.PV, AC_401_Alkalinity_PV
FT-101.PV, FT_101_InfluentFlow_PV
LT-401.PV, LT_401_TankLevel_PV
TS-401.PV, TS_401_Temperature_PV
PIC-401.XOUT, PIC_401_pH_MV_Percent
PIC-402.XOUT, PIC_402_Alkalinity_MV_Percent

* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
TRUE, PH-401.Alarm_Enable
0.875, PH-401.Scaling_Slope
-3.5, PH-401.Scaling_Offset
300.0, AC-401.PV_High
50.0, AC-401.PV_Low
TRUE, AC-401.Alarm_Enable
31.25, AC-401.Scaling_Slope
-125.0, AC-401.Scaling_Offset
50.0, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
20.0, LT-401.PV_Low
TRUE, LT-401.Alarm_Enable
6.25, LT-401.Scaling_Slope
-25.0, LT-401.Scaling_Offset
10.0, TS-401.PV_Low
TRUE, TS-401.Alarm_Enable
7.0, PIC-401.SP
2.0, PIC-401.KP
1.0, PIC-401.TR
0.2, PIC-401.TD
0.0, PIC-401.MV_MIN
100.0, PIC-401.MV_MAX
8.0, PIC-401.PV_High
6.0, PIC-401.PV_Low
0.1, PIC-401.Deviation_Limit
TRUE, PIC-401.AUTO
150.0, PIC-402.SP
1.5, PIC-402.KP
0.8, PIC-402.TR
0.1, PIC-402.TD
0.0, PIC-402.MV_MIN
75.0, PIC-402.MV_MAX
300.0, PIC-402.PV_High
50.0, PIC-402.PV_Low
5.0, PIC-402.Deviation_Limit
TRUE, PIC-402.AUTO
```

---

## Step 10: append_two_inputs
**Time:** 10:38:10

### Output:
```
* Function Blocks *
ANALOG_IN AC-401
MOTOR_VSD CD-401
ANALOG_IN FT-101
ANALOG_IN LT-401
ANALOG_IN PH-401
PID_BASIC PIC-401
PID_BASIC PIC-402
ANALOG_IN TS-401

* Variables *
REAL PH_401_pH_PV
REAL AC_401_Alkalinity_PV
REAL FT_101_InfluentFlow_PV
REAL LT_401_TankLevel_PV
REAL TS_401_Temperature_PV
REAL PIC_401_pH_MV_Percent
REAL PIC_402_Alkalinity_MV_Percent

* Functions *
GT Compare_PID_Outputs_GT
SEL Select_Max_MV_SEL
OR SensorFaults_OR
OR CD401_Inhibit_OR

* Data Connections * 
PH-401.PV, PIC-401.PV
AC-401.PV, PIC-402.PV
PIC-401.XOUT, Compare_PID_Outputs_GT.IN1
PIC-402.XOUT, Compare_PID_Outputs_GT.IN2
Compare_PID_Outputs_GT.OUT, Select_Max_MV_SEL.G
PIC-402.XOUT, Select_Max_MV_SEL.IN0
PIC-401.XOUT, Select_Max_MV_SEL.IN1
Select_Max_MV_SEL.OUT, CD-401.Speed_SP
PH-401.High_Alarm, CD401_Inhibit_OR.IN1
PH-401.Low_Alarm, CD401_Inhibit_OR.IN2
AC-401.High_Alarm, CD401_Inhibit_OR.IN3
AC-401.Low_Alarm, CD401_Inhibit_OR.IN4
PH-401.General_Fault, SensorFaults_OR.IN1
AC-401.General_Fault, SensorFaults_OR.IN2
FT-101.Low_Alarm, CD401_Inhibit_OR.IN5
FT-101.General_Fault, CD401_Inhibit_OR.IN6
LT-401.Low_Alarm, CD401_Inhibit_OR.IN7
TS-401.Low_Alarm, CD401_Inhibit_OR.IN8
SensorFaults_OR.OUT, CD401_Inhibit_OR.IN9
CD401_Inhibit_OR.OUT, CD-401.Inhibit
SensorFaults_OR.OUT, PIC-401.Inhibit
SensorFaults_OR.OUT, PIC-402.Inhibit
PH-401.PV, PH_401_pH_PV
AC-401.PV, AC_401_Alkalinity_PV
FT-101.PV, FT_101_InfluentFlow_PV
LT-401.PV, LT_401_TankLevel_PV
TS-401.PV, TS_401_Temperature_PV
PIC-401.XOUT, PIC_401_pH_MV_Percent
PIC-402.XOUT, PIC_402_Alkalinity_MV_Percent

* Parameter Data Connections *
8.0, PH-401.PV_High
6.0, PH-401.PV_Low
TRUE, PH-401.Alarm_Enable
0.875, PH-401.Scaling_Slope
-3.5, PH-401.Scaling_Offset
300.0, AC-401.PV_High
50.0, AC-401.PV_Low
TRUE, AC-401.Alarm_Enable
31.25, AC-401.Scaling_Slope
-125.0, AC-401.Scaling_Offset
50.0, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
20.0, LT-401.PV_Low
TRUE, LT-401.Alarm_Enable
6.25, LT-401.Scaling_Slope
-25.0, LT-401.Scaling_Offset
10.0, TS-401.PV_Low
TRUE, TS-401.Alarm_Enable
7.0, PIC-401.SP
2.0, PIC-401.KP
1.0, PIC-401.TR
0.2, PIC-401.TD
0.0, PIC-401.MV_MIN
100.0, PIC-401.MV_MAX
8.0, PIC-401.PV_High
6.0, PIC-401.PV_Low
0.1, PIC-401.Deviation_Limit
TRUE, PIC-401.AUTO
150.0, PIC-402.SP
1.5, PIC-402.KP
0.8, PIC-402.TR
0.1, PIC-402.TD
0.0, PIC-402.MV_MIN
75.0, PIC-402.MV_MAX
300.0, PIC-402.PV_High
50.0, PIC-402.PV_Low
5.0, PIC-402.Deviation_Limit
TRUE, PIC-402.AUTO
```

---


