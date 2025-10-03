# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 04:05:49

## Step 1: contextgen1-sensors
**Time:** 04:05:49

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
**Time:** 04:06:12

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
**Time:** 04:06:24

### Output:
```
*** Available Control Strategies ***
Control Strategy | Probability
Ratio Control | 0.98
PID Control | 0.92
OVERRIDE | 0.80

Selected Control Strategy: Ratio Control
Short explanation:
Primary requirement is to compute and maintain a flow ratio (hot blast air to pulverized coal) with a slave PID controlling the valve; interlocks act as overrides but the core logic is ratio control.

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
**Timestamp:** 2025-09-24 04:06:51

## Step 1: openplc-function-blocks-v2
**Time:** 04:06:51

### Output:
```
* Function Blocks *
ANALOG_IN FT-301
ANALOG_IN PT-301
ANALOG_IN TT-301
RATIO_CONTROL FFIC-303
PID_BASIC FIC-302
VALVE_ELECTRIC FV-302
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 04:07:21

### Output:
```
* Function Blocks *
ANALOG_IN FT-301
ANALOG_IN PT-301
ANALOG_IN TT-301
RATIO_CONTROL FFIC-303
PID_BASIC FIC-302
VALVE_ELECTRIC FV-302
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 04:07:51

### Output:
```
* Functions *
ADD RatioBias_Add_ADD
MIN RatioUpperLimit_MIN
MAX RatioClamp_MAX
LT LowFlow_LT_LT
SEL LowFlowSel_SEL

* Block-to-Block Connections *
FT-301.PV, FFIC-303.PrimaryPV
RatioBias_Add_ADD.OUT, RatioUpperLimit_MIN.IN2
RatioUpperLimit_MIN.OUT, RatioClamp_MAX.IN2
RatioClamp_MAX.OUT, FFIC-303.RatioSP
FT-301.PV, LowFlow_LT_LT.IN1
LowFlow_LT_LT.OUT, LowFlowSel_SEL.G
FFIC-303.SlaveSP, LowFlowSel_SEL.IN0
LowFlowSel_SEL.OUT, FIC-302.SP
FIC-302.XOUT, FV-302.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 04:09:03

### Output:
```
* Functions * 
OR FT301_RangeFail_OR
OR PT301_RangeFail_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR ESD_Close_OR

* Data Connections *
FT-301.Low_Alarm, FT301_RangeFail_OR.IN1
FT-301.High_Alarm, FT301_RangeFail_OR.IN2
PT-301.Low_Alarm, PT301_RangeFail_OR.IN1
PT-301.High_Alarm, PT301_RangeFail_OR.IN2
FT301_RangeFail_OR.OUT, RatioInhibit1_OR.IN1
TT-301.Low_Alarm, RatioInhibit1_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit2_OR.IN1
PT301_RangeFail_OR.OUT, RatioInhibit2_OR.IN2
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN1
FT-301.General_Fault, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, FFIC-303.Inhibit
TT-301.Low_Alarm, ESD_Close_OR.IN1
PT-301.High_Alarm, ESD_Close_OR.IN2
ESD_Close_OR.OUT, FIC-302.Inhibit
ESD_Close_OR.OUT, FV-302.Inhibit

* Parameter Data Connections *
100, FT-301.PV_Low
5000, FT-301.PV_High
TRUE, FT-301.Alarm_Enable
900, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.5, PT-301.PV_Low
2.5, PT-301.PV_High
TRUE, PT-301.Alarm_Enable
9000, FIC-302.PV_High
200, FIC-302.PV_Low
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 04:10:18

### Output:
```
* Parameter Data Connections *
5000.0, FT-301.PV_High
100.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
2.5, PT-301.PV_High
1.5, PT-301.PV_Low
TRUE, PT-301.Alarm_Enable
900.0, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.8, RatioBias_Add_ADD.IN1
0.0, RatioBias_Add_ADD.IN2
2.0, RatioUpperLimit_MIN.IN1
1.5, RatioClamp_MAX.IN1
100.0, LowFlow_LT_LT.IN2
200.0, LowFlowSel_SEL.IN1
TRUE, FFIC-303.Auto
0.0, FFIC-303.Bias
0.0, FFIC-303.MV_MIN
9000.0, FFIC-303.MV_MAX
1000.0, FFIC-303.ManOut
TRUE, FIC-302.AUTO
0.0, FIC-302.MV_MIN
100.0, FIC-302.MV_MAX
9000.0, FIC-302.PV_High
200.0, FIC-302.PV_Low
FALSE, FV-302.Manual_Mode
0.0, FV-302.Manual_Position
100.0, FV-302.Open_Limit
0.0, FV-302.Close_Limit
T#10s, FV-302.Timeout
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 04:12:18

