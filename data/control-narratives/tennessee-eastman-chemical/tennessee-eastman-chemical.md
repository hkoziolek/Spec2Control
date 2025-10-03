# Multi-Column Chemical Distillation System Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Feed System**
3. **Column 1 and Reboiler**
4. **Decanter 1**
5. **Column 2 and Reboiler**
6. **Separator**
7. **Column 3 and Reboiler**
8. **Decanter 2**
9. **Condenser Systems**
10. **Product Flow Control**

---


## 1 **Process Overview and Scope**

The chemical process utilizes a multi-column distillation system to separate feedstock into distinct product streams while maintaining stringent operational parameters. The overall objective is to achieve efficient separation and purification through precise control of flow, pressure, temperature, and level conditions across interconnected process stages. This ensures consistent product quality, optimizes energy usage, and minimizes waste. The system is designed to provide stable operation and adaptability to variations in feedstock composition, aligning with both production targets and safety standards.

The process is divided into sequential phases, including feedstock introduction, distillation across three columns, phase separation via decanters, and final purification through a separator. Each phase is interconnected, with upstream conditions influencing downstream performance. Critical control strategies include maintaining thermal balance through reboilers and condensers, regulating flow rates to ensure steady material movement, and using feedback loops for real-time adjustments. Temperature and pressure controls are integral to maintaining optimal distillation efficiency, while level control ensures proper phase separation and prevents system disturbances.

Operational safety and reliability are prioritized throughout the system. Redundant controls and alarms protect against deviations in critical parameters, reducing the risk of equipment damage or process instability. The design emphasizes smooth transitions between process stages and robust instrumentation for monitoring and control, ensuring consistent operation even under variable conditions. Overall, the process achieves efficient separation while adhering to high standards for safety, quality, and environmental compliance.


## 2 **Feed System**
|Tagname | Type | Description |
|---------|------|-------------|
|FAL-101 | Flow Alarm Low | Low flow alarm for feed system safety |
|FAL-102 | Flow Alarm Low | Secondary low flow alarm for redundancy |
|FAL-103 | Flow Alarm Low | Tertiary low flow alarm for critical protection |
|FIC-104 | Flow Controller | Controls feedstock flow into the process |
|FIT-101 | Flow Transmitter | Measures feedstock flow rate (0-200 GPM) |
|IAL-101 | Interlock Alarm Low | Low-level interlock for process safety |
|PI-001 | Pressure Indicator | Displays pressure in the feed system |
|PV-103 | Control Valve | Modulates feedstock flow (fail-closed) |
|XV-106 | On-Off Valve | Upstream shut-off valve for isolation |


### 2.1) Control Strategy Description

The feed system controls the flow of feedstock into the process using a single-loop PID feedback control strategy implemented in FIC-104. The process variable (PV) is the flow rate measured by FIT-101, with a transmitter range of 0-200 GPM (4-20 mA). The setpoint (SP) for FIC-104 is adjustable between 50 and 150 GPM, with a default operating setpoint of 100 GPM. The manipulated variable (MV) is the position of PV-103, a modulating control valve with a fail-closed configuration.

FIC-104 is configured for reverse-acting control to ensure that an increase in flow rate results in a decrease in valve opening. PID tuning parameters are set as follows: proportional gain (Kp) = 1.5, integral time (Ki) = 0.6 min, and derivative time (Kd) = 0.1 min. The controller output is constrained between 0% and 100% to match the valve's operating range. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes. Anti-windup protection is enabled to prevent integrator saturation during output clamping.

The raw signal from FIT-101 is scaled linearly to provide a calibrated flow value in engineering units (GPM) for control calculations. The setpoint input is clamped between 50 and 150 GPM to maintain process stability and protect downstream equipment.


### 2.2) Interlocks and Permissives

The feed control system includes interlocks to ensure safe operation. XV-106, a shut-off valve upstream of PV-103, must be fully open (confirmed by position feedback) before FIC-104 is allowed to operate in automatic mode. Additionally, the system requires a valid flow signal from FIT-101, with the transmitter output within the range of 4-20 mA. If the signal from FIT-101 is lost or falls outside the valid range, FIC-104 will switch to manual mode, and PV-103 will move to its fail-closed position.

A permissive is implemented to prevent FIC-104 from initiating control unless the downstream process pressure, as measured by PI-1, is within the range of 20-50 psig. This prevents over-pressurization of the downstream system during startup.


