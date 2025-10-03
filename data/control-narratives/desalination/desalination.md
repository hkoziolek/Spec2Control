# Desalination Plant Intake System Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Seawater and Reservoir Intake Pipelines**
3. **Intake Screens and Air-Blast Cleaning System**
4. **Intake Pumps and Sump Pumps**
5. **Shock Chlorination System**
6. **Sampling and Bypass Flow Systems**

---


## 1 **Process Overview and Scope**

The desalination plant intake system is designed to abstract feed water from seawater or reservoir sources, ensuring a reliable and controlled supply to downstream processes. The primary objective of the system is to maintain consistent water quality and flow while protecting downstream equipment and the surrounding environment. This is achieved through a combination of automated monitoring, interlocks, and coordinated control strategies. The system operates in distinct phases, including water abstraction, debris removal, flow regulation, biofouling prevention, and water quality monitoring, all of which are integrated to ensure seamless operation and adaptability to varying plant demands.

The process begins with dedicated intake pipelines for seawater and reservoir sources, equipped with pollution analyzers to safeguard water quality and enable immediate shutdown in contamination events. Intake screens remove debris and protect aquatic life, with periodic air-blast cleaning sequences maintaining screen efficiency. Variable frequency drive (VFD) pumps regulate the flow of feed water, dynamically adjusting to plant requirements and ensuring operational flexibility. Supporting systems, such as sump pumps for flood protection and shock chlorination for biofouling control, work in tandem to enhance reliability and water quality. Sampling and bypass systems provide continuous monitoring and operational redundancy, ensuring the intake system meets performance and safety criteria.

To achieve these control objectives, the system employs automated sequences, permissives, and interlocks that govern the operation of all equipment. These strategies ensure that each subsystem operates within defined parameters, preventing equipment damage and process interruptions. Alarms and status definitions provide operators with real-time feedback, enabling prompt responses to deviations. Safety is a critical consideration throughout all process phases, with features such as pollution shutdowns, redundant equipment, and fail-safe mechanisms integrated to protect both the plant and the environment. The overall design ensures a balance of high efficiency, operational reliability, and compliance with regulatory standards.


## 2 **Seawater and Reservoir Intake Pipelines**
|Tagname | Type | Description |
|---------|------|-------------|
|AT-101 | Analyzer Transmitter | Measures specific process parameters for seawater pipeline analysis |
|AT-103 | Analyzer Transmitter | Monitors reservoir pipeline quality parameters |
|FC-101 | Flow Controller | Regulates seawater pipeline flow using PID control logic |
|FC-102 | Flow Controller | Controls reservoir pipeline flow via PID algorithm |
|FT-101 | Flow Transmitter | Measures flow rate in the seawater pipeline (0-5000 m³/h) |
|FT-102 | Flow Transmitter | Monitors flow rate in the reservoir pipeline (0-3000 m³/h) |
|FV-101 | Flow Valve | Adjusts seawater pipeline flow; pneumatically actuated, fail-closed |
|FV-102 | Flow Valve | Modulates reservoir pipeline flow; pneumatically actuated, fail-closed |
|LT-104 | Level Transmitter | Measures liquid level in associated reservoir or tank |
|LT-105 | Level Transmitter | Monitors liquid level for process control or safety |
|XV-102 | On-Off Valve | Provides isolation for reservoir pipeline during maintenance or emergencies |


### 2.1) Control Strategy Description

The control logic for the seawater and reservoir intake pipelines utilizes a PID control algorithm to regulate the flow rate of water through the respective pipelines. The process variable (PV) is the flow rate measured by the flow transmitter FT-101 for the seawater pipeline and FT-102 for the reservoir pipeline. The operator-defined setpoint (SP) for flow is clamped between 16% and 75% of the transmitter range to maintain safe operating conditions. The manipulated variable (MV) is the position of the flow control valves FV-101 and FV-102, which are pneumatically actuated and fail-closed upon loss of control signal.

