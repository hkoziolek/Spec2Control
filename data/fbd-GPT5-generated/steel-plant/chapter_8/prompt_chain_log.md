# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 04:49:40

## Step 1: contextgen1-sensors
**Time:** 04:49:40

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
**Time:** 04:49:59

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
```

---

## Step 3: contextgen1-strategies
**Time:** 04:50:13

### Output:
```
*** Available Control Strategies ***
Control Strategy | Probability
Ratio Control | 0.98
PID Control | 0.95
OVERRIDE | 0.60
Cascade Control | 0.20
FEEDFORWARD | 0.15
SPLIT RANGE | 0.05
VOTING | 0.05
Duty-Standby | 0.01

Selected Control Strategy: Ratio Control
Short explanation: The narrative specifies maintaining a fixed air-to-fuel ratio using fuel flow (FT-701) to compute an air flow setpoint for the air flow PID (FIC-702), which modulates FV-702; this matches the Ratio Control strategy with a slave PID controller.

* Control Strategy *
Ratio Control
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
**Timestamp:** 2025-09-24 04:50:56

## Step 1: openplc-function-blocks-v2
**Time:** 04:50:56

### Output:
```
* Function Blocks *
ANALOG_IN FT-701
ANALOG_IN FT-702
ANALOG_IN TT-701
ANALOG_IN FLT-701
PID_BASIC FIC-702
VALVE_ELECTRIC FV-702
RATIO_CONTROL FFIC-701
BOOL_IN BLS-701
DIGITAL_IN ALM-701
DIGITAL_IN ALM-702
DIGITAL_IN ALM-703
DIGITAL_IN ALM-704
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 04:51:14

### Output:
```
* Function Blocks *
ANALOG_IN FT-701
ANALOG_IN FT-702
ANALOG_IN TT-701
ANALOG_IN FLT-701
PID_BASIC FIC-702
VALVE_ELECTRIC FV-702
RATIO_CONTROL FFIC-701
BOOL_IN BLS-701
DIGITAL_IN ALM-701
DIGITAL_IN ALM-702
DIGITAL_IN ALM-703
DIGITAL_IN ALM-704
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 04:52:05

### Output:
```
* Functions *

* Block-to-Block Connections *
FT-701.PV, FFIC-701.PrimaryPV
FT-702.PV, FFIC-701.SecondaryPV
FFIC-701.SlaveSP, FIC-702.SP
FT-702.PV, FIC-702.PV
FIC-702.XOUT, FV-702.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 04:52:46

### Output:
```
* Functions * 
OR TT701High_OR
OR TxFaults_OR
OR LowFuelOrTemp_OR
OR RatioControlInhibit_OR
OR ValveInhibit_OR
NOT BurnerOff_NOT

* Data Connections *
TT-701.High_Alarm, ALM-704.DI_Raw
FT-701.General_Fault, ALM-702.DI_Raw
FT-702.General_Fault, ALM-703.DI_Raw
TT-701.High_Alarm, TT701High_OR.IN1
ALM-704.DI_Out, TT701High_OR.IN2
FT-701.Low_Alarm, LowFuelOrTemp_OR.IN1
TT-701.Low_Alarm, LowFuelOrTemp_OR.IN2
ALM-702.DI_Out, TxFaults_OR.IN1
ALM-703.DI_Out, TxFaults_OR.IN2
BLS-701.Bool_Out, BurnerOff_NOT.IN
TT701High_OR.OUT, RatioControlInhibit_OR.IN1
TxFaults_OR.OUT, RatioControlInhibit_OR.IN2
FT-701.Low_Alarm, RatioControlInhibit_OR.IN3
BurnerOff_NOT.OUT, RatioControlInhibit_OR.IN4
RatioControlInhibit_OR.OUT, FFIC-701.Inhibit
LowFuelOrTemp_OR.OUT, ValveInhibit_OR.IN1
TT701High_OR.OUT, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-702.Inhibit
ValveInhibit_OR.OUT, FIC-702.Inhibit

