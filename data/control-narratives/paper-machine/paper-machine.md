# Chemical Pulping and Paper Production Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Wood Handling and Chipping**
3. **Continuous Digester**
4. **Washing and Screening**
5. **Bleaching Towers**
6. **Refining and Machine Chest**
7. **Approach Flow and Forming**
8. **Press Section**
9. **Dryer Section**
10. **Finishing and Winding**

---


## 1 **Process Overview and Scope**

The chemical pulping and paper production process is designed to transform raw wood materials into high-quality paper through a series of interconnected stages. The primary objective is to ensure stable operation, consistent product quality, and equipment protection while maximizing efficiency and safety. Beginning with wood handling and chipping, debarked logs are processed into uniform chips suitable for chemical pulping. These chips are fed into a continuous digester, where temperature, pressure, and chemical ratios are carefully controlled to achieve the desired pulp properties, including target Kappa number and alkali levels. Subsequent washing and screening stages remove spent liquor and contaminants, preparing the pulp for bleaching and refining. These critical upstream phases establish the foundation for downstream paper formation and finishing.

The process progresses through controlled bleaching, refining, and stock preparation, where pulp brightness and consistency are optimized. Multistage bleaching towers and refiners employ pH, temperature, and specific-edge-load control strategies to ensure pulp meets quality standards. The diluted stock enters the paper machine, where approach-flow systems adjust fibre consistency, sheet basis weight, and turbulence for uniform sheet formation. Drying and dewatering stages further refine the product as moisture is gradually reduced, and web tension is stabilized. Finally, finishing operations such as calendaring, coating, and winding complete the process, delivering paper with precise physical and aesthetic properties.

The control system integrates advanced strategies such as cascade loops, model-predictive control, and cross-directional profiling to synchronize operations across process sections. Safety mechanisms, including density and pressure safeguards, protect critical equipment, while automated feedback loops maintain optimal conditions throughout the system. Each stage is interdependent, with upstream conditions directly influencing downstream performance. By balancing operational efficiency with rigorous safety and quality standards, the process ensures reliable production of consistent, high-quality paper products.


## 2 **Wood Handling and Chipping**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-101 | Flow Controller | Maintains flow rate of debarked logs through chipper at setpoint of 250 m³/h |
|FV-106 | Flow Valve | Controls flow downstream of the chipper, fail-closed for overfeeding prevention |
|LT-101 | Level Transmitter | Measures flow rate of logs, transmitting 4–20 mA signal for 0–400 m³/h range |
|LV-103 | Level Valve | Regulates level in associated process system |
|M-102 | Motor | Drives conveyor to control log flow speed (0–3 m/s) |
|XV-102 | On-Off Valve | Isolation valve for process control or safety |
|XV-104 | On-Off Valve | Isolation valve for process control or safety |
|XV-105 | On-Off Valve | Isolation valve for process control or safety |


### 2.1) Control Strategy Description

The primary control objective for the wood handling and chipping section is to maintain the flow rate of debarked logs through the knife-ring chipper at a target setpoint of 250 m³/h, ensuring consistent chip length within the range of 12–25 mm. Flow measurement is provided by LT-101, which transmits a 4–20 mA signal corresponding to a flow range of 0–400 m³/h. The PID controller FC-101 is configured as reverse-acting to decrease motor speed on M-102 when the flow exceeds the setpoint.

The PID tuning parameters for FC-101 are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.3 minutes. The controller output (MV) drives the speed reference of motor M-102, scaled between 0–100% corresponding to conveyor speed limits of 0–3 m/s. Anti-windup logic is implemented to prevent integral accumulation when the output is clamped at its limits. Bumpless transfer is enabled to ensure smooth transitions between manual and automatic modes.

The final control element is FV-106, a flow control valve positioned downstream of the chipper. FV-106 is configured as fail-closed to prevent overfeeding in the event of a fault. The valve response time is designed to achieve a settling time of less than 5 seconds for flow rate disturbances. A deadband of 2% is applied to the setpoint to minimize hunting behavior near the target flow rate.


### 2.2) Interlocks and Permissives

The operation of FC-101 is interlocked with the status of XV-102 and XV-104. Both shut-off valves must be confirmed open before the PID loop is enabled. LT-101 must provide a valid signal within its calibrated range (0–400 m³/h) for FC-101 to execute control. If LT-101 signal falls below 4 mA or exceeds 20 mA, the PID loop will be disabled, and M-102 will be stopped.

Permissive logic ensures that M-102 cannot start unless LV-103 indicates a chip level above 20% in the chipper feed hopper. Additionally, XV-105 must be closed to isolate downstream equipment during startup or maintenance. The control system clamps the setpoint for FC-101 to a safe operating range of 50–350 m³/h to prevent excessive feed rates that could damage the chipper.


### 2.3) Alarm and Fault Handling

An alarm is triggered if the process variable (PV) from LT-101 deviates by more than ±10% from the setpoint for longer than 30 seconds. High-priority alarms include "Flow High" and "Flow Low," which are activated if LT-101 exceeds 380 m³/h or drops below 20 m³/h, respectively.

