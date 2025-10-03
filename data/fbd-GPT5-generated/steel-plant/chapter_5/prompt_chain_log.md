# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 04:17:25

## Step 1: contextgen1-sensors
**Time:** 04:17:25

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
**Time:** 04:17:43

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
**Time:** 04:18:03

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
| VOTING | 0.98 |
| PID Control | 0.75 |
| OVERRIDE | 0.65 |

Selected Control Strategy: VOTING
Short explanation: Redundant sensor voting (2oo3 with degradation to 1oo2) is central to BOF operation, determining valid temperature signals and interlocks that drive lance control and alarms.

* Control Strategy *
VOTING
** Description ** 
The system includes multiple identical sensors (e.g., three temperature transmitters), a voting logic unit, and an actuator. Each sensor provides an analog input to the voting logic unit, which compares the signals. Based on a predefined logic (e.g., 2-out-of-3 agreement), the unit selects the valid signal. This selected signal is then used to drive the actuator or trigger alarms, ensuring reliable operation even if one sensor fails.
** Intended Block-to-Block Connections Types **
ANALOG_IN1.PV, VOTING_ANALOG.Input1
ANALOG_IN2.PV, VOTING_ANALOG.Input2
ANALOG_IN3.PV, VOTING_ANALOG.Input3
"Median", VOTING_ANALOG.Voting_Scheme
VOTING_ANALOG.Voted_Output, PID_BASIC.PV

*** Available Function Block Types ***
VOTING_ANALOG
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of the block's purpose
Input,Input1,REAL,First analog input.
Input,Input2,REAL,Second analog input.
Input,Input3,REAL,Third analog input (for 2oo3).
Input,Deviation_Limit,REAL,Maximum allowed deviation between inputs for agreement.
Input,Voting_Scheme,ENUM,Selection of voting scheme (e.g. 2oo3 or Median or Average).
Input,EnableAlarm,BOOL,Enables or disables alarm monitoring.
Input,Inhibit,BOOL,Inhibits voting functionality and can receive alarm signals.
Output,Voted_Output,REAL,The validated analog output value.
Output,Sensor1_Fault,BOOL,Indicates if Input1 is deemed faulty.
Output,Sensor2_Fault,BOOL,Indicates if Input2 is deemed faulty.
Output,Sensor3_Fault,BOOL,Indicates if Input3 is deemed faulty.
Output,Alarm_Voting_Error,BOOL,Indicates a disagreement among inputs or insufficient healthy sensors.
Output,Healthy_Sensors_Count,INT,Number of currently healthy sensors.

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
**Timestamp:** 2025-09-24 04:18:36

## Step 1: openplc-function-blocks-v2
**Time:** 04:18:36

### Output:
```
* Function Blocks *
ANALOG_IN FT-401
ANALOG_IN PT-401A
ANALOG_IN PT-401B
ANALOG_IN PT-401C
ANALOG_IN TT-401A
ANALOG_IN TT-401B
ANALOG_IN TT-401C
VOTING_ANALOG TT-401-V
VALVE_ELECTRIC BOF-402
BOOL_IN I-401
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 04:19:36

### Output:
```
* Function Block List *
* Function Blocks *
ANALOG_IN FT-401
ANALOG_IN PT-401A
ANALOG_IN PT-401B
ANALOG_IN PT-401C
ANALOG_IN TT-401A
ANALOG_IN TT-401B
ANALOG_IN TT-401C
VOTING_ANALOG TT-401-V
VALVE_ELECTRIC BOF-402
BOOL_IN I-401
ANALOG_IN TT-401
VOTING_ANALOG PT-401-V
BOOL_IN DA-401
BOOL_IN FA-401
BOOL_IN MA-401
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 04:20:43

### Output:
```
* Functions *

* Block-to-Block Connections *
TT-401A.PV, TT-401-V.Input1
TT-401B.PV, TT-401-V.Input2
TT-401C.PV, TT-401-V.Input3
TT-401-V.Voted_Output, BOF-402.Control_Signal
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 04:21:16

### Output:
```
* Functions * 
AND TT401_1450_A_B_AND
AND TT401_1450_A_C_AND
AND TT401_1450_B_C_AND
OR TT401_1450_2oo3_OR
OR TT401_1450_2oo3_stage2_OR
NOT TT401_1450_2oo3_NOT
OR PTA_OutOfRange_OR
NOT PTA_InRange_NOT
OR PTB_OutOfRange_OR
NOT PTB_InRange_NOT
OR PTC_OutOfRange_OR
NOT PTC_InRange_NOT
AND PT_InRange_AB_AND
AND PT_InRange_AC_AND
AND PT_InRange_BC_AND
OR PT_2oo3_InRange_OR
OR PT_2oo3_InRange_stage2_OR
NOT PT_2oo3_InRange_NOT
OR Faults_TT_AB_OR
OR Faults_TT_ABC_OR
OR Faults_PT_AB_OR
OR Faults_PT_ABC_OR
OR Faults_All_TT_PT_OR
OR Faults_All_OR
NOT TT401A_Healthy_NOT
NOT TT401B_Healthy_NOT
NOT TT401C_Healthy_NOT
AND TT_Healthy_AB_AND
AND TT_AllHealthy_AND
NOT TT_Startup_NotOk_NOT
OR Inhibit_TempPress_OR
OR Inhibit_AddFlow_OR
OR Inhibit_AddDA_OR
OR Inhibit_AddFA_OR
OR Inhibit_AddStartup_OR