* Parameter Data Connections *
5000, FT-701.PV_High
200, FT-701.PV_Low
15000, FT-702.PV_High
0, FT-702.PV_Low
1200, TT-701.PV_High
800, TT-701.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 04:54:09

### Output:
```
* Parameter Data Connections *
10.0, FFIC-701.RatioSP
0.0, FFIC-701.MV_MIN
15000.0, FFIC-701.MV_MAX
TRUE, FFIC-701.Auto
TRUE, FIC-702.AUTO
0.0, FIC-702.PV_Low
15000.0, FIC-702.PV_High
0.0, FT-702.PV_Low
15000.0, FT-702.PV_High
TRUE, FT-702.Alarm_Enable
200.0, FT-701.PV_Low
5000.0, FT-701.PV_High
TRUE, FT-701.Alarm_Enable
800.0, TT-701.PV_Low
1200.0, TT-701.PV_High
TRUE, TT-701.Alarm_Enable
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 04:55:15

### Output:
```
* Parameter Data Connections *
10.0, FFIC-701.RatioSP
0.0, FFIC-701.MV_MIN
15000.0, FFIC-701.MV_MAX
0.0, FFIC-701.Bias
TRUE, FFIC-701.Auto
TRUE, FIC-702.AUTO
0.0, FIC-702.PV_Low
15000.0, FIC-702.PV_High
0.0, FIC-702.MV_MIN
100.0, FIC-702.MV_MAX
0.0, FT-702.PV_Low
15000.0, FT-702.PV_High
TRUE, FT-702.Alarm_Enable
200.0, FT-701.PV_Low
5000.0, FT-701.PV_High
TRUE, FT-701.Alarm_Enable
800.0, TT-701.PV_Low
1200.0, TT-701.PV_High
TRUE, TT-701.Alarm_Enable
100.0, FV-702.Open_Limit
0.0, FV-702.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 04:56:34

### Output:
```
* Variables *
REAL FT701_FuelFlow_PV
REAL FT702_AirFlow_SP
REAL FT702_AirFlow_PV
REAL TT701_FurnaceTemp_PV

* Data Connections *
FT-701.PV, FT701_FuelFlow_PV
FFIC-701.SlaveSP, FT702_AirFlow_SP
FT-702.PV, FT702_AirFlow_PV
TT-701.PV, TT701_FurnaceTemp_PV
```

---

## Step 8: openplc-rule-checks
**Time:** 04:57:19