In the event of a fault in LT-101, such as signal loss or out-of-range values, FC-101 will enter manual mode, and M-102 will be stopped. FV-106 will be commanded to its fail-closed position to prevent unregulated flow. A "PID Fault" alarm will indicate controller malfunction, prompting operator intervention.

For motor faults on M-102, the control system will shut down the PID loop and close XV-102 and XV-104 to isolate the chipper. Restart timers are implemented to delay reactivation of M-102 for 60 seconds after fault clearance to protect the motor and downstream equipment.


## 3 **Continuous Digester**
|Tagname | Type | Description |
|---------|------|-------------|
|FC-202 | Flow Controller | Adjusts liquor recirculation flow to maintain pressure setpoint. |
|FC-203 | Flow Controller | Modulates steam flow to control digester temperature. |
|FV-202 | Flow Valve | Regulates liquor flow for pressure control. |
|PIC-101 | Pressure Controller | Maintains digester pressure at a setpoint of 800 kPa. |
|PT-101 | Pressure Transmitter | Measures digester pressure for control purposes. |
|SV-203 | Steam Valve | Controls steam flow to adjust digester temperature. |
|TIC-104 | Temperature Controller | Regulates digester temperature at a setpoint of 170 °C. |
|TT-103 | Temperature Transmitter | Measures digester temperature for control feedback. |


### 3.1) Control Strategy Description

The continuous digester operates with a cascade control system to regulate chip feed rate, white liquor ratio, digester temperature, pressure, and slurry consistency. The primary loop, configured as a temperature control loop, ensures stable digester temperature at a setpoint of 170 °C using TIC-104. TIC-104 receives temperature measurements from TT-103, which is scaled linearly to provide calibrated values between 20 °C and 200 °C. The output of TIC-104 serves as the remote setpoint (RSP) for the secondary loop, which controls steam flow via FC-203. FC-203 modulates the steam control valve (SV-203) to maintain rapid response to temperature disturbances. Secondary loop tuning parameters are set to Kp=3.5 and Ki=0.3 min to ensure a faster response time compared to the primary loop, which is tuned to Kp=1.2 and Ki=2.0 min.

The pressure control loop operates similarly, with PT-101 measuring digester pressure and PIC-101 maintaining a setpoint of 800 kPa. PIC-101 outputs a remote setpoint to FC-202, which adjusts the liquor recirculation flow through valve FV-202. This configuration ensures stable pressure control while rejecting disturbances in the liquor flow. The secondary loop response time is configured to be 7 times faster than the primary loop to prevent cascade hunting and ensure smooth operation.

Manual setpoint changes for TIC-104 and PIC-101 are clamped between 20 °C and 90 °C and 700 kPa to 900 kPa, respectively, to maintain operational safety. Deadband logic with a hysteresis of 3% is applied to prevent rapid switching between control states near the setpoints. Signal scaling between the primary and secondary controllers ensures proper interaction, with TIC-104 output scaled to match the input range of FC-203 (0–100% RSP).


### 3.2) Interlocks and Permissives

Steam flow control (FC-203) is interlocked with high-pressure permissives from PT-101. If PT-101 detects pressure exceeding 900 kPa, FC-203 output is overridden to close SV-203 fully, preventing overpressure conditions. Similarly, liquor recirculation control (FC-202) is interlocked with low-pressure permissives; if PT-101 detects pressure below 700 kPa, FC-202 output is overridden to fully open FV-202 to restore pressure. Temperature control via TIC-104 is interlocked with TT-103 signal validity; if TT-103 fails or provides erroneous data, TIC-104 enters manual mode, and steam flow is adjusted manually through FC-203.

Cascade mode activation requires permissives confirming valid signals from TT-103 and PT-101, as well as confirmation that the secondary controllers (FC-203 and FC-202) are operational. Transition delays of 5 seconds are applied during mode switching to prevent abrupt changes in control action. If any permissive fails, the system defaults to local/manual control mode.


### 3.3) Alarm and Fault Handling

High-temperature alarms are triggered if TT-103 detects a temperature exceeding 180 °C. TIC-104 responds by reducing the RSP to FC-203, throttling steam flow through SV-203. If temperature exceeds 185 °C, an emergency shutdown sequence is initiated, closing SV-203 and isolating the digester. Low-temperature alarms activate if TT-103 detects a temperature below 160 °C, prompting TIC-104 to increase the RSP to FC-203 to restore temperature.

Pressure alarms are similarly configured, with high-pressure alarms activating at 850 kPa and low-pressure alarms at 750 kPa. PIC-101 adjusts the RSP to FC-202 to mitigate pressure deviations. If PT-101 fails or provides invalid data, PIC-101 enters manual mode, and FV-202 is adjusted manually.

Secondary loop failures, such as FC-203 or FC-202 malfunction, result in the primary controllers (TIC-104 and PIC-101) entering manual mode. Cascade mode is disabled, and operators are alerted through fault indicators. Alarm acknowledgment is required to reset the system to automatic control once faults are resolved.


