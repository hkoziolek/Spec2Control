# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 01:37:22

## Step 1: contextgen1-sensors
**Time:** 01:37:22

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
```

---

## Step 2: contextgen1-actuators
**Time:** 01:37:36

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
**Time:** 01:38:00

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
|------------------|-----------------------|
| Ratio Control | 0.99 |
| PID Control | 0.95 |
| OVERRIDE | 0.70 |

Selected Control Strategy: Ratio Control 
Short explanation: Core requirement is to maintain a fixed ratio between propane (wild flow) and mixed refrigerant (controlled flow) using a ratio controller driving a slave PID loop.

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
**Timestamp:** 2025-09-24 01:38:26

## Step 1: openplc-function-blocks-v2
**Time:** 01:38:26

### Output:
```
* Function Blocks *
ANALOG_IN FT-501
ANALOG_IN FT-502
ANALOG_IN PT-501
ANALOG_IN TIT-102
RATIO_CONTROL FFIC-503
PID_BASIC FIC-504
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC FV-501
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 01:39:00

### Output:
```
* Function Block List * 
* Function Blocks *
ANALOG_IN FT-501
ANALOG_IN FT-502
ANALOG_IN PT-501
ANALOG_IN TIT-102
RATIO_CONTROL FFIC-503
PID_BASIC FIC-504
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC FV-501
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 01:39:23

### Output:
```
* Functions *
ADD RatioMin_ADD
ADD RatioMax_ADD

* Block-to-Block Connections *
FT-501.PV, FFIC-503.PrimaryPV
FT-502.PV, FFIC-503.SecondaryPV
FT-501.PV, RatioMin_ADD.IN1
FT-501.PV, RatioMin_ADD.IN2
RatioMin_ADD.OUT, FFIC-503.MV_MIN
FT-501.PV, RatioMax_ADD.IN1
RatioMin_ADD.OUT, RatioMax_ADD.IN2
RatioMax_ADD.OUT, FFIC-503.MV_MAX
FFIC-503.SlaveSP, FIC-504.SP
FT-502.PV, FIC-504.PV
FIC-504.XOUT, FV-502.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 01:40:11

### Output:
```
* Functions * 
OR FT501_OutOfRange_OR
OR FT502_OutOfRange_OR
OR FlowFault_OR
OR FlowRange_OR
OR RangeOrFault_OR
OR InhibitCause_OR

* Data Connections *
FT-501.High_Alarm, FT501_OutOfRange_OR.IN1
FT-501.Low_Alarm, FT501_OutOfRange_OR.IN2
FT-502.High_Alarm, FT502_OutOfRange_OR.IN1
FT-502.Low_Alarm, FT502_OutOfRange_OR.IN2
FT501_OutOfRange_OR.OUT, FlowRange_OR.IN1
FT502_OutOfRange_OR.OUT, FlowRange_OR.IN2
FT-501.General_Fault, FlowFault_OR.IN1
FT-502.General_Fault, FlowFault_OR.IN2
FlowRange_OR.OUT, RangeOrFault_OR.IN1
FlowFault_OR.OUT, RangeOrFault_OR.IN2
RangeOrFault_OR.OUT, InhibitCause_OR.IN1
PT-501.Low_Alarm, InhibitCause_OR.IN2
InhibitCause_OR.OUT, FFIC-503.Inhibit
InhibitCause_OR.OUT, FIC-504.Inhibit
InhibitCause_OR.OUT, FV-502.Inhibit

* Parameter Data Connections *
5000, FT-501.PV_High
500, FT-501.PV_Low
2000, FT-502.PV_High
200, FT-502.PV_Low
2.0, PT-501.PV_Low
-155, TIT-102.PV_High
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 01:41:14

### Output:
```
* Parameter Data Connections *
2.5, FFIC-503.RatioSP
TRUE, FFIC-503.Auto
0.0, FFIC-503.Bias
TRUE, FIC-504.AUTO
2000.0, FIC-504.PV_High
200.0, FIC-504.PV_Low
TRUE, FT-501.Alarm_Enable
5000.0, FT-501.PV_High
500.0, FT-501.PV_Low
TRUE, FT-502.Alarm_Enable
2000.0, FT-502.PV_High
200.0, FT-502.PV_Low
TRUE, PT-501.Alarm_Enable
2.0, PT-501.PV_Low
TRUE, TIT-102.Alarm_Enable
-155.0, TIT-102.PV_High
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 01:42:58