* Data Connections *
TT-401A.High_Alarm, TT401_1450_A_B_AND.IN1
TT-401B.High_Alarm, TT401_1450_A_B_AND.IN2
TT-401A.High_Alarm, TT401_1450_A_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_A_C_AND.IN2
TT-401B.High_Alarm, TT401_1450_B_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_B_C_AND.IN2
TT401_1450_A_B_AND.OUT, TT401_1450_2oo3_OR.IN1
TT401_1450_A_C_AND.OUT, TT401_1450_2oo3_OR.IN2
TT401_1450_2oo3_OR.OUT, TT401_1450_2oo3_stage2_OR.IN1
TT401_1450_B_C_AND.OUT, TT401_1450_2oo3_stage2_OR.IN2
TT401_1450_2oo3_stage2_OR.OUT, TT401_1450_2oo3_NOT.IN

PT-401A.High_Alarm, PTA_OutOfRange_OR.IN1
PT-401A.Low_Alarm, PTA_OutOfRange_OR.IN2
PTA_OutOfRange_OR.OUT, PTA_InRange_NOT.IN
PT-401B.High_Alarm, PTB_OutOfRange_OR.IN1
PT-401B.Low_Alarm, PTB_OutOfRange_OR.IN2
PTB_OutOfRange_OR.OUT, PTB_InRange_NOT.IN
PT-401C.High_Alarm, PTC_OutOfRange_OR.IN1
PT-401C.Low_Alarm, PTC_OutOfRange_OR.IN2
PTC_OutOfRange_OR.OUT, PTC_InRange_NOT.IN
PTA_InRange_NOT.OUT, PT_InRange_AB_AND.IN1
PTB_InRange_NOT.OUT, PT_InRange_AB_AND.IN2
PTA_InRange_NOT.OUT, PT_InRange_AC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_AC_AND.IN2
PTB_InRange_NOT.OUT, PT_InRange_BC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_BC_AND.IN2
PT_InRange_AB_AND.OUT, PT_2oo3_InRange_OR.IN1
PT_InRange_AC_AND.OUT, PT_2oo3_InRange_OR.IN2
PT_2oo3_InRange_OR.OUT, PT_2oo3_InRange_stage2_OR.IN1
PT_InRange_BC_AND.OUT, PT_2oo3_InRange_stage2_OR.IN2
PT_2oo3_InRange_stage2_OR.OUT, PT_2oo3_InRange_NOT.IN

TT-401A.General_Fault, Faults_TT_AB_OR.IN1
TT-401B.General_Fault, Faults_TT_AB_OR.IN2
Faults_TT_AB_OR.OUT, Faults_TT_ABC_OR.IN1
TT-401C.General_Fault, Faults_TT_ABC_OR.IN2
PT-401A.General_Fault, Faults_PT_AB_OR.IN1
PT-401B.General_Fault, Faults_PT_AB_OR.IN2
Faults_PT_AB_OR.OUT, Faults_PT_ABC_OR.IN1
PT-401C.General_Fault, Faults_PT_ABC_OR.IN2
Faults_TT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN1
Faults_PT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN2
Faults_All_TT_PT_OR.OUT, Faults_All_OR.IN1
FT-401.General_Fault, Faults_All_OR.IN2
Faults_All_OR.OUT, FA-401.Bool_In

TT-401-V.Alarm_Voting_Error, DA-401.Bool_In

TT-401A.General_Fault, TT401A_Healthy_NOT.IN
TT401A_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN1
TT-401B.General_Fault, TT401B_Healthy_NOT.IN
TT401B_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN2
TT_Healthy_AB_AND.OUT, TT_AllHealthy_AND.IN1
TT-401C.General_Fault, TT401C_Healthy_NOT.IN
TT401C_Healthy_NOT.OUT, TT_AllHealthy_AND.IN2
TT_AllHealthy_AND.OUT, TT_Startup_NotOk_NOT.IN