### Output:
```
* Function Blocks *
ANALOG_IN FT-701
ANALOG_IN FT-702
ANALOG_IN TT-701
PID_BASIC FIC-702
VALVE_ELECTRIC FV-702
RATIO_CONTROL FFIC-701
BOOL_IN BLS-701
DIGITAL_IN ALM-701
DIGITAL_IN ALM-702
DIGITAL_IN ALM-703
DIGITAL_IN ALM-704

* Variables *
REAL FT701_FuelFlow_PV
REAL FT702_AirFlow_SP
REAL FT702_AirFlow_PV
REAL TT701_FurnaceTemp_PV
REAL FFIC701_Bias
BOOL BURNER_STATUS

* Functions *
OR TT701High_OR
OR TxFaults_OR
OR LowFuelOrTemp_OR
OR RatioControlInhibit_OR
OR ValveInhibit_OR
OR RatioLimit_OR
NOT BurnerOff_NOT
GT RatioHigh_GT
LT RatioLow_LT

* Data Connections * 
FT-701.PV, FFIC-701.PrimaryPV
FT-702.PV, FFIC-701.SecondaryPV
FFIC-701.SlaveSP, FIC-702.SP
FT-702.PV, FIC-702.PV
FIC-702.XOUT, FV-702.Control_Signal
FT-701.PV, FT701_FuelFlow_PV
FFIC-701.SlaveSP, FT702_AirFlow_SP
FT-702.PV, FT702_AirFlow_PV
TT-701.PV, TT701_FurnaceTemp_PV
TT-701.High_Alarm, ALM-704.DI_Raw
FT-701.General_Fault, ALM-702.DI_Raw
FT-702.General_Fault, ALM-703.DI_Raw
TT-701.High_Alarm, TT701High_OR.IN1
ALM-704.DI_Out, TT701High_OR.IN2
FT-701.Low_Alarm, LowFuelOrTemp_OR.IN1
TT-701.Low_Alarm, LowFuelOrTemp_OR.IN2
ALM-702.DI_Out, TxFaults_OR.IN1
ALM-703.DI_Out, TxFaults_OR.IN2
BURNER_STATUS, BLS-701.Bool_In
BLS-701.Bool_Out, BurnerOff_NOT.IN
TT701High_OR.OUT, RatioControlInhibit_OR.IN1
TxFaults_OR.OUT, RatioControlInhibit_OR.IN2
FT-701.Low_Alarm, RatioControlInhibit_OR.IN3
BurnerOff_NOT.OUT, RatioControlInhibit_OR.IN4
RatioControlInhibit_OR.OUT, FFIC-701.Inhibit
LowFuelOrTemp_OR.OUT, ValveInhibit_OR.IN1
TT701High_OR.OUT, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-702.Inhibit
ValveInhibit_OR.OUT, FV-702.Manual_Mode
ValveInhibit_OR.OUT, FIC-702.Inhibit
FFIC-701.ActiveRatio, RatioHigh_GT.IN1
FFIC-701.ActiveRatio, RatioLow_LT.IN1
RatioHigh_GT.OUT, RatioLimit_OR.IN1
RatioLow_LT.OUT, RatioLimit_OR.IN2
RatioLimit_OR.OUT, ALM-701.DI_Raw
FFIC701_Bias, FFIC-701.Bias

* Parameter Data Connections *
10.0, FFIC-701.RatioSP
0.0, FFIC-701.MV_MIN
15000.0, FFIC-701.MV_MAX
TRUE, FFIC-701.Auto
TRUE, FIC-702.AUTO
0.0, FIC-702.MV_MIN
100.0, FIC-702.MV_MAX
15000.0, FIC-702.PV_High
0.0, FIC-702.PV_Low
2.0, FIC-702.KP
5.0, FIC-702.TR
0.5, FIC-702.TD
1000.0, FIC-702.Deviation_Limit
5000.0, FT-701.PV_High
200.0, FT-701.PV_Low
TRUE, FT-701.Alarm_Enable
15000.0, FT-702.PV_High
0.0, FT-702.PV_Low
TRUE, FT-702.Alarm_Enable
1200.0, TT-701.PV_High
800.0, TT-701.PV_Low
TRUE, TT-701.Alarm_Enable
100.0, FV-702.Open_Limit
0.0, FV-702.Close_Limit
T#10s, FV-702.Timeout
0.0, FV-702.Manual_Position
12.0, RatioHigh_GT.IN2
8.0, RatioLow_LT.IN2
```

---

## Step 9: openplc-rule-checks2
**Time:** 05:00:11