### Output:
```
* Parameter Data Connections *
2.5, FFIC-503.RatioSP
TRUE, FFIC-503.Auto
0.0, FFIC-503.Bias
312.5, FT-501.Scaling_Slope
-1250.0, FT-501.Scaling_Offset
TRUE, FT-501.Alarm_Enable
5000.0, FT-501.PV_High
500.0, FT-501.PV_Low
125.0, FT-502.Scaling_Slope
-500.0, FT-502.Scaling_Offset
TRUE, FT-502.Alarm_Enable
2000.0, FT-502.PV_High
200.0, FT-502.PV_Low
TRUE, PT-501.Alarm_Enable
2.0, PT-501.PV_Low
TRUE, TIT-102.Alarm_Enable
-155.0, TIT-102.PV_High
TRUE, FIC-504.AUTO
2000.0, FIC-504.PV_High
200.0, FIC-504.PV_Low
0.0, FIC-504.MV_MIN
100.0, FIC-504.MV_MAX
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 01:44:32

### Output:
```
* Variables *
REAL FT_501_PropaneFlow_PV
REAL FT_502_MRFlow_PV
REAL PT_501_Pressure_PV
REAL TIT_102_Temperature_PV
REAL FIC_504_SP_MRFlow
REAL FFIC_503_ActiveRatio
REAL FV_502_ControlSignal
REAL FV_501_Feedback_Pos

* Data Connections *
FT-501.PV, FT_501_PropaneFlow_PV
FT-502.PV, FT_502_MRFlow_PV
PT-501.PV, PT_501_Pressure_PV
TIT-102.PV, TIT_102_Temperature_PV
FFIC-503.SlaveSP, FIC_504_SP_MRFlow
FFIC-503.ActiveRatio, FFIC_503_ActiveRatio
FIC-504.XOUT, FV_502_ControlSignal
FV-501.Feedback_Pos, FV_501_Feedback_Pos
```

---

## Step 8: openplc-rule-checks
**Time:** 01:45:28

### Output:
```
* Function Blocks *
ANALOG_IN FT-501
ANALOG_IN FT-502
ANALOG_IN PT-501
ANALOG_IN TIT-102
RATIO_CONTROL FFIC-503
PID_BASIC FIC-504
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC FV-501

* Variables *
REAL FT_501_PropaneFlow_PV
REAL FT_502_MRFlow_PV
REAL PT_501_Pressure_PV
REAL TIT_102_Temperature_PV
REAL FIC_504_SP_Selected
REAL FFIC_503_ActiveRatio
REAL FV_502_ControlSignal
REAL FV_501_Feedback_Pos
REAL RatioBias_Manual
BOOL AntiSurgeActive
BOOL PropaneLowFlow
BOOL FlowRangeOrFault
BOOL RatioControlInhibit
BOOL RatioDevHigh_ALM
BOOL RatioDevLow_ALM

* Functions *
DIV RatioMin_DIV
DIV RatioMax_DIV
OR FT501_OutOfRangeCheck
OR FT502_OutOfRangeCheck
OR FlowFaultCheck
OR FlowRangeCheck
OR RangeOrFault
OR ControlInhibitCause
GE FV501_FullyOpen_GE
TON FV501_OpenHold_TON
LT PropaneLowFlow_LT
SEL AntiSurge_SP_SEL
SEL LowFlow_SP_SEL
SEL FaultOverride_SP_SEL
ADD RatioSP_AutoBump_ADD
SEL RatioSP_AutoTrim_SEL
ADD RatioSP_ManualBias_ADD
OR RatioDisable_OR1
OR RatioDisable_OR2
NOT RatioAuto_NOT
GT RatioDevHigh_GT
LT RatioDevLow_LT
TON RatioDevHigh_TON
TON RatioDevLow_TON