### 2.3) Alarm and Fault Handling

The control system generates a high-flow alarm (FAL-101) if the flow rate measured by FIT-101 exceeds 180 GPM. A low-flow alarm (FAL-102) is triggered if the flow rate falls below 40 GPM. Both alarms are latched and require operator acknowledgment before being cleared.

In the event of a fault in FIT-101, such as a transmitter failure or a signal outside the 4-20 mA range, a fault alarm (FAL-103) is activated, and FIC-104 transitions to manual mode. PV-103 will move to its fail-closed position to isolate the feedstock supply. The operator must investigate and resolve the fault before resuming automatic control.

If XV-106 fails to open or its position feedback is invalid, an interlock alarm (IAL-101) is triggered, and FIC-104 is disabled. The system will not allow control to resume until XV-106 is confirmed open.


## 3 **Column 1 and Reboiler**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-004  | Flow Controller       | Controls flow rate in the process line          |
|LIC-106 | Level Controller      | Maintains liquid level in Column 1              |
|LT-105  | Level Transmitter     | Measures liquid level in Column 1               |
|LV-104  | Level Valve           | Regulates liquid outflow from Column 1          |
|TIC-101 | Temperature Controller| Controls temperature in Column 1                |
|TIT-103 | Temperature Transmitter| Measures temperature in Column 1               |
|XV-102  | On-Off Valve          | Controls steam flow to the reboiler             |


### 3.1) Control Strategy Description

The temperature control of Column 1 is managed by TIC-101, which receives a process variable (PV) from TIT-103. The setpoint (SP) for TIC-101 is configured at 180°C to maintain optimal separation conditions. TIC-101 operates in reverse-acting mode, where an increase in PV results in a decrease in the manipulated variable (MV) to control the steam flow to the reboiler.

The PID tuning parameters for TIC-101 are defined as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.1 minutes. The controller output (MV) ranges from 0% to 100%, corresponding to a 4-20mA signal to the final control element, XV-102. The temperature transmitter, TIT-103, has a measurement span of 0°C to 250°C and outputs a 4-20mA signal to TIC-101.

The liquid level in Column 1 is controlled by LIC-106, which receives the PV from LT-105. The SP is set at 50% of the column height to ensure steady operation. LIC-106 operates in direct-acting mode, where an increase in PV results in an increase in MV to LV-104. The PID tuning parameters for LIC-106 are: Kp = 2.5, Ki = 0.9 minutes, and Kd = 0.0 minutes. The level transmitter, LT-105, has a range of 0% to 100% and outputs a 4-20mA signal.

Both TIC-101 and LIC-106 include bumpless transfer logic to ensure smooth transitions between manual and automatic modes. The SP for TIC-101 is clamped between 170°C and 190°C, while the SP for LIC-106 is clamped between 40% and 60% to maintain process stability. Anti-windup protection is implemented in both controllers to prevent integral term saturation.


### 3.2) Interlocks and Permissives

The operation of TIC-101 is interlocked with the status of XV-102. If XV-102 fails to respond within 5 seconds of a control signal, TIC-101 will automatically switch to manual mode, and an operator alarm will be generated. Additionally, TIC-101 will not activate unless the feed flow to Column 1, as monitored by FC-4, is above 10% of its design capacity.

LIC-106 is interlocked with LV-104 such that if LV-104 fails in the closed position (fail-closed configuration), LIC-106 will hold its output at 0% to prevent overfilling of Column 1. A permissive is configured to ensure that LIC-106 cannot operate unless the reboiler steam flow, controlled by TIC-101, is active.

A 21-second delay is implemented in the control logic of TIC-101 to prevent false activation during transient conditions, such as startup or feed composition changes. Similarly, LIC-106 includes a 15-second delay to avoid oscillations caused by rapid level fluctuations.


### 3.3) Alarm and Fault Handling

High-temperature and low-temperature alarms for Column 1 are configured at 200°C and 160°C, respectively, based on the PV from TIT-103. If the high-temperature alarm is triggered, TIC-101 will immediately reduce its output to 0%, closing XV-102 to cut off steam flow. Conversely, a low-temperature alarm will generate an operator notification but will not alter the controller output.

For LIC-106, high-level and low-level alarms are set at 80% and 20% of the column height, respectively, based on the PV from LT-105. A high-level alarm will immediately close LV-104 to prevent overflow, while a low-level alarm will generate an operator notification without altering the controller output.

