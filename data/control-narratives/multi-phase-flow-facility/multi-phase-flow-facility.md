# Multi-Phase Separation and Storage System Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **2-Phase Separator Control**
3. **3-Phase Separator Control**
4. **Oil Tank Control**
5. **Water Tank and Pump Control**
6. **Water Coalescer Control**
7. **Air Compressor Control**

---


## 1 **Process Overview and Scope**

The process is designed to manage and separate multi-phase flow streams comprising oil, water, and air, with the primary objective of ensuring efficient separation, storage, and transfer of these components while maintaining safe and reliable operations. The system is divided into distinct functional stages, including initial separation into liquid and gas phases, further refinement into individual oil, water, and air streams, and subsequent storage and handling. Key control strategies emphasize maintaining stable pressure, flow, and level conditions throughout the process to avoid disruptions and ensure consistent output quality.

The process begins with the 2-phase separator, which separates incoming mixed flow into liquid and gas streams, followed by the 3-phase separator, which further separates liquid into oil and water while segregating air streams. Separated oil and water are stored in dedicated tanks, with levels and flows monitored to support downstream operations. Water is further processed through a coalescer to remove impurities, while compressed air is supplied for system requirements. Control loops across the system regulate critical parameters such as pressure, level, and flow, leveraging transmitters and valves to ensure seamless coordination between process stages.

Safety and operational reliability are integral to the process design, with controls implemented to prevent overpressure, maintain proper separation efficiency, and ensure stable storage conditions. Interdependencies between the separators, storage tanks, pumps, and auxiliary systems are managed to optimize overall performance and mitigate risks. These measures collectively support the overarching goal of achieving efficient phase separation and resource handling while adhering to industry safety and quality standards.


## 2 **2-Phase Separator Control**
|Tagname | Type | Description |
|---------|------|-------------|
|CV-401 | Control Valve | Regulates separator pressure based on PIC-401 output |
|CV-406 | Control Valve | Modulates liquid flow rate per FIC-406 command |
|FFIC-402 | Ratio Controller | Calculates liquid flow setpoint using gas flow measurement and ratio |
|FIC-406 | Flow Controller | Controls liquid flow rate exiting the separator |
|FT-404 | Flow Transmitter | Measures gas flow rate exiting the separator |
|FT-406 | Flow Transmitter | Measures liquid flow rate exiting the separator |
|PIC-401 | Pressure Controller | Maintains separator pressure at 5.0 bar |
|PT-403 | Pressure Transmitter | Monitors separator pressure for control and interlock purposes |
|PT-408 | Pressure Transmitter | Auxiliary pressure measurement for system monitoring |


### 2.1) Control Strategy Description

The 2-phase separator control system utilizes ratio control to maintain a proportional relationship between the liquid and gas flow rates exiting the separator. Flow transmitter FT406 measures the liquid flow rate, while flow transmitter FT404 measures the gas flow rate. The ratio controller FFIC402 calculates the liquid flow setpoint based on the gas flow measurement and a predefined ratio. The ratio setpoint is configured to maintain a 2.5:1 liquid-to-gas flow ratio, ensuring optimal separation efficiency.

The ratio calculation is performed as follows: Liquid flow setpoint (SP) = Gas flow rate (FT404) × 2.5. The calculated liquid flow setpoint is sent to flow controller FIC406, which modulates the control valve CV406 to achieve the desired liquid flow rate. The gas flow rate measured by FT404 is treated as the wild flow variable, while the liquid flow rate is the controlled variable. Flow measurement ranges for FT406 and FT404 are 0-500 kg/hr and 0-1000 kg/hr, respectively. Ratio adjustments are limited between 2.0:1 and 3.0:1 to prevent operational instability.

Pressure transmitter PT403 monitors separator pressure, and pressure controller PIC401 adjusts control valve CV401 to maintain a pressure setpoint of 5.0 bar, ensuring stable operation of the separation process.


### 2.2) Interlocks and Permissives