### Output:
```
* Parameter Data Connections *
5000.0, FT-301.PV_High
100.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
2.5, PT-301.PV_High
1.5, PT-301.PV_Low
TRUE, PT-301.Alarm_Enable
900.0, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.8, RatioBias_Add_ADD.IN1
0.0, RatioBias_Add_ADD.IN2
2.0, RatioUpperLimit_MIN.IN1
1.5, RatioClamp_MAX.IN1
100.0, LowFlow_LT_LT.IN2
200.0, LowFlowSel_SEL.IN1
TRUE, FFIC-303.Auto
0.0, FFIC-303.Bias
200.0, FFIC-303.MV_MIN
9000.0, FFIC-303.MV_MAX
1000.0, FFIC-303.ManOut
TRUE, FIC-302.AUTO
0.0, FIC-302.MV_MIN
100.0, FIC-302.MV_MAX
9000.0, FIC-302.PV_High
200.0, FIC-302.PV_Low
FALSE, FV-302.Manual_Mode
0.0, FV-302.Manual_Position
100.0, FV-302.Open_Limit
0.0, FV-302.Close_Limit
T#10s, FV-302.Timeout
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 04:14:17

### Output:
```
* Variables *
REAL FFIC303_HotBlastAirFlow_SP
REAL FT301_PulverizedCoalFlow_PV
REAL PT301_FurnacePressure_PV
REAL TT301_HotBlastAirTemperature_PV

* Data Connections *
FFIC-303.SlaveSP, FFIC303_HotBlastAirFlow_SP
FT-301.PV, FT301_PulverizedCoalFlow_PV
PT-301.PV, PT301_FurnacePressure_PV
TT-301.PV, TT301_HotBlastAirTemperature_PV
```

---

## Step 8: openplc-rule-checks
**Time:** 04:14:48

### Output:
```
* Function Blocks *
ANALOG_IN FT-301
ANALOG_IN PT-301
ANALOG_IN TT-301
RATIO_CONTROL FFIC-303
PID_BASIC FIC-302
VALVE_ELECTRIC FV-302

* Variables *
REAL FFIC303_HotBlastAirFlow_SP
REAL FT301_PulverizedCoalFlow_PV
REAL PT301_FurnacePressure_PV
REAL TT301_HotBlastAirTemperature_PV
REAL HotBlastAirFlow_PV

* Functions *
ADD RatioBias_Add_ADD
MIN RatioUpperLimit_MIN
MAX RatioClamp_MAX
LT LowFlow_LT_LT
SEL LowFlowSel_SEL
SEL RangeFailSel_SEL
OR FT301_RangeFail_OR
OR PT301_RangeFail_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR ESD_Close_OR