## 4 **Washing and Screening**
|Tagname | Type | Description |
|---------|------|-------------|
|DT-301 | Density Transmitter | Measures the density of the process fluid |
|FV-106 | Flow Valve | Regulates flow rate through the pressure screen |
|PIC-104 | Pressure Controller | Maintains pressure setpoint in the screening system |
|PIT-103 | Pressure Transmitter | Measures pressure in the pressure screening system |
|PT-101 | Pressure Transmitter | Monitors system pressure for control purposes |
|XV-102 | On-Off Valve | Isolates flow in the process line |
|XV-107 | On-Off Valve | Provides isolation for maintenance or emergency conditions |


### 4.1) Control Strategy Description

The washing and screening section employs a PID control loop to maintain optimal pressure in the pressure screening system, ensuring consistent removal of contaminants and protection of slot plates. The primary controlled variable (PV) is the pressure measured by PIT-103, with the setpoint (SP) configured at 250 kPa. The control output (MV) manipulates the position of flow control valve FV-106 to regulate the flow rate through the pressure screen.

The PID controller, PIC-104, is configured as a reverse-acting controller with the following tuning parameters: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.1 minutes. The controller output is clamped between 0% and 100% to ensure the valve operates within its design limits. The control range of PIT-103 is 0–500 kPa, with a 4–20 mA signal scaled linearly to the controller.

The final control element, FV-106, is a pneumatically actuated modulating valve with a fail-closed position to ensure system isolation during fault conditions. The valve's response time is 2 seconds, and it is equipped with position feedback to prevent hunting. Bumpless transfer logic is implemented in PIC-104 to allow smooth transitions between manual and automatic modes without disturbing the process.

To prevent oscillations, a 5% deadband is applied around the setpoint, inhibiting control output changes when the pressure is within ±12.5 kPa of the target. Signal scaling logic ensures the raw transmitter signal is converted to calibrated engineering units before entering the PID algorithm.


### 4.2) Interlocks and Permissives

The operation of PIC-104 is subject to the following interlocks and permissives. The controller will not activate unless PT-101, the upstream pressure transmitter, indicates a pressure above 150 kPa to confirm sufficient feed pressure. Additionally, XV-102, the upstream shut-off valve, must be fully open, as verified by its limit switch, before FV-106 can operate. If PT-101 detects a pressure exceeding 400 kPa, PIC-104 will automatically drive FV-106 to 0% open to prevent overpressure in the screening system.

A permissive from the slot plate protection system ensures that PIC-104 is enabled only when the density transmitter DT-301 confirms a pulp density below 3.5%. This prevents excessive wear on the slot plates. XV-107, the downstream shut-off valve, must also be fully open to allow proper flow through the system.


### 4.3) Alarm and Fault Handling

PIC-104 generates a high-pressure alarm if PIT-103 registers a pressure above 275 kPa for more than 5 seconds, alerting operators to potential flow restrictions or blockages. A low-pressure alarm is triggered if PIT-103 falls below 200 kPa, indicating insufficient flow through the pressure screen. Both alarms are latched and require operator acknowledgment.

In the event of a transmitter fault or loss of signal from PIT-103, PIC-104 will enter a fail-safe mode, driving FV-106 to its fail-closed position. A fault alarm will be generated, and the system will inhibit the automatic mode until the fault is resolved. Anti-windup logic in PIC-104 prevents integral action from accumulating during fault conditions, ensuring stable operation upon signal restoration.

A system-wide fault is triggered if PT-101 or DT-301 reports values outside their calibrated ranges, immediately closing XV-102 and XV-107 to isolate the system. Operators are required to verify and reset the interlocks before resuming normal operation.


## 5 **Bleaching Towers**
|Tagname | Type | Description |
|---------|------|-------------|
|AT-102 | pH Transmitter | Measures pH of pulp slurry in bleaching tower |
|AT-107 | pH Transmitter | Monitors pH at secondary process location |
|FV-101 | Flow Control Valve | Regulates acid dosing flow rate to control pH |
|FV-103 | Flow Control Valve | Adjusts steam flow for temperature control |
|LIC-102 | Level Controller | Controls acid dosing based on pH feedback |
|LIC-104 | Level Controller | Manages level in auxiliary process tank |
|TIC-106 | Temperature Controller | Maintains setpoint temperature at 65°C |
|TIT-106 | Temperature Transmitter | Measures process temperature for control loop |
|XV-104 | On-Off Valve | Provides isolation for maintenance or emergency shutdown |


### 5.1) Control Strategy Description

The bleaching tower control system employs a PID feedback loop to maintain the pH of the pulp slurry within a target setpoint range of 9.0 to 9.5, as measured by pH transmitter AT-102. The controller, identified as LIC-102, is configured for reverse-acting operation to ensure that an increase in pH results in a decrease in the manipulated variable (MV), which is the flow rate of acid dosing through flow control valve FV-101. The PID parameters are tuned with proportional gain (Kp) set to 1.8, integral time (Ki) set to 0.5 minutes, and derivative time (Kd) set to 0.1 minutes to achieve a settling time of less than 30 seconds.

