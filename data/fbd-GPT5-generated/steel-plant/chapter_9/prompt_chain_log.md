# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 05:02:23

## Step 1: contextgen1-sensors
**Time:** 05:02:23

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
**Time:** 05:03:08

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
**Time:** 05:03:16

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Probability Needed |
|------------------|--------------------|
| Ratio Control | 0.98 |
| PID Control | 0.90 |
| OVERRIDE | 0.55 |
| Cascade Control | 0.15 |
| FEEDFORWARD | 0.10 |
| VOTING | 0.05 |
| SPLIT RANGE | 0.05 |
| Duty-Standby | 0.01 |

Selected Control Strategy: Ratio Control 
Short explanation: The narrative specifies computing an air-flow setpoint from the gas flow using a configurable ratio, sending that setpoint to a slave flow PID (FIC-802) to modulate FV-802, with permissives switching the slave to manual when conditions are not met.

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
**Timestamp:** 2025-09-24 05:03:40

## Step 1: openplc-function-blocks-v2
**Time:** 05:03:40

### Output:
```
* Function Blocks *
ANALOG_IN AL-801
ANALOG_IN AL-802
ANALOG_IN AL-803
ANALOG_IN AL-804
ANALOG_IN FT-801
ANALOG_IN FT-802
ANALOG_IN PT-801
RATIO_CONTROL FFIC-801
PID_BASIC FIC-802
VALVE_ELECTRIC FV-802
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 05:04:21

### Output:
```
* Function Blocks *
ANALOG_IN AL-801
ANALOG_IN AL-802
ANALOG_IN AL-803
ANALOG_IN AL-804
ANALOG_IN FT-801
ANALOG_IN FT-802
ANALOG_IN PT-801
RATIO_CONTROL FFIC-801
PID_BASIC FIC-802
VALVE_ELECTRIC FV-802
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 05:05:10

### Output:
```
* Functions *

* Block-to-Block Connections *
FT-801.PV, FFIC-801.PrimaryPV
FT-802.PV, FFIC-801.SecondaryPV
FFIC-801.SlaveSP, FIC-802.SP
FT-802.PV, FIC-802.PV
FIC-802.XOUT, FV-802.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 05:05:44

### Output:
```
* Functions * 
OR PT801_OutOfRange_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR RatioInhibit4_OR
OR FIC802_Manual_OR
OR FIC802_Manual2_OR

* Data Connections *
PT-801.High_Alarm, PT801_OutOfRange_OR.IN1
PT-801.Low_Alarm, PT801_OutOfRange_OR.IN2
FT-801.Low_Alarm, RatioInhibit1_OR.IN1
FT-802.High_Alarm, RatioInhibit1_OR.IN2
PT801_OutOfRange_OR.OUT, RatioInhibit2_OR.IN1
FT-801.General_Fault, RatioInhibit2_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit3_OR.IN1
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, RatioInhibit4_OR.IN1
PT-801.General_Fault, RatioInhibit4_OR.IN2
RatioInhibit4_OR.OUT, FFIC-801.Inhibit
PT801_OutOfRange_OR.OUT, FV-802.Inhibit
FT-801.Low_Alarm, FIC802_Manual_OR.IN1
FT-801.General_Fault, FIC802_Manual_OR.IN2
FIC802_Manual_OR.OUT, FIC802_Manual2_OR.IN1
PT-801.General_Fault, FIC802_Manual2_OR.IN2
FIC802_Manual2_OR.OUT, FIC-802.Inhibit

* Parameter Data Connections *
100, FT-801.PV_Low
0.5, PT-801.PV_Low
2.0, PT-801.PV_High
6000, FT-802.PV_High
3.0, AL-801.PV_High
2.0, AL-802.PV_Low
TRUE, FT-801.Alarm_Enable
TRUE, FT-802.Alarm_Enable
TRUE, PT-801.Alarm_Enable
TRUE, AL-801.Alarm_Enable
TRUE, AL-802.Alarm_Enable
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 05:06:49

