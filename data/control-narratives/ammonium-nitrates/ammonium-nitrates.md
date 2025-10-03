# Ammonium Nitrate Production Process Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Neutralization Reactor**
3. **Evaporation and Conditioning**
4. **Prilling Tower/Granulator**
5. **Cooling and Coating Circuit**
6. **Storage and Load-Out**

---


## 1 **Process Overview and Scope**

The production process for ammonium nitrate is designed to ensure high product quality, operational safety, and compliance with environmental standards. The process begins with the neutralization of ammonia and nitric acid in a controlled reactor environment, producing a neutral liquor of approximately 60 wt % ammonium nitrate. This liquor is then concentrated through a multi-effect evaporator system to achieve the desired melt concentration of 99 wt %, while minimizing thermal decomposition and recovering condensate for reuse. The concentrated melt is subsequently solidified into prills or granules using either a prilling tower or fluidized-bed granulator, with controlled cooling and exhaust-gas scrubbing to manage emissions and ensure uniform particle size.

Following solidification, the product undergoes cooling and coating to stabilize its thermal properties and prevent caking during storage. Rotary or belt coolers lower the temperature, while an anti-caking agent is applied to ensure product integrity. Dust extraction systems maintain clean operating conditions throughout this stage. Finally, the finished product is transferred to silos for storage, with level monitoring, aeration, and automated load-out sequencing ensuring efficient handling and shipping operations. Critical control strategies across all stages include precise flow, temperature, and pressure regulation, as well as advanced interlocks and alarms to mitigate risks and maintain safe operating conditions.

Key relationships between process sections are maintained to ensure seamless material flow and consistent product quality. For example, the evaporator feed rate is directly influenced by neutralizer output, while the solidification stage relies on melt properties established during evaporation. Safety and operational integrity are prioritized throughout the system, with alarms, trips, and emission controls integrated to prevent environmental impact and equipment damage. This holistic approach aligns production objectives with stringent safety and regulatory requirements, ensuring reliable and efficient operation.


## 2 **Neutralization Reactor**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-101 | Flow Controller | Controls reactor inlet flow rate |
|FIC-102 | Flow Controller | Modulates nitric acid flow to maintain ratio control |
|FT-101 | Flow Transmitter | Measures ammonia gas flow for ratio control input |
|FV-101 | Flow Valve | Regulates ammonia gas flow into the reactor |
|FV-102 | Flow Valve | Controls nitric acid flow based on ratio controller setpoint |
|LT-104 | Level Transmitter | Monitors reactor level for interlock permissive signal |
|PH-105 | pH Transmitter | Measures reactor pH for process monitoring |
|TIC-103 | Temperature Controller | Regulates reactor temperature for optimal conditions |
|VS-107 | Vent Scrubber | Removes harmful gases from reactor exhaust for safety compliance |


### 2.1) Control Strategy Description

The neutralization reactor employs ratio control to maintain a precise proportional relationship between ammonia gas flow (wild flow) and nitric acid flow (controlled flow) to achieve optimal neutralization conditions. Ammonia flow is measured by FT-101 with a range of 0-500 kg/hr and serves as the wild flow input to the ratio controller FFIC-102. The ratio controller calculates the nitric acid flow setpoint using the configured ammonia-to-acid ratio of 1.8:1. The calculated setpoint is sent to FIC-102, which modulates the acid flow control valve FV-102 to maintain the desired flow rate. For example, if FT-101 measures ammonia flow at 400 kg/hr, FFIC-102 calculates the nitric acid flow setpoint as 720 kg/hr (400 × 1.8). The ratio controller is configured with ratio adjustment limits of 1.5:1 to 2.0:1 to ensure safe operation and prevent over-neutralization or acid excess. Signal scaling ensures that FT-101 and FFIC-102 inputs are linearly mapped to the controller range of 0-100%. A 2% deadband is implemented in FFIC-102 to minimize valve wear during steady-state conditions.