The process variable (PV) from AT-102 is transmitted as a 4–20 mA signal corresponding to a pH range of 0 to 14. The output of LIC-102 is scaled to operate FV-101 within a control range of 10% to 90% open. The valve is configured to fail-closed upon loss of signal to prevent over-dosing of acid. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes, with the last MV value held as the bias during mode switching.

Temperature control is managed by a separate PID loop with TIT-106 providing the PV signal for temperature measurement. The controller TIC-106 adjusts the steam flow through FV-103 to maintain a setpoint temperature of 65°C. The PID parameters for TIC-106 are Kp = 2.0, Ki = 0.4 minutes, and Kd = 0.05 minutes, ensuring rapid response without overshoot. TIT-106 transmits temperature data as a 4–20 mA signal over a range of 0–100°C.

Retention time in the bleaching tower is indirectly controlled by regulating the pulp flow rate via LIC-104, which adjusts the position of shut-off valve XV-104. The retention time setpoint is maintained at 120 minutes, with a proportional gain of 1.5, integral time of 1.0 minutes, and derivative time of 0.2 minutes. Flow measurement is derived from a differential pressure transmitter, scaled to 0–200 m³/h.


### 5.2) Interlocks and Permissives

The acid dosing system interlock ensures that FV-101 cannot open unless the upstream flow rate, as measured by a flow transmitter, is greater than 10 m³/h. Additionally, the pH control loop (LIC-102) is inhibited if AT-102 detects a pH below 2.0 or above 12.0 to prevent unsafe operating conditions. For temperature control, TIC-106 is disabled if the temperature exceeds 80°C, as indicated by TIT-106, to prevent thermal degradation of the pulp.

The retention time control loop (LIC-104) is interlocked with the pulp flow system to ensure XV-104 remains in a fail-closed position if the flow rate drops below 5 m³/h or if the downstream pressure exceeds 5 bar. Permissives require that the bleaching tower level is within 20–80% of its capacity before any control loop is enabled.


### 5.3) Alarm and Fault Handling

High-priority alarms are generated for pH deviations beyond the setpoint range of ±1.0, with LIC-102 triggering a "HIGH pH" alarm at 10.5 and a "LOW pH" alarm at 8.5. Similarly, TIC-106 generates a "HIGH TEMP" alarm at 75°C and a "LOW TEMP" alarm at 55°C. These alarms initiate a gradual ramp-down of the respective control valves to prevent abrupt process changes.

Sensor faults, such as signal loss from AT-102 or TIT-106, result in the respective control loops defaulting to manual mode with the last known MV held constant. A fault in AT-107 triggers a "pH SENSOR FAULT" alarm, and the acid dosing system is automatically isolated by closing FV-101. Redundant transmitters are not implemented; therefore, operators must manually verify measurements during sensor faults.

For retention time control, LIC-104 triggers a "RETENTION TIME DEVIATION" alarm if the calculated retention time deviates by more than 10 minutes from the setpoint. XV-104 is forced closed if this deviation persists for more than 60 seconds.


## 6 **Refining and Machine Chest**
|Tagname | Type | Description |
|---------|------|-------------|
|CT-501 | Consistency Transmitter | Measures pulp consistency at machine chest outlet |
|FC-502 | Flow Controller | Controls dilution water flow to achieve target consistency |
|FV-502 | Flow Valve | Modulates water flow for consistency control |
|LT-501 | Level Transmitter | Measures level in the refining or machine chest section |
|M-501 | Motor | Drives the primary refiner for pulp processing |
|PT-502 | Pressure Transmitter | Measures pressure in the refining or dilution system |


### 6.1) Control Strategy Description

The control system for the **Refining and Machine Chest** section ensures precise regulation of pulp consistency and specific-edge-load (SEL) during refining, followed by dilution to a target consistency of 3% in the machine chest. The primary control loop regulates the SEL of the double-disc refiners using motor load feedback, while a secondary loop controls the dilution water flow to achieve the desired pulp consistency.

The SEL control loop uses the motor load signal from the primary refiner motor (M-501) as the process variable (PV) and compares it to the operator-defined SEL setpoint (SEL_SP). The SEL controller (SELC-501) is configured as a reverse-acting PID controller with tuning parameters Kp=1.8, Ki=0.5 min, and Kd=0.1 min. The SEL_SP is clamped between 0.4 and 1.0 W·s/mm² to ensure safe operation. The SEL measurement, derived from the motor load (M-501) and plate gap, is normalized to a 4-20 mA signal corresponding to 0.2 to 1.2 W·s/mm². The controller output (MV) modulates the refiner plate gap actuator, with a control output range of 0-100%.

The dilution consistency control loop uses the consistency transmitter (CT-501) to measure the pulp consistency at the machine chest outlet. The transmitter signal is scaled to 4-20 mA, corresponding to a consistency range of 2.0% to 5.0%. The consistency controller (FC-502) is configured as a direct-acting PID controller with tuning parameters Kp=2.2, Ki=0.7 min, and Kd=0.0 min. The operator-defined consistency setpoint (CONS_SP) is limited to a range of 2.5% to 3.5%. The controller output modulates the dilution water flow control valve (FV-502), which is a fail-closed valve with a linear flow characteristic. The control output range for FV-502 is 0-100%, corresponding to a flow rate of 0-50 m³/h.