For the seawater pipeline, the PID controller (FC-101) is configured as reverse-acting to ensure that an increase in flow setpoint results in an increase in the valve opening. The tuning parameters for FC-101 are set as follows: proportional gain (Kp) = 2.5, integral time (Ki) = 0.8 minutes, and derivative time (Kd) = 0.2 minutes. The controller output is limited to a range of 0% to 100% to prevent overdriving the actuator. The transmitter FT-101 has a calibrated range of 0 to 5000 m³/h and provides a 4-20 mA signal to the controller.

For the reservoir pipeline, the PID controller (FC-102) operates with identical tuning parameters: Kp = 2.5, Ki = 0.8 minutes, and Kd = 0.2 minutes. The transmitter FT-102 has a calibrated range of 0 to 3000 m³/h and also provides a 4-20 mA signal. The control output adjusts the position of FV-102, which is similarly pneumatically actuated and fails closed.

Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes. In manual mode, the operator can directly adjust the valve position, while in automatic mode, the PID controller maintains the flow rate at the setpoint. Anti-windup protection is enabled by clamping the integral term to prevent excessive accumulation during output saturation.


### 2.2) Interlocks and Permissives

The operation of the flow control valves FV-101 and FV-102 is subject to several interlocks and permissives to ensure safe and reliable operation. The valves will not open unless the corresponding pipeline shut-off valve (XV-102) is confirmed to be in the fully open position, as indicated by the limit switch feedback. Additionally, the associated analyzer transmitters AT-101 and AT-103 continuously monitor water quality parameters. If contamination is detected beyond the predefined threshold (e.g., turbidity > 50 NTU or salinity > 35 PSU), the control system will initiate a safe shutdown sequence by closing FV-101 and FV-102.

A low-level permissive is implemented to prevent pump cavitation. If the water level in the intake sump, as measured by LT-104, falls below 2.0 meters, the valves FV-101 and FV-102 are forced closed, and an alarm is generated. Similarly, a high-level permissive ensures that the valves do not open if the downstream storage tank level, monitored by LT-105, exceeds 95% of its capacity.


### 2.3) Alarm and Fault Handling

The control system is equipped with comprehensive alarm and fault-handling mechanisms to address abnormal conditions. High and low flow rate alarms are generated if the flow rate deviates beyond ±10% of the setpoint for more than 30 seconds. The high flow alarm is triggered at 5500 m³/h for FT-101 and 3300 m³/h for FT-102, while the low flow alarm is triggered at 450 m³/h for FT-101 and 270 m³/h for FT-102.

In the event of a transmitter fault, such as a loss of signal from FT-101 or FT-102 (signal < 3.6 mA or > 21 mA), the corresponding PID controller will enter a fail-safe mode, driving the control valve (FV-101 or FV-102) to its fail-closed position. An alarm indicating "Flow Transmitter Fault" will be displayed on the HMI.

If the analyzer transmitters AT-101 or AT-103 detect contamination, the system will trigger a "Water Quality Alarm" and execute a safe shutdown by closing the shut-off valve XV-102 and the flow control valve. The operator must acknowledge the alarm and manually reset the system after the contamination is resolved.

All alarms are logged with a timestamp and priority level. Critical alarms, such as "Contamination Detected" or "Low Sump Level," are classified as high-priority and require immediate operator intervention.


## 3 **Intake Screens and Air-Blast Cleaning System**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-104 | Flow Controller | Modulates FV-105 to achieve FT-102 setpoint based on FFIC-103 output |
|FT-101 | Flow Transmitter | Measures real-time compressed air supply rate to the air-blast system |
|FT-102 | Flow Transmitter | Measures air delivered to individual screens during cleaning bursts |
|FV-105 | Flow Valve | Regulates air flow to maintain the setpoint determined by FIC-104 |
|HIS-101 | Human-Machine Interface | Allows operator input for adjusting ratio setpoint and monitoring system |
|HMI-101 | Human-Machine Interface | Provides interface for operator control and system status visualization |
|PIT-105 | Pressure Transmitter | Measures pressure in the compressed air system for monitoring purposes |
|PIT-106 | Pressure Transmitter | Monitors pressure in the air-blast cleaning system for safety and control |
|PT-103 | Pressure Transmitter | Measures pressure upstream of the cleaning system for control feedback |
|PT-104 | Pressure Transmitter | Monitors pressure downstream of the cleaning system for operational checks |
|PT-108 | Pressure Transmitter | Provides pressure data for system diagnostics and performance analysis |


