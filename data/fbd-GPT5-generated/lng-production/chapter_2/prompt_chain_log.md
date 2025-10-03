# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 00:58:06

## Step 1: contextgen1-sensors
**Time:** 00:58:06

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
**Time:** 00:58:29

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
**Time:** 00:58:41

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability |
| Ratio Control | 0.96 |
| PID Control | 0.78 |
| OVERRIDE | 0.32 |

Selected Control Strategy: Ratio Control
Short explanation: The narrative specifies a ratio controller (IIC-101) computing the liquid separation setpoint from feed-gas flow (FT-101) and liquid flow (IT-102), with the valve LCV-101 modulated to meet that setpoint, aligning with the Ratio Control strategy using an optional slave PID.

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
**Timestamp:** 2025-09-24 00:59:14

## Step 1: openplc-function-blocks-v2
**Time:** 00:59:14

### Output:
```
* Function Blocks *
ANALOG_IN DP-101
ANALOG_IN DP-102
ANALOG_IN FT-101
RATIO_CONTROL IIC-101
ANALOG_IN IT-102
VALVE_ELECTRIC LCV-101
ANALOG_IN LT-101
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 00:59:30

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN DP-101
ANALOG_IN DP-102
ANALOG_IN FT-101
RATIO_CONTROL IIC-101
ANALOG_IN IT-102
VALVE_ELECTRIC LCV-101
ANALOG_IN LT-101
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 01:00:02

### Output:
```
* Functions *

* Block-to-Block Connections *
FT-101.PV, IIC-101.PrimaryPV
IT-102.PV, IIC-101.SecondaryPV
IIC-101.SlaveSP, LCV-101.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 01:00:38

### Output:
```
* Functions * 
OR DP_Trip_OR
OR IIC_Permissive_OR
OR IT_OutOfRange_OR
OR LCV_Inhibit_OR

* Data Connections *
DP-101.High_Alarm, DP_Trip_OR.IN1
DP-102.High_Alarm, DP_Trip_OR.IN2
DP_Trip_OR.OUT, IIC_Permissive_OR.IN1
LT-101.High_Alarm, IIC_Permissive_OR.IN2
FT-101.Low_Alarm, IIC_Permissive_OR.IN3
IIC_Permissive_OR.OUT, IIC-101.Inhibit
IT-102.High_Alarm, IT_OutOfRange_OR.IN1
IT-102.Low_Alarm, IT_OutOfRange_OR.IN2
IT_OutOfRange_OR.OUT, LCV_Inhibit_OR.IN1
FT-101.Low_Alarm, LCV_Inhibit_OR.IN2
IT-102.General_Fault, LCV_Inhibit_OR.IN3
LCV_Inhibit_OR.OUT, LCV-101.Inhibit

* Parameter Data Connections *
5000, FT-101.PV_High
100, FT-101.PV_Low
2000, IT-102.PV_High
0, IT-102.PV_Low
10, DP-101.PV_High
0, DP-101.PV_Low
10, DP-102.PV_High
0, DP-102.PV_Low
80, LT-101.PV_High
0, LT-101.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 01:01:38

### Output:
```
* Parameter Data Connections *
2.5, IIC-101.RatioSP
0, IIC-101.MV_MIN
2000, IIC-101.MV_MAX
TRUE, IIC-101.Auto
5000, FT-101.PV_High
0, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
2000, IT-102.PV_High
0, IT-102.PV_Low
TRUE, IT-102.Alarm_Enable
10, DP-101.PV_High
TRUE, DP-101.Alarm_Enable
10, DP-102.PV_High
TRUE, DP-102.Alarm_Enable
80, LT-101.PV_High
TRUE, LT-101.Alarm_Enable
FALSE, LCV-101.Manual_Mode
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 01:02:29

### Output:
```
* Parameter Data Connections *
2.5, IIC-101.RatioSP
0, IIC-101.MV_MIN
2000, IIC-101.MV_MAX
TRUE, IIC-101.Auto
500, IIC-101.ManOut
5000, FT-101.PV_High
100, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
312.5, FT-101.Scaling_Slope
-1250, FT-101.Scaling_Offset
2000, IT-102.PV_High
0, IT-102.PV_Low
TRUE, IT-102.Alarm_Enable
125, IT-102.Scaling_Slope
-500, IT-102.Scaling_Offset
10, DP-101.PV_High
0, DP-101.PV_Low
TRUE, DP-101.Alarm_Enable
0.625, DP-101.Scaling_Slope
-2.5, DP-101.Scaling_Offset
10, DP-102.PV_High
0, DP-102.PV_Low
TRUE, DP-102.Alarm_Enable
0.625, DP-102.Scaling_Slope
-2.5, DP-102.Scaling_Offset
80, LT-101.PV_High
0, LT-101.PV_Low
TRUE, LT-101.Alarm_Enable
6.25, LT-101.Scaling_Slope
-25, LT-101.Scaling_Offset
FALSE, LCV-101.Manual_Mode
100, LCV-101.Open_Limit
0, LCV-101.Close_Limit
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 01:03:14

### Output:
```
* Variables *
REAL FT101_FeedGasFlow_PV
REAL IT102_LiqSepFlow_PV
REAL LT101_SlugCatcherLevel_PV
REAL DP101_InletSepDP_PV
REAL DP102_InletSepDP_PV
REAL IIC101_LiqSepFlow_SP
REAL IIC101_CalculatedRatio