### Output:
```
* Function Blocks *
ANALOG_IN FT-701
ANALOG_IN FT-702
ANALOG_IN TT-701
PID_BASIC FIC-702
VALVE_ELECTRIC FV-702
RATIO_CONTROL FFIC-701
BOOL_IN BLS-701
DIGITAL_IN ALM-701
DIGITAL_IN ALM-702
DIGITAL_IN ALM-703
DIGITAL_IN ALM-704

* Variables *
REAL FT701_FuelFlow_PV
REAL FT702_AirFlow_SP
REAL FT702_AirFlow_PV
REAL TT701_FurnaceTemp_PV
REAL FFIC701_Bias
BOOL BURNER_STATUS

* Functions *
OR TT701High_OR
OR TxFaults_OR
OR LowFuelOrTemp_OR
OR RatioControlInhibit_OR
OR ValveInhibit_OR
OR RatioLimit_OR
NOT BurnerOff_NOT
GT RatioHigh_GT
LT RatioLow_LT

* Data Connections * 
FT-701.PV, FFIC-701.PrimaryPV
FT-702.PV, FFIC-701.SecondaryPV
FFIC-701.SlaveSP, FIC-702.SP
FT-702.PV, FIC-702.PV
FIC-702.XOUT, FV-702.Control_Signal
FT-701.PV, FT701_FuelFlow_PV
FFIC-701.SlaveSP, FT702_AirFlow_SP
FT-702.PV, FT702_AirFlow_PV
TT-701.PV, TT701_FurnaceTemp_PV
TT-701.High_Alarm, ALM-704.DI_Raw
FT-701.General_Fault, ALM-702.DI_Raw
FT-702.General_Fault, ALM-703.DI_Raw
TT-701.High_Alarm, TT701High_OR.IN1
ALM-704.DI_Out, TT701High_OR.IN2
FT-701.Low_Alarm, LowFuelOrTemp_OR.IN1
TT-701.Low_Alarm, LowFuelOrTemp_OR.IN2
ALM-702.DI_Out, TxFaults_OR.IN1
ALM-703.DI_Out, TxFaults_OR.IN2
BURNER_STATUS, BLS-701.Bool_In
BLS-701.Bool_Out, BurnerOff_NOT.IN
TT701High_OR.OUT, RatioControlInhibit_OR.IN1
TxFaults_OR.OUT, RatioControlInhibit_OR.IN2
FT-701.Low_Alarm, RatioControlInhibit_OR.IN3
BurnerOff_NOT.OUT, RatioControlInhibit_OR.IN4
RatioControlInhibit_OR.OUT, FFIC-701.Inhibit
LowFuelOrTemp_OR.OUT, ValveInhibit_OR.IN1
TT701High_OR.OUT, ValveInhibit_OR.IN2
ValveInhibit_OR.OUT, FV-702.Inhibit
ValveInhibit_OR.OUT, FV-702.Manual_Mode
ValveInhibit_OR.OUT, FIC-702.Inhibit
FFIC-701.ActiveRatio, RatioHigh_GT.IN1
FFIC-701.ActiveRatio, RatioLow_LT.IN1
RatioHigh_GT.OUT, RatioLimit_OR.IN1
RatioLow_LT.OUT, RatioLimit_OR.IN2
RatioLimit_OR.OUT, ALM-701.DI_Raw
FFIC701_Bias, FFIC-701.Bias

* Parameter Data Connections *
10.0, FFIC-701.RatioSP
0.0, FFIC-701.MV_MIN
15000.0, FFIC-701.MV_MAX
TRUE, FFIC-701.Auto
TRUE, FIC-702.AUTO
0.0, FIC-702.MV_MIN
100.0, FIC-702.MV_MAX
15000.0, FIC-702.PV_High
0.0, FIC-702.PV_Low
2.0, FIC-702.KP
5.0, FIC-702.TR
0.5, FIC-702.TD
1000.0, FIC-702.Deviation_Limit
5000.0, FT-701.PV_High
200.0, FT-701.PV_Low
TRUE, FT-701.Alarm_Enable
15000.0, FT-702.PV_High
0.0, FT-702.PV_Low
TRUE, FT-702.Alarm_Enable
1200.0, TT-701.PV_High
800.0, TT-701.PV_Low
TRUE, TT-701.Alarm_Enable
100.0, FV-702.Open_Limit
0.0, FV-702.Close_Limit
T#10s, FV-702.Timeout
0.0, FV-702.Manual_Position
12.0, RatioHigh_GT.IN2
8.0, RatioLow_LT.IN2
```

---

## Step 10: append_two_inputs
**Time:** 05:00:37