### 2.2) Interlocks and Permissives

The ratio control system is interlocked with the reactor level transmitter LT-104 and the vent scrubber VS-107 to ensure safe operation. LT-104 provides a permissive signal to FFIC-102, allowing acid flow only when the reactor level is above 20% and below 90% of its capacity. If the level falls below 20%, acid flow is stopped to prevent dry running of the reactor. If the level exceeds 90%, acid flow is stopped to prevent overflow. VS-107 provides a permissive signal to FT-101, ensuring ammonia sparging is disabled if vent scrubber operation is interrupted. Additionally, FFIC-102 will clamp the acid flow setpoint to zero if TIC-103 detects reactor temperature exceeding 190 °C, preventing thermal runaway. Manual mode selection for FFIC-102 and FIC-101 is available but requires operator confirmation via a dedicated DCS screen.


### 2.3) Alarm and Fault Handling

Alarm conditions are configured for deviations in the ammonia-to-acid ratio, flow measurement faults, and reactor conditions. FFIC-102 generates a high-ratio alarm if the calculated ratio exceeds 2.0:1 and a low-ratio alarm if it falls below 1.5:1. FT-101 and FIC-102 generate flow fault alarms if their measured values fall below 10 kg/hr for more than 30 seconds, triggering a low-flow cutoff to prevent unstable operation. TIC-103 generates a high-temperature alarm at 190 °C and shuts off acid flow via FV-102 and ammonia sparging via FV-101. PH-105 provides a pH deviation alarm if the reactor pH deviates more than ±0.3 from the target value of 7.0, indicating improper neutralization. All alarms are logged in the DCS, and operators are prompted to acknowledge and investigate the cause of the fault. In the event of a critical fault, FFIC-102 transitions to manual mode, allowing operators to control acid flow directly while troubleshooting the system.


## 3 **Evaporation and Conditioning**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-102 | Flow Controller | Regulates steam flow to maintain temperature setpoint in secondary loop |
|FV-102 | Flow Valve | Adjusts steam flow based on control signal from FIC-102 |
|HS-204 | Hand Switch | Manual override for equipment operation |
|P-205 | Pump | Circulates neutral liquor in the evaporator system |
|PT-203 | Pressure Transmitter | Measures vacuum pressure in the evaporator system |
|PV-106 | Pressure Valve | Controls pressure within the system |
|TIC-201 | Temperature Controller | Maintains melt temperature setpoint in primary loop |
|TT-103 | Temperature Transmitter | Measures melt temperature for TIC-201 input |
|TT-104 | Temperature Transmitter | Measures steam temperature at evaporator inlet for FIC-102 input |
|VS-206 | Vacuum Switch | Monitors vacuum conditions for system safety |
|XV-101 | On-Off Valve | Provides isolation for system components during maintenance or emergency shutdown |


### 3.1) Control Strategy Description

The triple-effect forced-circulation evaporator system employs cascade control to maintain melt temperature (TIC-201) and vacuum pressure (PT-203) for optimal concentration of neutral liquor to 99 wt % ammonium nitrate. The primary loop is configured to regulate melt temperature using TIC-201 as the master controller. TIC-201 receives input from TT-103, which measures the melt temperature, and maintains a setpoint of 198 °C. The output of TIC-201, scaled linearly between 1% and 96%, serves as the remote setpoint (RSP) for the secondary loop.

The secondary loop, controlled by FIC-102, adjusts steam flow via FV-102 to achieve the temperature setpoint provided by TIC-201. FIC-102 receives input from TT-104, which measures steam temperature at the evaporator inlet. The secondary loop is tuned for faster response with proportional gain (Kp) set to 3.5 and integral time (Ki) set to 0.3 minutes, ensuring rapid disturbance rejection. The primary loop is tuned for slower, stable control with Kp set to 1.2 and Ki set to 2.0 minutes. This tuning hierarchy ensures decoupling between loops, minimizing interaction and preventing hunting.