* Data Connections *
FT-301.PV, FFIC-303.PrimaryPV
RatioBias_Add_ADD.OUT, RatioUpperLimit_MIN.IN2
RatioUpperLimit_MIN.OUT, RatioClamp_MAX.IN2
RatioClamp_MAX.OUT, FFIC-303.RatioSP
FT-301.PV, LowFlow_LT_LT.IN1
LowFlow_LT_LT.OUT, LowFlowSel_SEL.G
FFIC-303.SlaveSP, LowFlowSel_SEL.IN0
LowFlowSel_SEL.OUT, RangeFailSel_SEL.IN0
FT301_RangeFail_OR.OUT, RangeFailSel_SEL.G
RangeFailSel_SEL.OUT, FIC-302.SP
HotBlastAirFlow_PV, FFIC-303.SecondaryPV
HotBlastAirFlow_PV, FIC-302.PV
FIC-302.XOUT, FV-302.Control_Signal
FT-301.Low_Alarm, FT301_RangeFail_OR.IN1
FT-301.High_Alarm, FT301_RangeFail_OR.IN2
PT-301.Low_Alarm, PT301_RangeFail_OR.IN1
PT-301.High_Alarm, PT301_RangeFail_OR.IN2
FT301_RangeFail_OR.OUT, RatioInhibit1_OR.IN1
TT-301.Low_Alarm, RatioInhibit1_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit2_OR.IN1
PT301_RangeFail_OR.OUT, RatioInhibit2_OR.IN2
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN1
FT-301.General_Fault, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, FFIC-303.Inhibit
TT-301.Low_Alarm, ESD_Close_OR.IN1
PT-301.High_Alarm, ESD_Close_OR.IN2
ESD_Close_OR.OUT, FIC-302.Inhibit
ESD_Close_OR.OUT, FV-302.Inhibit
FFIC-303.SlaveSP, FFIC303_HotBlastAirFlow_SP
FT-301.PV, FT301_PulverizedCoalFlow_PV
PT-301.PV, PT301_FurnacePressure_PV
TT-301.PV, TT301_HotBlastAirTemperature_PV

* Parameter Data Connections *
5000.0, FT-301.PV_High
100.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
2.5, PT-301.PV_High
1.5, PT-301.PV_Low
TRUE, PT-301.Alarm_Enable
900.0, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.8, RatioBias_Add_ADD.IN1
0.0, RatioBias_Add_ADD.IN2
2.0, RatioUpperLimit_MIN.IN1
1.5, RatioClamp_MAX.IN1
100.0, LowFlow_LT_LT.IN2
200.0, LowFlowSel_SEL.IN1
500.0, RangeFailSel_SEL.IN1
TRUE, FFIC-303.Auto
0.0, FFIC-303.Bias
200.0, FFIC-303.MV_MIN
9000.0, FFIC-303.MV_MAX
1000.0, FFIC-303.ManOut
TRUE, FIC-302.AUTO
0.0, FIC-302.MV_MIN
100.0, FIC-302.MV_MAX
9000.0, FIC-302.PV_High
200.0, FIC-302.PV_Low
FALSE, FV-302.Manual_Mode
0.0, FV-302.Manual_Position
100.0, FV-302.Open_Limit
0.0, FV-302.Close_Limit
T#10s, FV-302.Timeout
```

---

## Step 9: openplc-rule-checks2
**Time:** 04:16:20

### Output:
```
* Function Blocks *
ANALOG_IN FT-301
ANALOG_IN PT-301
ANALOG_IN TT-301
RATIO_CONTROL FFIC-303
PID_BASIC FIC-302
VALVE_ELECTRIC FV-302

* Variables *
REAL FFIC303_HotBlastAirFlow_SP
REAL FT301_PulverizedCoalFlow_PV
REAL PT301_FurnacePressure_PV
REAL TT301_HotBlastAirTemperature_PV
REAL HotBlastAirFlow_PV

* Functions *
ADD RatioBias_Add_ADD
MIN RatioUpperLimit_MIN
MAX RatioClamp_MAX
LT LowFlow_LT_LT
SEL LowFlowSel_SEL
SEL RangeFailSel_SEL
OR FT301_RangeFail_OR
OR PT301_RangeFail_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR ESD_Close_OR