### Output:
```
* Parameter Data Connections *
6.25, FT-801.Scaling_Slope
-25.0, FT-801.Scaling_Offset
2.0, FT-801.PV_Low
6.25, PT-801.Scaling_Slope
-25.0, PT-801.Scaling_Offset
2.5, FFIC-801.RatioSP
6000.0, FFIC-801.MV_MAX
50.0, FIC-802.X0
6000.0, FIC-802.PV_High
50.0, FV-802.Manual_Position
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 05:08:30

### Output:
```
* Parameter Data Connections *
6.25, FT-801.Scaling_Slope
-25.0, FT-801.Scaling_Offset
100.0, FT-801.PV_Low
5000.0, FT-801.PV_High
6.25, PT-801.Scaling_Slope
-25.0, PT-801.Scaling_Offset
0.5, PT-801.PV_Low
2.0, PT-801.PV_High
2.5, FFIC-801.RatioSP
0.0, FFIC-801.MV_MIN
6000.0, FFIC-801.MV_MAX
50.0, FIC-802.X0
0.0, FIC-802.PV_Low
6000.0, FIC-802.PV_High
0.0, FT-802.PV_Low
6000.0, FT-802.PV_High
50.0, FV-802.Manual_Position
3.0, AL-801.PV_High
2.0, AL-802.PV_Low
TRUE, FT-801.Alarm_Enable
TRUE, FT-802.Alarm_Enable
TRUE, PT-801.Alarm_Enable
TRUE, AL-801.Alarm_Enable
TRUE, AL-802.Alarm_Enable
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 05:09:25

### Output:
```
* Variables *
REAL FIC802_AirFlow_SP_FromRatio
REAL FFIC801_ActiveAirToGasRatio
REAL FT801_BFG_Flow_PV
REAL FT802_Air_Flow_PV
REAL PT801_BFG_Pressure_PV

* Data Connections *
FFIC-801.SlaveSP, FIC802_AirFlow_SP_FromRatio
FFIC-801.ActiveRatio, FFIC801_ActiveAirToGasRatio
FT-801.PV, FT801_BFG_Flow_PV
FT-802.PV, FT802_Air_Flow_PV
PT-801.PV, PT801_BFG_Pressure_PV
```

---

## Step 8: openplc-rule-checks
**Time:** 05:10:08