Signal scaling between TIC-201 and FIC-102 ensures compatibility between the melt temperature range (190–210 °C) and the steam flow range (0–100%). Operator-entered setpoints for TIC-201 are clamped between 14% and 92% to maintain safe operation. Cascade mode allows TIC-201 to automatically adjust FIC-102's setpoint, while local/manual mode permits direct operator control of FV-102. Transition delays of 5 seconds are implemented during mode switching to prevent process instability.


### 3.2) Interlocks and Permissives

Steam flow control via FV-102 is interlocked with HS-204 to trip steam supply in the event of high melt temperature exceeding 210 °C. TIC-201 will hold its output at 0% if HS-204 trips, preventing further heating. Vacuum pressure control via PV-106 is permitted only when TIC-201 is in cascade mode and PT-203 indicates a vacuum level within the operating range of 0.2–0.5 bar. Permissive logic ensures that TIC-201 will not initiate cascade control until TT-103 and TT-104 are validated to be within calibrated ranges (±0.5 °C accuracy). Steam flow adjustments are inhibited if TT-104 indicates inlet steam temperature below 100 °C.

The molten-salt jacketed pump P-205 will not start unless TIC-201 is in cascade mode and melt temperature exceeds 195 °C. Additionally, XV-101, the shut-off valve, must be open for steam flow to FV-102. Barometric condenser VS-206 operation is interlocked with PT-203 to ensure vacuum pressure remains below 0.5 bar before initiating condensate recovery.


### 3.3) Alarm and Fault Handling

High-temperature alarms are triggered if TT-103 detects melt temperature exceeding 210 °C. Upon alarm activation, TIC-201 output is forced to 0%, and HS-204 trips steam supply by closing XV-101. Low-temperature alarms are triggered if TT-103 detects melt temperature below 190 °C for more than 10 seconds, prompting an operator notification but allowing continued operation. Vacuum pressure alarms are activated if PT-203 detects pressure above 0.5 bar or below 0.2 bar. In such cases, TIC-201 will suspend cascade control and revert to manual mode.

Secondary controller FIC-102 failure results in TIC-201 holding its output at the last valid setpoint and switching to manual mode. Operators are notified immediately, and FV-102 can be adjusted manually. Deadband logic prevents cascade hunting by suspending TIC-201 output adjustments for temperature deviations smaller than ±0.2 °C. Faults in TT-103 or TT-104 trigger an immediate shutdown of TIC-201 and FIC-102, with all control valves (FV-102, PV-106) forced to their fail-safe positions.


## 4 **Prilling Tower/Granulator**
|Tagname | Type | Description |
|---------|------|-------------|
|AT-303 | Analyzer Transmitter | Monitors and analyzes process parameters for quality control |
|FIC-301 | Flow Controller | Regulates melt flow to maintain bed temperature stability |
|FT-301 | Flow Transmitter | Measures melt flow rate for feedback to FIC-301 |
|FV-301 | Flow Valve | Adjusts melt flow based on FIC-301 output |
|GR-306 | Granulator | Facilitates solidification of ammonium nitrate in the prilling process |
|PR-305 | Pressure Transmitter | Monitors pressure within the prilling tower system |
|RTD-302 | Temperature Transmitter | Provides bed temperature feedback to TIC-302 |
|TIC-302 | Temperature Controller | Maintains bed temperature stability via cascade control |
|VS-304 | Vibration Sensor | Detects vibration levels in equipment for operational safety |


### 4.1) Control Strategy Description

The cascade control system for the **Prilling Tower/Granulator** is designed to regulate melt flow and bed temperature to ensure consistent solidification of ammonium nitrate. The primary loop is configured to maintain bed temperature stability via TIC-302, while the secondary loop modulates melt flow using FIC-301. The primary controller, TIC-302, receives bed temperature feedback from RTD-302, compares it to the operator-defined setpoint of 185°C, and outputs a remote setpoint (RSP) to FIC-301. FIC-301, the secondary controller, adjusts melt flow based on FT-301 feedback to achieve the temperature stabilization demanded by TIC-302.