In the event of a transmitter fault in TIT-103 or LT-105, the respective controllers (TIC-101 or LIC-106) will freeze their outputs at the last valid value and generate a fault alarm. Manual intervention will be required to restore normal operation.


## 4 **Decanter 1**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-004   | Flow Controller       | Regulates flow to decanter system to prevent overcapacity. |
|FIT-103  | Flow Transmitter      | Measures flow rate for upstream control loop.             |
|FTL-101  | Level Transmitter Low | Low-level measurement for decanter system.                |
|LAH-101  | Level Alarm High      | High-level alarm for decanter overflow protection.        |
|LAL-101  | Level Alarm Low       | Low-level alarm for decanter underfill protection.        |
|LIC-101  | Level Controller      | Maintains liquid level in decanter by controlling PV-102. |
|LT-104   | Level Transmitter     | Measures liquid level in decanter for LIC-101 control.    |
|PV-102   | Pressure Valve        | Controls liquid drainage from decanter system.            |


### 4.1) Control Strategy Description

The Decanter 1 system is designed to separate liquid phases from the overhead product of Column 1. Level control is implemented via LIC-101, which maintains the liquid level within the decanter by manipulating the opening of PV-102. The process variable (PV) is the liquid level measured by LT-104, and the manipulated variable (MV) is the valve position of PV-102. The setpoint (SP) for LIC-101 is configured at 65% of the decanter level, with an allowable operating range between 20% and 88% to ensure safe operation.

LIC-101 operates in reverse-acting mode, as an increase in the level (PV) requires the valve (PV-102) to open further to drain liquid. The PID tuning parameters for LIC-101 are as follows: proportional gain (Kp) = 1.8, integral time (Ki) = 0.6 minutes, and derivative time (Kd) = 0.1 minutes. The controller output (CO) is limited to a range of 0% to 100% to match the valve actuator signal.

The level measurement from LT-104 is transmitted as a 4-20mA signal corresponding to a level range of 0-5 meters. This signal is normalized to a 0-100% scale within LIC-101. The control valve PV-102 is a pneumatically actuated globe valve with a fail-closed configuration to prevent overfilling in the event of an actuator failure.


### 4.2) Interlocks and Permissives

The operation of LIC-101 is interlocked with the upstream flow control loop FC-4 to ensure that the decanter does not exceed its design capacity. If FIT-103 detects a flow rate exceeding 120% of the decanter's maximum design flow (measured as 0-50 m³/h), LIC-101 will automatically override the setpoint to 50% to reduce the risk of overflow.

A permissive is implemented to prevent PV-102 from opening unless LT-104 indicates a level above 10%. This ensures that the valve does not operate in dry conditions, which could lead to cavitation or mechanical damage.


### 4.3) Alarm and Fault Handling

High and low-level alarms are configured on LIC-101. A high-level alarm (LAH-101) is triggered when LT-104 measures a level above 90%, and a low-level alarm (LAL-101) is triggered when the level falls below 15%. Both alarms are transmitted to the operator interface for immediate attention.

In the event of a fault in LT-104, such as a signal loss or invalid reading, LIC-101 will enter manual mode, and PV-102 will default to a fail-closed position. The operator will be notified via a fault alarm (FTL-101) on the HMI. A bumpless transfer mechanism is implemented in LIC-101 to ensure a smooth transition between manual and automatic modes without introducing process disturbances.


## 5 **Column 2 and Reboiler**
|Tagname | Type | Description |
|---------|------|-------------|
|FV-105 | Flow Valve | Regulates steam flow to the reboiler for temperature control |
|LIC-107 | Level Controller | Maintains liquid level in Column 2 |
|LT-107 | Level Transmitter | Measures liquid level in Column 2 |
|LV-102 | Level Valve | Controls liquid discharge from Column 2 |
|TIC-106 | Temperature Controller | Regulates reboiler temperature using steam flow |
|TIT-106 | Temperature Transmitter | Measures reboiler temperature for feedback control |


### 5.1) Control Strategy Description

The control of Column 2 and its associated reboiler is implemented using PID feedback loops to maintain stable process conditions. The primary control objectives are to regulate the temperature of the reboiler using steam flow and to maintain the liquid level in Column 2.