### Output:
```
* Function Blocks *
ANALOG_IN AL-801
ANALOG_IN AL-802
ANALOG_IN AL-803
ANALOG_IN AL-804
ANALOG_IN FT-801
ANALOG_IN FT-802
ANALOG_IN PT-801
RATIO_CONTROL FFIC-801
PID_BASIC FIC-802
VALVE_ELECTRIC FV-802

* Variables *
REAL FIC802_AirFlow_SP_FromRatio
REAL FFIC801_ActiveAirToGasRatio
REAL FT801_BFG_Flow_PV
REAL FT802_Air_Flow_PV
REAL PT801_BFG_Pressure_PV
REAL AL801_HighRatio_SP
REAL AL802_LowRatio_SP
BOOL AL801_HighRatio_Alarm
BOOL AL802_LowRatio_Alarm
BOOL AL803_FT801_Fault_Alarm
BOOL AL804_PT801_Fault_Alarm

* Functions *
OR PT801_OutOfRange_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR RatioInhibit4_OR
OR FIC802_Manual_OR
OR FIC802_Manual2_OR
GT HighRatio_GT
LT LowRatio_LT
TON HighRatio_TON

* Data Connections *
FT-801.PV, FFIC-801.PrimaryPV
FT-802.PV, FFIC-801.SecondaryPV
FFIC-801.SlaveSP, FIC-802.SP
FT-802.PV, FIC-802.PV
FIC-802.XOUT, FV-802.Control_Signal
PT-801.High_Alarm, PT801_OutOfRange_OR.IN1
PT-801.Low_Alarm, PT801_OutOfRange_OR.IN2
PT801_OutOfRange_OR.OUT, RatioInhibit2_OR.IN1
PT801_OutOfRange_OR.OUT, FV-802.Inhibit
FT-801.Low_Alarm, RatioInhibit1_OR.IN1
FT-802.High_Alarm, RatioInhibit1_OR.IN2
FT-801.General_Fault, RatioInhibit2_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit3_OR.IN1
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, RatioInhibit4_OR.IN1
PT-801.General_Fault, RatioInhibit4_OR.IN2
RatioInhibit4_OR.OUT, FFIC-801.Inhibit
FT-801.Low_Alarm, FIC802_Manual_OR.IN1
FT-801.General_Fault, FIC802_Manual_OR.IN2
FIC802_Manual_OR.OUT, FIC802_Manual2_OR.IN1
PT-801.General_Fault, FIC802_Manual2_OR.IN2
FIC802_Manual2_OR.OUT, FIC-802.Inhibit
FFIC-801.ActiveRatio, HighRatio_GT.IN1
AL801_HighRatio_SP, HighRatio_GT.IN2
HighRatio_GT.OUT, HighRatio_TON.IN
HighRatio_TON.Q, AL801_HighRatio_Alarm
FFIC-801.ActiveRatio, LowRatio_LT.IN1
AL802_LowRatio_SP, LowRatio_LT.IN2
LowRatio_LT.OUT, AL802_LowRatio_Alarm
FFIC-801.SlaveSP, FIC802_AirFlow_SP_FromRatio
FFIC-801.ActiveRatio, FFIC801_ActiveAirToGasRatio
FT-801.PV, FT801_BFG_Flow_PV
FT-802.PV, FT802_Air_Flow_PV
PT-801.PV, PT801_BFG_Pressure_PV
FT-801.General_Fault, AL803_FT801_Fault_Alarm
PT-801.General_Fault, AL804_PT801_Fault_Alarm

* Parameter Data Connections *
6.25, FT-801.Scaling_Slope
-25.0, FT-801.Scaling_Offset
100.0, FT-801.PV_Low
5000.0, FT-801.PV_High
6.25, FT-802.Scaling_Slope
-25.0, FT-802.Scaling_Offset
0.0, FT-802.PV_Low
6000.0, FT-802.PV_High
6.25, PT-801.Scaling_Slope
-25.0, PT-801.Scaling_Offset
0.5, PT-801.PV_Low
2.0, PT-801.PV_High
TRUE, FT-801.Alarm_Enable
TRUE, FT-802.Alarm_Enable
TRUE, PT-801.Alarm_Enable
TRUE, AL-801.Alarm_Enable
TRUE, AL-802.Alarm_Enable
2.5, FFIC-801.RatioSP
0.0, FFIC-801.MV_MIN
6000.0, FFIC-801.MV_MAX
0.0, FFIC-801.Bias
0.0, FFIC-801.TrimKp
T#0s, FFIC-801.TrimTi
TRUE, FFIC-801.Auto
TRUE, FIC-802.AUTO
0.0, FIC-802.MV_MIN
100.0, FIC-802.MV_MAX
0.0, FIC-802.PV_Low
6000.0, FIC-802.PV_High
50.0, FIC-802.X0
50.0, FV-802.Manual_Position
3.0, AL801_HighRatio_SP
2.0, AL802_LowRatio_SP
T#5s, HighRatio_TON.PT
```

---

## Step 9: openplc-rule-checks2
**Time:** 05:11:40