The ratio control system is interlocked with the separator pressure control to ensure safe operation. If PT403 detects a pressure deviation exceeding ±0.5 bar from the setpoint, PIC401 overrides ratio control and closes CV406 to prevent liquid overflow. Additionally, the ratio controller FFIC402 is disabled if FT404 detects a gas flow rate below 50 kg/hr, preventing erroneous ratio calculations during low flow conditions.

Permissives include validation of FT406 and FT404 signals. If either transmitter fails or provides a signal outside the calibrated range, FFIC402 enters manual mode, allowing operators to manually adjust the liquid flow setpoint. The ratio control system is also disabled during separator startup or shutdown sequences, as indicated by PT408 readings below 1.0 bar.


### 2.3) Alarm and Fault Handling

Alarm conditions are configured for deviations in the liquid-to-gas ratio beyond ±0.2 from the setpoint. If the ratio exceeds the allowable limits, an alarm is triggered, and FFIC402 transitions to manual mode. FT406 and FT404 are equipped with signal validation alarms to detect transmitter faults or calibration drift.

Low flow alarms are set at 50 kg/hr for FT404 and 20 kg/hr for FT406. If either flow transmitter detects a flow below these thresholds, the control system initiates a low-flow shutdown sequence, closing CV406 and isolating the liquid stream. Separator pressure alarms are set at 6.0 bar for high pressure and 4.0 bar for low pressure, with PIC401 taking corrective action to stabilize the system.


## 3 **3-Phase Separator Control**
|Tagname | Type | Description |
|---------|------|-------------|
|FV-102 | Flow Valve | Regulates outlet flow to control separator pressure |
|LI-502 | Level Transmitter | Monitors separator level for operator observation |
|PIC-501 | Pressure Controller | Maintains separator pressure at setpoint using PID control |
|PT-501 | Pressure Transmitter | Provides pressure measurement signal for control loop |


### 3.1) Control Strategy Description

The 3-phase separator pressure is controlled using PIC501, which regulates the outlet flow via FV102 to maintain a stable pressure setpoint. The pressure transmitter PT501 provides a 4-20mA signal corresponding to a pressure range of 0-150 psi. The controller PIC501 is configured for reverse-acting control to increase valve opening as pressure decreases. The PID tuning parameters are set as follows: Kp = 2.0, Ki = 0.5 min, and Kd = 0.1 min. The setpoint for pressure control is fixed at 75 psi and is clamped between 70 psi and 80 psi to ensure process stability. The level inside the separator is monitored using LI502, which provides a 4-20mA signal corresponding to a level range of 0-100% and serves as an input for operator monitoring but does not directly influence the PID loop. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes.


### 3.2) Interlocks and Permissives

The control loop for PIC501 is interlocked with PT501 to ensure valid pressure readings; if PT501 fails or provides a signal outside the range of 4-20mA, the controller output to FV102 will be forced to its fail-safe position. FV102 is configured to fail-closed to prevent overpressure conditions in the separator. Additionally, the separator operation is permitted only when LI502 indicates a level above 10% to prevent dry running conditions. Any deviation from normal operating conditions will inhibit PIC501 operation and alert the operator.


### 3.3) Alarm and Fault Handling

Pressure alarms are configured on PT501 to trigger high-pressure and low-pressure warnings at 85 psi and 65 psi, respectively. A critical high-pressure alarm at 90 psi will initiate a shutdown of FV102 and isolate the separator. Level transmitter LI502 provides high and low-level alarms at 90% and 5%, respectively, to warn operators of abnormal separator conditions. In the event of a fault in PT501, PIC501 will enter manual mode, and FV102 will default to its fail-closed position. Alarm acknowledgment and reset logic are implemented to ensure operator intervention before resuming normal operation.