* Data Connections * 
FT-501.PV, FFIC-503.PrimaryPV
FT-502.PV, FFIC-503.SecondaryPV
FT-501.PV, RatioMin_DIV.IN1
FT-501.PV, RatioMax_DIV.IN1
RatioMin_DIV.OUT, FFIC-503.MV_MIN
RatioMax_DIV.OUT, FFIC-503.MV_MAX
TIT-102.High_Alarm, RatioSP_AutoTrim_SEL.G
RatioSP_AutoTrim_SEL.OUT, RatioSP_AutoBump_ADD.IN2
RatioSP_AutoBump_ADD.OUT, RatioSP_ManualBias_ADD.IN1
RatioBias_Manual, RatioSP_ManualBias_ADD.IN2
RatioSP_ManualBias_ADD.OUT, FFIC-503.RatioSP
FV-501.Feedback_Pos, FV501_FullyOpen_GE.IN1
FV501_FullyOpen_GE.OUT, FV501_OpenHold_TON.IN
FV501_OpenHold_TON.Q, AntiSurge_SP_SEL.G
FFIC-503.SlaveSP, AntiSurge_SP_SEL.IN0
AntiSurge_SP_SEL.OUT, LowFlow_SP_SEL.IN0
FT-501.PV, PropaneLowFlow_LT.IN1
PropaneLowFlow_LT.OUT, LowFlow_SP_SEL.G
LowFlow_SP_SEL.OUT, FaultOverride_SP_SEL.IN0
RangeOrFault.OUT, FaultOverride_SP_SEL.G
FaultOverride_SP_SEL.OUT, FIC-504.SP
FaultOverride_SP_SEL.OUT, FIC_504_SP_Selected
FT-501.High_Alarm, FT501_OutOfRangeCheck.IN1
FT-501.Low_Alarm, FT501_OutOfRangeCheck.IN2
FT-502.High_Alarm, FT502_OutOfRangeCheck.IN1
FT-502.Low_Alarm, FT502_OutOfRangeCheck.IN2
FT501_OutOfRangeCheck.OUT, FlowRangeCheck.IN1
FT502_OutOfRangeCheck.OUT, FlowRangeCheck.IN2
FT-501.General_Fault, FlowFaultCheck.IN1
FT-502.General_Fault, FlowFaultCheck.IN2
FlowRangeCheck.OUT, RangeOrFault.IN1
FlowFaultCheck.OUT, RangeOrFault.IN2
RangeOrFault.OUT, RatioDisable_OR1.IN1
PropaneLowFlow_LT.OUT, RatioDisable_OR1.IN2
RatioDisable_OR1.OUT, RatioDisable_OR2.IN1
FV501_OpenHold_TON.Q, RatioDisable_OR2.IN2
RatioDisable_OR2.OUT, ControlInhibitCause.IN1
PT-501.Low_Alarm, ControlInhibitCause.IN2
ControlInhibitCause.OUT, FFIC-503.Inhibit
ControlInhibitCause.OUT, FIC-504.Inhibit
ControlInhibitCause.OUT, FV-502.Inhibit
ControlInhibitCause.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-503.Auto
FT-502.PV, FIC-504.PV
FIC-504.XOUT, FV-502.Control_Signal
FIC-504.XOUT, FV_502_ControlSignal
FT-501.PV, FT_501_PropaneFlow_PV
FT-502.PV, FT_502_MRFlow_PV
PT-501.PV, PT_501_Pressure_PV
TIT-102.PV, TIT_102_Temperature_PV
FFIC-503.ActiveRatio, FFIC_503_ActiveRatio
FV-501.Feedback_Pos, FV_501_Feedback_Pos
FFIC-503.RatioErr, RatioDevHigh_GT.IN1
RatioDevHigh_GT.OUT, RatioDevHigh_TON.IN
RatioDevHigh_TON.Q, RatioDevHigh_ALM
FFIC-503.RatioErr, RatioDevLow_LT.IN1
RatioDevLow_LT.OUT, RatioDevLow_TON.IN
RatioDevLow_TON.Q, RatioDevLow_ALM