TT401_1450_2oo3_NOT.OUT, Inhibit_TempPress_OR.IN1
PT_2oo3_InRange_NOT.OUT, Inhibit_TempPress_OR.IN2
Inhibit_TempPress_OR.OUT, Inhibit_AddFlow_OR.IN1
FT-401.Low_Alarm, Inhibit_AddFlow_OR.IN2
Inhibit_AddFlow_OR.OUT, Inhibit_AddDA_OR.IN1
DA-401.Bool_Out, Inhibit_AddDA_OR.IN2
Inhibit_AddDA_OR.OUT, Inhibit_AddFA_OR.IN1
FA-401.Bool_Out, Inhibit_AddFA_OR.IN2
Inhibit_AddFA_OR.OUT, Inhibit_AddStartup_OR.IN1
TT_Startup_NotOk_NOT.OUT, Inhibit_AddStartup_OR.IN2
Inhibit_AddStartup_OR.OUT, I-401.Bool_In

I-401.Bool_Out, BOF-402.Inhibit

* Parameter Data Connections *
1450, TT-401A.PV_High
1450, TT-401B.PV_High
1450, TT-401C.PV_High
90, PT-401A.PV_Low
120, PT-401A.PV_High
90, PT-401B.PV_Low
120, PT-401B.PV_High
90, PT-401C.PV_Low
120, PT-401C.PV_High
500, FT-401.PV_Low
5, TT-401-V.Deviation_Limit
TRUE, TT-401-V.EnableAlarm
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 04:24:13

### Output:
```
* Parameter Data Connections *
0.05, TT-401-V.Deviation_Limit
90.0, PT-401A.PV_Low
120.0, PT-401A.PV_High
90.0, PT-401B.PV_Low
120.0, PT-401B.PV_High
90.0, PT-401C.PV_Low
120.0, PT-401C.PV_High
500.0, FT-401.PV_Low
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 04:25:01

### Output:
```
* Parameter Data Connections *
0.05, TT-401-V.Deviation_Limit
90.0, PT-401A.PV_Low
120.0, PT-401A.PV_High
90.0, PT-401B.PV_Low
120.0, PT-401B.PV_High
90.0, PT-401C.PV_Low
120.0, PT-401C.PV_High
500.0, FT-401.PV_Low
TRUE, TT-401-V.EnableAlarm
2oo3, TT-401-V.Voting_Scheme
1450.0, TT-401A.PV_High
1450.0, TT-401B.PV_High
1450.0, TT-401C.PV_High
TRUE, TT-401A.Alarm_Enable
TRUE, TT-401B.Alarm_Enable
TRUE, TT-401C.Alarm_Enable
TRUE, PT-401A.Alarm_Enable
TRUE, PT-401B.Alarm_Enable
TRUE, PT-401C.Alarm_Enable
TRUE, FT-401.Alarm_Enable
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 04:26:54

### Output:
```
* Variables *
REAL TT_401_V_Voted_Temp
REAL PT_401_V_Voted_Pressure

* Data Connections *
TT-401-V.Voted_Output, TT_401_V_Voted_Temp
PT-401-V.Voted_Output, PT_401_V_Voted_Pressure
```

---

## Step 8: openplc-rule-checks
**Time:** 04:27:34