## 4 **Oil Tank Control**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-302 | Flow Controller | Regulates flow to maintain tank level based on LI-201 feedback |
|FV-101 | Flow Valve | Air-actuated control valve for flow regulation with fail-closed functionality |
|LI-201 | Level Transmitter | Measures oil tank level for feedback control loop |
|T-200 | Tank | Oil storage tank monitored and controlled for level |
|XV-010 | On-Off Valve | Ensures flow path is open for control loop operation |
|XV-011 | On-Off Valve | Ensures flow path is open for control loop operation |


### 4.1) Control Strategy Description

The oil tank T200 level is maintained via feedback control implemented on FIC302, which regulates the flow through FV-101 based on the level measurement provided by LI201. The process variable (PV) is the tank level from LI201, scaled from 0% to 100% corresponding to 0-5 meters. The setpoint (SP) for LI201 is configured at 70% (3.5 meters). FIC302 operates in reverse-acting mode to decrease flow through FV-101 as the level approaches the setpoint. The PID tuning parameters for FIC302 are defined as follows: proportional gain (Kp) = 1.8, integral time (Ki) = 2.0 minutes, and derivative time (Kd) = 0.3 minutes. The output (MV) of FIC302 is constrained between 0% and 100%, corresponding to the 4-20mA signal range sent to FV-101. FV-101 is an air-actuated control valve with fail-closed functionality to ensure isolation during fault conditions. Bumpless transfer logic is implemented to allow smooth transitions between manual and automatic modes without process disruption.


### 4.2) Interlocks and Permissives

The control loop for FIC302 is interlocked with the status of V10 and V11. Both valves must be fully open to enable flow control; their positions are verified using discrete feedback signals. If either valve is closed, FIC302 output is forced to 0%, closing FV-101. Additionally, the loop is permissive on the operational status of LI201; if LI201 fails or provides an invalid signal (e.g., out of range or loss of communication), FIC302 transitions to manual mode with a fixed output of 25% to maintain minimal flow. A high-level interlock is configured on LI201 at 90% (4.5 meters), which overrides FIC302 and closes FV-101 to prevent overflow.


### 4.3) Alarm and Fault Handling

Level alarms are configured for LI201 as follows: a low-level alarm at 20% (1.0 meter) and a high-level alarm at 80% (4.0 meters). These alarms trigger visual and audible notifications in the control system. If LI201 fails, an instrument fault alarm is activated, and the control system forces FIC302 into manual mode. FV-101 position feedback is monitored; any deviation greater than 5% between the commanded position and actual position triggers a valve fault alarm. In case of a high-level interlock activation at 90%, an emergency shutdown signal is sent to FV-101 and logged in the system. Settling time for the control loop is targeted at less than 60 seconds under normal operating conditions, ensuring rapid response to process disturbances.


## 5 **Water Tank and Pump Control**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-101 | Flow Controller | Maintains flow rate at 50 GPM using FT-102 as PV |
|FIC-102 | Flow Controller | Maintains flow rate at 45 GPM using FT-104 as PV |
|FT-102 | Flow Transmitter | Measures flow rate for FIC-101 control loop |
|FT-104 | Flow Transmitter | Measures flow rate for FIC-102 control loop |
|FV-103 | Control Valve | Modulates flow based on FIC-101 output |
|LI-101 | Level Transmitter | Measures water tank level in T-100 |
|P-001 | Pump | Adjusts flow rate based on FIC-102 output |
|T-100 | Tank | Stores water for circulation loop system |


### 5.1) Control Strategy Description

The primary control objective for the water tank (T100) system is to maintain a stable flow rate through the circulation loop using FIC101 and FIC102. The process variable (PV) for FIC101 is the flow rate measured by FT102, while the PV for FIC102 is the flow rate measured by FT104. The setpoint (SP) for FIC101 is 50 GPM, and the SP for FIC102 is 45 GPM. Both controllers operate in single-loop feedback control mode.