* Parameter Data Connections *
"FT-501 Propane Flow", FT-501.Name
"Propane flow to MCHE (wild flow)", FT-501.Description
312.5, FT-501.Scaling_Slope
-1250.0, FT-501.Scaling_Offset
TRUE, FT-501.Alarm_Enable
5000.0, FT-501.PV_High
500.0, FT-501.PV_Low
"FT-502 MR Flow", FT-502.Name
"Mixed refrigerant flow to MCHE (controlled flow)", FT-502.Description
125.0, FT-502.Scaling_Slope
-500.0, FT-502.Scaling_Offset
TRUE, FT-502.Alarm_Enable
2000.0, FT-502.PV_High
200.0, FT-502.PV_Low
"PT-501 End-Flash Drum Pressure", PT-501.Name
"End-flash drum pressure for permissive", PT-501.Description
0.1875, PT-501.Scaling_Slope
-0.75, PT-501.Scaling_Offset
TRUE, PT-501.Alarm_Enable
2.0, PT-501.PV_Low
"TIT-102 MCHE Outlet Temp", TIT-102.Name
"MCHE outlet temperature for auto trim", TIT-102.Description
12.5, TIT-102.Scaling_Slope
-250.0, TIT-102.Scaling_Offset
TRUE, TIT-102.Alarm_Enable
-155.0, TIT-102.PV_High
"FFIC-503 MR/Propane Ratio Controller", FFIC-503.Name
"Computes MR flow SP from propane flow and ratio with overrides", FFIC-503.Description
0.0, FFIC-503.Bias
0.0, FFIC-503.TrimKp
T#0s, FFIC-503.TrimTi
"FIC-504 MR Flow PID", FIC-504.Name
"Controls MR valve to match MR flow SP", FIC-504.Description
TRUE, FIC-504.AUTO
0.0, FIC-504.MV_MIN
100.0, FIC-504.MV_MAX
1.5, FIC-504.KP
30.0, FIC-504.TR
0.0, FIC-504.TD
2000.0, FIC-504.PV_High
200.0, FIC-504.PV_Low
100.0, FIC-504.Deviation_Limit
"FV-502 MR Control Valve", FV-502.Name
"Valve adjusting MR flow per PID output", FV-502.Description
FALSE, FV-502.Manual_Mode
0.0, FV-502.Manual_Position
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
T#30s, FV-502.Timeout
"FV-501 Propane Anti-Surge Valve", FV-501.Name
"Propane compressor anti-surge valve (status used for override)", FV-501.Description
TRUE, FV-501.Manual_Mode
0.0, FV-501.Manual_Position
100.0, FV-501.Open_Limit
0.0, FV-501.Close_Limit
T#30s, FV-501.Timeout
3.0, RatioMin_DIV.IN2
2.0, RatioMax_DIV.IN2
0.4, RatioSP_AutoBump_ADD.IN1
0.0, RatioSP_AutoTrim_SEL.IN0
0.1, RatioSP_AutoTrim_SEL.IN1
99.0, FV501_FullyOpen_GE.IN2
1000.0, AntiSurge_SP_SEL.IN1
100.0, LowFlow_SP_SEL.IN1
500.0, FaultOverride_SP_SEL.IN1
500.0, PropaneLowFlow_LT.IN2
T#5s, FV501_OpenHold_TON.PT
0.2, RatioDevHigh_GT.IN2
-0.2, RatioDevLow_LT.IN2
T#10s, RatioDevHigh_TON.PT
T#10s, RatioDevLow_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 01:49:05