TIC-302 is tuned with proportional gain (Kp=1.2) and integral time (Ki=2.0 min) to ensure stable bed temperature control. FIC-301 is tuned with faster dynamics (Kp=3.5, Ki=0.3 min) to reject disturbances in melt flow quickly. The secondary loop operates 5-10 times faster than the primary loop to decouple melt flow disturbances from the slower bed temperature response. The melt flow control valve, FV-301, responds to FIC-301 output within a range of 0-100% to maintain flow rates between 2.5–5.0 m³/h, scaled to match the engineering units of FT-301.

The cascade configuration includes signal scaling between TIC-302 and FIC-301 to ensure RSP alignment with the secondary loop’s operating range. In cascade mode, TIC-302 dynamically adjusts FIC-301’s setpoint based on bed temperature deviations, while FIC-301 independently controls melt flow using FT-301 feedback. Mode selection allows operators to switch between cascade, local, and manual operation. In local mode, FIC-301 operates independently with a fixed setpoint, bypassing TIC-302. Setpoint clamping prevents TIC-302 from commanding melt flow rates outside the permissible range, ensuring FV-301 does not saturate.


### 4.2) Interlocks and Permissives

The cascade control system is interlocked to ensure safe operation. Melt flow control via FIC-301 is enabled only when FT-301 confirms flow within the range of 2.5–5.0 m³/h and FV-301 is responsive. TIC-302 will not output a remote setpoint to FIC-301 unless RTD-302 indicates a valid temperature reading within the operational range of 150–200°C. Additionally, the exhaust gas scrubber VS-304 must be operational and AT-303 must confirm air humidity below 15 g H₂O/kg before cascade control is permitted.

Permissives include verification that PR-305 or GR-306 is actively collecting solidified product, ensuring that the melt flow and bed temperature control loops are functioning within the context of the solidification process. If FT-301 or RTD-302 signals are invalid, the system automatically transitions to manual mode, requiring operator intervention.


### 4.3) Alarm and Fault Handling

Alarm conditions are triggered if TIC-302 detects bed temperature deviations exceeding ±5°C from the setpoint or if FIC-301 fails to maintain melt flow within ±0.1 m³/h of its commanded setpoint. High-priority alarms include FV-301 saturation, FT-301 signal loss, or RTD-302 temperature readings outside the range of 150–200°C. In the event of a secondary loop failure, such as FT-301 signal loss or FV-301 malfunction, the system transitions to local mode, where FIC-301 operates independently with a fixed setpoint.

If TIC-302 fails, the cascade control system will automatically disable RSP output to FIC-301, locking melt flow at the last known setpoint to prevent uncontrolled flow. Deadband logic is applied to TIC-302 to prevent hunting during minor bed temperature fluctuations, ensuring stable operation. Timer delays are implemented during cascade mode transitions to avoid abrupt changes that could destabilize the secondary loop. Operator alarms are displayed on the DCS, and fault conditions require manual acknowledgment before the system can resume cascade control.


## 5 **Cooling and Coating Circuit**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-402 | Flow Controller | Adjusts flow rate of anti-caking agent in secondary loop |
|FT-402 | Flow Transmitter | Measures flow rate of anti-caking agent for feedback to FIC-402 |
|FV-402 | Flow Valve | Modulates flow of anti-caking agent based on FIC-402 output |
|MP-405 | Pump | Circulates cooling medium through the cooling circuit |
|PS-403 | Pressure Switch | Monitors pressure in the cooling circuit for safety interlock |
|PSA-404 | Pressure Alarm | Alerts high-pressure condition in the cooling circuit |
|TIC-401 | Temperature Controller | Regulates cooler outlet temperature via cascade control |
|TT-401 | Temperature Transmitter | Measures cooler outlet temperature for feedback to TIC-401 |