FIC101 and FIC102 are configured as reverse-acting PID controllers. The proportional gain (Kp) for both controllers is set to 2.0, the integral time (Ki) is set to 1.0 minute, and the derivative time (Kd) is set to 0.1 minute. The control output (MV) from FIC101 modulates FV-103, which is a fail-closed valve with a control range of 0% to 100%. The control output from FIC102 adjusts the speed of pump P01 using a 4-20mA signal. The output limits of both controllers are clamped between 0% and 100% to prevent actuator saturation.

The flow transmitters FT102 and FT104 provide 4-20mA signals corresponding to a flow range of 0 to 100 GPM. These signals are linearly scaled within the controllers to ensure accurate control calculations. Bumpless transfer logic is implemented to allow seamless transition between manual and automatic modes. Anti-windup protection is enabled to prevent integrator saturation during manual operation or output clamping.


### 5.2) Interlocks and Permissives

The operation of FIC101 and FIC102 is interlocked with the level in water tank T100, monitored by LI101. If the level in T100 falls below 20% or exceeds 90%, both controllers are forced to manual mode, and the outputs are set to 0%. Additionally, pump P01 will not start unless the level in T100 is greater than 25% and the downstream valve FV-103 is confirmed open via position feedback.

A permissive is included to ensure that FV-103 does not open unless pump P01 is running and the flow rate measured by FT102 exceeds 10 GPM. A timer introduces an 8-second delay to validate the flow condition and avoid transient interlock trips during startup.


### 5.3) Alarm and Fault Handling

An alarm is triggered if the flow rate measured by FT102 deviates from the setpoint of FIC101 by more than ±10 GPM for a duration exceeding 15 seconds. Similarly, an alarm is generated if the flow rate measured by FT104 deviates from the setpoint of FIC102 by more than ±8 GPM for the same duration. Both alarms are classified as high-priority process alarms.

A fault in FT102 or FT104, such as a signal loss or out-of-range condition, will result in the associated controller (FIC101 or FIC102) transitioning to manual mode with its output frozen at the last valid value. A fault in LI101 will trigger a system-level shutdown, stopping pump P01 and closing FV-103 to prevent damage to downstream equipment.


## 6 **Water Coalescer Control**
|Tagname | Type | Description |
|---------|------|-------------|
|FT-105 | Flow Transmitter | Measures flow rate downstream of water coalescer (0-50 gpm range) |
|LI-503 | Level Transmitter | Measures liquid level in the water coalescer (0-100% range) |
|LIC-502 | Level Controller | Controls flow rate downstream of water coalescer via LVC-502 |
|LIC-503 | Level Controller | Maintains liquid level in the water coalescer via LVC-507 |
|LVC-502 | Level Valve | Regulates flow rate downstream of water coalescer (fail-open) |
|LVC-507 | Level Valve | Regulates liquid level in the water coalescer (fail-closed) |
|P-001 | Pump | Circulates process fluid in the system |


### 6.1) Control Strategy Description

The water coalescer level is controlled using LIC-503, which maintains the liquid level within the coalescer to ensure optimal impurity removal. The process variable (PV) is the liquid level measured by LI-503, with a calibrated range of 0-100% corresponding to a 4-20mA signal. The setpoint (SP) for LIC-503 is configured at 65% to maintain stable operation. LIC-503 employs a reverse-acting PID controller to regulate the output to LVC-507, which is a fail-closed control valve. The PID tuning parameters for LIC-503 are configured as follows: proportional gain (Kp) = 2.0, integral time (Ki) = 1.5 minutes, and derivative time (Kd) = 0.1 minutes. The output range of LIC-503 is clamped between 0% and 100% to prevent actuator saturation. Bumpless transfer is implemented to ensure smooth transitions between manual and automatic modes.

Flow control downstream of the water coalescer is managed by LIC-502, which adjusts LVC-502 to maintain the flow rate measured by FT-105. FT-105 provides a 4-20mA signal corresponding to a flow range of 0-50 gpm. The setpoint for LIC-502 is set at 35 gpm, and the PID tuning parameters are configured as follows: Kp = 1.8, Ki = 2.0 minutes, and Kd = 0.0 minutes. LIC-502 is direct-acting, and LVC-502 is fail-open to ensure flow continuity in the event of a controller or valve failure.