### Output:
```
* Function Blocks *
ANALOG_IN FT-701
ANALOG_IN FT-702
ANALOG_IN TT-701
PID_BASIC FIC-702
VALVE_ELECTRIC FV-702
RATIO_CONTROL FFIC-701
BOOL_IN BLS-701
DIGITAL_IN ALM-701
DIGITAL_IN ALM-702
DIGITAL_IN ALM-703
DIGITAL_IN ALM-704

* Variables *
REAL FT701_FuelFlow_PV
REAL FT702_AirFlow_SP
REAL FT702_AirFlow_PV
REAL TT701_FurnaceTemp_PV
REAL FFIC701_Bias
BOOL BURNER_STATUS

* Functions *
OR RatioControlInhibit_OR
OR ValveInhibit_OR
OR RatioLimit_OR
NOT BurnerOff_NOT
GT RatioHigh_GT
LT RatioLow_LT

* Data Connections * 
FT-701.PV, FFIC-701.PrimaryPV
FT-702.PV, FFIC-701.SecondaryPV
FFIC-701.SlaveSP, FIC-702.SP
FT-702.PV, FIC-702.PV
FIC-702.XOUT, FV-702.Control_Signal
FT-701.PV, FT701_FuelFlow_PV
FFIC-701.SlaveSP, FT702_AirFlow_SP
FT-702.PV, FT702_AirFlow_PV
TT-701.PV, TT701_FurnaceTemp_PV
TT-701.High_Alarm, ALM-704.DI_Raw
FT-701.General_Fault, ALM-702.DI_Raw
FT-702.General_Fault, ALM-703.DI_Raw
BURNER_STATUS, BLS-701.Bool_In
BLS-701.Bool_Out, BurnerOff_NOT.IN
TT-701.High_Alarm, RatioControlInhibit_OR.IN1
ALM-704.DI_Out, RatioControlInhibit_OR.IN2
FT-701.Low_Alarm, RatioControlInhibit_OR.IN3
BurnerOff_NOT.OUT, RatioControlInhibit_OR.IN4
ALM-702.DI_Out, RatioControlInhibit_OR.IN5
ALM-703.DI_Out, RatioControlInhibit_OR.IN6
RatioControlInhibit_OR.OUT, FFIC-701.Inhibit
FT-701.Low_Alarm, ValveInhibit_OR.IN1
TT-701.Low_Alarm, ValveInhibit_OR.IN2
TT-701.High_Alarm, ValveInhibit_OR.IN3
ALM-704.DI_Out, ValveInhibit_OR.IN4
ValveInhibit_OR.OUT, FV-702.Inhibit
ValveInhibit_OR.OUT, FV-702.Manual_Mode
ValveInhibit_OR.OUT, FIC-702.Inhibit
FFIC-701.ActiveRatio, RatioHigh_GT.IN1
FFIC-701.ActiveRatio, RatioLow_LT.IN1
RatioHigh_GT.OUT, RatioLimit_OR.IN1
RatioLow_LT.OUT, RatioLimit_OR.IN2
RatioLimit_OR.OUT, ALM-701.DI_Raw
FFIC701_Bias, FFIC-701.Bias

* Parameter Data Connections *
10.0, FFIC-701.RatioSP
0.0, FFIC-701.MV_MIN
15000.0, FFIC-701.MV_MAX
TRUE, FFIC-701.Auto
TRUE, FIC-702.AUTO
0.0, FIC-702.MV_MIN
100.0, FIC-702.MV_MAX
15000.0, FIC-702.PV_High
0.0, FIC-702.PV_Low
2.0, FIC-702.KP
5.0, FIC-702.TR
0.5, FIC-702.TD
1000.0, FIC-702.Deviation_Limit
5000.0, FT-701.PV_High
200.0, FT-701.PV_Low
TRUE, FT-701.Alarm_Enable
15000.0, FT-702.PV_High
0.0, FT-702.PV_Low
TRUE, FT-702.Alarm_Enable
1200.0, TT-701.PV_High
800.0, TT-701.PV_Low
TRUE, TT-701.Alarm_Enable
100.0, FV-702.Open_Limit
0.0, FV-702.Close_Limit
T#10s, FV-702.Timeout
0.0, FV-702.Manual_Position
12.0, RatioHigh_GT.IN2
8.0, RatioLow_LT.IN2
```

---