### 5.1) Control Strategy Description

The cooling and coating circuit employs a cascade control strategy to maintain product thermal stability and ensure uniform application of the anti-caking agent. The primary loop, controlled by TIC-401, regulates the cooler outlet temperature to a setpoint of 45 °C. TIC-401 receives temperature feedback from TT-401, which measures the cooler outlet temperature after linear scaling to compensate for sensor drift. TIC-401 outputs a remote setpoint (RSP) to the secondary loop, controlled by FIC-402, which adjusts the flow rate of the anti-caking agent. FIC-402 modulates control valve FV-402 to maintain the flow rate at the desired setpoint, ensuring precise application of the agent.

The secondary loop operates with a faster response time, tuned to reject disturbances within 2 seconds, compared to the primary loop’s slower response of approximately 10 seconds. Secondary controller FIC-402 is tuned with Kp=3.5 and Ki=0.3 min, while TIC-401 is tuned with Kp=1.2 and Ki=2.0 min to ensure stable cascade operation. Signal scaling is applied between TIC-401’s output range of 0–100% and FIC-402’s input range of 0–10 L/min to maintain compatibility. Manual setpoint adjustments for TIC-401 are clamped between 22 °C and 80 °C to prevent unsafe operating conditions.

In cascade mode, TIC-401 dynamically adjusts FIC-402’s setpoint to maintain the cooler outlet temperature. During secondary loop failure, TIC-401 enters local mode, maintaining the last known stable setpoint for FIC-402. Deadband logic is implemented in TIC-401 to prevent hunting between loops, with a ±0.5 °C tolerance band around the cooler temperature setpoint.


### 5.2) Interlocks and Permissives

Cascade control activation is permitted only when TT-401 and FT-402 are operational and within calibrated ranges. TT-401 must report a valid temperature signal between 0 °C and 100 °C, and FT-402 must measure flow rates between 0.5 L/min and 10 L/min. The dust extraction system, monitored by PS-403, must maintain a differential pressure of ≤200 Pa to ensure adequate ventilation during operation. PSA-404 must confirm particle size distribution within 2–4 mm before allowing cascade mode, ensuring proper coating conditions. MP-405 must report moisture levels below 0.3 wt % to prevent caking.

If TT-401 fails or reports an invalid signal, TIC-401 automatically switches to manual mode, allowing operators to set a fixed flow rate for FIC-402. Similarly, if FT-402 fails, FIC-402 enters manual mode, holding the last known valve position. Cascade mode is disabled if PS-403 exceeds 200 Pa or PSA-404 detects particle size deviations beyond the acceptable range.


### 5.3) Alarm and Fault Handling

Alarm conditions for TIC-401 include deviations exceeding ±2 °C from the setpoint, triggering a high-temperature alarm at 50 °C and a low-temperature alarm at 40 °C. FIC-402 generates alarms for flow rates below 0.5 L/min or above 10 L/min, indicating potential valve or pump issues. TT-401 failure triggers a fault alarm, switching TIC-401 to manual mode and notifying operators.

In the event of secondary loop failure, TIC-401 freezes its output to FIC-402 at the last stable setpoint, preventing erratic flow adjustments. FIC-402 enters manual mode, allowing operators to manually position FV-402. If PS-403 exceeds 200 Pa, the dust extraction system trips, halting the cooling and coating circuit to prevent unsafe conditions. All alarms are logged in the DCS, and operators are required to acknowledge faults before re-enabling cascade control.