### 6.2) Interlocks and Permissives

The operation of LIC-503 is interlocked with LI-503 to prevent overfilling or emptying of the water coalescer. If LI-503 detects a level above 90% or below 10%, LIC-503 output is overridden to close LVC-507, and an alarm is triggered. Additionally, LIC-502 is interlocked with FT-105 to ensure flow rate stability; if FT-105 detects a flow rate below 5 gpm, LIC-502 output is overridden to fully open LVC-502 to restore flow. Both LIC-503 and LIC-502 are permissive-controlled by the status of P01, the pump feeding the water coalescer. If P01 is not running, both control loops are disabled, and LVC-502 and LVC-507 are forced to their fail positions.


### 6.3) Alarm and Fault Handling

High and low-level alarms are configured for LI-503 at 90% and 10%, respectively. If either alarm is triggered, LIC-503 enters fault mode, closing LVC-507 and disabling automatic control. Similarly, FT-105 has high and low flow alarms set at 45 gpm and 5 gpm, respectively. Upon alarm activation, LIC-502 output is overridden to fully open LVC-502. A fault in the signal from LI-503 or FT-105 (e.g., signal loss or out-of-range values) results in the respective controller entering manual mode, with the operator required to adjust valve positions manually. Hysteresis of 5% is applied to all alarm thresholds to prevent oscillation between alarm states.


## 7 **Air Compressor Control**
|Tagname | Type | Description |
|---------|------|-------------|
|PIC-105 | Pressure Controller | Maintains system pressure using PID control logic |
|PIT-106 | Pressure Transmitter | Measures system pressure for feedback to controller |
|V-010   | Control Valve       | Modulates air flow to maintain pressure setpoint |


### 7.1) Control Strategy Description

The air compressor control system utilizes a PID feedback loop to maintain the pressure of compressed air within the system. The controlled variable (PV) is the pressure measured by PIT-106, with the target setpoint (SP) configured at 8.5 bar. The pressure indicator controller PIC-105 is configured as a reverse-acting controller to reduce the manipulated variable (MV) output when the process variable exceeds the setpoint.

The PID tuning parameters for PIC-105 are defined as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.3 minutes. The output range of PIC-105 is clamped between 0% and 100% to ensure safe operation of the final control element. The final control element is a modulating valve V10, which is configured to fail-closed upon loss of signal to prevent over-pressurization.

The pressure transmitter PIT-106 provides a 4-20 mA signal corresponding to a pressure range of 0 to 10 bar. Signal scaling is applied within PIC-105 to normalize the input for the PID algorithm. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes.


### 7.2) Interlocks and Permissives

The operation of PIC-105 is interlocked with the status of the air compressor. The compressor must be running, as indicated by a permissive signal from the compressor control system, before PIC-105 can adjust V10. Additionally, the pressure measured by PIT-106 must remain within the range of 0.5 bar to 10 bar; if the pressure falls outside this range, the controller output is disabled, and V10 is forced to its fail-closed position.

A timer delay of 7 seconds is integrated into the control logic to filter transient pressure spikes upon compressor startup. This ensures that PIC-105 does not react to temporary fluctuations that could destabilize the system.


### 7.3) Alarm and Fault Handling

High-pressure and low-pressure alarms are configured based on the readings from PIT-106. A high-pressure alarm is triggered if the pressure exceeds 9.5 bar, while a low-pressure alarm is activated if the pressure drops below 0.5 bar. Both alarms are displayed on the operator interface and require acknowledgment.

In the event of a transmitter fault or loss of signal from PIT-106, PIC-105 enters a fault state, and V10 is driven to its fail-closed position. The system also generates a fault alarm to notify operators of the issue. Diagnostic logic within PIC-105 monitors for controller output saturation and integral windup conditions, activating an anti-windup mechanism to prevent control instability.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 7

- Total Tagnames: 36

- Word Count: 3400