Both control loops include bumpless transfer logic to ensure smooth transitions between Auto and Manual modes. In Manual mode, the operator directly adjusts the control output (MV) within the permissible range. Anti-windup protection is implemented to prevent integral windup during saturation of the control output.


### 6.2) Interlocks and Permissives

The SEL control loop (SELC-501) is interlocked with the refiner motor (M-501) status. The SEL controller is enabled only when M-501 is running and the plate gap is within the operating range of 0.5 to 5.0 mm, as indicated by the plate gap position transmitter. If M-501 trips or the plate gap exceeds the permissible range, SELC-501 output is forced to 0%, and the refiner is stopped.

The dilution consistency control loop (FC-502) is interlocked with the machine chest level transmitter (LT-501). The controller is enabled only when the machine chest level is above 20% to prevent dilution water flow when the chest is empty. If the level drops below 20%, the FC-502 output is forced to 0%, closing FV-502.

A permissive ensures that the dilution water supply pressure, monitored by PT-502, is within the range of 300 to 600 kPa before enabling the FC-502 loop. If the pressure falls outside this range, the controller output is held at its last value, and an alarm is triggered.


### 6.3) Alarm and Fault Handling

The SEL control loop generates a high-specific-edge-load alarm (ALM-SEL-HI) if the measured SEL exceeds 1.1 W·s/mm² for more than 5 seconds. A low-specific-edge-load alarm (ALM-SEL-LO) is triggered if the SEL drops below 0.3 W·s/mm² for more than 5 seconds. Both alarms require operator acknowledgment and automatically reset when the SEL returns to the normal operating range.

The dilution consistency control loop generates a high-consistency alarm (ALM-CONS-HI) if the measured consistency exceeds 4.0% and a low-consistency alarm (ALM-CONS-LO) if the consistency drops below 2.0%. These alarms are latched and require manual acknowledgment after the process variable returns to the normal range.

A fault in the consistency transmitter (CT-501), such as a signal below 3.6 mA or above 21.0 mA, triggers a transmitter fault alarm (ALM-CT-501-FAULT). In this case, the FC-502 controller output is forced to 0%, closing FV-502 to prevent over-dilution.

For both loops, a watchdog timer monitors the controller scan rate. If the scan rate exceeds 500 ms, a controller fault alarm (ALM-CTRL-FAULT) is triggered, and the respective loop is placed in Manual mode.


## 7 **Approach Flow and Forming**
|Tagname | Type | Description |
|---------|------|-------------|
|ALM-601 | Level Alarm | High-level alarm for slurry tank overflow protection |
|ALM-602 | Level Alarm | Low-level alarm for slurry tank underflow detection |
|ALM-603 | General Alarm | Alarm for abnormal system conditions |
|ALM-604 | General Alarm | Alarm for equipment malfunction or failure |
|CT-601 | Consistency Transmitter | Measures fibre slurry consistency in the range of 0.5–3.0% |
|FIC-601 | Flow Controller | Regulates dilution water flow based on ratio control setpoint |
|FS-601 | Flow Switch | Detects flow presence or absence in the dilution water line |
|FT-601 | Flow Transmitter | Measures dilution water flow rate in the range of 0–500 m³/hr |
|FV-601 | Flow Valve | Controls dilution water flow rate to maintain setpoint |
|P-601 | Pump | Transfers fibre slurry to the forming system |
|PIT-601 | Pressure Transmitter | Monitors pressure in the slurry pipeline |
|VT-601 | Vibration Transmitter | Detects vibration levels in the pump or pipeline system |


### 7.1) Control Strategy Description

The approach flow and forming system employs ratio control to maintain precise proportional relationships between the fibre slurry consistency and dilution water flow rate. The wild flow measurement is provided by the consistency transmitter CT-601, which measures the fibre slurry consistency in the range of 0.5–3.0%. The controlled flow is the dilution water flow rate, regulated by the flow control valve FV-601, with flow measured by the flow transmitter FT-601 in the range of 0–500 m³/hr. The ratio controller, designated as FFIC-601, calculates the setpoint for the dilution water flow (FT-601) based on the measured consistency (CT-601) and the operator-defined ratio setpoint.

The ratio is configured to maintain a dilution water-to-slurry consistency ratio of 2.5:1 under normal operating conditions. The ratio controller FFIC-601 calculates the dilution water flow setpoint as follows:
**FT-601 SP = CT-601 PV × Ratio SP**,
where the Ratio SP is adjustable between 2.0:1 and 3.0:1. The calculated setpoint is sent to the flow controller FIC-601, which modulates the flow control valve FV-601 to maintain the desired dilution water flow.