### Output:
```
* Function Blocks *
ANALOG_IN AL-801
ANALOG_IN AL-802
ANALOG_IN AL-803
ANALOG_IN AL-804
ANALOG_IN FT-801
ANALOG_IN FT-802
ANALOG_IN PT-801
RATIO_CONTROL FFIC-801
PID_BASIC FIC-802
VALVE_ELECTRIC FV-802
TON HighRatio_TON

* Variables *
REAL FIC802_AirFlow_SP_FromRatio
REAL FFIC801_ActiveAirToGasRatio
REAL FT801_BFG_Flow_PV
REAL FT802_Air_Flow_PV
REAL PT801_BFG_Pressure_PV
REAL AL801_HighRatio_SP
REAL AL802_LowRatio_SP
BOOL AL801_HighRatio_Alarm
BOOL AL802_LowRatio_Alarm
BOOL AL803_FT801_Fault_Alarm
BOOL AL804_PT801_Fault_Alarm

* Functions *
OR PT801_OutOfRange_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR RatioInhibit4_OR
OR FIC802_Manual_OR
OR FIC802_Manual2_OR
GT HighRatio_GT
LT LowRatio_LT

* Data Connections *
FT-801.PV, FFIC-801.PrimaryPV
FT-802.PV, FFIC-801.SecondaryPV
FFIC-801.SlaveSP, FIC-802.SP
FT-802.PV, FIC-802.PV
FIC-802.XOUT, FV-802.Control_Signal
PT-801.High_Alarm, PT801_OutOfRange_OR.IN1
PT-801.Low_Alarm, PT801_OutOfRange_OR.IN2
PT801_OutOfRange_OR.OUT, RatioInhibit2_OR.IN1
PT801_OutOfRange_OR.OUT, FV-802.Inhibit
FT-801.Low_Alarm, RatioInhibit1_OR.IN1
FT-802.High_Alarm, RatioInhibit1_OR.IN2
FT-801.General_Fault, RatioInhibit2_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit3_OR.IN1
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, RatioInhibit4_OR.IN1
PT-801.General_Fault, RatioInhibit4_OR.IN2
RatioInhibit4_OR.OUT, FFIC-801.Inhibit
FT-801.Low_Alarm, FIC802_Manual_OR.IN1
FT-801.General_Fault, FIC802_Manual_OR.IN2
FIC802_Manual_OR.OUT, FIC802_Manual2_OR.IN1
PT-801.General_Fault, FIC802_Manual2_OR.IN2
FIC802_Manual2_OR.OUT, FIC-802.Inhibit
FFIC-801.ActiveRatio, HighRatio_GT.IN1
AL801_HighRatio_SP, HighRatio_GT.IN2
HighRatio_GT.OUT, HighRatio_TON.IN
HighRatio_TON.Q, AL801_HighRatio_Alarm
FFIC-801.ActiveRatio, LowRatio_LT.IN1
AL802_LowRatio_SP, LowRatio_LT.IN2
LowRatio_LT.OUT, AL802_LowRatio_Alarm
FFIC-801.SlaveSP, FIC802_AirFlow_SP_FromRatio
FFIC-801.ActiveRatio, FFIC801_ActiveAirToGasRatio
FT-801.PV, FT801_BFG_Flow_PV
FT-802.PV, FT802_Air_Flow_PV
PT-801.PV, PT801_BFG_Pressure_PV
FT-801.General_Fault, AL803_FT801_Fault_Alarm
PT-801.General_Fault, AL804_PT801_Fault_Alarm

* Parameter Data Connections *
6.25, FT-801.Scaling_Slope
-25.0, FT-801.Scaling_Offset
100.0, FT-801.PV_Low
5000.0, FT-801.PV_High
6.25, FT-802.Scaling_Slope
-25.0, FT-802.Scaling_Offset
0.0, FT-802.PV_Low
6000.0, FT-802.PV_High
6.25, PT-801.Scaling_Slope
-25.0, PT-801.Scaling_Offset
0.5, PT-801.PV_Low
2.0, PT-801.PV_High
TRUE, FT-801.Alarm_Enable
TRUE, FT-802.Alarm_Enable
TRUE, PT-801.Alarm_Enable
TRUE, AL-801.Alarm_Enable
TRUE, AL-802.Alarm_Enable
2.5, FFIC-801.RatioSP
0.0, FFIC-801.MV_MIN
6000.0, FFIC-801.MV_MAX
0.0, FFIC-801.Bias
0.0, FFIC-801.TrimKp
T#0s, FFIC-801.TrimTi
TRUE, FFIC-801.Auto
TRUE, FIC-802.AUTO
0.0, FIC-802.MV_MIN
100.0, FIC-802.MV_MAX
0.0, FIC-802.PV_Low
6000.0, FIC-802.PV_High
50.0, FIC-802.X0
50.0, FV-802.Manual_Position
3.0, AL801_HighRatio_SP
2.0, AL802_LowRatio_SP
T#5s, HighRatio_TON.PT
```

---

## Step 10: append_two_inputs
**Time:** 05:12:11