**Temperature Control:**
The reboiler temperature is controlled by the temperature control loop with the tagname TIC-106. The process variable (PV) is measured by TIT-106, which has a calibrated range of 0 to 300°C and outputs a 4-20mA signal. The setpoint (SP) for TIC-106 is operator-adjustable within the range of 150°C to 250°C, with a default setpoint of 200°C. The controller is configured as reverse acting since an increase in temperature requires a decrease in steam flow. The PID tuning parameters are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.2 minutes. The manipulated variable (MV) from TIC-106 modulates the position of FV-105, a fail-closed valve, which regulates the steam flow to the reboiler. The valve position is limited to a range of 0-100% to prevent overdriving the actuator. Bumpless transfer is implemented for smooth transitions between automatic and manual modes.

**Level Control:**
The liquid level in Column 2 is maintained by the level control loop LIC-107. The PV is provided by LT-107, which measures the column level with a range of 0-100% and outputs a 4-20mA signal. The SP for LIC-107 is set to 50% of the column height, with clamping to prevent values outside the range of 25% to 75%. The controller is direct acting, as an increase in level requires an increase in liquid outflow. The PID tuning parameters are configured as Kp = 2.5, Ki = 1.0 minutes, and Kd = 0.0 minutes. LIC-107 modulates LV-102, a fail-open valve, to control the outflow of liquid from Column 2. The valve is designed to fully close at 0% MV and fully open at 100% MV. Anti-windup logic is included to prevent integral accumulation when the valve is at its limits.


### 5.2) Interlocks and Permissives

To ensure safe operation, the following interlocks and permissives are implemented:
1. The steam flow control valve FV-105 will not open unless the reboiler condensate return valve is confirmed open. This is achieved through a permissive signal from a limit switch on the condensate return system.
2. The level control valve LV-102 is interlocked to close if the level in Column 2, as measured by LT-107, falls below 10% to prevent pump cavitation.
3. The temperature control loop TIC-106 includes a high-temperature interlock that shuts FV-105 if the temperature measured by TIT-106 exceeds 275°C.
4. Manual override of LIC-107 is only permitted when the level in Column 2 is within the range of 30% to 70%, as verified by LT-107.


### 5.3) Alarm and Fault Handling

The following alarms and fault-handling mechanisms are configured for Column 2 and the reboiler:
1. A high-temperature alarm (TIT-106-HI) is triggered if the temperature exceeds 260°C, providing early warning before the high-temperature interlock activates.
2. A low-level alarm (LT-107-LO) is activated if the column level drops below 20%, alerting operators to potential liquid depletion.
3. A high-level alarm (LT-107-HI) is generated if the level exceeds 80%, indicating potential overflow conditions.
4. In the event of a transmitter fault (e.g., TIT-106 or LT-107 signal loss), the associated control loops (TIC-106 and LIC-107) will switch to manual mode with the last known MV held constant. An alarm will be generated to notify operators of the fault.
5. All alarms are configured with a 5-second delay to prevent nuisance trips due to transient conditions.

This control strategy ensures stable operation of Column 2 and its reboiler while maintaining safety and process efficiency.


## 6 **Separator**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-006 | Flow Controller | Regulates liquid flow to maintain separator level |
|FV-103 | Flow Valve | Controls heat input to separator for temperature regulation |
|LIC-102 | Level Controller | Maintains liquid level in separator at setpoint |
|LT-102 | Level Transmitter | Measures liquid level in separator |
|PIC-501 | Pressure Controller | Regulates separator pressure at setpoint |
|PIT-104 | Pressure Transmitter | Measures separator pressure |
|TI-006 | Temperature Transmitter | Provides temperature measurement for separator control |
|TIC-101 | Temperature Controller | Controls separator temperature via heat input adjustment |


### 6.1) Control Strategy Description

The Separator section employs PID control to maintain stable temperature, pressure, and level conditions for effective phase separation. Temperature control is achieved using TIC-101, which regulates the heat input to the separator via FV-103. TIC-101 operates in direct-acting mode to increase heating when the temperature falls below the setpoint. The temperature setpoint (SP) is fixed at 145°C, with a proportional gain (Kp) of 2.0, integral time (Ki) of 0.5 minutes, and derivative time (Kd) of 0.1 minutes. The temperature transmitter (TI6) provides a 4-20mA signal corresponding to a measurement span of 100°C to 200°C. The control output (MV) drives FV-103, which is a fail-closed valve to ensure safety during system faults.

