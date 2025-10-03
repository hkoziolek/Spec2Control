# Prompt Chain: contextgen1.txt
**Timestamp:** 2025-09-24 03:55:25

## Step 1: contextgen1-sensors
**Time:** 03:55:25

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
**Time:** 03:55:40

### Output:
```
MOTOR_ON_OFF
Direction,Pin Name,Type,Description
Input,Name,STRING,Descriptive name of the function block
Input,Description,STRING,Longer description of motor's purpose.
Input,Start_Cmd,BOOL,Command to start the motor.
Input,Stop_Cmd,BOOL,Command to stop the motor.
Input,Start_Delay,TIME,Delay before motor starts after command.
Input,MinRunTime,TIME,Minimum time motor must run once started.
Input,Inhibit,BOOL,Inhibits starting the motor and can receive alarm signals.
Output,Motor_Start_Out,BOOL,Output to motor starter.
Output,FB_Running,BOOL,Feedback indicating motor is running.
Output,FB_Trip,BOOL,Feedback indicating motor has tripped (overload, fault).
Output,Alarm_Start_Fail,BOOL,Indicates motor failed to start.
Output,Alarm_Stop_Fail,BOOL,Indicates motor failed to stop.

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
**Time:** 03:55:53

### Output:
```
*** Available Control Strategies ***
| Control Strategy | Estimated Probability |
| VOTING | 0.97 |

Selected Control Strategy: VOTING
Short explanation: The narrative centers on 2oo3 voting with median selection and degraded 1oo2 mode for redundant pressure and temperature sensors, matching the VOTING strategy.

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
**Timestamp:** 2025-09-24 03:56:27

## Step 1: openplc-function-blocks-v2
**Time:** 03:56:27

### Output:
```
* Function Blocks *
ANALOG_IN PT-201A
ANALOG_IN PT-201B
ANALOG_IN PT-201C
ANALOG_IN TT-201A
ANALOG_IN TT-201B
ANALOG_IN TT-201C
VOTING_ANALOG PT-201_VOTE
VOTING_ANALOG TT-201_VOTE
BOOL_IN I-201
BOOL_IN I-202
BOOL_IN SI-201
BOOL_IN SI-202
DIGITAL_IN MO-201
DIGITAL_IN MO-202
MOTOR_ON_OFF P-201
```

---

## Step 2: openplc-function-blocks-validation
**Time:** 03:56:57

### Output:
```
* Function Block List *
* Function Blocks *
ANALOG_IN PT-201A
ANALOG_IN PT-201B
ANALOG_IN PT-201C
ANALOG_IN TT-201A
ANALOG_IN TT-201B
ANALOG_IN TT-201C
VOTING_ANALOG PT-201_VOTE
VOTING_ANALOG TT-201_VOTE
BOOL_IN I-201
BOOL_IN I-202
BOOL_IN SI-201
BOOL_IN SI-202
DIGITAL_IN MO-201
DIGITAL_IN MO-202
MOTOR_ON_OFF P-201
```

---

## Step 3: openplc-block-connections-and-logic
**Time:** 03:58:02

### Output:
```
* Functions *

* Block-to-Block Connections *
PT-201A.PV, PT-201_VOTE.Input1
PT-201B.PV, PT-201_VOTE.Input2
PT-201C.PV, PT-201_VOTE.Input3
TT-201A.PV, TT-201_VOTE.Input1
TT-201B.PV, TT-201_VOTE.Input2
TT-201C.PV, TT-201_VOTE.Input3
```

---

## Step 4: openplc-block-connections-interlocks
**Time:** 03:58:27