* Data Connections *
FT-101.PV, FT101_FeedGasFlow_PV
IT-102.PV, IT102_LiqSepFlow_PV
LT-101.PV, LT101_SlugCatcherLevel_PV
DP-101.PV, DP101_InletSepDP_PV
DP-102.PV, DP102_InletSepDP_PV
IIC-101.SlaveSP, IIC101_LiqSepFlow_SP
IIC-101.ActiveRatio, IIC101_CalculatedRatio
```

---

## Step 8: openplc-rule-checks
**Time:** 01:03:51

### Output:
```
* Function Blocks *
ANALOG_IN DP-101
ANALOG_IN DP-102
ANALOG_IN FT-101
ANALOG_IN IT-102
ANALOG_IN LT-101
RATIO_CONTROL IIC-101
VALVE_ELECTRIC LCV-101

* Variables *
REAL FT101_FeedGasFlow_PV
REAL IT102_LiqSepFlow_PV
REAL LT101_SlugCatcherLevel_PV
REAL DP101_InletSepDP_PV
REAL DP102_InletSepDP_PV
REAL IIC101_LiqSepFlow_SP
REAL IIC101_CalculatedRatio

* Functions *
OR DP_Trip_OR
OR IIC_Permissive1_OR
OR IIC_Permissive_OR
OR IT_OutOfRange_OR
OR LCV_Inhibit1_OR
OR LCV_Inhibit_OR

* Data Connections * 
FT-101.PV, IIC-101.PrimaryPV
IT-102.PV, IIC-101.SecondaryPV
IIC-101.SlaveSP, LCV-101.Control_Signal
DP-101.High_Alarm, DP_Trip_OR.IN1
DP-102.High_Alarm, DP_Trip_OR.IN2
DP_Trip_OR.OUT, IIC_Permissive1_OR.IN1
LT-101.High_Alarm, IIC_Permissive1_OR.IN2
IIC_Permissive1_OR.OUT, IIC_Permissive_OR.IN1
FT-101.Low_Alarm, IIC_Permissive_OR.IN2
IIC_Permissive_OR.OUT, IIC-101.Inhibit
IT-102.High_Alarm, IT_OutOfRange_OR.IN1
IT-102.Low_Alarm, IT_OutOfRange_OR.IN2
IT_OutOfRange_OR.OUT, LCV_Inhibit1_OR.IN1
FT-101.Low_Alarm, LCV_Inhibit1_OR.IN2
LCV_Inhibit1_OR.OUT, LCV_Inhibit_OR.IN1
IT-102.General_Fault, LCV_Inhibit_OR.IN2
LCV_Inhibit_OR.OUT, LCV-101.Inhibit
FT-101.PV, FT101_FeedGasFlow_PV
IT-102.PV, IT102_LiqSepFlow_PV
LT-101.PV, LT101_SlugCatcherLevel_PV
DP-101.PV, DP101_InletSepDP_PV
DP-102.PV, DP102_InletSepDP_PV
IIC-101.SlaveSP, IIC101_LiqSepFlow_SP
IIC-101.ActiveRatio, IIC101_CalculatedRatio