A low flow cutoff is implemented to prevent instability during low-consistency operation. If the fibre slurry consistency (CT-601) falls below 0.5%, the ratio controller FFIC-601 clamps the dilution water flow setpoint (FT-601 SP) to a minimum value of 10 m³/hr. The operator has manual bias capability to adjust the ratio within ±0.2 of the setpoint for fine-tuning during transitions or process upsets.


### 7.2) Interlocks and Permissives

The ratio control loop FFIC-601 is enabled only when the fan pump P-601 is running, as verified by the pump status signal P-601 RUN. Additionally, the dilution water system must be operational, confirmed by the flow switch FS-601, which ensures a minimum flow of 5 m³/hr through the dilution water line. If either condition is not met, the ratio controller FFIC-601 is placed in manual mode, and the flow control valve FV-601 is set to a fail-safe position of 20% open.

To prevent cavitation in the fan pump P-601, the pressure at the pump discharge, measured by PIT-601, must exceed 300 kPa. If the pressure falls below this threshold, the ratio control loop is disabled, and an alarm is triggered. The system also includes a permissive to ensure that the vacuum deaerator is operational, verified by the vacuum transmitter VT-601, which must indicate a vacuum level of at least 30 kPa before the ratio control loop is activated.


### 7.3) Alarm and Fault Handling

An alarm is generated if the ratio controller FFIC-601 detects that the calculated dilution water flow setpoint (FT-601 SP) exceeds the maximum allowable flow of 500 m³/hr or falls below the minimum allowable flow of 10 m³/hr. The alarm tag is configured as ALM-601, with a priority level of 2 for high flow and 3 for low flow.

If the consistency transmitter CT-601 fails, as indicated by a diagnostic signal or a reading outside the valid range of 0.5–3.0%, the ratio controller FFIC-601 transitions to manual mode, and the dilution water flow setpoint (FT-601 SP) is held at the last valid value. A transmitter failure alarm, ALM-602, is triggered with a priority level of 1. Similarly, if the flow transmitter FT-601 fails, the flow control valve FV-601 is driven to its fail-safe position of 20% open, and an alarm, ALM-603, is generated.

In the event of a sudden process upset, such as a rapid change in slurry consistency exceeding 0.5% per second, the ratio controller FFIC-601 implements a lead-lag compensation with a time constant of 2 seconds to stabilize the dilution water flow. If the upset persists for more than 10 seconds, an alarm, ALM-604, is triggered to notify the operator of the abnormal condition.


## 8 **Press Section**
|Tagname | Type | Description |
|---------|------|-------------|
|CS-701 | Control Switch | Enables or disables control system operation. |
|HS-701 | Hand Switch | Manual override for system control. |
|LIC-701 | Level Controller | Regulates hydraulic pressure to maintain sheet moisture setpoint. |
|MM-701 | Moisture Sensor | Measures sheet moisture content exiting the press section. |
|PT-701 | Pressure Transmitter | Monitors hydraulic pressure applied to the shoe press. |
|PV-101 | Pressure Valve | Adjusts hydraulic pressure to control sheet moisture. |
|SB-701 | Signal Booster | Amplifies control signals for reliable transmission. |
|TT-102 | Temperature Transmitter | Measures temperature in the press section. |


### 8.1) Control Strategy Description

The press section PID control logic is implemented to regulate the moisture content of the sheet exiting the two-nip shoe-press train using feedback from microwave moisture sensor MM-701. The control objective is to maintain the sheet moisture at a setpoint of 52.0% (SP) within an allowable deadband of ±0.5%. The measured variable (PV) is the moisture content signal from MM-701, which outputs a 4-20 mA signal corresponding to a range of 40.0% to 60.0% moisture. The manipulated variable (MV) is the hydraulic pressure applied to the shoe press via control valve PV-101.

The PID controller (LIC-701) is configured for reverse-acting control, where an increase in PV results in a decrease in MV. The controller tuning parameters are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 min, and derivative time (Kd) = 0.2 min. The output of the controller is clamped between 0% and 100% to ensure the hydraulic pressure remains within the operational limits of the press system. The controller includes anti-windup logic to prevent integral accumulation when the output is saturated.

The signal from MM-701 is scaled from 4-20 mA to engineering units (40.0% to 60.0%) before entering the PID controller. Bumpless transfer logic is implemented to ensure a smooth transition between manual and automatic modes. Manual setpoint adjustments are clamped between 50.0% and 54.0% moisture to maintain safe operating conditions. A deadband of 0.5% is applied to the control output to prevent hunting and excessive wear on PV-101.


### 8.2) Interlocks and Permissives

The PID control loop is enabled only when the following permissives are satisfied: the shoe press hydraulic system is operational (HS-701 = ON), the press section conveyor is running (CS-701 = ON), and the sheet is present as detected by the sheet break sensor (SB-701 = OFF). If any of these conditions are not met, LIC-701 is forced to manual mode, and the output is held at its last value.

An interlock is configured such that if the shower water temperature exceeds 75.0°C as measured by TT-102, or if the press fabric moisture exceeds 65.0% as measured by MM-701, PV-101 is commanded to its fail-safe position (fail-closed) to protect the equipment. Additionally, if the hydraulic pressure exceeds 1200 kPa as measured by PT-701, the control loop is disabled, and an emergency shutdown (ESD) signal is initiated.