### Output:
```
* Function Blocks *
ANALOG_IN FT-401
ANALOG_IN PT-401A
ANALOG_IN PT-401B
ANALOG_IN PT-401C
ANALOG_IN TT-401A
ANALOG_IN TT-401B
ANALOG_IN TT-401C
VOTING_ANALOG TT-401-V
VALVE_ELECTRIC BOF-402
BOOL_IN I-401
BOOL_IN DA-401
BOOL_IN FA-401

* Variables *
REAL TT_401_V_Voted_Temp

* Functions *
AND TT401_1450_A_B_AND
AND TT401_1450_A_C_AND
AND TT401_1450_B_C_AND
OR TT401_1450_2oo3_OR
OR TT401_1450_2oo3_stage2_OR
NOT TT401_1450_2oo3_NOT
OR PTA_OutOfRange_OR
NOT PTA_InRange_NOT
OR PTB_OutOfRange_OR
NOT PTB_InRange_NOT
OR PTC_OutOfRange_OR
NOT PTC_InRange_NOT
AND PT_InRange_AB_AND
AND PT_InRange_AC_AND
AND PT_InRange_BC_AND
OR PT_2oo3_InRange_OR
OR PT_2oo3_InRange_stage2_OR
NOT PT_2oo3_InRange_NOT
OR Faults_TT_AB_OR
OR Faults_TT_ABC_OR
OR Faults_PT_AB_OR
OR Faults_PT_ABC_OR
OR Faults_All_TT_PT_OR
OR Faults_All_OR
NOT TT401A_Healthy_NOT
NOT TT401B_Healthy_NOT
NOT TT401C_Healthy_NOT
AND TT_Healthy_AB_AND
AND TT_AllHealthy_AND
NOT TT_Startup_NotOk_NOT
OR Inhibit_TempPress_OR
OR Inhibit_AddFlow_OR
OR Inhibit_AddDA_OR
OR Inhibit_AddFA_OR
OR Inhibit_AddStartup_OR

* Data Connections * 
TT-401A.PV, TT-401-V.Input1
TT-401B.PV, TT-401-V.Input2
TT-401C.PV, TT-401-V.Input3
TT-401-V.Voted_Output, BOF-402.Control_Signal

TT-401A.High_Alarm, TT401_1450_A_B_AND.IN1
TT-401B.High_Alarm, TT401_1450_A_B_AND.IN2
TT-401A.High_Alarm, TT401_1450_A_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_A_C_AND.IN2
TT-401B.High_Alarm, TT401_1450_B_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_B_C_AND.IN2
TT401_1450_A_B_AND.OUT, TT401_1450_2oo3_OR.IN1
TT401_1450_A_C_AND.OUT, TT401_1450_2oo3_OR.IN2
TT401_1450_2oo3_OR.OUT, TT401_1450_2oo3_stage2_OR.IN1
TT401_1450_B_C_AND.OUT, TT401_1450_2oo3_stage2_OR.IN2
TT401_1450_2oo3_stage2_OR.OUT, TT401_1450_2oo3_NOT.IN

PT-401A.High_Alarm, PTA_OutOfRange_OR.IN1
PT-401A.Low_Alarm, PTA_OutOfRange_OR.IN2
PTA_OutOfRange_OR.OUT, PTA_InRange_NOT.IN
PT-401B.High_Alarm, PTB_OutOfRange_OR.IN1
PT-401B.Low_Alarm, PTB_OutOfRange_OR.IN2
PTB_OutOfRange_OR.OUT, PTB_InRange_NOT.IN
PT-401C.High_Alarm, PTC_OutOfRange_OR.IN1
PT-401C.Low_Alarm, PTC_OutOfRange_OR.IN2
PTC_OutOfRange_OR.OUT, PTC_InRange_NOT.IN
PTA_InRange_NOT.OUT, PT_InRange_AB_AND.IN1
PTB_InRange_NOT.OUT, PT_InRange_AB_AND.IN2
PTA_InRange_NOT.OUT, PT_InRange_AC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_AC_AND.IN2
PTB_InRange_NOT.OUT, PT_InRange_BC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_BC_AND.IN2
PT_InRange_AB_AND.OUT, PT_2oo3_InRange_OR.IN1
PT_InRange_AC_AND.OUT, PT_2oo3_InRange_OR.IN2
PT_2oo3_InRange_OR.OUT, PT_2oo3_InRange_stage2_OR.IN1
PT_InRange_BC_AND.OUT, PT_2oo3_InRange_stage2_OR.IN2
PT_2oo3_InRange_stage2_OR.OUT, PT_2oo3_InRange_NOT.IN

TT-401A.General_Fault, Faults_TT_AB_OR.IN1
TT-401B.General_Fault, Faults_TT_AB_OR.IN2
Faults_TT_AB_OR.OUT, Faults_TT_ABC_OR.IN1
TT-401C.General_Fault, Faults_TT_ABC_OR.IN2
PT-401A.General_Fault, Faults_PT_AB_OR.IN1
PT-401B.General_Fault, Faults_PT_AB_OR.IN2
Faults_PT_AB_OR.OUT, Faults_PT_ABC_OR.IN1
PT-401C.General_Fault, Faults_PT_ABC_OR.IN2
Faults_TT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN1
Faults_PT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN2
Faults_All_TT_PT_OR.OUT, Faults_All_OR.IN1
FT-401.General_Fault, Faults_All_OR.IN2
Faults_All_OR.OUT, FA-401.Bool_In

TT-401-V.Alarm_Voting_Error, DA-401.Bool_In

TT-401A.General_Fault, TT401A_Healthy_NOT.IN
TT401A_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN1
TT-401B.General_Fault, TT401B_Healthy_NOT.IN
TT401B_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN2
TT_Healthy_AB_AND.OUT, TT_AllHealthy_AND.IN1
TT-401C.General_Fault, TT401C_Healthy_NOT.IN
TT401C_Healthy_NOT.OUT, TT_AllHealthy_AND.IN2
TT_AllHealthy_AND.OUT, TT_Startup_NotOk_NOT.IN

TT401_1450_2oo3_NOT.OUT, Inhibit_TempPress_OR.IN1
PT_2oo3_InRange_NOT.OUT, Inhibit_TempPress_OR.IN2
Inhibit_TempPress_OR.OUT, Inhibit_AddFlow_OR.IN1
FT-401.Low_Alarm, Inhibit_AddFlow_OR.IN2
Inhibit_AddFlow_OR.OUT, Inhibit_AddDA_OR.IN1
DA-401.Bool_Out, Inhibit_AddDA_OR.IN2
Inhibit_AddDA_OR.OUT, Inhibit_AddFA_OR.IN1
FA-401.Bool_Out, Inhibit_AddFA_OR.IN2
Inhibit_AddFA_OR.OUT, Inhibit_AddStartup_OR.IN1
TT_Startup_NotOk_NOT.OUT, Inhibit_AddStartup_OR.IN2
Inhibit_AddStartup_OR.OUT, I-401.Bool_In

I-401.Bool_Out, BOF-402.Inhibit

TT-401-V.Voted_Output, TT_401_V_Voted_Temp

* Parameter Data Connections *
0.05, TT-401-V.Deviation_Limit
2oo3, TT-401-V.Voting_Scheme
TRUE, TT-401-V.EnableAlarm
1450.0, TT-401A.PV_High
1450.0, TT-401B.PV_High
1450.0, TT-401C.PV_High
90.0, PT-401A.PV_Low
120.0, PT-401A.PV_High
90.0, PT-401B.PV_Low
120.0, PT-401B.PV_High
90.0, PT-401C.PV_Low
120.0, PT-401C.PV_High
500.0, FT-401.PV_Low
TRUE, TT-401A.Alarm_Enable
TRUE, TT-401B.Alarm_Enable
TRUE, TT-401C.Alarm_Enable
TRUE, PT-401A.Alarm_Enable
TRUE, PT-401B.Alarm_Enable
TRUE, PT-401C.Alarm_Enable
TRUE, FT-401.Alarm_Enable
```