### Output:
```
* Functions * 
AND PT_High_AB_AND
AND PT_High_AC_AND
AND PT_High_BC_AND
OR PT_High2oo3_OR
AND TT_High_AB_AND
AND TT_High_AC_AND
AND TT_High_BC_AND
OR TT_High2oo3_OR
NOT PT_LowA_NOT
NOT PT_LowB_NOT
NOT PT_LowC_NOT
AND PT_Perm_OK_AB_AND
AND PT_Perm_OK_AC_AND
AND PT_Perm_OK_BC_AND
OR PT_Perm2oo3_OR
NOT TT_HighA_NOT
NOT TT_HighB_NOT
NOT TT_HighC_NOT
AND TT_Perm_OK_AB_AND
AND TT_Perm_OK_AC_AND
AND TT_Perm_OK_BC_AND
OR TT_Perm2oo3_OR
AND StartupPermissive_AND
NOT StartupPermissive_NOT
OR PT_Faults_AB_OR
OR PT_Faults_ABC_OR
OR PT_Alarms_OR
NOT MO201_NOT
AND PT_Summary_Gated_AND
OR TT_Faults_AB_OR
OR TT_Faults_ABC_OR
OR TT_Alarms_OR
NOT MO202_NOT
AND TT_Summary_Gated_AND
OR P201_Inhibit_OR

* Data Connections *
PT-201A.High_Alarm, PT_High_AB_AND.IN1
PT-201B.High_Alarm, PT_High_AB_AND.IN2
PT-201A.High_Alarm, PT_High_AC_AND.IN1
PT-201C.High_Alarm, PT_High_AC_AND.IN2
PT-201B.High_Alarm, PT_High_BC_AND.IN1
PT-201C.High_Alarm, PT_High_BC_AND.IN2
PT_High_AB_AND.OUT, PT_High2oo3_OR.IN1
PT_High_AC_AND.OUT, PT_High2oo3_OR.IN2
PT_High_BC_AND.OUT, PT_High2oo3_OR.IN3
PT_High2oo3_OR.OUT, I-201.Bool_In
TT-201A.High_Alarm, TT_High_AB_AND.IN1
TT-201B.High_Alarm, TT_High_AB_AND.IN2
TT-201A.High_Alarm, TT_High_AC_AND.IN1
TT-201C.High_Alarm, TT_High_AC_AND.IN2
TT-201B.High_Alarm, TT_High_BC_AND.IN1
TT-201C.High_Alarm, TT_High_BC_AND.IN2
TT_High_AB_AND.OUT, TT_High2oo3_OR.IN1
TT_High_AC_AND.OUT, TT_High2oo3_OR.IN2
TT_High_BC_AND.OUT, TT_High2oo3_OR.IN3
TT_High2oo3_OR.OUT, I-202.Bool_In
PT-201A.Low_Alarm, PT_LowA_NOT.IN
PT-201B.Low_Alarm, PT_LowB_NOT.IN
PT-201C.Low_Alarm, PT_LowC_NOT.IN
PT_LowA_NOT.OUT, PT_Perm_OK_AB_AND.IN1
PT_LowB_NOT.OUT, PT_Perm_OK_AB_AND.IN2
PT_LowA_NOT.OUT, PT_Perm_OK_AC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_AC_AND.IN2
PT_LowB_NOT.OUT, PT_Perm_OK_BC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_BC_AND.IN2
PT_Perm_OK_AB_AND.OUT, PT_Perm2oo3_OR.IN1
PT_Perm_OK_AC_AND.OUT, PT_Perm2oo3_OR.IN2
PT_Perm_OK_BC_AND.OUT, PT_Perm2oo3_OR.IN3
TT-201A.High_Alarm, TT_HighA_NOT.IN
TT-201B.High_Alarm, TT_HighB_NOT.IN
TT-201C.High_Alarm, TT_HighC_NOT.IN
TT_HighA_NOT.OUT, TT_Perm_OK_AB_AND.IN1
TT_HighB_NOT.OUT, TT_Perm_OK_AB_AND.IN2
TT_HighA_NOT.OUT, TT_Perm_OK_AC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_AC_AND.IN2
TT_HighB_NOT.OUT, TT_Perm_OK_BC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_BC_AND.IN2
TT_Perm_OK_AB_AND.OUT, TT_Perm2oo3_OR.IN1
TT_Perm_OK_AC_AND.OUT, TT_Perm2oo3_OR.IN2
TT_Perm_OK_BC_AND.OUT, TT_Perm2oo3_OR.IN3
PT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN1
TT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN2
StartupPermissive_AND.OUT, StartupPermissive_NOT.IN
PT-201A.General_Fault, PT_Faults_AB_OR.IN1
PT-201B.General_Fault, PT_Faults_AB_OR.IN2
PT_Faults_AB_OR.OUT, PT_Faults_ABC_OR.IN1
PT-201C.General_Fault, PT_Faults_ABC_OR.IN2
PT-201_VOTE.Alarm_Voting_Error, PT_Alarms_OR.IN1
PT_Faults_ABC_OR.OUT, PT_Alarms_OR.IN2
MO-201.DI_Out, MO201_NOT.IN
PT_Alarms_OR.OUT, PT_Summary_Gated_AND.IN1
MO201_NOT.OUT, PT_Summary_Gated_AND.IN2
PT_Summary_Gated_AND.OUT, SI-201.Bool_In
TT-201A.General_Fault, TT_Faults_AB_OR.IN1
TT-201B.General_Fault, TT_Faults_AB_OR.IN2
TT_Faults_AB_OR.OUT, TT_Faults_ABC_OR.IN1
TT-201C.General_Fault, TT_Faults_ABC_OR.IN2
TT-201_VOTE.Alarm_Voting_Error, TT_Alarms_OR.IN1
TT_Faults_ABC_OR.OUT, TT_Alarms_OR.IN2
MO-202.DI_Out, MO202_NOT.IN
TT_Alarms_OR.OUT, TT_Summary_Gated_AND.IN1
MO202_NOT.OUT, TT_Summary_Gated_AND.IN2
TT_Summary_Gated_AND.OUT, SI-202.Bool_In
StartupPermissive_NOT.OUT, P201_Inhibit_OR.IN1
I-201.Bool_Out, P201_Inhibit_OR.IN2
I-202.Bool_Out, P201_Inhibit_OR.IN3
SI-201.Bool_Out, P201_Inhibit_OR.IN4
SI-202.Bool_Out, P201_Inhibit_OR.IN5
P201_Inhibit_OR.OUT, P-201.Inhibit

* Parameter Data Connections *
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201A.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, PT-201C.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201A.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201C.PV_High
TRUE, TT-201C.Alarm_Enable
5.0, PT-201_VOTE.Deviation_Limit
TRUE, PT-201_VOTE.EnableAlarm
"2oo3", PT-201_VOTE.Voting_Scheme
5.0, TT-201_VOTE.Deviation_Limit
TRUE, TT-201_VOTE.EnableAlarm
"Median", TT-201_VOTE.Voting_Scheme
TRUE, I-201.Alarm_OnTrue
TRUE, I-202.Alarm_OnTrue
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-202.Alarm_OnTrue
```