* Data Connections *
FT-301.PV, FFIC-303.PrimaryPV
RatioBias_Add_ADD.OUT, RatioUpperLimit_MIN.IN2
RatioUpperLimit_MIN.OUT, RatioClamp_MAX.IN2
RatioClamp_MAX.OUT, FFIC-303.RatioSP
FT-301.PV, LowFlow_LT_LT.IN1
LowFlow_LT_LT.OUT, LowFlowSel_SEL.G
FFIC-303.SlaveSP, LowFlowSel_SEL.IN0
LowFlowSel_SEL.OUT, RangeFailSel_SEL.IN0
FT301_RangeFail_OR.OUT, RangeFailSel_SEL.G
RangeFailSel_SEL.OUT, FIC-302.SP
HotBlastAirFlow_PV, FFIC-303.SecondaryPV
HotBlastAirFlow_PV, FIC-302.PV
FIC-302.XOUT, FV-302.Control_Signal
FT-301.Low_Alarm, FT301_RangeFail_OR.IN1
FT-301.High_Alarm, FT301_RangeFail_OR.IN2
PT-301.Low_Alarm, PT301_RangeFail_OR.IN1
PT-301.High_Alarm, PT301_RangeFail_OR.IN2
FT301_RangeFail_OR.OUT, RatioInhibit1_OR.IN1
TT-301.Low_Alarm, RatioInhibit1_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit2_OR.IN1
PT301_RangeFail_OR.OUT, RatioInhibit2_OR.IN2
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN1
FT-301.General_Fault, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, FFIC-303.Inhibit
TT-301.Low_Alarm, ESD_Close_OR.IN1
PT-301.High_Alarm, ESD_Close_OR.IN2
ESD_Close_OR.OUT, FIC-302.Inhibit
ESD_Close_OR.OUT, FV-302.Inhibit
FFIC-303.SlaveSP, FFIC303_HotBlastAirFlow_SP
FT-301.PV, FT301_PulverizedCoalFlow_PV
PT-301.PV, PT301_FurnacePressure_PV
TT-301.PV, TT301_HotBlastAirTemperature_PV

* Parameter Data Connections *
5000.0, FT-301.PV_High
100.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
2.5, PT-301.PV_High
1.5, PT-301.PV_Low
TRUE, PT-301.Alarm_Enable
900.0, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.8, RatioBias_Add_ADD.IN1
0.0, RatioBias_Add_ADD.IN2
2.0, RatioUpperLimit_MIN.IN1
1.5, RatioClamp_MAX.IN1
100.0, LowFlow_LT_LT.IN2
200.0, LowFlowSel_SEL.IN1
500.0, RangeFailSel_SEL.IN1
TRUE, FFIC-303.Auto
0.0, FFIC-303.Bias
200.0, FFIC-303.MV_MIN
9000.0, FFIC-303.MV_MAX
1000.0, FFIC-303.ManOut
TRUE, FIC-302.AUTO
0.0, FIC-302.MV_MIN
100.0, FIC-302.MV_MAX
9000.0, FIC-302.PV_High
200.0, FIC-302.PV_Low
FALSE, FV-302.Manual_Mode
0.0, FV-302.Manual_Position
100.0, FV-302.Open_Limit
0.0, FV-302.Close_Limit
T#10s, FV-302.Timeout
```

---

## Step 10: append_two_inputs
**Time:** 04:16:39

### Output:
```
* Function Blocks *
ANALOG_IN FT-301
ANALOG_IN PT-301
ANALOG_IN TT-301
RATIO_CONTROL FFIC-303
PID_BASIC FIC-302
VALVE_ELECTRIC FV-302

* Variables *
REAL FFIC303_HotBlastAirFlow_SP
REAL FT301_PulverizedCoalFlow_PV
REAL PT301_FurnacePressure_PV
REAL TT301_HotBlastAirTemperature_PV
REAL HotBlastAirFlow_PV