### 8.3) Alarm and Fault Handling

High and low alarms are configured for the moisture content measured by MM-701. A high alarm (MM-701.HI) is triggered at 58.0%, and a low alarm (MM-701.LO) is triggered at 46.0%. These alarms are latched and require operator acknowledgment. A deviation alarm (LIC-701.DEV) is activated if the difference between the setpoint and the process variable exceeds 2.0% for more than 30 seconds.

In the event of a transmitter fault (MM-701.FLT), the PID controller LIC-701 is automatically switched to manual mode, and the control output is held at its last value. A fault alarm is raised, and the operator is required to investigate and resolve the issue before the loop can be returned to automatic control. Similarly, if PV-101 fails to respond to control signals, as indicated by the valve position feedback, an alarm (PV-101.FLT) is generated, and the valve is commanded to its fail-closed position.


## 9 **Dryer Section**
|Tagname | Type | Description |
|---------|------|-------------|
|F-801 | Exhaust Fan | Regulates exhaust fan speed for dryer section airflow control. |
|FV-801 | Flow Valve | Controls steam flow to maintain cylinder temperature. |
|IR-801 | Infrared Scanner | Provides moisture feedback for drying process optimization. |
|M-801 | Motor | Drives mechanical components in the dryer section. |
|PT-801 | Pressure Transmitter | Measures steam pressure in the cylinder system. |
|SC-801 | Steam Cylinder | Provides heat for drying via steam-heated surface. |
|TC-801 | Temperature Controller | Regulates hood air temperature using PID control. |
|TT-801 | Temperature Transmitter | Measures cylinder temperature for process control. |
|TT-802 | Temperature Transmitter | Measures hood air temperature for control feedback. |
|WT-801 | Web Tension Sensor | Monitors web tension to ensure stable drying. |
|XV-802 | On-Off Valve | Controls hot air damper for hood temperature regulation. |


### 9.1) Control Strategy Description

The dryer section utilizes PID control to regulate the steam-heated cylinder temperature (SC-801), hood air temperature (TC-801), exhaust fan speed (F-801), infra-red moisture scanner feedback (IR-801), and web tension (WT-801). The primary control objective is to maintain the final sheet moisture content at 4.5% ± 0.2% while ensuring stable web tension and uniform drying.

For SC-801, the temperature control loop uses TT-801 as the process variable (PV) with a setpoint (SP) of 115°C. The PID controller (TC-801) is configured for reverse-acting control to reduce steam flow when the cylinder temperature exceeds the SP. Tuning parameters are set as Kp=3.0, Ki=0.5 min, and Kd=0.1 min. The controller output (MV) drives FV-801, a steam control valve, with an output range of 0–100% corresponding to 4–20 mA. TT-801 has a measurement span of 0–150°C and signal type 4–20 mA. FV-801 is configured to fail-closed to prevent overheating during loss of control signal.

For TC-801, hood air temperature is controlled using TT-802 as PV with an SP of 85°C. The PID controller is configured for direct-acting control, increasing hot air flow when the temperature falls below the SP. Tuning parameters are Kp=2.5, Ki=0.8 min, and Kd=0.2 min. The controller output drives XV-802, a hot air damper actuator, with an output range of 10–90% scaled linearly to 4–20 mA. TT-802 has a measurement span of 50–120°C. XV-802 is configured to fail-open for safety during signal loss.

Infra-red moisture scanner IR-801 provides real-time feedback to a moisture control loop. The PV is the sheet moisture content, measured in % with a span of 0–10%. The SP is set to 4.5%. The PID controller adjusts exhaust fan speed (F-801) via a variable frequency drive (VFD) to control drying intensity. Tuning parameters are Kp=1.8, Ki=0.6 min, and Kd=0.05 min. The VFD signal output range is 0–100%, scaled to 4–20 mA. The VFD is configured for bumpless transfer between manual and automatic modes.

Web tension control uses WT-801 load cells to measure tension in N/m with a span of 0–500 N/m. The SP is set to 250 N/m. The PID controller adjusts the torque on the downstream drive roll to maintain tension. Tuning parameters are Kp=4.0, Ki=1.0 min, and Kd=0.3 min. The controller output drives the motor torque control signal, scaled 0–100% to 4–20 mA. Anti-windup logic is implemented to prevent integral saturation during sudden load changes.


### 9.2) Interlocks and Permissives

Steam flow to SC-801 is interlocked with the cylinder pressure transmitter (PT-801). Steam flow is inhibited if PT-801 indicates pressure above 900 kPa. Hood air temperature control via TC-801 is permissive on XV-802 being in the open position and TT-802 reading within the range of 50–120°C. Exhaust fan speed control via F-801 is interlocked with IR-801 availability; fan speed adjustment is disabled if IR-801 signal is lost or out of range.