### Output:
```
* Function Blocks *
ANALOG_IN FT-501
ANALOG_IN FT-502
ANALOG_IN PT-501
ANALOG_IN TIT-102
RATIO_CONTROL FFIC-503
PID_BASIC FIC-504
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC FV-501

* Variables *
REAL FT_501_PropaneFlow_PV
REAL FT_502_MRFlow_PV
REAL PT_501_Pressure_PV
REAL TIT_102_Temperature_PV
REAL FIC_504_SP_Selected
REAL FFIC_503_ActiveRatio
REAL FV_502_ControlSignal
REAL FV_501_Feedback_Pos
REAL RatioBias_Manual
BOOL AntiSurgeActive
BOOL PropaneLowFlow
BOOL FlowRangeOrFault
BOOL RatioControlInhibit
BOOL RatioDevHigh_ALM
BOOL RatioDevLow_ALM

* Functions *
DIV RatioMin_DIV
DIV RatioMax_DIV
OR FT501_OutOfRangeCheck
OR FT502_OutOfRangeCheck
OR FlowFaultCheck
OR FlowRangeCheck
OR RangeOrFault
OR ControlInhibitCause
GE FV501_FullyOpen_GE
TON FV501_OpenHold_TON
LT PropaneLowFlow_LT
SEL AntiSurge_SP_SEL
SEL LowFlow_SP_SEL
SEL FaultOverride_SP_SEL
ADD RatioSP_AutoBump_ADD
SEL RatioSP_AutoTrim_SEL
ADD RatioSP_ManualBias_ADD
OR RatioDisable_OR1
OR RatioDisable_OR2
NOT RatioAuto_NOT
GT RatioDevHigh_GT
LT RatioDevLow_LT
TON RatioDevHigh_TON
TON RatioDevLow_TON

* Data Connections * 
FT-501.PV, FFIC-503.PrimaryPV
FT-502.PV, FFIC-503.SecondaryPV
FT-501.PV, RatioMin_DIV.IN1
FT-501.PV, RatioMax_DIV.IN1
RatioMin_DIV.OUT, FFIC-503.MV_MIN
RatioMax_DIV.OUT, FFIC-503.MV_MAX
TIT-102.High_Alarm, RatioSP_AutoTrim_SEL.G
RatioSP_AutoTrim_SEL.OUT, RatioSP_AutoBump_ADD.IN2
RatioSP_AutoBump_ADD.OUT, RatioSP_ManualBias_ADD.IN1
RatioBias_Manual, RatioSP_ManualBias_ADD.IN2
RatioSP_ManualBias_ADD.OUT, FFIC-503.RatioSP
FV-501.Feedback_Pos, FV501_FullyOpen_GE.IN1
FV501_FullyOpen_GE.OUT, FV501_OpenHold_TON.IN
FV501_OpenHold_TON.Q, AntiSurge_SP_SEL.G
FFIC-503.SlaveSP, AntiSurge_SP_SEL.IN0
AntiSurge_SP_SEL.OUT, LowFlow_SP_SEL.IN0
FT-501.PV, PropaneLowFlow_LT.IN1
PropaneLowFlow_LT.OUT, LowFlow_SP_SEL.G
LowFlow_SP_SEL.OUT, FaultOverride_SP_SEL.IN0
RangeOrFault.OUT, FaultOverride_SP_SEL.G
FaultOverride_SP_SEL.OUT, FIC-504.SP
FaultOverride_SP_SEL.OUT, FIC_504_SP_Selected
FT-501.High_Alarm, FT501_OutOfRangeCheck.IN1
FT-501.Low_Alarm, FT501_OutOfRangeCheck.IN2
FT-502.High_Alarm, FT502_OutOfRangeCheck.IN1
FT-502.Low_Alarm, FT502_OutOfRangeCheck.IN2
FT501_OutOfRangeCheck.OUT, FlowRangeCheck.IN1
FT502_OutOfRangeCheck.OUT, FlowRangeCheck.IN2
FT-501.General_Fault, FlowFaultCheck.IN1
FT-502.General_Fault, FlowFaultCheck.IN2
FlowRangeCheck.OUT, RangeOrFault.IN1
FlowFaultCheck.OUT, RangeOrFault.IN2
RangeOrFault.OUT, RatioDisable_OR1.IN1
PropaneLowFlow_LT.OUT, RatioDisable_OR1.IN2
RatioDisable_OR1.OUT, RatioDisable_OR2.IN1
FV501_OpenHold_TON.Q, RatioDisable_OR2.IN2
RatioDisable_OR2.OUT, ControlInhibitCause.IN1
PT-501.Low_Alarm, ControlInhibitCause.IN2
ControlInhibitCause.OUT, FFIC-503.Inhibit
ControlInhibitCause.OUT, FIC-504.Inhibit
ControlInhibitCause.OUT, FV-502.Inhibit
ControlInhibitCause.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-503.Auto
FT-502.PV, FIC-504.PV
FIC-504.XOUT, FV-502.Control_Signal
FIC-504.XOUT, FV_502_ControlSignal
FT-501.PV, FT_501_PropaneFlow_PV
FT-502.PV, FT_502_MRFlow_PV
PT-501.PV, PT_501_Pressure_PV
TIT-102.PV, TIT_102_Temperature_PV
FFIC-503.ActiveRatio, FFIC_503_ActiveRatio
FV-501.Feedback_Pos, FV_501_Feedback_Pos
FFIC-503.RatioErr, RatioDevHigh_GT.IN1
RatioDevHigh_GT.OUT, RatioDevHigh_TON.IN
RatioDevHigh_TON.Q, RatioDevHigh_ALM
FFIC-503.RatioErr, RatioDevLow_LT.IN1
RatioDevLow_LT.OUT, RatioDevLow_TON.IN
RatioDevLow_TON.Q, RatioDevLow_ALM

* Parameter Data Connections *
312.5, FT-501.Scaling_Slope
-1250.0, FT-501.Scaling_Offset
TRUE, FT-501.Alarm_Enable
5000.0, FT-501.PV_High
500.0, FT-501.PV_Low
125.0, FT-502.Scaling_Slope
-500.0, FT-502.Scaling_Offset
TRUE, FT-502.Alarm_Enable
2000.0, FT-502.PV_High
200.0, FT-502.PV_Low
0.1875, PT-501.Scaling_Slope
-0.75, PT-501.Scaling_Offset
TRUE, PT-501.Alarm_Enable
2.0, PT-501.PV_Low
12.5, TIT-102.Scaling_Slope
-250.0, TIT-102.Scaling_Offset
TRUE, TIT-102.Alarm_Enable
-155.0, TIT-102.PV_High
0.0, FFIC-503.Bias
0.0, FFIC-503.TrimKp
T#0s, FFIC-503.TrimTi
TRUE, FIC-504.AUTO
0.0, FIC-504.MV_MIN
100.0, FIC-504.MV_MAX
1.5, FIC-504.KP
30.0, FIC-504.TR
0.0, FIC-504.TD
2000.0, FIC-504.PV_High
200.0, FIC-504.PV_Low
100.0, FIC-504.Deviation_Limit
FALSE, FV-502.Manual_Mode
0.0, FV-502.Manual_Position
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
T#30s, FV-502.Timeout
TRUE, FV-501.Manual_Mode
0.0, FV-501.Manual_Position
100.0, FV-501.Open_Limit
0.0, FV-501.Close_Limit
T#30s, FV-501.Timeout
3.0, RatioMin_DIV.IN2
2.0, RatioMax_DIV.IN2
0.4, RatioSP_AutoBump_ADD.IN1
0.0, RatioSP_AutoTrim_SEL.IN0
0.1, RatioSP_AutoTrim_SEL.IN1
99.0, FV501_FullyOpen_GE.IN2
1000.0, AntiSurge_SP_SEL.IN1
100.0, LowFlow_SP_SEL.IN1
500.0, FaultOverride_SP_SEL.IN1
500.0, PropaneLowFlow_LT.IN2
T#5s, FV501_OpenHold_TON.PT
0.2, RatioDevHigh_GT.IN2
-0.2, RatioDevLow_LT.IN2
T#10s, RatioDevHigh_TON.PT
T#10s, RatioDevLow_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 01:50:00

### Output:
```
* Function Blocks *
ANALOG_IN FT-501
ANALOG_IN FT-502
ANALOG_IN PT-501
ANALOG_IN TIT-102
RATIO_CONTROL FFIC-503
PID_BASIC FIC-504
VALVE_ELECTRIC FV-502
VALVE_ELECTRIC FV-501