---

## Step 9: openplc-rule-checks2
**Time:** 04:29:27

### Output:
```
* Function Blocks *
ANALOG_IN FT-401
ANALOG_IN PT-401A
ANALOG_IN PT-401B
ANALOG_IN PT-401C
ANALOG_IN TT-401A
ANALOG_IN TT-401B
ANALOG_IN TT-401C
VOTING_ANALOG TT-401-V
VALVE_ELECTRIC BOF-402
BOOL_IN I-401
BOOL_IN DA-401
BOOL_IN FA-401

* Variables *
REAL TT_401_V_Voted_Temp

* Functions *
AND TT401_1450_A_B_AND
AND TT401_1450_A_C_AND
AND TT401_1450_B_C_AND
OR TT401_1450_2oo3_OR
OR TT401_1450_2oo3_stage2_OR
NOT TT401_1450_2oo3_NOT
OR PTA_OutOfRange_OR
NOT PTA_InRange_NOT
OR PTB_OutOfRange_OR
NOT PTB_InRange_NOT
OR PTC_OutOfRange_OR
NOT PTC_InRange_NOT
AND PT_InRange_AB_AND
AND PT_InRange_AC_AND
AND PT_InRange_BC_AND
OR PT_2oo3_InRange_OR
OR PT_2oo3_InRange_stage2_OR
NOT PT_2oo3_InRange_NOT
OR Faults_TT_AB_OR
OR Faults_TT_ABC_OR
OR Faults_PT_AB_OR
OR Faults_PT_ABC_OR
OR Faults_All_TT_PT_OR
OR Faults_All_OR
NOT TT401A_Healthy_NOT
NOT TT401B_Healthy_NOT
NOT TT401C_Healthy_NOT
AND TT_Healthy_AB_AND
AND TT_AllHealthy_AND
NOT TT_Startup_NotOk_NOT
OR Inhibit_TempPress_OR
OR Inhibit_AddFlow_OR
OR Inhibit_AddDA_OR
OR Inhibit_AddFA_OR
OR Inhibit_AddStartup_OR

* Data Connections * 
TT-401A.PV, TT-401-V.Input1
TT-401B.PV, TT-401-V.Input2
TT-401C.PV, TT-401-V.Input3
TT-401-V.Voted_Output, BOF-402.Control_Signal

TT-401A.High_Alarm, TT401_1450_A_B_AND.IN1
TT-401B.High_Alarm, TT401_1450_A_B_AND.IN2
TT-401A.High_Alarm, TT401_1450_A_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_A_C_AND.IN2
TT-401B.High_Alarm, TT401_1450_B_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_B_C_AND.IN2
TT401_1450_A_B_AND.OUT, TT401_1450_2oo3_OR.IN1
TT401_1450_A_C_AND.OUT, TT401_1450_2oo3_OR.IN2
TT401_1450_2oo3_OR.OUT, TT401_1450_2oo3_stage2_OR.IN1
TT401_1450_B_C_AND.OUT, TT401_1450_2oo3_stage2_OR.IN2
TT401_1450_2oo3_stage2_OR.OUT, TT401_1450_2oo3_NOT.IN

PT-401A.High_Alarm, PTA_OutOfRange_OR.IN1
PT-401A.Low_Alarm, PTA_OutOfRange_OR.IN2
PTA_OutOfRange_OR.OUT, PTA_InRange_NOT.IN
PT-401B.High_Alarm, PTB_OutOfRange_OR.IN1
PT-401B.Low_Alarm, PTB_OutOfRange_OR.IN2
PTB_OutOfRange_OR.OUT, PTB_InRange_NOT.IN
PT-401C.High_Alarm, PTC_OutOfRange_OR.IN1
PT-401C.Low_Alarm, PTC_OutOfRange_OR.IN2
PTC_OutOfRange_OR.OUT, PTC_InRange_NOT.IN
PTA_InRange_NOT.OUT, PT_InRange_AB_AND.IN1
PTB_InRange_NOT.OUT, PT_InRange_AB_AND.IN2
PTA_InRange_NOT.OUT, PT_InRange_AC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_AC_AND.IN2
PTB_InRange_NOT.OUT, PT_InRange_BC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_BC_AND.IN2
PT_InRange_AB_AND.OUT, PT_2oo3_InRange_OR.IN1
PT_InRange_AC_AND.OUT, PT_2oo3_InRange_OR.IN2
PT_2oo3_InRange_OR.OUT, PT_2oo3_InRange_stage2_OR.IN1
PT_InRange_BC_AND.OUT, PT_2oo3_InRange_stage2_OR.IN2
PT_2oo3_InRange_stage2_OR.OUT, PT_2oo3_InRange_NOT.IN

TT-401A.General_Fault, Faults_TT_AB_OR.IN1
TT-401B.General_Fault, Faults_TT_AB_OR.IN2
Faults_TT_AB_OR.OUT, Faults_TT_ABC_OR.IN1
TT-401C.General_Fault, Faults_TT_ABC_OR.IN2
PT-401A.General_Fault, Faults_PT_AB_OR.IN1
PT-401B.General_Fault, Faults_PT_AB_OR.IN2
Faults_PT_AB_OR.OUT, Faults_PT_ABC_OR.IN1
PT-401C.General_Fault, Faults_PT_ABC_OR.IN2
Faults_TT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN1
Faults_PT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN2
Faults_All_TT_PT_OR.OUT, Faults_All_OR.IN1
FT-401.General_Fault, Faults_All_OR.IN2
Faults_All_OR.OUT, FA-401.Bool_In

TT-401-V.Alarm_Voting_Error, DA-401.Bool_In

TT-401A.General_Fault, TT401A_Healthy_NOT.IN
TT401A_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN1
TT-401B.General_Fault, TT401B_Healthy_NOT.IN
TT401B_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN2
TT_Healthy_AB_AND.OUT, TT_AllHealthy_AND.IN1
TT-401C.General_Fault, TT401C_Healthy_NOT.IN
TT401C_Healthy_NOT.OUT, TT_AllHealthy_AND.IN2
TT_AllHealthy_AND.OUT, TT_Startup_NotOk_NOT.IN

TT401_1450_2oo3_NOT.OUT, Inhibit_TempPress_OR.IN1
PT_2oo3_InRange_NOT.OUT, Inhibit_TempPress_OR.IN2
Inhibit_TempPress_OR.OUT, Inhibit_AddFlow_OR.IN1
FT-401.Low_Alarm, Inhibit_AddFlow_OR.IN2
Inhibit_AddFlow_OR.OUT, Inhibit_AddDA_OR.IN1
DA-401.Bool_Out, Inhibit_AddDA_OR.IN2
Inhibit_AddDA_OR.OUT, Inhibit_AddFA_OR.IN1
FA-401.Bool_Out, Inhibit_AddFA_OR.IN2
Inhibit_AddFA_OR.OUT, Inhibit_AddStartup_OR.IN1
TT_Startup_NotOk_NOT.OUT, Inhibit_AddStartup_OR.IN2
Inhibit_AddStartup_OR.OUT, I-401.Bool_In

I-401.Bool_Out, BOF-402.Inhibit

TT-401-V.Voted_Output, TT_401_V_Voted_Temp

* Parameter Data Connections *
0.05, TT-401-V.Deviation_Limit
2oo3, TT-401-V.Voting_Scheme
TRUE, TT-401-V.EnableAlarm
1450.0, TT-401A.PV_High
1450.0, TT-401B.PV_High
1450.0, TT-401C.PV_High
90.0, PT-401A.PV_Low
120.0, PT-401A.PV_High
90.0, PT-401B.PV_Low
120.0, PT-401B.PV_High
90.0, PT-401C.PV_Low
120.0, PT-401C.PV_High
500.0, FT-401.PV_Low
TRUE, TT-401A.Alarm_Enable
TRUE, TT-401B.Alarm_Enable
TRUE, TT-401C.Alarm_Enable
TRUE, PT-401A.Alarm_Enable
TRUE, PT-401B.Alarm_Enable
TRUE, PT-401C.Alarm_Enable
TRUE, FT-401.Alarm_Enable
```