---

## Step 5: openplc-parameter-data-connections
**Time:** 04:00:41

### Output:
```
* Parameter Data Connections *
TRUE, PT-201A.Alarm_Enable
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201C.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, TT-201A.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201C.Alarm_Enable
75.0, TT-201C.PV_High
"2oo3", PT-201_VOTE.Voting_Scheme
5.0, PT-201_VOTE.Deviation_Limit
TRUE, PT-201_VOTE.EnableAlarm
"Median", TT-201_VOTE.Voting_Scheme
5.0, TT-201_VOTE.Deviation_Limit
TRUE, TT-201_VOTE.EnableAlarm
TRUE, I-201.Alarm_OnTrue
TRUE, I-201.Latch_Enable
TRUE, I-202.Alarm_OnTrue
TRUE, I-202.Latch_Enable
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-201.Latch_Enable
TRUE, SI-202.Alarm_OnTrue
TRUE, SI-202.Latch_Enable
```

---

## Step 6: openplc-input-variables-and-connections
**Time:** 04:01:41

### Output:
```
* Parameter Data Connections *
TRUE, PT-201A.Alarm_Enable
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201C.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, TT-201A.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201C.Alarm_Enable
75.0, TT-201C.PV_High
"2oo3", PT-201_VOTE.Voting_Scheme
5.0, PT-201_VOTE.Deviation_Limit
TRUE, PT-201_VOTE.EnableAlarm
"Median", TT-201_VOTE.Voting_Scheme
5.0, TT-201_VOTE.Deviation_Limit
TRUE, TT-201_VOTE.EnableAlarm
TRUE, I-201.Alarm_OnTrue
TRUE, I-201.Latch_Enable
TRUE, I-202.Alarm_OnTrue
TRUE, I-202.Latch_Enable
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-201.Latch_Enable
TRUE, SI-202.Alarm_OnTrue
TRUE, SI-202.Latch_Enable
```

---

## Step 7: openplc-output-variables-and-connections
**Time:** 04:02:33

### Output:
```
* Variables *
REAL PT-201_VOTE
REAL TT-201_VOTE

* Data Connections *
PT-201_VOTE.Voted_Output, PT-201_VOTE
TT-201_VOTE.Voted_Output, TT-201_VOTE
```

---

## Step 8: openplc-rule-checks
**Time:** 04:02:54