* Parameter Data Connections *
"DP-101 Inlet Separator DP", DP-101.Name
"Differential pressure across inlet separator A", DP-101.Description
10, DP-101.PV_High
0, DP-101.PV_Low
TRUE, DP-101.Alarm_Enable
0.625, DP-101.Scaling_Slope
-2.5, DP-101.Scaling_Offset
"DP-102 Inlet Separator DP", DP-102.Name
"Differential pressure across inlet separator B", DP-102.Description
10, DP-102.PV_High
0, DP-102.PV_Low
TRUE, DP-102.Alarm_Enable
0.625, DP-102.Scaling_Slope
-2.5, DP-102.Scaling_Offset
"FT-101 Feed-Gas Flow", FT-101.Name
"Feed-gas flow to ratio control (0–5000 Nm3/hr)", FT-101.Description
5000, FT-101.PV_High
100, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
312.5, FT-101.Scaling_Slope
-1250, FT-101.Scaling_Offset
"IT-102 Liquid Separation Flow", IT-102.Name
"Liquid separation flow (0–2000 Nm3/hr)", IT-102.Description
2000, IT-102.PV_High
0, IT-102.PV_Low
TRUE, IT-102.Alarm_Enable
125, IT-102.Scaling_Slope
-500, IT-102.Scaling_Offset
"LT-101 Slug Catcher Level", LT-101.Name
"Slug catcher level used for permissive (0–100%)", LT-101.Description
80, LT-101.PV_High
0, LT-101.PV_Low
TRUE, LT-101.Alarm_Enable
6.25, LT-101.Scaling_Slope
-25, LT-101.Scaling_Offset
"Ratio Controller IIC-101", IIC-101.Name
"Computes liquid separation flow SP from feed-gas flow and ratio", IIC-101.Description
TRUE, IIC-101.Auto
2.5, IIC-101.RatioSP
0, IIC-101.Bias
0, IIC-101.MV_MIN
2000, IIC-101.MV_MAX
500, IIC-101.ManOut
"LCV-101 Liquid Control Valve", LCV-101.Name
"Valve modulating liquid separation flow", LCV-101.Description
FALSE, LCV-101.Manual_Mode
0, LCV-101.Manual_Position
100, LCV-101.Open_Limit
0, LCV-101.Close_Limit
```

---

## Step 9: openplc-rule-checks2
**Time:** 01:05:24

### Output:
```
* Function Blocks *
ANALOG_IN DP-101
ANALOG_IN DP-102
ANALOG_IN FT-101
ANALOG_IN IT-102
ANALOG_IN LT-101
RATIO_CONTROL IIC-101
VALVE_ELECTRIC LCV-101

* Variables *
REAL FT101_FeedGasFlow_PV
REAL IT102_LiqSepFlow_PV
REAL LT101_SlugCatcherLevel_PV
REAL DP101_InletSepDP_PV
REAL DP102_InletSepDP_PV
REAL IIC101_LiqSepFlow_SP
REAL IIC101_CalculatedRatio

* Functions *
OR DP_Trip_OR
OR IIC_Permissive1_OR
OR IIC_Permissive_OR
OR IT_OutOfRange_OR
OR LCV_Inhibit1_OR
OR LCV_Inhibit_OR

* Data Connections * 
FT-101.PV, IIC-101.PrimaryPV
IT-102.PV, IIC-101.SecondaryPV
IIC-101.SlaveSP, LCV-101.Control_Signal
DP-101.High_Alarm, DP_Trip_OR.IN1
DP-102.High_Alarm, DP_Trip_OR.IN2
DP_Trip_OR.OUT, IIC_Permissive1_OR.IN1
LT-101.High_Alarm, IIC_Permissive1_OR.IN2
IIC_Permissive1_OR.OUT, IIC_Permissive_OR.IN1
FT-101.Low_Alarm, IIC_Permissive_OR.IN2
IIC_Permissive_OR.OUT, IIC-101.Inhibit
IT-102.High_Alarm, IT_OutOfRange_OR.IN1
IT-102.Low_Alarm, IT_OutOfRange_OR.IN2
IT_OutOfRange_OR.OUT, LCV_Inhibit1_OR.IN1
FT-101.Low_Alarm, LCV_Inhibit1_OR.IN2
LCV_Inhibit1_OR.OUT, LCV_Inhibit_OR.IN1
IT-102.General_Fault, LCV_Inhibit_OR.IN2
LCV_Inhibit_OR.OUT, LCV-101.Inhibit
FT-101.PV, FT101_FeedGasFlow_PV
IT-102.PV, IT102_LiqSepFlow_PV
LT-101.PV, LT101_SlugCatcherLevel_PV
DP-101.PV, DP101_InletSepDP_PV
DP-102.PV, DP102_InletSepDP_PV
IIC-101.SlaveSP, IIC101_LiqSepFlow_SP
IIC-101.ActiveRatio, IIC101_CalculatedRatio