Pressure control is managed by PIC-501, which maintains a setpoint of 1.5 bar using feedback from PIT-104. PIC-501 operates in reverse-acting mode, reducing pressure when the process variable exceeds the setpoint. The pressure transmitter (PIT-104) provides a 4-20mA signal over a range of 0 bar to 3 bar. The PID tuning parameters for PIC-501 are Kp=1.5, Ki=0.8 minutes, and Kd=0.2 minutes. The control output adjusts a vent valve (not shown in the diagram) with fail-open characteristics.

Level control is implemented using LIC-102, which regulates the liquid level in the separator via FC-6. LIC-102 operates in direct-acting mode, increasing flow through FC-6 when the level drops below the setpoint of 60%. The level transmitter (LT-102) provides a 4-20mA signal corresponding to a span of 0% to 100%. The PID tuning parameters for LIC-102 are Kp=3.0, Ki=1.0 minutes, and Kd=0.0 minutes. FC-6 is a fail-closed control valve to prevent over-drainage during system failures.

Bumpless transfer is enabled for all controllers to ensure smooth transitions between manual and automatic modes. A deadband of ±2% is applied to all control loops to prevent unnecessary control actions during steady-state operation.


### 6.2) Interlocks and Permissives

The Separator section includes interlocks to ensure safe operation. TIC-101 is interlocked with a high-temperature alarm from TI6, which trips the heating system if the temperature exceeds 160°C. Similarly, PIC-501 is interlocked with a high-pressure alarm from PIT-104, which activates a relief valve if the pressure exceeds 2.5 bar. LIC-102 is interlocked with a low-level alarm from LT-102, which shuts down FC-6 if the level drops below 20% to prevent pump cavitation.

Permissives include a requirement for the separator feed valve to be open before any control loops are activated. Additionally, the heating system controlled by TIC-101 requires confirmation of flow through FC-6 to prevent overheating during stagnant conditions.


### 6.3) Alarm and Fault Handling

The Separator section includes alarm handling for critical faults. High-temperature alarms are triggered when TI6 exceeds 160°C, initiating a shutdown of FV-103 and alerting operators. High-pressure alarms from PIT-104 at 2.5 bar activate a relief valve and send a fault signal to the DCS. Low-level alarms from LT-102 at 20% disable FC-6 and initiate an emergency feed cutoff to prevent equipment damage.

Fault handling includes automatic switching of controllers to manual mode during transmitter failures. For TIC-101, a transmitter fault in TI6 sets the controller output to a default bias of 50% to maintain approximate heating. Similarly, PIC-501 defaults to 25% vent opening during PIT-104 faults, and LIC-102 defaults FC-6 to 50% open during LT-102 faults. Operators are notified via the DCS for immediate corrective action.


## 7 **Column 3 and Reboiler**
|Tagname | Type | Description |
|---------|------|-------------|
|LI-003   | Level Transmitter     | Measures liquid level in Column 3 with 0–100% range output. |
|LIC-101  | Level Controller      | Maintains liquid level in Column 1 at setpoint.             |
|LIC-103  | Level Controller      | Controls liquid outlet flow to maintain Column 3 level.    |
|TI-008   | Temperature Transmitter | Measures Column 3 temperature with 0–250°C range.          |
|TIC-106  | Temperature Controller | Regulates steam flow to reboiler to control Column 3 temperature. |
|XV-104   | On-Off Valve          | Modulates liquid outlet flow from Column 3.                |
|XV-105   | On-Off Valve          | Controls steam flow to reboiler for Column 3 temperature regulation. |


### 7.1) Control Strategy Description

The temperature within Column 3 is controlled by TIC-106, which regulates the steam flow to the associated reboiler via XV-105. TIC-106 operates as a reverse-acting PID controller to maintain the column temperature at the setpoint of 180°C. The process variable (PV) is provided by TI8, which measures the column temperature with a transmitter range of 0–250°C and outputs a 4–20mA signal. The manipulated variable (MV) from TIC-106 adjusts the position of XV-105, a fail-closed control valve, with an actuator range of 0–100% open.

PID tuning parameters for TIC-106 are configured as follows: proportional gain (Kp) = 3.2, integral time (Ki) = 1.0 min, and derivative time (Kd) = 0.3 min. The controller output range is clamped between 5–95% to prevent overcorrection. Bumpless transfer is enabled to ensure seamless switching between manual and automatic modes. Signal scaling is applied to normalize the input from TI8 to match the controller input range.