* Functions *
ADD RatioBias_Add_ADD
MIN RatioUpperLimit_MIN
MAX RatioClamp_MAX
LT LowFlow_LT_LT
SEL LowFlowSel_SEL
SEL RangeFailSel_SEL
OR FT301_RangeFail_OR
OR PT301_RangeFail_OR
OR RatioInhibit1_OR
OR RatioInhibit2_OR
OR RatioInhibit3_OR
OR ESD_Close_OR

* Data Connections *
FT-301.PV, FFIC-303.PrimaryPV
RatioBias_Add_ADD.OUT, RatioUpperLimit_MIN.IN2
RatioUpperLimit_MIN.OUT, RatioClamp_MAX.IN2
RatioClamp_MAX.OUT, FFIC-303.RatioSP
FT-301.PV, LowFlow_LT_LT.IN1
LowFlow_LT_LT.OUT, LowFlowSel_SEL.G
FFIC-303.SlaveSP, LowFlowSel_SEL.IN0
LowFlowSel_SEL.OUT, RangeFailSel_SEL.IN0
FT301_RangeFail_OR.OUT, RangeFailSel_SEL.G
RangeFailSel_SEL.OUT, FIC-302.SP
HotBlastAirFlow_PV, FFIC-303.SecondaryPV
HotBlastAirFlow_PV, FIC-302.PV
FIC-302.XOUT, FV-302.Control_Signal
FT-301.Low_Alarm, FT301_RangeFail_OR.IN1
FT-301.High_Alarm, FT301_RangeFail_OR.IN2
PT-301.Low_Alarm, PT301_RangeFail_OR.IN1
PT-301.High_Alarm, PT301_RangeFail_OR.IN2
FT301_RangeFail_OR.OUT, RatioInhibit1_OR.IN1
TT-301.Low_Alarm, RatioInhibit1_OR.IN2
RatioInhibit1_OR.OUT, RatioInhibit2_OR.IN1
PT301_RangeFail_OR.OUT, RatioInhibit2_OR.IN2
RatioInhibit2_OR.OUT, RatioInhibit3_OR.IN1
FT-301.General_Fault, RatioInhibit3_OR.IN2
RatioInhibit3_OR.OUT, FFIC-303.Inhibit
TT-301.Low_Alarm, ESD_Close_OR.IN1
PT-301.High_Alarm, ESD_Close_OR.IN2
ESD_Close_OR.OUT, FIC-302.Inhibit
ESD_Close_OR.OUT, FV-302.Inhibit
FFIC-303.SlaveSP, FFIC303_HotBlastAirFlow_SP
FT-301.PV, FT301_PulverizedCoalFlow_PV
PT-301.PV, PT301_FurnacePressure_PV
TT-301.PV, TT301_HotBlastAirTemperature_PV

* Parameter Data Connections *
5000.0, FT-301.PV_High
100.0, FT-301.PV_Low
TRUE, FT-301.Alarm_Enable
2.5, PT-301.PV_High
1.5, PT-301.PV_Low
TRUE, PT-301.Alarm_Enable
900.0, TT-301.PV_Low
TRUE, TT-301.Alarm_Enable
1.8, RatioBias_Add_ADD.IN1
0.0, RatioBias_Add_ADD.IN2
2.0, RatioUpperLimit_MIN.IN1
1.5, RatioClamp_MAX.IN1
100.0, LowFlow_LT_LT.IN2
200.0, LowFlowSel_SEL.IN1
500.0, RangeFailSel_SEL.IN1
TRUE, FFIC-303.Auto
0.0, FFIC-303.Bias
200.0, FFIC-303.MV_MIN
9000.0, FFIC-303.MV_MAX
1000.0, FFIC-303.ManOut
TRUE, FIC-302.AUTO
0.0, FIC-302.MV_MIN
100.0, FIC-302.MV_MAX
9000.0, FIC-302.PV_High
200.0, FIC-302.PV_Low
FALSE, FV-302.Manual_Mode
0.0, FV-302.Manual_Position
100.0, FV-302.Open_Limit
0.0, FV-302.Close_Limit
T#10s, FV-302.Timeout
```

---