### Output:
```
* Function Blocks *
ANALOG_IN PT-201A
ANALOG_IN PT-201B
ANALOG_IN PT-201C
ANALOG_IN TT-201A
ANALOG_IN TT-201B
ANALOG_IN TT-201C
VOTING_ANALOG CO-201
VOTING_ANALOG CO-202
BOOL_IN I-201
BOOL_IN I-202
BOOL_IN SI-201
BOOL_IN SI-202
DIGITAL_IN MO-201
DIGITAL_IN MO-202
MOTOR_ON_OFF P-201

* Variables *
REAL PT-201_VOTE
REAL TT-201_VOTE

* Functions *
AND PT_High_AB_AND
AND PT_High_AC_AND
AND PT_High_BC_AND
OR PT_High2oo3_OR
AND TT_High_AB_AND
AND TT_High_AC_AND
AND TT_High_BC_AND
OR TT_High2oo3_OR
NOT PT_LowA_NOT
NOT PT_LowB_NOT
NOT PT_LowC_NOT
AND PT_Perm_OK_AB_AND
AND PT_Perm_OK_AC_AND
AND PT_Perm_OK_BC_AND
OR PT_Perm2oo3_OR
NOT TT_HighA_NOT
NOT TT_HighB_NOT
NOT TT_HighC_NOT
AND TT_Perm_OK_AB_AND
AND TT_Perm_OK_AC_AND
AND TT_Perm_OK_BC_AND
OR TT_Perm2oo3_OR
AND StartupPermissive_AND
NOT StartupPermissive_NOT
OR PT_Faults_AB_OR
OR PT_Faults_ABC_OR
OR PT_Alarms_OR
NOT MO201_NOT
AND PT_Summary_Gated_AND
OR TT_Faults_AB_OR
OR TT_Faults_ABC_OR
OR TT_Alarms_OR
NOT MO202_NOT
AND TT_Summary_Gated_AND
OR P201_Inhibit_OR

* Data Connections *
PT-201A.PV, CO-201.Input1
PT-201B.PV, CO-201.Input2
PT-201C.PV, CO-201.Input3
TT-201A.PV, CO-202.Input1
TT-201B.PV, CO-202.Input2
TT-201C.PV, CO-202.Input3
PT-201A.High_Alarm, PT_High_AB_AND.IN1
PT-201B.High_Alarm, PT_High_AB_AND.IN2
PT-201A.High_Alarm, PT_High_AC_AND.IN1
PT-201C.High_Alarm, PT_High_AC_AND.IN2
PT-201B.High_Alarm, PT_High_BC_AND.IN1
PT-201C.High_Alarm, PT_High_BC_AND.IN2
PT_High_AB_AND.OUT, PT_High2oo3_OR.IN1
PT_High_AC_AND.OUT, PT_High2oo3_OR.IN2
PT_High_BC_AND.OUT, PT_High2oo3_OR.IN3
PT_High2oo3_OR.OUT, I-201.Bool_In
TT-201A.High_Alarm, TT_High_AB_AND.IN1
TT-201B.High_Alarm, TT_High_AB_AND.IN2
TT-201A.High_Alarm, TT_High_AC_AND.IN1
TT-201C.High_Alarm, TT_High_AC_AND.IN2
TT-201B.High_Alarm, TT_High_BC_AND.IN1
TT-201C.High_Alarm, TT_High_BC_AND.IN2
TT_High_AB_AND.OUT, TT_High2oo3_OR.IN1
TT_High_AC_AND.OUT, TT_High2oo3_OR.IN2
TT_High_BC_AND.OUT, TT_High2oo3_OR.IN3
TT_High2oo3_OR.OUT, I-202.Bool_In
PT-201A.Low_Alarm, PT_LowA_NOT.IN
PT-201B.Low_Alarm, PT_LowB_NOT.IN
PT-201C.Low_Alarm, PT_LowC_NOT.IN
PT_LowA_NOT.OUT, PT_Perm_OK_AB_AND.IN1
PT_LowB_NOT.OUT, PT_Perm_OK_AB_AND.IN2
PT_LowA_NOT.OUT, PT_Perm_OK_AC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_AC_AND.IN2
PT_LowB_NOT.OUT, PT_Perm_OK_BC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_BC_AND.IN2
PT_Perm_OK_AB_AND.OUT, PT_Perm2oo3_OR.IN1
PT_Perm_OK_AC_AND.OUT, PT_Perm2oo3_OR.IN2
PT_Perm_OK_BC_AND.OUT, PT_Perm2oo3_OR.IN3
TT-201A.High_Alarm, TT_HighA_NOT.IN
TT-201B.High_Alarm, TT_HighB_NOT.IN
TT-201C.High_Alarm, TT_HighC_NOT.IN
TT_HighA_NOT.OUT, TT_Perm_OK_AB_AND.IN1
TT_HighB_NOT.OUT, TT_Perm_OK_AB_AND.IN2
TT_HighA_NOT.OUT, TT_Perm_OK_AC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_AC_AND.IN2
TT_HighB_NOT.OUT, TT_Perm_OK_BC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_BC_AND.IN2
TT_Perm_OK_AB_AND.OUT, TT_Perm2oo3_OR.IN1
TT_Perm_OK_AC_AND.OUT, TT_Perm2oo3_OR.IN2
TT_Perm_OK_BC_AND.OUT, TT_Perm2oo3_OR.IN3
PT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN1
TT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN2
StartupPermissive_AND.OUT, StartupPermissive_NOT.IN
PT-201A.General_Fault, PT_Faults_AB_OR.IN1
PT-201B.General_Fault, PT_Faults_AB_OR.IN2
PT_Faults_AB_OR.OUT, PT_Faults_ABC_OR.IN1
PT-201C.General_Fault, PT_Faults_ABC_OR.IN2
CO-201.Alarm_Voting_Error, PT_Alarms_OR.IN1
PT_Faults_ABC_OR.OUT, PT_Alarms_OR.IN2
MO-201.DI_Out, MO201_NOT.IN
PT_Alarms_OR.OUT, PT_Summary_Gated_AND.IN1
MO201_NOT.OUT, PT_Summary_Gated_AND.IN2
PT_Summary_Gated_AND.OUT, SI-201.Bool_In
TT-201A.General_Fault, TT_Faults_AB_OR.IN1
TT-201B.General_Fault, TT_Faults_AB_OR.IN2
TT_Faults_AB_OR.OUT, TT_Faults_ABC_OR.IN1
TT-201C.General_Fault, TT_Faults_ABC_OR.IN2
CO-202.Alarm_Voting_Error, TT_Alarms_OR.IN1
TT_Faults_ABC_OR.OUT, TT_Alarms_OR.IN2
MO-202.DI_Out, MO202_NOT.IN
TT_Alarms_OR.OUT, TT_Summary_Gated_AND.IN1
MO202_NOT.OUT, TT_Summary_Gated_AND.IN2
TT_Summary_Gated_AND.OUT, SI-202.Bool_In
StartupPermissive_NOT.OUT, P201_Inhibit_OR.IN1
I-201.Bool_Out, P201_Inhibit_OR.IN2
I-202.Bool_Out, P201_Inhibit_OR.IN3
SI-201.Bool_Out, P201_Inhibit_OR.IN4
SI-202.Bool_Out, P201_Inhibit_OR.IN5
P201_Inhibit_OR.OUT, P-201.Inhibit
CO-201.Voted_Output, PT-201_VOTE
CO-202.Voted_Output, TT-201_VOTE

* Parameter Data Connections *
TRUE, PT-201A.Alarm_Enable
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201C.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, TT-201A.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201C.Alarm_Enable
75.0, TT-201C.PV_High
"2oo3", CO-201.Voting_Scheme
5.0, CO-201.Deviation_Limit
TRUE, CO-201.EnableAlarm
"Median", CO-202.Voting_Scheme
5.0, CO-202.Deviation_Limit
TRUE, CO-202.EnableAlarm
TRUE, I-201.Alarm_OnTrue
TRUE, I-201.Latch_Enable
TRUE, I-202.Alarm_OnTrue
TRUE, I-202.Latch_Enable
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-201.Latch_Enable
TRUE, SI-202.Alarm_OnTrue
TRUE, SI-202.Latch_Enable
```