The level within Column 3 is maintained by LIC-103, which controls the liquid outlet flow via XV-104. LIC-103 is configured as a direct-acting PID controller with a setpoint of 70% level. The PV is derived from LI3, which has a measurement span of 0–100% and outputs a 4–20mA signal. The MV modulates XV-104, a fail-open valve, with a control range of 0–100% open. PID tuning parameters for LIC-103 are set as follows: Kp = 2.5, Ki = 0.8 min, and Kd = 0.1 min. Anti-windup logic is implemented to prevent integral accumulation during saturation events.


### 7.2) Interlocks and Permissives

Steam flow control through XV-105 is inhibited unless the column temperature, as measured by TI8, is below 200°C to prevent overheating. Additionally, TIC-106 output is locked at 0% if the reboiler condensate level, monitored by LIC-101, exceeds 85% to avoid flooding. The startup sequence for Column 3 requires a permissive signal from LIC-103 indicating the column level is above 30% and a delay of 12 seconds after the start command to ensure proper stabilization.

XV-104 is interlocked to close if the column level, as measured by LI3, falls below 15% to prevent pump cavitation. The control logic includes a deadband of ±2% around the LIC-103 setpoint to minimize hunting. Both TIC-106 and LIC-103 are configured with mode selection logic to allow manual override during maintenance operations.


### 7.3) Alarm and Fault Handling

High-temperature alarms are triggered when TI8 exceeds 195°C, and an emergency shutdown signal is sent to close XV-105 if the temperature reaches 210°C. TIC-106 generates a fault alarm if the PV deviates from the SP by more than 10°C for over 30 seconds. Low-level alarms are activated when LI3 falls below 10%, with LIC-103 entering a fault mode that locks XV-104 at 0% open.

In the event of transmitter failure for TI8 or LI3, TIC-106 and LIC-103 default to manual mode with their outputs frozen at the last known value. Diagnostic alarms are raised for signal loss or transmitter calibration errors. Alarm acknowledgment is required before resuming automatic control, and fault conditions are logged for maintenance review.


## 8 **Decanter 2**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-008  | Flow Controller       | Maintains constant product flow rate downstream of Decanter 2 |
|FIT-105 | Flow Transmitter      | Measures flow rate with a range of 0-150 L/min               |
|LIC-106 | Level Controller      | Regulates Decanter 2 liquid level by modulating XV-101       |
|LT-102  | Level Transmitter     | Provides level measurement for Decanter 2                   |
|LT-103  | Level Transmitter     | Additional level measurement (context not specified)        |
|LT-107  | Level Transmitter     | Additional level measurement (context not specified)        |
|PV-104  | Pressure Valve        | Pressure control valve (context not specified)              |
|XV-101  | On-Off Valve          | Modulates flow to control Decanter 2 level, fail-closed     |


### 8.1) Control Strategy Description

The decanter level control is implemented using LIC-106, which regulates the liquid level in Decanter 2 by modulating XV-101. The process variable (PV) is the level measurement provided by LT-102, with a transmitter range of 0-100% corresponding to a 4-20mA signal. The setpoint (SP) for LIC-106 is fixed at 65% to maintain optimal separation efficiency. LIC-106 is configured as a reverse-acting controller, ensuring that an increase in level decreases the valve opening.

PID tuning parameters for LIC-106 are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.0 minutes. The controller output (MV) is clamped between 0% and 100%, with bumpless transfer logic implemented for smooth transitions between manual and automatic modes. Anti-windup protection is enabled to prevent integral windup during saturation conditions.

XV-101 is a fail-closed valve, ensuring safety in the event of actuator or signal failure. The valve response time is calibrated for a settling time of 10 seconds to minimize oscillations. Signal scaling is applied to normalize the LT-102 output range to match the LIC-106 input requirements.

Flow regulation is managed by FC-8, which maintains a constant product flow rate downstream of Decanter 2. FIT-105 provides the flow measurement, with a transmitter range of 0-150 L/min corresponding to a 4-20mA signal. FC-8 is configured as a direct-acting PID controller with tuning parameters set to Kp = 2.5, Ki = 0.8 minutes, and Kd = 0.2 minutes. The SP for FC-8 is fixed at 120 L/min, and the controller output modulates PV-104, a fail-open control valve.