## 6 **Storage and Load-Out**
|Tagname | Type | Description |
|---------|------|-------------|
|AP-503 | Analyzer | Monitors product quality parameters during load-out operations. |
|FIC-507 | Flow Controller | Regulates SC-504 discharge rate to maintain desired flow ratio. |
|LT-501 | Level Transmitter | Measures silo level to prevent overloading or underfeeding. |
|PLC-506 | Programmable Logic Controller | Executes control logic for storage and load-out processes. |
|PRV-502 | Pressure Relief Valve | Protects system from overpressure conditions. |
|RIC-506 | Ratio Controller | Calculates flow setpoint for SC-504 based on WB-505 flow and ratio setpoint. |
|SC-504 | Screw Conveyor | Transfers product from silo at controlled discharge rate. |
|WB-505 | Weighbridge | Provides continuous product flow rate measurement for ratio control. |


### 6.1) Control Strategy Description

The **Storage and Load-Out** section utilizes ratio control to maintain proportional relationships between product flow rates during silo discharge and load-out operations. The wild flow measurement is derived from the weighbridge WB-505, which provides a continuous product flow rate signal in the range of 0–2000 kg/hr. The controlled flow measurement is the reclaim screw conveyor SC-504, which adjusts its discharge rate based on the desired ratio. The ratio controller RIC-506 calculates the controlled flow setpoint using the formula:
**SC-504 Flow SP = WB-505 Flow × Ratio SP**.

The ratio setpoint is configured to maintain a 1.5:1 relationship between the weighbridge flow and the screw conveyor flow. This ensures that the product discharge rate from the silo matches the load-out requirements while avoiding overfilling or underfeeding. The ratio controller RIC-506 outputs the calculated setpoint to the flow controller FIC-507, which modulates the speed of SC-504 via its motor drive to achieve the desired flow.

The ratio adjustment limits are defined as 1.0:1 to 2.0:1 to accommodate varying load-out conditions. A manual bias adjustment is available through the HMI, allowing operators to fine-tune the ratio within these bounds. Automatic ratio trim is implemented based on silo level feedback from LT-501; if the silo level exceeds 80%, the ratio is reduced to prevent overloading SC-504. Conversely, if the silo level drops below 20%, the ratio is increased to expedite load-out operations.


### 6.2) Interlocks and Permissives

The ratio control logic is integrated with interlocks and permissives to ensure safe and reliable operation. The reclaim screw conveyor SC-504 will not start unless the following conditions are met:
1. The silo level LT-501 must be above the low-level threshold of 10%.
2. The aeration pads AP-503 must be active to ensure product flowability.
3. The over-pressure relief valve PRV-502 must be closed, confirming that the silo is operating within safe pressure limits.

The weighbridge WB-505 signal is normalized to a 0–100% scale to ensure compatibility with the ratio controller RIC-506. A Boolean interlock disables ratio control if the WB-505 flow rate falls below 100 kg/hr, preventing erroneous operation during low-flow conditions. Mode switching between automatic ratio control and manual operation is bumpless, with safety checks to ensure that the reclaim screw conveyor SC-504 does not exceed its maximum speed of 1500 RPM during transitions.


### 6.3) Alarm and Fault Handling

Alarm handling is implemented to address deviations in ratio control and equipment faults. If the calculated ratio exceeds the configured limits of 1.0:1 to 2.0:1, an alarm is triggered on the HMI, and the ratio controller RIC-506 clamps the setpoint to the nearest limit. A low-flow alarm is activated if the weighbridge WB-505 signal drops below 100 kg/hr, and the reclaim screw conveyor SC-504 is stopped to prevent damage or underfeeding.

Silo level alarms are configured as follows:
- High-level alarm at 90% (LT-501) triggers a reduction in the ratio setpoint to 1.0:1.
- Low-level alarm at 10% (LT-501) stops SC-504 and activates the aeration pads AP-503 to restore flowability.

Fault conditions in PRV-502 or AP-503 result in an immediate shutdown of SC-504 and disable ratio control. Hysteresis of 5% is applied to alarm thresholds to prevent nuisance alarms due to minor fluctuations. All alarms and faults are logged in PLC-506 for operator review and troubleshooting.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 6

- Total Tagnames: 43

- Word Count: 3693