### 3.1) Control Strategy Description

The intake screens cleaning system utilizes ratio control to maintain precise proportional relationships between the compressed air flow delivered to each screen and the cleaning cycle duration. The wild flow, measured by flow transmitter FT-101, represents the real-time compressed air supply rate to the air-blast system, ranging from 0 to 500 Nm³/hr. The controlled flow, measured by flow transmitter FT-102, governs the air delivered to individual screens during cleaning bursts. Ratio controller FFIC-103 calculates the controlled flow setpoint based on the configured ratio of 2.0:1, ensuring that FT-102 setpoint equals twice the value of FT-101. The flow control loop is closed by flow controller FIC-104, which modulates control valve FV-105 to achieve the calculated setpoint.

Raw flow signals from FT-101 and FT-102 undergo linear scaling within FFIC-103 to ensure accurate ratio calculation. The ratio setpoint is adjustable between 1.5:1 and 3.0:1 via operator input through HMI-101, allowing flexibility in cleaning intensity. A low-flow cutoff is implemented such that FFIC-103 disables control if FT-101 falls below 50 Nm³/hr, preventing insufficient cleaning bursts. Hysteresis of 2% is applied to the ratio setpoint to avoid rapid oscillations near threshold values.


### 3.2) Interlocks and Permissives

The air-blast cleaning system operates under strict interlocks to ensure safe ratio control. Compressor status permissives are tied to PT-103 and PT-104, which monitor receiver pressures. If either PT-103 or PT-104 falls below 6.0 bar, FFIC-103 enters a HOLD state, freezing the ratio calculation and preventing air delivery. Additionally, FV-105 is interlocked with PIT-105 and PIT-106 to ensure that the downstream pressure remains within 4.0–8.0 bar during cleaning bursts. If PIT-105 or PIT-106 detects pressure outside this range, FV-105 closes, and FFIC-103 outputs a FAIL signal.

Boolean interlocks are implemented to prevent simultaneous cleaning of multiple screens. Cleaning sequence permissives are managed by discrete signals from SW-SCREEN-1 to SW-SCREEN-6 and RES-SCREEN-1 to RES-SCREEN-4. FFIC-103 only calculates the controlled flow setpoint for one screen at a time, ensuring proportional air delivery to the active screen. Mode selection logic ensures bumpless transfer between automatic ratio control and manual operation, verified by permissives on HMI-101.


### 3.3) Alarm and Fault Handling

Alarms are generated for deviations in ratio control and system faults. If the ratio deviates by more than 5% from the configured setpoint, FFIC-103 triggers a RATIO_DEVIATION alarm visible on HMI-101. Low-flow conditions on FT-101 below 50 Nm³/hr activate a LOW_FLOW alarm, and FFIC-103 transitions to MANUAL mode. Pressure transmitter PT-108 monitors the compressed air supply line; readings below 5.0 bar or above 9.0 bar generate a SUPPLY_PRESSURE alarm and initiate a system shutdown sequence.

Valve position feedback from FV-105 is continuously monitored. If FV-105 fails to achieve the commanded position within 2 seconds, a VALVE_FAILURE alarm is triggered, and FFIC-103 halts ratio control. In the event of multiple screen activation signals, FFIC-103 outputs a SCREEN_CONFLICT alarm, requiring operator intervention to resolve the cleaning sequence. All alarms are logged in the plant historian system (HIS-101) for diagnostic analysis.