### 8.2) Interlocks and Permissives

The operation of LIC-106 is interlocked with LT-103 to prevent overflow conditions. If LT-103 detects a level exceeding 90%, LIC-106 output is forced to 0%, fully closing XV-101. Similarly, FIT-105 is interlocked with LT-107 to ensure adequate flow conditions; if LT-107 detects a level below 20%, FC-8 output is forced to 0%, closing PV-104.

Permissives for LIC-106 include confirmation that LT-102 is transmitting a valid signal within its calibrated range (4-20mA). If LT-102 signal is lost or falls outside the range, LIC-106 enters manual mode, and XV-101 is closed. FC-8 operation is permitted only when FIT-105 signal is valid and Decanter 2 is online.

A 14-second delay is imposed on LIC-106 and FC-8 activation following system startup to allow stabilization of upstream conditions. Mode selection logic ensures that manual overrides on LIC-106 and FC-8 are prioritized during maintenance operations.


### 8.3) Alarm and Fault Handling

High-level alarms are triggered by LT-103 when the level in Decanter 2 exceeds 85%, generating an audible and visual alert in the control room. Low-level alarms are activated by LT-107 if the level drops below 15%, indicating potential flow disruption. FIT-105 generates a flow deviation alarm if the measured flow deviates by more than ±10% from the setpoint.

Fault conditions for LIC-106 include transmitter failure from LT-102 or valve actuator failure on XV-101. In either case, LIC-106 output is forced to 0%, closing XV-101. FC-8 fault conditions include signal loss from FIT-105 or actuator failure on PV-104, resulting in FC-8 output being forced to 100%, fully opening PV-104 to ensure bypass flow.

Alarm acknowledgment requires operator intervention, and system reset logic ensures that LIC-106 and FC-8 resume normal operation only after fault conditions are cleared.


## 9 **Condenser Systems**
|Tagname | Type | Description |
|---------|------|-------------|
|FI-103   | Flow Transmitter   | Measures flow rate of cooling medium through condenser system. |
|FIC-103  | Flow Controller    | Regulates cooling medium flow to maintain overhead vapor temperature. |
|LC-002   | Level Controller   | Controls liquid level in associated vessel or system. |
|LV-102   | Level Valve        | Adjusts cooling medium flow rate based on controller output. |
|TIT-101  | Temperature Transmitter | Measures temperature of overhead vapors in condenser system. |
|XV-104   | On-Off Valve       | Ensures cooling medium supply is open before LV-102 operation. |


### 9.1) Control Strategy Description

The condenser system utilizes PID control to regulate the flow rate of cooling medium through the condenser to maintain a stable temperature of overhead vapors. The process variable (PV) is the temperature measured by TIT-101, with the setpoint (SP) defined at 45°C. The manipulated variable (MV) is the position of LV-102, which adjusts the flow rate of the cooling medium. The PID controller, FIC-103, is configured as reverse-acting to ensure that an increase in temperature results in an increase in cooling medium flow.

The PID tuning parameters for FIC-103 are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 min, and derivative time (Kd) = 0.3 min. The controller output range is normalized to 0-100% to correspond to the valve position signal, which operates on a 4-20mA scale. The temperature transmitter TIT-101 has a measurement span of 0-100°C with a 4-20mA output signal.

The final control element, LV-102, is a fail-closed valve to ensure cooling medium flow stops during a fault condition. Bumpless transfer logic is implemented to allow smooth transitions between manual and automatic modes. A 2% deadband is applied to reduce valve oscillation during steady-state operation.


### 9.2) Interlocks and Permissives

The operation of LV-102 is interlocked with XV-104, a shut-off valve upstream of the cooling medium supply. XV-104 must be in the open position before LV-102 can modulate. TIT-101 must provide a valid signal within the transmitter range (0-100°C) for the PID control loop to operate. If TIT-101 fails or provides an out-of-range signal, FIC-103 will default to manual mode, and LV-102 will move to its fail-closed position.

Permissive logic ensures that the condenser system operates only when the distillation column is active, as indicated by a valid level signal from LC-002. Additionally, the cooling medium pump must be running, verified by a flow signal from FI-103, before LV-102 can modulate.


### 9.3) Alarm and Fault Handling