* Variables *
REAL FT_501_PropaneFlow_PV
REAL FT_502_MRFlow_PV
REAL PT_501_Pressure_PV
REAL TIT_102_Temperature_PV
REAL FIC_504_SP_Selected
REAL FFIC_503_ActiveRatio
REAL FV_502_ControlSignal
REAL FV_501_Feedback_Pos
REAL RatioBias_Manual
BOOL AntiSurgeActive
BOOL PropaneLowFlow
BOOL FlowRangeOrFault
BOOL RatioControlInhibit
BOOL RatioDevHigh_ALM
BOOL RatioDevLow_ALM

* Functions *
DIV RatioMin_DIV
DIV RatioMax_DIV
OR FT501_OutOfRangeCheck
OR FT502_OutOfRangeCheck
OR FlowFaultCheck
OR FlowRangeCheck
OR RangeOrFault
OR ControlInhibitCause
GE FV501_FullyOpen_GE
TON FV501_OpenHold_TON
LT PropaneLowFlow_LT
SEL AntiSurge_SP_SEL
SEL LowFlow_SP_SEL
SEL FaultOverride_SP_SEL
ADD RatioSP_AutoBump_ADD
SEL RatioSP_AutoTrim_SEL
ADD RatioSP_ManualBias_ADD
OR RatioDisable_OR1
OR RatioDisable_OR2
NOT RatioAuto_NOT
GT RatioDevHigh_GT
LT RatioDevLow_LT
TON RatioDevHigh_TON
TON RatioDevLow_TON