## 4 **Intake Pumps and Sump Pumps**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-101 | Flow Controller | Regulates feedwater flow rate using PID logic |
|FT-101 | Flow Transmitter | Measures real-time feedwater flow rate in m³/h |
|LT-101 | Level Transmitter | Monitors liquid level in associated tank or vessel |
|VFD-101A | Variable Frequency Drive | Modulates pump motor speed to control flow rate |


### 4.1) Control Strategy Description

The intake pump control system utilizes PID feedback loops to regulate feedwater flow rate based on real-time demand, measured by flow transmitter FT-101. The controlled variable (PV) is the flow rate, measured in m³/h, with a transmitter range of 0–500 m³/h and a 4–20mA signal output. The setpoint (SP) for flow rate is dynamically adjustable between 100–450 m³/h, constrained by operational limits to ensure pump integrity and process stability. The final control element is the variable frequency drive (VFD) associated with each intake pump (VFD-101A/B/C/D), which modulates motor speed to achieve the desired flow rate.

The PID controller, designated as FIC-101, is configured as reverse-acting to decrease motor speed when flow exceeds the setpoint. Tuning parameters are set as follows: proportional gain (Kp) = 2.5, integral time (Ki) = 0.8 min, derivative time (Kd) = 0.2 min. The output signal (MV) to the VFD is normalized between 0–100% speed, with anti-windup logic implemented to prevent integral accumulation during saturation. Bumpless transfer logic ensures smooth transitions between manual and automatic modes, preserving control stability during operator interventions.

Raw flow signals from FT-101 are scaled linearly within the controller to provide calibrated flow values in engineering units (m³/h). A deadband of ±2 m³/h is applied to the control logic to prevent hunting during steady-state operation. The control loop achieves a typical response time of 5 seconds and a settling time of 15 seconds under nominal conditions.


### 4.2) Interlocks and Permissives

Pump operation is governed by interlocks and permissives to ensure safe and reliable performance. Each intake pump (P101A/B/C/D) is interlocked with level transmitter LT-101, which monitors sump water level with a range of 0–10 meters and a 4–20mA signal. Pumps are permitted to start only if the sump level is above 2.0 meters (low-level permissive) and below 8.0 meters (high-level permissive). If LT-101 detects a level outside this range, the controller FIC-101 inhibits pump operation by setting the VFD output (MV) to 0%.

Automatic pump changeover logic is implemented to alternate between duty and standby pumps (P101A/B/C/D) based on runtime hours. If a duty pump trips or exceeds 500 runtime hours, the standby pump is activated, and the tripped pump is locked out until manually reset. Leak detection sensors on each pump casing provide additional permissives; a detected leak disables the corresponding VFD and triggers an alarm.

Sump pumps SPUMP-201A/B are interlocked with LT-101 to maintain sump level within acceptable limits. If the sump level exceeds 8.5 meters, SPUMP-201A/B are activated to prevent flooding, overriding normal intake pump operation by shutting down P101A/B/C/D.


### 4.3) Alarm and Fault Handling

The control system generates alarms for deviations in process variables and equipment faults. If the flow rate measured by FT-101 deviates from the setpoint by more than ±10 m³/h for over 30 seconds, a "Flow Deviation" alarm is triggered, prompting operator intervention. If the sump level measured by LT-101 falls below 1.5 meters or exceeds 9.0 meters, a "Sump Level Critical" alarm is raised, and all intake pumps (P101A/B/C/D) are shut down to prevent damage.

Pump motor faults, such as overcurrent or overheating detected by motor protection relays (M103A/B/C/D), immediately stop the affected pump and trigger a "Pump Motor Fault" alarm. Leak detection sensors on pump casings activate a "Pump Leak Detected" alarm and disable the corresponding VFD output.

In the event of a controller failure or communication loss between FIC-101 and FT-101, the system defaults to manual mode, with operator control of VFD speed via HMI. A "Controller Fault" alarm is displayed, and bumpless transfer logic ensures smooth transition to manual operation without disrupting flow rate.