* Parameter Data Connections *
10, DP-101.PV_High
0, DP-101.PV_Low
TRUE, DP-101.Alarm_Enable
0.625, DP-101.Scaling_Slope
-2.5, DP-101.Scaling_Offset
10, DP-102.PV_High
0, DP-102.PV_Low
TRUE, DP-102.Alarm_Enable
0.625, DP-102.Scaling_Slope
-2.5, DP-102.Scaling_Offset
5000, FT-101.PV_High
100, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
312.5, FT-101.Scaling_Slope
-1250, FT-101.Scaling_Offset
2000, IT-102.PV_High
0, IT-102.PV_Low
TRUE, IT-102.Alarm_Enable
125, IT-102.Scaling_Slope
-500, IT-102.Scaling_Offset
80, LT-101.PV_High
0, LT-101.PV_Low
TRUE, LT-101.Alarm_Enable
6.25, LT-101.Scaling_Slope
-25, LT-101.Scaling_Offset
TRUE, IIC-101.Auto
2.5, IIC-101.RatioSP
0, IIC-101.Bias
0, IIC-101.MV_MIN
2000, IIC-101.MV_MAX
500, IIC-101.ManOut
FALSE, LCV-101.Manual_Mode
0, LCV-101.Manual_Position
100, LCV-101.Open_Limit
0, LCV-101.Close_Limit
```

---

## Step 10: append_two_inputs
**Time:** 01:06:10

### Output:
```
* Function Blocks *
ANALOG_IN DP-101
ANALOG_IN DP-102
ANALOG_IN FT-101
ANALOG_IN IT-102
ANALOG_IN LT-101
RATIO_CONTROL IIC-101
VALVE_ELECTRIC LCV-101

* Variables *
REAL FT101_FeedGasFlow_PV
REAL IT102_LiqSepFlow_PV
REAL LT101_SlugCatcherLevel_PV
REAL DP101_InletSepDP_PV
REAL DP102_InletSepDP_PV
REAL IIC101_LiqSepFlow_SP
REAL IIC101_CalculatedRatio

* Functions *
OR DP_Trip_OR
OR IIC_Permissive1_OR
OR IIC_Permissive_OR
OR IT_OutOfRange_OR
OR LCV_Inhibit1_OR
OR LCV_Inhibit_OR

* Data Connections * 
FT-101.PV, IIC-101.PrimaryPV
IT-102.PV, IIC-101.SecondaryPV
IIC-101.SlaveSP, LCV-101.Control_Signal
DP-101.High_Alarm, DP_Trip_OR.IN1
DP-102.High_Alarm, DP_Trip_OR.IN2
DP_Trip_OR.OUT, IIC_Permissive1_OR.IN1
LT-101.High_Alarm, IIC_Permissive1_OR.IN2
IIC_Permissive1_OR.OUT, IIC_Permissive_OR.IN1
FT-101.Low_Alarm, IIC_Permissive_OR.IN2
IIC_Permissive_OR.OUT, IIC-101.Inhibit
IT-102.High_Alarm, IT_OutOfRange_OR.IN1
IT-102.Low_Alarm, IT_OutOfRange_OR.IN2
IT_OutOfRange_OR.OUT, LCV_Inhibit1_OR.IN1
FT-101.Low_Alarm, LCV_Inhibit1_OR.IN2
LCV_Inhibit1_OR.OUT, LCV_Inhibit_OR.IN1
IT-102.General_Fault, LCV_Inhibit_OR.IN2
LCV_Inhibit_OR.OUT, LCV-101.Inhibit
FT-101.PV, FT101_FeedGasFlow_PV
IT-102.PV, IT102_LiqSepFlow_PV
LT-101.PV, LT101_SlugCatcherLevel_PV
DP-101.PV, DP101_InletSepDP_PV
DP-102.PV, DP102_InletSepDP_PV
IIC-101.SlaveSP, IIC101_LiqSepFlow_SP
IIC-101.ActiveRatio, IIC101_CalculatedRatio

* Parameter Data Connections *
10, DP-101.PV_High
0, DP-101.PV_Low
TRUE, DP-101.Alarm_Enable
0.625, DP-101.Scaling_Slope
-2.5, DP-101.Scaling_Offset
10, DP-102.PV_High
0, DP-102.PV_Low
TRUE, DP-102.Alarm_Enable
0.625, DP-102.Scaling_Slope
-2.5, DP-102.Scaling_Offset
5000, FT-101.PV_High
100, FT-101.PV_Low
TRUE, FT-101.Alarm_Enable
312.5, FT-101.Scaling_Slope
-1250, FT-101.Scaling_Offset
2000, IT-102.PV_High
0, IT-102.PV_Low
TRUE, IT-102.Alarm_Enable
125, IT-102.Scaling_Slope
-500, IT-102.Scaling_Offset
80, LT-101.PV_High
0, LT-101.PV_Low
TRUE, LT-101.Alarm_Enable
6.25, LT-101.Scaling_Slope
-25, LT-101.Scaling_Offset
TRUE, IIC-101.Auto
2.5, IIC-101.RatioSP
0, IIC-101.Bias
0, IIC-101.MV_MIN
2000, IIC-101.MV_MAX
500, IIC-101.ManOut
FALSE, LCV-101.Manual_Mode
0, LCV-101.Manual_Position
100, LCV-101.Open_Limit
0, LCV-101.Close_Limit
```

---