### Output:
```
* Function Blocks *
ANALOG_IN AL-801
ANALOG_IN AL-802
ANALOG_IN AL-803
ANALOG_IN AL-804
ANALOG_IN FT-801
ANALOG_IN FT-802
ANALOG_IN PT-801
RATIO_CONTROL FFIC-801
PID_BASIC FIC-802
VALVE_ELECTRIC FV-802
TON HighRatio_TON

* Variables *
REAL FIC802_AirFlow_SP_FromRatio
REAL FFIC801_ActiveAirToGasRatio
REAL FT801_BFG_Flow_PV
REAL FT802_Air_Flow_PV
REAL PT801_BFG_Pressure_PV
REAL AL801_HighRatio_SP
REAL AL802_LowRatio_SP
BOOL AL801_HighRatio_Alarm
BOOL AL802_LowRatio_Alarm
BOOL AL803_FT801_Fault_Alarm
BOOL AL804_PT801_Fault_Alarm

* Functions *
OR PT801_OutOfRange_OR
OR RatioInhibitCombine_OR
OR RatioInhibitFinal_OR
OR FIC802_Manual_OR
OR FIC802_Manual2_OR
GT HighRatio_GT
LT LowRatio_LT

* Data Connections *
FT-801.PV, FFIC-801.PrimaryPV
FT-802.PV, FFIC-801.SecondaryPV
FFIC-801.SlaveSP, FIC-802.SP
FT-802.PV, FIC-802.PV
FIC-802.XOUT, FV-802.Control_Signal
PT-801.High_Alarm, PT801_OutOfRange_OR.IN1
PT-801.Low_Alarm, PT801_OutOfRange_OR.IN2
PT801_OutOfRange_OR.OUT, FV-802.Inhibit
FIC802_Manual2_OR.OUT, RatioInhibitCombine_OR.IN1
FT-802.High_Alarm, RatioInhibitCombine_OR.IN2
RatioInhibitCombine_OR.OUT, RatioInhibitFinal_OR.IN1
PT801_OutOfRange_OR.OUT, RatioInhibitFinal_OR.IN2
RatioInhibitFinal_OR.OUT, FFIC-801.Inhibit
FT-801.Low_Alarm, FIC802_Manual_OR.IN1
FT-801.General_Fault, FIC802_Manual_OR.IN2
FIC802_Manual_OR.OUT, FIC802_Manual2_OR.IN1
PT-801.General_Fault, FIC802_Manual2_OR.IN2
FIC802_Manual2_OR.OUT, FIC-802.Inhibit
FFIC-801.ActiveRatio, HighRatio_GT.IN1
AL801_HighRatio_SP, HighRatio_GT.IN2
HighRatio_GT.OUT, HighRatio_TON.IN
HighRatio_TON.Q, AL801_HighRatio_Alarm
FFIC-801.ActiveRatio, LowRatio_LT.IN1
AL802_LowRatio_SP, LowRatio_LT.IN2
LowRatio_LT.OUT, AL802_LowRatio_Alarm
FFIC-801.SlaveSP, FIC802_AirFlow_SP_FromRatio
FFIC-801.ActiveRatio, FFIC801_ActiveAirToGasRatio
FT-801.PV, FT801_BFG_Flow_PV
FT-802.PV, FT802_Air_Flow_PV
PT-801.PV, PT801_BFG_Pressure_PV
FT-801.General_Fault, AL803_FT801_Fault_Alarm
PT-801.General_Fault, AL804_PT801_Fault_Alarm

* Parameter Data Connections *
6.25, FT-801.Scaling_Slope
-25.0, FT-801.Scaling_Offset
100.0, FT-801.PV_Low
5000.0, FT-801.PV_High
6.25, FT-802.Scaling_Slope
-25.0, FT-802.Scaling_Offset
0.0, FT-802.PV_Low
6000.0, FT-802.PV_High
6.25, PT-801.Scaling_Slope
-25.0, PT-801.Scaling_Offset
0.5, PT-801.PV_Low
2.0, PT-801.PV_High
TRUE, FT-801.Alarm_Enable
TRUE, FT-802.Alarm_Enable
TRUE, PT-801.Alarm_Enable
TRUE, AL-801.Alarm_Enable
TRUE, AL-802.Alarm_Enable
2.5, FFIC-801.RatioSP
0.0, FFIC-801.MV_MIN
6000.0, FFIC-801.MV_MAX
0.0, FFIC-801.Bias
0.0, FFIC-801.TrimKp
T#0s, FFIC-801.TrimTi
TRUE, FFIC-801.Auto
TRUE, FIC-802.AUTO
0.0, FIC-802.MV_MIN
100.0, FIC-802.MV_MAX
0.0, FIC-802.PV_Low
6000.0, FIC-802.PV_High
50.0, FIC-802.X0
50.0, FV-802.Manual_Position
3.0, AL801_HighRatio_SP
2.0, AL802_LowRatio_SP
T#5s, HighRatio_TON.PT
```

---