## 5 **Shock Chlorination System**
|Tagname | Type | Description |
|---------|------|-------------|
|ANK-301 | Interlock | Ensures system safety by preventing unauthorized operation. |
|FAH-301 | Flow Alarm High | High flow rate alarm for process protection. |
|FAL-301 | Flow Alarm Low | Low flow rate alarm for process protection. |
|FIC-301 | Flow Controller | Regulates flow rate to maintain setpoint in shock chlorination system. |
|FT-301 | Flow Transmitter | Measures flow rate for sodium hypochlorite dosing control. |
|FV-301 | Flow Valve | Modulates flow rate in the chlorination process. |
|LAL-301 | Level Alarm Low | Low level alarm for tank monitoring. |
|LT-301 | Level Transmitter | Measures liquid level in the storage tank. |
|PAH-103 | Pressure Alarm High | High pressure alarm for system protection. |
|PFA-301 | Pump Flow Alarm | Monitors pump flow for abnormal conditions. |
|TAH-101 | Temperature Alarm High | High temperature alarm for process safety. |
|UMP-301A | Pump | Metering pump for sodium hypochlorite dosing. |
|XV-107 | On-Off Valve | Isolation valve for emergency shutdown. |


### 5.1) Control Strategy Description

The shock chlorination system regulates sodium hypochlorite dosing by controlling the flow rate through the metering pump CHLOR-PUMP-301A/B. The process variable (PV) is the measured flow rate from flow transmitter FT-301, which has a calibrated range of 0-50 L/min and outputs a 4-20 mA signal. The setpoint (SP) for the flow rate is operator-adjustable between 10 and 45 L/min, with a default setpoint of 30 L/min.

The PID controller, designated as FIC-301, is configured for reverse-acting control, where an increase in PV results in a decrease in the manipulated variable (MV) to maintain SP. The tuning parameters for the controller are set as follows: proportional gain (Kp) = 1.8, integral time (Ki) = 0.5 minutes, and derivative time (Kd) = 0.05 minutes. The controller output (MV) modulates the stroke of CHLOR-PUMP-301A/B, with a control range of 0-100% corresponding to a flow rate of 0-50 L/min. Output limits are clamped between 5% and 95% to prevent pump underperformance or overdriving.

The final control element is the pump stroke actuator, which responds linearly to the controller output. Bumpless transfer logic ensures seamless transitions between manual and automatic modes by initializing the controller output to the current manual position upon switching to automatic mode. Anti-windup protection is implemented to freeze integral action when the output reaches its limits.

A signal scaling function normalizes the 4-20 mA input from FT-301 to a 0-100% range for the controller input. The control loop includes a 1% hysteresis band around the setpoint to prevent hunting and a 23-second delay timer to filter transient flow disturbances.


### 5.2) Interlocks and Permissives

The shock chlorination system operates only when the following permissives are satisfied: CHLOR-TANK-301 level, as measured by LT-301, must be above 20% to ensure sufficient chemical availability; CHLOR-PUMP-301A/B must be in the AVAILABLE state, verified by the pump status signal from UMP-301A. The system is interlocked with the dechlorination process to prevent simultaneous operation if downstream chlorine levels, measured by ANK-301, exceed 0.5 ppm.

The flow control valve FV-301 is interlocked to fail-closed upon detection of a high-pressure condition (PAH-103) exceeding 6 bar or a high-temperature condition (TAH-101) exceeding 50°C. Additionally, the system will not start if the shut-off valve XV-107 is not in the fully open position, as confirmed by its limit switch.


### 5.3) Alarm and Fault Handling

The system generates a high-flow alarm (FAH-301) if the flow rate exceeds 48 L/min and a low-flow alarm (FAL-301) if the flow rate falls below 8 L/min for more than 10 seconds. Both alarms are latched and require operator acknowledgment to reset. A pump fault alarm (PFA-301) is triggered if CHLOR-PUMP-301A/B fails to start within 5 seconds of a run command or if the pump trips during operation.