Web tension control via WT-801 is permissive on the upstream drive roll motor (M-801) being operational. Tension control is inhibited if WT-801 signal falls below 10% of span or exceeds 90% of span, triggering a drive roll stop command. All control loops include a permissive for manual override, allowing operators to disable automatic control for maintenance purposes.


### 9.3) Alarm and Fault Handling

High-temperature alarms are configured for SC-801 and TC-801. If TT-801 exceeds 125°C or TT-802 exceeds 95°C, an alarm is triggered, and FV-801 and XV-802 are forced to their fail-safe positions (fail-closed and fail-open, respectively). A low-pressure alarm is set for PT-801; if pressure drops below 600 kPa, steam flow is inhibited, and an operator notification is issued.

Moisture scanner IR-801 triggers a high-moisture alarm if the sheet moisture exceeds 5.0%. The exhaust fan speed is ramped to maximum, and an operator notification is issued. WT-801 triggers a high-tension alarm if tension exceeds 400 N/m, initiating a controlled stop of the drive roll to prevent web damage. All PID controllers are equipped with fault detection logic to identify signal loss or out-of-range conditions. Upon fault detection, controllers revert to manual mode, and a fault notification is logged in the control system.


## 10 **Finishing and Winding**
|Tagname | Type | Description |
|---------|------|-------------|
|AL-901 | Analyzer | Monitors process parameter for quality control |
|AL-903 | Analyzer | Provides additional process analysis data |
|CW-901 | Cooling Water System | Supplies cooling water to the process |
|FIC-904 | Flow Controller | Regulates coating flow rate to maintain setpoint |
|FT-901 | Force Transmitter | Measures calender stack nip load (0–100 kN) |
|FT-902 | Flow Transmitter | Measures coating flow rate (0–500 L/min) |
|FV-104 | Flow Valve | Modulates coating flow rate based on control signal |
|XV-105 | On-Off Valve | Isolates or permits flow in the process line |


### 10.1) Control Strategy Description

In the **Finishing and Winding** section, ratio control is implemented to maintain a precise proportional relationship between the coating application rate and the calender stack nip load. The wild variable is the calender stack nip load, measured by force transmitter FT-901, with a range of 0–100 kN. The controlled variable is the coating flow rate, regulated by flow control valve FV-104, with flow transmitter FT-902 measuring a range of 0–500 L/min. The ratio controller, designated as FFIC-903, calculates the setpoint for the coating flow rate based on the measured nip load and a configurable ratio setpoint.

The ratio setpoint, entered by the operator via the human-machine interface (HMI), is adjustable between 1.5:1 and 3.0:1. For example, if the nip load is measured at 60 kN and the ratio setpoint is 2.0:1, FFIC-903 calculates the coating flow setpoint as 120 L/min. This setpoint is sent to the flow controller FIC-904, which modulates FV-104 to maintain the desired flow rate. The ratio controller includes a manual bias adjustment feature, allowing operators to fine-tune the ratio within ±0.2 of the setpoint for quality optimization.

To ensure stable operation, the ratio controller is equipped with low-flow cutoff logic. If the nip load falls below 5 kN, FFIC-903 outputs a zero setpoint to FIC-904, closing FV-104 to prevent under-coating. Additionally, signal scaling ensures that all measurements are normalized to engineering units before ratio calculations. Transition ramping logic is employed during startup or ratio setpoint changes, limiting the rate of change to 0.1 ratio units per second to avoid process disturbances.


### 10.2) Interlocks and Permissives

The ratio control loop is interlocked with the calender stack and coating station to ensure safe operation. XV-105, the upstream shut-off valve for the coating station, must be open, and the calender stack must be running at a minimum nip load of 5 kN (verified by FT-901) before FFIC-903 is enabled. If either permissive condition is not met, FFIC-903 outputs a zero setpoint to FIC-904, forcing FV-104 to close.

An additional interlock ensures that the LASER coat-weight sensor CW-901 is operational and transmitting valid data. If CW-901 detects a coat-weight deviation exceeding ±10% from the target, FFIC-903 is automatically disabled, and the system reverts to manual control. The operator is alerted to investigate and resolve the issue before re-enabling the ratio control loop.


### 10.3) Alarm and Fault Handling

The system generates alarms for deviations and faults within the ratio control loop. A high-ratio deviation alarm (AL-903-H) is triggered if the actual coating flow rate deviates by more than 5% from the setpoint calculated by FFIC-903 for more than 10 seconds. This alarm prompts the operator to check FV-104 and associated instrumentation for potential issues.

A low-nip-load alarm (AL-901-L) is activated if FT-901 measures a nip load below 5 kN, indicating that the calender stack is not operating within the required range for coating application. This condition forces FFIC-903 to output a zero setpoint to FIC-904, preventing coating flow.

Instrumentation faults, such as signal loss from FT-901, FT-902, or CW-901, trigger a system fault alarm (AL-903-F) and disable FFIC-903. The system transitions to manual control, and FV-104 is closed to prevent uncontrolled coating application. The operator must address the fault and confirm resolution before reactivating the ratio control loop.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 10

- Total Tagnames: 72

- Word Count: 6796