* Data Connections * 
FT-501.PV, FFIC-503.PrimaryPV
FT-502.PV, FFIC-503.SecondaryPV
FT-501.PV, RatioMin_DIV.IN1
FT-501.PV, RatioMax_DIV.IN1
RatioMin_DIV.OUT, FFIC-503.MV_MIN
RatioMax_DIV.OUT, FFIC-503.MV_MAX
TIT-102.High_Alarm, RatioSP_AutoTrim_SEL.G
RatioSP_AutoTrim_SEL.OUT, RatioSP_AutoBump_ADD.IN2
RatioSP_AutoBump_ADD.OUT, RatioSP_ManualBias_ADD.IN1
RatioBias_Manual, RatioSP_ManualBias_ADD.IN2
RatioSP_ManualBias_ADD.OUT, FFIC-503.RatioSP
FV-501.Feedback_Pos, FV501_FullyOpen_GE.IN1
FV501_FullyOpen_GE.OUT, FV501_OpenHold_TON.IN
FV501_OpenHold_TON.Q, AntiSurge_SP_SEL.G
FFIC-503.SlaveSP, AntiSurge_SP_SEL.IN0
AntiSurge_SP_SEL.OUT, LowFlow_SP_SEL.IN0
FT-501.PV, PropaneLowFlow_LT.IN1
PropaneLowFlow_LT.OUT, LowFlow_SP_SEL.G
LowFlow_SP_SEL.OUT, FaultOverride_SP_SEL.IN0
RangeOrFault.OUT, FaultOverride_SP_SEL.G
FaultOverride_SP_SEL.OUT, FIC-504.SP
FaultOverride_SP_SEL.OUT, FIC_504_SP_Selected
FT-501.High_Alarm, FT501_OutOfRangeCheck.IN1
FT-501.Low_Alarm, FT501_OutOfRangeCheck.IN2
FT-502.High_Alarm, FT502_OutOfRangeCheck.IN1
FT-502.Low_Alarm, FT502_OutOfRangeCheck.IN2
FT501_OutOfRangeCheck.OUT, FlowRangeCheck.IN1
FT502_OutOfRangeCheck.OUT, FlowRangeCheck.IN2
FT-501.General_Fault, FlowFaultCheck.IN1
FT-502.General_Fault, FlowFaultCheck.IN2
FlowRangeCheck.OUT, RangeOrFault.IN1
FlowFaultCheck.OUT, RangeOrFault.IN2
RangeOrFault.OUT, RatioDisable_OR1.IN1
PropaneLowFlow_LT.OUT, RatioDisable_OR1.IN2
RatioDisable_OR1.OUT, RatioDisable_OR2.IN1
FV501_OpenHold_TON.Q, RatioDisable_OR2.IN2
RatioDisable_OR2.OUT, ControlInhibitCause.IN1
PT-501.Low_Alarm, ControlInhibitCause.IN2
ControlInhibitCause.OUT, FFIC-503.Inhibit
ControlInhibitCause.OUT, FIC-504.Inhibit
ControlInhibitCause.OUT, FV-502.Inhibit
ControlInhibitCause.OUT, RatioAuto_NOT.IN
RatioAuto_NOT.OUT, FFIC-503.Auto
FT-502.PV, FIC-504.PV
FIC-504.XOUT, FV-502.Control_Signal
FIC-504.XOUT, FV_502_ControlSignal
FT-501.PV, FT_501_PropaneFlow_PV
FT-502.PV, FT_502_MRFlow_PV
PT-501.PV, PT_501_Pressure_PV
TIT-102.PV, TIT_102_Temperature_PV
FFIC-503.ActiveRatio, FFIC_503_ActiveRatio
FV-501.Feedback_Pos, FV_501_Feedback_Pos
FFIC-503.RatioErr, RatioDevHigh_GT.IN1
RatioDevHigh_GT.OUT, RatioDevHigh_TON.IN
RatioDevHigh_TON.Q, RatioDevHigh_ALM
FFIC-503.RatioErr, RatioDevLow_LT.IN1
RatioDevLow_LT.OUT, RatioDevLow_TON.IN
RatioDevLow_TON.Q, RatioDevLow_ALM