An alarm is triggered if TIT-101 detects a temperature above 55°C, indicating potential condenser inefficiency. A high-high temperature alarm at 60°C will initiate an emergency shutdown sequence, closing XV-104 and LV-102 to prevent damage to downstream equipment.

If TIT-101 fails or provides a signal outside its calibrated range, an instrument fault alarm is activated, and FIC-103 enters manual mode. LV-102 will move to its fail-closed position to halt cooling medium flow. Additionally, a low-flow alarm from FI-103 (<5% of the flow range) will disable LV-102 modulation and close XV-104 to protect the pump from dry running.

Response times for fault detection and alarm activation are configured at 2 seconds to ensure rapid corrective action. Settling time for the PID loop is targeted at 10 seconds under normal operating conditions, ensuring stable temperature control without excessive oscillation.


## 10 **Product Flow Control**
|Tagname | Type | Description |
|---------|------|-------------|
|FAH-102 | Flow Alarm High | High flow alarm for process stream protection |
|FAL-102 | Flow Alarm Low | Low flow alarm to prevent insufficient process flow |
|FIF-102 | Flow Interlock | Interlock to prevent operation under unsafe flow conditions |
|FIT-102 | Flow Transmitter | Measures flow rate for PID control loop |
|IIC-103 | Flow Controller | PID controller for maintaining flow rate setpoint |
|LC-002 | Level Controller | Regulates tank level within safe operating limits |
|LIH-201 | Level Alarm High | High level alarm for storage tank overflow prevention |
|LT-201 | Level Transmitter | Measures storage tank level for monitoring and control |
|LV-101 | Level Valve | Pneumatically actuated valve for controlling tank level |
|VAF-101 | Valve Alarm Failure | Alarm indicating valve failure condition |


### 10.1) Control Strategy Description

The flow control strategy for the product stream utilizes a PID feedback loop to maintain the flow rate at the desired setpoint. The process variable (PV) is the flow rate measured by FIT-102, which has a calibrated range of 0-200 m³/h and outputs a 4-20 mA signal. The manipulated variable (MV) is the position of the control valve LV-101, which is pneumatically actuated and configured to fail-closed on loss of signal.

The PID controller, IIC-103, operates in reverse-acting mode to decrease the valve opening as the flow rate increases above the setpoint. The controller is tuned with the following parameters: proportional gain (Kp) of 1.8, integral time (Ki) of 0.5 minutes, and derivative time (Kd) of 0.1 minutes. The controller output (CO) is clamped between 0% and 100% to ensure the valve operates within its physical limits. The operator-defined setpoint (SP) is limited between 40 m³/h and 180 m³/h to maintain safe operating conditions and prevent overloading downstream processes.

The raw 4-20 mA signal from FIT-102 is linearly scaled to engineering units (m³/h) within IIC-103 for control calculations. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes, preventing process disturbances.


### 10.2) Interlocks and Permissives

The control loop is interlocked with the downstream storage tank level to prevent overflow. If the level in the storage tank, as measured by LT-201, exceeds 90% of its maximum capacity, a high-level interlock (LIH-201) forces LV-101 to fully close, overriding the PID control. Additionally, the system requires a permissive signal from the upstream decanter (LC-002) to ensure sufficient product availability. If the level in the decanter drops below 10%, the permissive is removed, and the control valve LV-101 is forced to the closed position.

The control loop also includes a startup permissive that ensures the flow rate is within 10% of the setpoint before enabling automatic control. This prevents abrupt changes in valve position during process initialization.


### 10.3) Alarm and Fault Handling

The system generates a high-flow alarm (FAH-102) if the flow rate measured by FIT-102 exceeds 190 m³/h, indicating potential process instability or valve malfunction. A low-flow alarm (FAL-102) is triggered if the flow rate falls below 30 m³/h, signaling potential upstream supply issues. Both alarms are displayed on the operator interface and logged for diagnostic purposes.

In the event of a fault in FIT-102, such as signal loss or transmitter failure, the PID controller IIC-103 enters manual mode, and the control valve LV-101 is driven to a fail-safe position (fully closed). An alarm (FIF-102) is generated to notify the operator of the transmitter fault. The system also includes diagnostics for the control valve actuator. If LV-101 fails to respond to control signals, a valve fault alarm (VAF-101) is activated, and the loop is locked out until manual intervention resolves the issue.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 10

- Total Tagnames: 58

- Word Count: 5921