---

## Step 9: openplc-rule-checks2
**Time:** 04:04:31

### Output:
```
* Function Blocks *
ANALOG_IN PT-201A
ANALOG_IN PT-201B
ANALOG_IN PT-201C
ANALOG_IN TT-201A
ANALOG_IN TT-201B
ANALOG_IN TT-201C
VOTING_ANALOG CO-201
VOTING_ANALOG CO-202
BOOL_IN I-201
BOOL_IN I-202
BOOL_IN SI-201
BOOL_IN SI-202
DIGITAL_IN MO-201
DIGITAL_IN MO-202
MOTOR_ON_OFF P-201

* Variables *
REAL PT-201_VOTE
REAL TT-201_VOTE

* Functions *
AND PT_High_AB_AND
AND PT_High_AC_AND
AND PT_High_BC_AND
OR PT_High2oo3_OR
AND TT_High_AB_AND
AND TT_High_AC_AND
AND TT_High_BC_AND
OR TT_High2oo3_OR
NOT PT_LowA_NOT
NOT PT_LowB_NOT
NOT PT_LowC_NOT
AND PT_Perm_OK_AB_AND
AND PT_Perm_OK_AC_AND
AND PT_Perm_OK_BC_AND
OR PT_Perm2oo3_OR
NOT TT_HighA_NOT
NOT TT_HighB_NOT
NOT TT_HighC_NOT
AND TT_Perm_OK_AB_AND
AND TT_Perm_OK_AC_AND
AND TT_Perm_OK_BC_AND
OR TT_Perm2oo3_OR
AND StartupPermissive_AND
NOT StartupPermissive_NOT
OR PT_Faults_AB_OR
OR PT_Faults_ABC_OR
OR PT_Alarms_OR
NOT MO201_NOT
AND PT_Summary_Gated_AND
OR TT_Faults_AB_OR
OR TT_Faults_ABC_OR
OR TT_Alarms_OR
NOT MO202_NOT
AND TT_Summary_Gated_AND
OR P201_Inhibit_OR

* Data Connections *
PT-201A.PV, CO-201.Input1
PT-201B.PV, CO-201.Input2
PT-201C.PV, CO-201.Input3
TT-201A.PV, CO-202.Input1
TT-201B.PV, CO-202.Input2
TT-201C.PV, CO-202.Input3
PT-201A.High_Alarm, PT_High_AB_AND.IN1
PT-201B.High_Alarm, PT_High_AB_AND.IN2
PT-201A.High_Alarm, PT_High_AC_AND.IN1
PT-201C.High_Alarm, PT_High_AC_AND.IN2
PT-201B.High_Alarm, PT_High_BC_AND.IN1
PT-201C.High_Alarm, PT_High_BC_AND.IN2
PT_High_AB_AND.OUT, PT_High2oo3_OR.IN1
PT_High_AC_AND.OUT, PT_High2oo3_OR.IN2
PT_High_BC_AND.OUT, PT_High2oo3_OR.IN3
PT_High2oo3_OR.OUT, I-201.Bool_In
TT-201A.High_Alarm, TT_High_AB_AND.IN1
TT-201B.High_Alarm, TT_High_AB_AND.IN2
TT-201A.High_Alarm, TT_High_AC_AND.IN1
TT-201C.High_Alarm, TT_High_AC_AND.IN2
TT-201B.High_Alarm, TT_High_BC_AND.IN1
TT-201C.High_Alarm, TT_High_BC_AND.IN2
TT_High_AB_AND.OUT, TT_High2oo3_OR.IN1
TT_High_AC_AND.OUT, TT_High2oo3_OR.IN2
TT_High_BC_AND.OUT, TT_High2oo3_OR.IN3
TT_High2oo3_OR.OUT, I-202.Bool_In
PT-201A.Low_Alarm, PT_LowA_NOT.IN
PT-201B.Low_Alarm, PT_LowB_NOT.IN
PT-201C.Low_Alarm, PT_LowC_NOT.IN
PT_LowA_NOT.OUT, PT_Perm_OK_AB_AND.IN1
PT_LowB_NOT.OUT, PT_Perm_OK_AB_AND.IN2
PT_LowA_NOT.OUT, PT_Perm_OK_AC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_AC_AND.IN2
PT_LowB_NOT.OUT, PT_Perm_OK_BC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_BC_AND.IN2
PT_Perm_OK_AB_AND.OUT, PT_Perm2oo3_OR.IN1
PT_Perm_OK_AC_AND.OUT, PT_Perm2oo3_OR.IN2
PT_Perm_OK_BC_AND.OUT, PT_Perm2oo3_OR.IN3
TT-201A.High_Alarm, TT_HighA_NOT.IN
TT-201B.High_Alarm, TT_HighB_NOT.IN
TT-201C.High_Alarm, TT_HighC_NOT.IN
TT_HighA_NOT.OUT, TT_Perm_OK_AB_AND.IN1
TT_HighB_NOT.OUT, TT_Perm_OK_AB_AND.IN2
TT_HighA_NOT.OUT, TT_Perm_OK_AC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_AC_AND.IN2
TT_HighB_NOT.OUT, TT_Perm_OK_BC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_BC_AND.IN2
TT_Perm_OK_AB_AND.OUT, TT_Perm2oo3_OR.IN1
TT_Perm_OK_AC_AND.OUT, TT_Perm2oo3_OR.IN2
TT_Perm_OK_BC_AND.OUT, TT_Perm2oo3_OR.IN3
PT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN1
TT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN2
StartupPermissive_AND.OUT, StartupPermissive_NOT.IN
PT-201A.General_Fault, PT_Faults_AB_OR.IN1
PT-201B.General_Fault, PT_Faults_AB_OR.IN2
PT_Faults_AB_OR.OUT, PT_Faults_ABC_OR.IN1
PT-201C.General_Fault, PT_Faults_ABC_OR.IN2
CO-201.Alarm_Voting_Error, PT_Alarms_OR.IN1
PT_Faults_ABC_OR.OUT, PT_Alarms_OR.IN2
MO-201.DI_Out, MO201_NOT.IN
PT_Alarms_OR.OUT, PT_Summary_Gated_AND.IN1
MO201_NOT.OUT, PT_Summary_Gated_AND.IN2
PT_Summary_Gated_AND.OUT, SI-201.Bool_In
TT-201A.General_Fault, TT_Faults_AB_OR.IN1
TT-201B.General_Fault, TT_Faults_AB_OR.IN2
TT_Faults_AB_OR.OUT, TT_Faults_ABC_OR.IN1
TT-201C.General_Fault, TT_Faults_ABC_OR.IN2
CO-202.Alarm_Voting_Error, TT_Alarms_OR.IN1
TT_Faults_ABC_OR.OUT, TT_Alarms_OR.IN2
MO-202.DI_Out, MO202_NOT.IN
TT_Alarms_OR.OUT, TT_Summary_Gated_AND.IN1
MO202_NOT.OUT, TT_Summary_Gated_AND.IN2
TT_Summary_Gated_AND.OUT, SI-202.Bool_In
StartupPermissive_NOT.OUT, P201_Inhibit_OR.IN1
I-201.Bool_Out, P201_Inhibit_OR.IN2
I-202.Bool_Out, P201_Inhibit_OR.IN3
SI-201.Bool_Out, P201_Inhibit_OR.IN4
SI-202.Bool_Out, P201_Inhibit_OR.IN5
P201_Inhibit_OR.OUT, P-201.Inhibit
CO-201.Voted_Output, PT-201_VOTE
CO-202.Voted_Output, TT-201_VOTE

* Parameter Data Connections *
TRUE, PT-201A.Alarm_Enable
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201C.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, TT-201A.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201C.Alarm_Enable
75.0, TT-201C.PV_High
"2oo3", CO-201.Voting_Scheme
5.0, CO-201.Deviation_Limit
TRUE, CO-201.EnableAlarm
"Median", CO-202.Voting_Scheme
5.0, CO-202.Deviation_Limit
TRUE, CO-202.EnableAlarm
TRUE, I-201.Alarm_OnTrue
TRUE, I-201.Latch_Enable
TRUE, I-202.Alarm_OnTrue
TRUE, I-202.Latch_Enable
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-201.Latch_Enable
TRUE, SI-202.Alarm_OnTrue
TRUE, SI-202.Latch_Enable
```