* Parameter Data Connections *
312.5, FT-501.Scaling_Slope
-1250.0, FT-501.Scaling_Offset
TRUE, FT-501.Alarm_Enable
5000.0, FT-501.PV_High
500.0, FT-501.PV_Low
125.0, FT-502.Scaling_Slope
-500.0, FT-502.Scaling_Offset
TRUE, FT-502.Alarm_Enable
2000.0, FT-502.PV_High
200.0, FT-502.PV_Low
0.1875, PT-501.Scaling_Slope
-0.75, PT-501.Scaling_Offset
TRUE, PT-501.Alarm_Enable
2.0, PT-501.PV_Low
12.5, TIT-102.Scaling_Slope
-250.0, TIT-102.Scaling_Offset
TRUE, TIT-102.Alarm_Enable
-155.0, TIT-102.PV_High
0.0, FFIC-503.Bias
0.0, FFIC-503.TrimKp
T#0s, FFIC-503.TrimTi
TRUE, FIC-504.AUTO
0.0, FIC-504.MV_MIN
100.0, FIC-504.MV_MAX
1.5, FIC-504.KP
30.0, FIC-504.TR
0.0, FIC-504.TD
2000.0, FIC-504.PV_High
200.0, FIC-504.PV_Low
100.0, FIC-504.Deviation_Limit
FALSE, FV-502.Manual_Mode
0.0, FV-502.Manual_Position
100.0, FV-502.Open_Limit
0.0, FV-502.Close_Limit
T#30s, FV-502.Timeout
TRUE, FV-501.Manual_Mode
0.0, FV-501.Manual_Position
100.0, FV-501.Open_Limit
0.0, FV-501.Close_Limit
T#30s, FV-501.Timeout
3.0, RatioMin_DIV.IN2
2.0, RatioMax_DIV.IN2
0.4, RatioSP_AutoBump_ADD.IN1
0.0, RatioSP_AutoTrim_SEL.IN0
0.1, RatioSP_AutoTrim_SEL.IN1
99.0, FV501_FullyOpen_GE.IN2
1000.0, AntiSurge_SP_SEL.IN1
100.0, LowFlow_SP_SEL.IN1
500.0, FaultOverride_SP_SEL.IN1
500.0, PropaneLowFlow_LT.IN2
T#5s, FV501_OpenHold_TON.PT
0.2, RatioDevHigh_GT.IN2
-0.2, RatioDevLow_LT.IN2
T#10s, RatioDevHigh_TON.PT
T#10s, RatioDevLow_TON.PT
```

---