In the event of a tank low-level condition (LAL-301) below 10%, the system shuts down the pump and closes FV-301 to prevent air ingress. If the dechlorination interlock is active due to high chlorine levels downstream, an alarm (DCLH-301) is raised, and the chlorination system is disabled until the chlorine concentration drops below 0.3 ppm for 60 seconds.


## 6 **Sampling and Bypass Flow Systems**
|Tagname | Type | Description |
|---------|------|-------------|
|AT-105 | Interlock | Ensures system operation within safe parameters. |
|FIC-104 | Flow Controller | Calculates sampling flow setpoint for ratio control. |
|FIT-101 | Flow Transmitter | Measures bypass flow rate for ratio control logic. |
|FV-102 | Flow Control Valve | Modulates sampling flow to achieve setpoint. |
|LV-103 | Level Valve | Regulates level in associated system or tank. |


### 6.1) Control Strategy Description

The Sampling and Bypass Flow System is designed to maintain a precise ratio between the bypass flow (wild flow) and the sampling flow (controlled flow) to ensure consistent water quality monitoring and pipeline flushing. Flow Indicator Transmitter FIT-101 measures the bypass flow rate, which serves as the wild flow input to the ratio control logic. The desired sampling-to-bypass flow ratio is maintained at a setpoint of 1:10 (sampling flow to bypass flow). This ratio is implemented using Flow Indicator Controller FIC-104, which calculates the sampling flow setpoint as 10% of the real-time bypass flow measured by FIT-101.

The calculated sampling flow setpoint is transmitted to Flow Control Valve FV-102, which modulates to achieve the required sampling flow. The sampling flow is measured by a dedicated flow transmitter (not shown in the current tagname list) and fed back to FIC-104 for closed-loop control. The ratio setpoint is adjustable within a range of 1:5 to 1:20 to accommodate varying operational requirements. Signal scaling is applied to FIT-101 to ensure accurate flow measurement within a range of 0-1000 m³/hr, and the calculated sampling flow setpoint is clamped between 0-200 m³/hr to prevent overdriving FV-102.


### 6.2) Interlocks and Permissives

The ratio control loop is enabled only when the bypass flow rate, as measured by FIT-101, exceeds a minimum threshold of 50 m³/hr to ensure stable operation. If the bypass flow falls below this threshold, the control loop is automatically disabled, and FV-102 is commanded to a fully closed position. A permissive signal from Analyzer Transmitter AT-105 ensures that water quality monitoring equipment is operational before enabling the sampling flow. Additionally, a permissive from Level Control Valve LV-103 ensures that adequate upstream water level is maintained before bypass flow is initiated.

In the event of a manual override, the ratio control loop is bypassed, and FV-102 can be directly manipulated by the operator. The system reverts to automatic ratio control only after the manual mode is disengaged, the bypass flow exceeds the minimum threshold, and all permissives are satisfied.


### 6.3) Alarm and Fault Handling

An alarm is triggered if the actual sampling-to-bypass flow ratio deviates by more than ±10% from the setpoint for a duration exceeding 30 seconds. This deviation alarm is displayed as "RATIO DEVIATION HIGH" or "RATIO DEVIATION LOW" on the operator interface. A fault in FIT-101, such as a loss of signal or an out-of-range condition, triggers a "FIT-101 FAULT" alarm and forces FV-102 to a fail-safe position (fully closed). Similarly, a fault in FIC-104 triggers a "FIC-104 FAULT" alarm, and the system transitions to manual mode with FV-102 held at its last valid position.

If AT-105 detects a water quality issue, a "QUALITY FAULT" alarm is raised, and the ratio control loop is disabled. In this condition, FV-102 is closed to prevent potentially contaminated water from entering the sampling system. All alarms are latched and require operator acknowledgment before the system can return to normal operation.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 6

- Total Tagnames: 39

- Word Count: 3842