---

## Step 10: append_two_inputs
**Time:** 04:05:05

### Output:
```
* Function Blocks *
ANALOG_IN PT-201A
ANALOG_IN PT-201B
ANALOG_IN PT-201C
ANALOG_IN TT-201A
ANALOG_IN TT-201B
ANALOG_IN TT-201C
VOTING_ANALOG CO-201
VOTING_ANALOG CO-202
BOOL_IN I-201
BOOL_IN I-202
BOOL_IN SI-201
BOOL_IN SI-202
DIGITAL_IN MO-201
DIGITAL_IN MO-202
MOTOR_ON_OFF P-201

* Variables *
REAL PT-201_VOTE
REAL TT-201_VOTE

* Functions *
AND PT_High_AB_AND
AND PT_High_AC_AND
AND PT_High_BC_AND
OR PT_High2oo3_OR
AND TT_High_AB_AND
AND TT_High_AC_AND
AND TT_High_BC_AND
OR TT_High2oo3_OR
NOT PT_LowA_NOT
NOT PT_LowB_NOT
NOT PT_LowC_NOT
AND PT_Perm_OK_AB_AND
AND PT_Perm_OK_AC_AND
AND PT_Perm_OK_BC_AND
OR PT_Perm2oo3_OR
NOT TT_HighA_NOT
NOT TT_HighB_NOT
NOT TT_HighC_NOT
AND TT_Perm_OK_AB_AND
AND TT_Perm_OK_AC_AND
AND TT_Perm_OK_BC_AND
OR TT_Perm2oo3_OR
AND StartupPermissive_AND
NOT StartupPermissive_NOT
OR PT_Faults_OR
OR PT_Alarms_OR
NOT MO201_NOT
AND PT_Summary_Gated_AND
OR TT_Faults_OR
OR TT_Alarms_OR
NOT MO202_NOT
AND TT_Summary_Gated_AND
OR P201_Inhibit_OR

* Data Connections *
PT-201A.PV, CO-201.Input1
PT-201B.PV, CO-201.Input2
PT-201C.PV, CO-201.Input3
TT-201A.PV, CO-202.Input1
TT-201B.PV, CO-202.Input2
TT-201C.PV, CO-202.Input3
PT-201A.High_Alarm, PT_High_AB_AND.IN1
PT-201B.High_Alarm, PT_High_AB_AND.IN2
PT-201A.High_Alarm, PT_High_AC_AND.IN1
PT-201C.High_Alarm, PT_High_AC_AND.IN2
PT-201B.High_Alarm, PT_High_BC_AND.IN1
PT-201C.High_Alarm, PT_High_BC_AND.IN2
PT_High_AB_AND.OUT, PT_High2oo3_OR.IN1
PT_High_AC_AND.OUT, PT_High2oo3_OR.IN2
PT_High_BC_AND.OUT, PT_High2oo3_OR.IN3
PT_High2oo3_OR.OUT, I-201.Bool_In
TT-201A.High_Alarm, TT_High_AB_AND.IN1
TT-201B.High_Alarm, TT_High_AB_AND.IN2
TT-201A.High_Alarm, TT_High_AC_AND.IN1
TT-201C.High_Alarm, TT_High_AC_AND.IN2
TT-201B.High_Alarm, TT_High_BC_AND.IN1
TT-201C.High_Alarm, TT_High_BC_AND.IN2
TT_High_AB_AND.OUT, TT_High2oo3_OR.IN1
TT_High_AC_AND.OUT, TT_High2oo3_OR.IN2
TT_High_BC_AND.OUT, TT_High2oo3_OR.IN3
TT_High2oo3_OR.OUT, I-202.Bool_In
PT-201A.Low_Alarm, PT_LowA_NOT.IN
PT-201B.Low_Alarm, PT_LowB_NOT.IN
PT-201C.Low_Alarm, PT_LowC_NOT.IN
PT_LowA_NOT.OUT, PT_Perm_OK_AB_AND.IN1
PT_LowB_NOT.OUT, PT_Perm_OK_AB_AND.IN2
PT_LowA_NOT.OUT, PT_Perm_OK_AC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_AC_AND.IN2
PT_LowB_NOT.OUT, PT_Perm_OK_BC_AND.IN1
PT_LowC_NOT.OUT, PT_Perm_OK_BC_AND.IN2
PT_Perm_OK_AB_AND.OUT, PT_Perm2oo3_OR.IN1
PT_Perm_OK_AC_AND.OUT, PT_Perm2oo3_OR.IN2
PT_Perm_OK_BC_AND.OUT, PT_Perm2oo3_OR.IN3
TT-201A.High_Alarm, TT_HighA_NOT.IN
TT-201B.High_Alarm, TT_HighB_NOT.IN
TT-201C.High_Alarm, TT_HighC_NOT.IN
TT_HighA_NOT.OUT, TT_Perm_OK_AB_AND.IN1
TT_HighB_NOT.OUT, TT_Perm_OK_AB_AND.IN2
TT_HighA_NOT.OUT, TT_Perm_OK_AC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_AC_AND.IN2
TT_HighB_NOT.OUT, TT_Perm_OK_BC_AND.IN1
TT_HighC_NOT.OUT, TT_Perm_OK_BC_AND.IN2
TT_Perm_OK_AB_AND.OUT, TT_Perm2oo3_OR.IN1
TT_Perm_OK_AC_AND.OUT, TT_Perm2oo3_OR.IN2
TT_Perm_OK_BC_AND.OUT, TT_Perm2oo3_OR.IN3
PT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN1
TT_Perm2oo3_OR.OUT, StartupPermissive_AND.IN2
StartupPermissive_AND.OUT, StartupPermissive_NOT.IN
PT-201A.General_Fault, PT_Faults_OR.IN1
PT-201B.General_Fault, PT_Faults_OR.IN2
PT-201C.General_Fault, PT_Faults_OR.IN3
CO-201.Alarm_Voting_Error, PT_Alarms_OR.IN1
PT_Faults_OR.OUT, PT_Alarms_OR.IN2
MO-201.DI_Out, MO201_NOT.IN
PT_Alarms_OR.OUT, PT_Summary_Gated_AND.IN1
MO201_NOT.OUT, PT_Summary_Gated_AND.IN2
PT_Summary_Gated_AND.OUT, SI-201.Bool_In
TT-201A.General_Fault, TT_Faults_OR.IN1
TT-201B.General_Fault, TT_Faults_OR.IN2
TT-201C.General_Fault, TT_Faults_OR.IN3
CO-202.Alarm_Voting_Error, TT_Alarms_OR.IN1
TT_Faults_OR.OUT, TT_Alarms_OR.IN2
MO-202.DI_Out, MO202_NOT.IN
TT_Alarms_OR.OUT, TT_Summary_Gated_AND.IN1
MO202_NOT.OUT, TT_Summary_Gated_AND.IN2
TT_Summary_Gated_AND.OUT, SI-202.Bool_In
StartupPermissive_NOT.OUT, P201_Inhibit_OR.IN1
I-201.Bool_Out, P201_Inhibit_OR.IN2
I-202.Bool_Out, P201_Inhibit_OR.IN3
SI-201.Bool_Out, P201_Inhibit_OR.IN4
SI-202.Bool_Out, P201_Inhibit_OR.IN5
P201_Inhibit_OR.OUT, P-201.Inhibit
CO-201.Voted_Output, PT-201_VOTE
CO-202.Voted_Output, TT-201_VOTE

* Parameter Data Connections *
TRUE, PT-201A.Alarm_Enable
100.0, PT-201A.PV_High
21.0, PT-201A.PV_Low
TRUE, PT-201B.Alarm_Enable
100.0, PT-201B.PV_High
21.0, PT-201B.PV_Low
TRUE, PT-201C.Alarm_Enable
100.0, PT-201C.PV_High
21.0, PT-201C.PV_Low
TRUE, TT-201A.Alarm_Enable
75.0, TT-201A.PV_High
TRUE, TT-201B.Alarm_Enable
75.0, TT-201B.PV_High
TRUE, TT-201C.Alarm_Enable
75.0, TT-201C.PV_High
"2oo3", CO-201.Voting_Scheme
5.0, CO-201.Deviation_Limit
TRUE, CO-201.EnableAlarm
"Median", CO-202.Voting_Scheme
5.0, CO-202.Deviation_Limit
TRUE, CO-202.EnableAlarm
TRUE, I-201.Alarm_OnTrue
TRUE, I-201.Latch_Enable
TRUE, I-202.Alarm_OnTrue
TRUE, I-202.Latch_Enable
TRUE, SI-201.Alarm_OnTrue
TRUE, SI-201.Latch_Enable
TRUE, SI-202.Alarm_OnTrue
TRUE, SI-202.Latch_Enable
```

---