---

## Step 10: append_two_inputs
**Time:** 04:29:58

### Output:
```
* Function Blocks *
ANALOG_IN FT-401
ANALOG_IN PT-401A
ANALOG_IN PT-401B
ANALOG_IN PT-401C
ANALOG_IN TT-401A
ANALOG_IN TT-401B
ANALOG_IN TT-401C
VOTING_ANALOG TT-401-V
VALVE_ELECTRIC BOF-402
BOOL_IN I-401
BOOL_IN DA-401
BOOL_IN FA-401

* Variables *
REAL TT_401_V_Voted_Temp

* Functions *
AND TT401_1450_A_B_AND
AND TT401_1450_A_C_AND
AND TT401_1450_B_C_AND
OR TT401_1450_2oo3_OR
OR TT401_1450_2oo3_stage2_OR
NOT TT401_1450_2oo3_NOT
OR PTA_OutOfRange_OR
NOT PTA_InRange_NOT
OR PTB_OutOfRange_OR
NOT PTB_InRange_NOT
OR PTC_OutOfRange_OR
NOT PTC_InRange_NOT
AND PT_InRange_AB_AND
AND PT_InRange_AC_AND
AND PT_InRange_BC_AND
OR PT_2oo3_InRange_OR
OR PT_2oo3_InRange_stage2_OR
NOT PT_2oo3_InRange_NOT
OR Faults_TT_AB_OR
OR Faults_TT_ABC_OR
OR Faults_PT_AB_OR
OR Faults_PT_ABC_OR
OR Faults_All_TT_PT_OR
OR Faults_All_OR
NOT TT401A_Healthy_NOT
NOT TT401B_Healthy_NOT
NOT TT401C_Healthy_NOT
AND TT_Healthy_AB_AND
AND TT_AllHealthy_AND
NOT TT_Startup_NotOk_NOT
OR Inhibit_TempPress_OR
OR Inhibit_AddFlow_OR
OR Inhibit_AddDA_OR
OR Inhibit_AddFA_OR
OR Inhibit_AddStartup_OR

* Data Connections * 
TT-401A.PV, TT-401-V.Input1
TT-401B.PV, TT-401-V.Input2
TT-401C.PV, TT-401-V.Input3
TT-401-V.Voted_Output, BOF-402.Control_Signal

TT-401A.High_Alarm, TT401_1450_A_B_AND.IN1
TT-401B.High_Alarm, TT401_1450_A_B_AND.IN2
TT-401A.High_Alarm, TT401_1450_A_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_A_C_AND.IN2
TT-401B.High_Alarm, TT401_1450_B_C_AND.IN1
TT-401C.High_Alarm, TT401_1450_B_C_AND.IN2
TT401_1450_A_B_AND.OUT, TT401_1450_2oo3_OR.IN1
TT401_1450_A_C_AND.OUT, TT401_1450_2oo3_OR.IN2
TT401_1450_2oo3_OR.OUT, TT401_1450_2oo3_stage2_OR.IN1
TT401_1450_B_C_AND.OUT, TT401_1450_2oo3_stage2_OR.IN2
TT401_1450_2oo3_stage2_OR.OUT, TT401_1450_2oo3_NOT.IN

PT-401A.High_Alarm, PTA_OutOfRange_OR.IN1
PT-401A.Low_Alarm, PTA_OutOfRange_OR.IN2
PTA_OutOfRange_OR.OUT, PTA_InRange_NOT.IN
PT-401B.High_Alarm, PTB_OutOfRange_OR.IN1
PT-401B.Low_Alarm, PTB_OutOfRange_OR.IN2
PTB_OutOfRange_OR.OUT, PTB_InRange_NOT.IN
PT-401C.High_Alarm, PTC_OutOfRange_OR.IN1
PT-401C.Low_Alarm, PTC_OutOfRange_OR.IN2
PTC_OutOfRange_OR.OUT, PTC_InRange_NOT.IN
PTA_InRange_NOT.OUT, PT_InRange_AB_AND.IN1
PTB_InRange_NOT.OUT, PT_InRange_AB_AND.IN2
PTA_InRange_NOT.OUT, PT_InRange_AC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_AC_AND.IN2
PTB_InRange_NOT.OUT, PT_InRange_BC_AND.IN1
PTC_InRange_NOT.OUT, PT_InRange_BC_AND.IN2
PT_InRange_AB_AND.OUT, PT_2oo3_InRange_OR.IN1
PT_InRange_AC_AND.OUT, PT_2oo3_InRange_OR.IN2
PT_2oo3_InRange_OR.OUT, PT_2oo3_InRange_stage2_OR.IN1
PT_InRange_BC_AND.OUT, PT_2oo3_InRange_stage2_OR.IN2
PT_2oo3_InRange_stage2_OR.OUT, PT_2oo3_InRange_NOT.IN

TT-401A.General_Fault, Faults_TT_AB_OR.IN1
TT-401B.General_Fault, Faults_TT_AB_OR.IN2
Faults_TT_AB_OR.OUT, Faults_TT_ABC_OR.IN1
TT-401C.General_Fault, Faults_TT_ABC_OR.IN2
PT-401A.General_Fault, Faults_PT_AB_OR.IN1
PT-401B.General_Fault, Faults_PT_AB_OR.IN2
Faults_PT_AB_OR.OUT, Faults_PT_ABC_OR.IN1
PT-401C.General_Fault, Faults_PT_ABC_OR.IN2
Faults_TT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN1
Faults_PT_ABC_OR.OUT, Faults_All_TT_PT_OR.IN2
Faults_All_TT_PT_OR.OUT, Faults_All_OR.IN1
FT-401.General_Fault, Faults_All_OR.IN2
Faults_All_OR.OUT, FA-401.Bool_In

TT-401-V.Alarm_Voting_Error, DA-401.Bool_In

TT-401A.General_Fault, TT401A_Healthy_NOT.IN
TT401A_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN1
TT-401B.General_Fault, TT401B_Healthy_NOT.IN
TT401B_Healthy_NOT.OUT, TT_Healthy_AB_AND.IN2
TT_Healthy_AB_AND.OUT, TT_AllHealthy_AND.IN1
TT-401C.General_Fault, TT401C_Healthy_NOT.IN
TT401C_Healthy_NOT.OUT, TT_AllHealthy_AND.IN2
TT_AllHealthy_AND.OUT, TT_Startup_NotOk_NOT.IN

TT401_1450_2oo3_NOT.OUT, Inhibit_TempPress_OR.IN1
PT_2oo3_InRange_NOT.OUT, Inhibit_TempPress_OR.IN2
Inhibit_TempPress_OR.OUT, Inhibit_AddFlow_OR.IN1
FT-401.Low_Alarm, Inhibit_AddFlow_OR.IN2
Inhibit_AddFlow_OR.OUT, Inhibit_AddDA_OR.IN1
DA-401.Bool_Out, Inhibit_AddDA_OR.IN2
Inhibit_AddDA_OR.OUT, Inhibit_AddFA_OR.IN1
FA-401.Bool_Out, Inhibit_AddFA_OR.IN2
Inhibit_AddFA_OR.OUT, Inhibit_AddStartup_OR.IN1
TT_Startup_NotOk_NOT.OUT, Inhibit_AddStartup_OR.IN2
Inhibit_AddStartup_OR.OUT, I-401.Bool_In

I-401.Bool_Out, BOF-402.Inhibit

TT-401-V.Voted_Output, TT_401_V_Voted_Temp

* Parameter Data Connections *
0.05, TT-401-V.Deviation_Limit
2oo3, TT-401-V.Voting_Scheme
TRUE, TT-401-V.EnableAlarm
1450.0, TT-401A.PV_High
1450.0, TT-401B.PV_High
1450.0, TT-401C.PV_High
90.0, PT-401A.PV_Low
120.0, PT-401A.PV_High
90.0, PT-401B.PV_Low
120.0, PT-401B.PV_High
90.0, PT-401C.PV_Low
120.0, PT-401C.PV_High
500.0, FT-401.PV_Low
TRUE, TT-401A.Alarm_Enable
TRUE, TT-401B.Alarm_Enable
TRUE, TT-401C.Alarm_Enable
TRUE, PT-401A.Alarm_Enable
TRUE, PT-401B.Alarm_Enable
TRUE, PT-401C.Alarm_Enable
TRUE, FT-401.Alarm_Enable
```

---


