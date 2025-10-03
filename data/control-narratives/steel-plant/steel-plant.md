# Integrated Steel Plant Process Control Narrative

---


## Table of Contents

1. Process Overview and Scope
2. Sinter Plant
3. Coking Facility
4. Blast Furnace
5. Basic Oxygen Furnace (BOF)
6. Secondary Metallurgy
7. Continuous Casting
8. Rolling Mills
9. By-Product Recovery Systems

---


## 1 ** Process Overview and Scope **

The steel plant operates as an integrated facility designed to convert iron ore, coal, and fluxes into crude steel through a series of interconnected process phases. The overall objective is to produce high-quality steel products efficiently while minimizing environmental impact and maximizing resource utilization. Starting with raw material preparation, iron ore fines are agglomerated in the sinter plant and charged to the blast furnace alongside coke produced in the on-site coking facility. The blast furnace employs hot blast air and injected pulverized coal to reduce iron ore, generating molten hot metal and slag. This molten metal is then transferred to the steelmaking stage for further refinement.

In the steel shop, basic oxygen furnaces (BOF) are used to refine the molten hot metal by blowing oxygen to remove impurities such as carbon and sulfur. Alloying additions are precisely controlled during this phase to achieve specific steel grades. Secondary metallurgy processes, including ladle furnace treatment, vacuum degassing, and inclusion modification, ensure tight control over composition and quality parameters. Once refined, liquid steel is solidified into semi-finished products such as slabs, blooms, or billets using continuous casting machines. These semi-finished products are subsequently rolled in downstream mills to produce finished steel products, including hot-rolled coils, plates, bars, and structural profiles.

Throughout the facility, advanced control strategies are employed to optimize energy efficiency, maintain product quality, and ensure safe operation. By-product recovery systems capture off-gases from the blast furnace, coke ovens, and BOF to generate steam and electricity, reducing external energy demand. Solid by-products such as slag, dust, and other residues are processed for reuse or sale, meeting stringent environmental and economic objectives. The integration of these systems ensures seamless coordination between process phases, contributing to a high-throughput, flexible production environment capable of meeting diverse market demands.


## 2 ** Sinter Plant ** 
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-102 | Flow Controller | Adjusts flux flow to maintain iron ore fines-to-flux ratio. |
|FT-101 | Flow Transmitter | Measures mass flow rate of iron ore fines (wild flow). |
|FT-102 | Flow Transmitter | Measures mass flow rate of fluxes for ratio control. |
|FV-102 | Flow Valve | Modulates flux flow to achieve setpoint calculated by ratio controller. |
|TIT-101 | Temperature Transmitter | Monitors sintering machine's temperature profile for quality feedback. |


### 2.1) Control Strategy Description

The sinter plant ratio control system ensures precise proportional blending of iron ore fines, fluxes, and coke breeze to maintain optimal sintering conditions. The wild flow, representing the uncontrolled mass flow rate of iron ore fines, is measured by FT-101, with a range of 0-1000 kg/hr. The controlled flow, representing the mass flow rate of fluxes, is adjusted by FIC-102 to maintain a fixed ratio of 2.5:1 (iron ore fines to fluxes). The ratio controller FFIC-103 calculates the flux flow setpoint (SP) as the product of the wild flow measurement (PV) from FT-101 and the ratio setpoint. For example, if FT-101 measures 600 kg/hr, FFIC-103 calculates the flux flow SP as 240 kg/hr. The control valve FV-102 modulates the flux flow to achieve this setpoint.

To ensure stability, the ratio setpoint is clamped between 2.0:1 and 3.0:1. Ratio bias adjustments are available via manual operator input on FFIC-103, allowing fine-tuning within ±0.2 of the setpoint. Automatic ratio trim logic adjusts the ratio based on sinter quality feedback from TIT-101, which monitors the sintering machine's temperature profile. A low flow cutoff disables ratio control if FT-101 measures less than 50 kg/hr, switching FIC-102 to manual mode to prevent hunting.


### 2.2) Interlocks and Permissives

The ratio control system incorporates interlocks to ensure safe operation. FFIC-103 is enabled only if FT-101 and FT-102 are operational, with valid flow measurements within their calibrated ranges. Boolean permissive logic ensures that FV-102 cannot open unless FT-101 detects a flow greater than 50 kg/hr and TIT-101 confirms a sintering machine temperature above 800°C. If FT-101 fails or TIT-101 measures a temperature below 800°C, FFIC-103 switches to manual mode, and FV-102 closes to prevent uncontrolled flux addition.

Mode selection logic allows operators to toggle between automatic ratio control and manual adjustment. In manual mode, FIC-102 operates independently of FFIC-103, allowing direct control of FV-102. Signal scaling ensures ratio calculations remain accurate across the full flow range, with wild flow signals normalized to a 0-1000 kg/hr scale before input to FFIC-103.


### 2.3) Alarm and Fault Handling

The control system generates alarms for ratio deviations exceeding ±0.1 from the setpoint. If FFIC-103 detects a calculated flux flow SP outside the allowable range (200-300 kg/hr), a high/low ratio alarm is triggered. FT-101 and FT-102 transmitters are equipped with fault detection logic; any sensor failure activates a transmitter fault alarm and disables FFIC-103.

In the event of a low flow condition (<50 kg/hr on FT-101), a low flow alarm is raised, and FFIC-103 transitions to manual mode. TIT-101 temperature deviations below 800°C trigger a sintering temperature alarm, inhibiting ratio control and closing FV-102 to prevent improper flux dosing. All alarms are logged in the plant historian for diagnostic purposes, and operators are notified via the HMI for corrective action.


## 3 ** Coking Facility ** 
|Tagname | Type | Description |
|---------|------|-------------|
|CO-201 | Coking Oven | Primary vessel for coke production process |
|CO-202 | Quenching Tower | Cools coke using quenching water |
|DA-201 | Deviation Alarm | Alerts when temperature sensors deviate beyond ±5% from median value |
|DA-202 | Deviation Alarm | Monitors pressure sensor deviations in the coking ovens |
|FA-201 | Flow Alarm | Indicates abnormal flow conditions in the quenching system |
|FA-202 | Flow Alarm | Monitors flow deviations in the coking process |
|I-201 | Interlock | Ensures safe operation of coking oven systems |
|I-202 | Interlock | Protects quenching tower operations from unsafe conditions |
|MO-201 | Maintenance Override | Allows manual exclusion of faulty pressure sensors |
|MO-202 | Maintenance Override | Enables manual bypass of faulty temperature sensors |
|P-201 | Pump | Circulates quenching water in the cooling system |
|PT-201A | Pressure Transmitter | Measures internal pressure of coking ovens |
|PT-201B | Pressure Transmitter | Redundant pressure measurement for coking ovens |
|PT-201C | Pressure Transmitter | Third pressure sensor for voting logic in coking ovens |
|SI-201 | System Interlock | Prevents unsafe pressure conditions in coking ovens |
|SI-202 | System Interlock | Protects against unsafe temperature conditions in quenching tower |
|TT-201A | Temperature Transmitter | Measures quenching water temperature in the tower |
|TT-201B | Temperature Transmitter | Redundant temperature measurement for quenching tower |
|TT-201C | Temperature Transmitter | Third temperature sensor for voting logic in quenching tower |


### 3.1) Control Strategy Description

The coking facility employs redundant measurement voting logic to ensure reliable control of critical parameters during coke production. Pressure transmitters PT-201A, PT-201B, and PT-201C monitor the internal pressure of the coking ovens (CO-201), while temperature sensors TT-201A, TT-201B, and TT-201C measure the quenching water temperature in the quenching tower (CO-202). A 2oo3 voting scheme is implemented for both pressure and temperature measurements to ensure system reliability and fault tolerance.

For pressure control, the voted output signal PT-201_VOTE is generated when at least two of the three pressure transmitters (PT-201A/B/C) read within ±5% of each other and exceed the setpoint of 21.0 psig. If one transmitter fails (e.g., signal <3.8 mA or >20.5 mA), the system transitions to degraded mode, operating as 1oo2 voting using the remaining two transmitters. Similarly, for temperature control, the voted output TT-201_VOTE is determined by the median value of TT-201A/B/C readings. A deviation alarm DA-201 is triggered if any temperature sensor deviates by more than ±5% from the median value.

Voting logic ensures that bad PV signals are automatically bypassed, and maintenance override provisions allow operators to manually exclude faulty sensors during troubleshooting. The control system integrates Boolean comparison logic to validate agreement between sensors and deadband logic to prevent chattering near setpoints.


### 3.2) Interlocks and Permissives

High-pressure interlock I-201 activates when PT-201_VOTE exceeds the high-pressure threshold of 100.0 psig, initiating an emergency venting sequence in the coking ovens (CO-201). Low-pressure permissive P-201 ensures normal operation only when PT-201_VOTE is above 21.0 psig. Temperature interlock I-202 engages when TT-201_VOTE exceeds 75.0°C, halting quenching operations in CO-202 to prevent thermal damage.

Interlocks are designed to operate in both normal and degraded modes. In degraded mode, the system uses 1oo2 voting logic for pressure and temperature control, ensuring continued operation with reduced redundancy. Permissives require both pressure and temperature conditions to be satisfied simultaneously for equipment startup, ensuring safe and stable operation.


### 3.3) Alarm and Fault Handling

Deviation alarms DA-201 and DA-202 are generated if the pressure or temperature transmitters exceed the allowable deviation limit of ±5% from the median value. Fault alarms FA-201 and FA-202 are triggered when any sensor signal falls outside the valid range (<3.8 mA or >20.5 mA).

In the event of a transmitter failure, the system automatically bypasses the faulty sensor and transitions to degraded mode operation. Maintenance override switches MO-201 and MO-202 allow operators to manually exclude sensors for calibration or replacement. Alarm aggregation logic consolidates deviation and fault alarms into summary indications SI-201 and SI-202, prioritizing critical faults for operator attention.

Edge detection logic monitors voting state changes and ensures smooth transitions between normal and degraded modes. Deadband logic prevents repetitive alarm activation near deviation thresholds, reducing nuisance alarms and maintaining system stability.


## 4 ** Blast Furnace ** 
|Tagname | Type | Description |
|---------|------|-------------|
|BF-301 | Equipment | Blast furnace for combustion and reduction processes |
|FIC-302 | Flow Controller | Controls hot blast air flowrate to maintain ratio setpoint |
|FT-301 | Flow Transmitter | Measures pulverized coal flowrate for ratio control |
|FV-302 | Flow Valve | Modulates hot blast air flow based on controller output |
|PT-301 | Pressure Transmitter | Measures pressure in the blast furnace system |
|TT-301 | Temperature Transmitter | Monitors temperature in the blast furnace system |


### 4.1) Control Strategy Description

The ratio control strategy for the blast furnace (BF-301) ensures precise proportional relationships between the injected pulverized coal flow (wild flow) and the hot blast air flow (controlled flow) to maintain optimal combustion and reduction conditions. The pulverized coal flowrate is measured by FT-301 with a range of 0-5000 kg/hr, while the hot blast air flowrate is controlled by FIC-302, which modulates control valve FV-302. The ratio controller, FFIC-303, calculates the setpoint for FIC-302 based on the measured pulverized coal flow and a fixed ratio setpoint of 1.8:1 (hot blast air to pulverized coal).

The ratio is implemented such that the hot blast air flow setpoint (SP) is dynamically calculated as:
Hot Blast Air SP = Pulverized Coal Flow (FT-301) × 1.8.

FFIC-303 is configured with ratio adjustment limits of 1.5:1 to 2.0:1 to allow for operational flexibility while maintaining safety and efficiency. The ratio controller also includes a manual bias adjustment capability of ±0.1 to fine-tune the ratio during transient conditions. Additionally, a low flow cutoff is implemented, where if FT-301 measures below 100 kg/hr, the ratio control is suspended, and FIC-302 reverts to a predefined minimum setpoint of 200 kg/hr to prevent air starvation.


### 4.2) Interlocks and Permissives

The ratio control loop is interlocked with the blast furnace safety system to ensure safe operation. The following conditions must be met for FFIC-303 to operate in automatic mode:
1. Pulverized coal flow (FT-301) must be within the range of 100-5000 kg/hr. If the flow is outside this range, the ratio control is disabled, and FIC-302 maintains a fixed fallback setpoint of 500 kg/hr.
2. Hot blast air temperature (TT-301) must be above 900°C to ensure proper combustion. If TT-301 falls below this threshold, the ratio control is disabled, and FIC-302 is closed.
3. Furnace pressure (PT-301) must be within the range of 1.5-2.5 bar(g). If PT-301 exceeds 2.5 bar(g), the ratio control is overridden, and FIC-302 is closed to reduce pressure buildup.

Mode switching between manual and automatic operation of FFIC-303 is bumpless, with the current controlled flow setpoint clamped to the calculated value during transitions to prevent process disturbances.


### 4.3) Alarm and Fault Handling

The ratio control system includes alarms to notify operators of abnormal conditions. A high pulverized coal flow alarm (FT-301-H) is triggered if the flow exceeds 5000 kg/hr, while a low flow alarm (FT-301-L) is activated if the flow drops below 100 kg/hr. Similarly, a high hot blast air flow alarm (FIC-302-H) is triggered at 9000 kg/hr, and a low flow alarm (FIC-302-L) is activated at 200 kg/hr.

In the event of a fault in the pulverized coal flow measurement (FT-301), the ratio controller FFIC-303 enters manual mode, and FIC-302 reverts to a fixed setpoint of 1000 kg/hr. If the hot blast air temperature (TT-301) or furnace pressure (PT-301) exceeds their respective alarm thresholds, the system initiates an emergency shutdown sequence, closing FV-302 and isolating the hot blast air supply. All alarm conditions are logged in the control system's historian for diagnostic purposes.


## 5 **  Basic Oxygen Furnace (BOF) ** 
|Tagname | Type | Description |
|---------|------|-------------|
|BOF-401 | Furnace | Basic Oxygen Furnace for steelmaking process. |
|BOF-402 | Lance | Oxygen lance for adjusting flowrate during blowing. |
|DA-401 | Deviation Alarm | Activates on excessive deviation between temperature sensors. |
|FA-401 | Flow Alarm | Monitors and alarms abnormal flow conditions. |
|FT-401 | Flow Transmitter | Measures oxygen flowrate to the lance. |
|I-401 | Interlock | Prevents lance operation unless permissive conditions are met. |
|MA-401 | Manual Adjustment | Allows manual bypass of sensors during maintenance. |
|PT-401A | Pressure Transmitter | Measures system pressure for interlock voting. |
|PT-401B | Pressure Transmitter | Measures system pressure for interlock voting. |
|PT-401C | Pressure Transmitter | Measures system pressure for interlock voting. |
|TT-401 | Temperature Transmitter | Measures furnace temperature during operation. |
|TT-401A | Temperature Transmitter | Redundant sensor for furnace temperature monitoring. |
|TT-401B | Temperature Transmitter | Redundant sensor for furnace temperature monitoring. |
|TT-401C | Temperature Transmitter | Redundant sensor for furnace temperature monitoring. |


### 5.1) Control Strategy Description

The Basic Oxygen Furnace (BOF-401) utilizes redundant temperature transmitters TT-401A, TT-401B, and TT-401C for critical process monitoring during oxygen blowing. A 2oo3 voting configuration is implemented to ensure reliable temperature measurement and control. The system continuously evaluates the process variable (PV) signals from TT-401A, TT-401B, and TT-401C. If two out of three transmitters report a temperature exceeding the setpoint of 1650°C, the voted output signal TT-401-V triggers the oxygen lance (BOF-402) to adjust flowrate via FT-401. The maximum allowable deviation between any two sensors is set at ±5% of the median value. If the deviation exceeds this limit, deviation alarm DA-401 activates. Signal quality checks are performed to detect bad PV conditions, defined as signals below 3.8 mA or above 20.5 mA. In degraded mode operation, if one transmitter fails, the voting logic transitions from 2oo3 to 1oo2, allowing the system to continue operation with reduced redundancy. Manual bypass of any sensor is permitted during maintenance via the HMI, which disables the corresponding input in the voting logic.


### 5.2) Interlocks and Permissives

The oxygen lance (BOF-402) is interlocked with the temperature voting logic to prevent operation unless the voted temperature TT-401-V exceeds 1450°C and all pressure transmitters PT-401A, PT-401B, and PT-401C report values within the range of 90–120 psig using a 2oo3 voting scheme. Flowmeter FT-401 must confirm a minimum oxygen flowrate of 500 Nm³/h as a permissive condition before oxygen blowing can commence. If any transmitter reports a bad PV condition or deviation alarm DA-401 is active, the interlock I-401 inhibits oxygen lance operation. The system also includes a startup permissive requiring all three temperature transmitters TT-401A, TT-401B, and TT-401C to pass signal quality checks before initiating the refining sequence.


### 5.3) Alarm and Fault Handling

Deviation alarm DA-401 is triggered if the temperature readings from TT-401A, TT-401B, or TT-401C differ by more than ±5% from the median value. If a transmitter fails and reports a bad PV condition (signal <3.8 mA or >20.5 mA), fault alarm FA-401 activates, and the failed transmitter is automatically bypassed in the voting logic. In degraded mode, the system transitions to 1oo2 voting, allowing continued operation with reduced redundancy. If two transmitters fail, the system enters a fault state, and the oxygen lance (BOF-402) is shut down. All alarms are aggregated in the HMI for operator acknowledgment. Maintenance override is available to manually bypass any transmitter, but this action requires confirmation of permissive conditions and acknowledgment of a maintenance mode alarm MA-401.


## 6 ** Secondary Metallurgy ** 
|Tagname | Type | Description |
|---------|------|-------------|
|PT-501 | Pressure Transmitter | Measures process pressure in the system. |
|SM-501 | Actuator | Modulates electrode position for heat input control. |
|TT-501 | Temperature Transmitter | Measures steel bath temperature in ladle furnace. |


### 6.1) Control Strategy Description

The secondary metallurgy section employs PID control to regulate critical process parameters during ladle furnace treatment and vacuum degassing. The primary control loop governs the ladle furnace temperature (TT-501.PV) to maintain the steel bath at a precise setpoint (TT-501.SP) of 1620°C ± 5°C. The PID controller, identified as TT-501.PID, operates in reverse-acting mode to modulate the heat input via the electrode position actuator (SM-501.EA). The process variable (PV) is measured by temperature transmitter TT-501, which has a calibrated range of 1200°C to 1800°C and outputs a 4-20mA signal.

The PID controller TT-501.PID is configured with the following tuning parameters: proportional gain (Kp) = 3.2, integral time (Ki) = 1.5 minutes, and derivative time (Kd) = 0.3 minutes. The controller output (MV) is clamped between 0% and 100%, corresponding to the full stroke of the electrode actuator (SM-501.EA). The actuator is configured as fail-down, retracting the electrodes in the event of signal loss to prevent overheating.

To ensure smooth operation, the control logic includes bumpless transfer when switching between manual and automatic modes. When switching to auto mode, the controller output (MV) is initialized to match the current actuator position. Anti-windup logic is implemented to prevent integral term accumulation when the output is saturated. A deadband of ±2°C is applied to the error signal to minimize control hunting.


### 6.2) Interlocks and Permissives

The PID control for TT-501.PID is interlocked with the ladle furnace safety and operational conditions. The furnace cannot be heated unless the following permissives are satisfied: SM-501.LID_POS == "Closed" (ladle furnace lid closed), PT-501.PV > 0.8 bar (minimum inert gas pressure), and SM-501.EA_POS > 10% (electrodes sufficiently lowered). If any of these conditions are not met, the PID controller output (MV) is forced to 0%, and heating is disabled.

Additionally, a high-temperature interlock (TT-501.PV > 1650°C) overrides the PID control and fully retracts the electrodes (SM-501.EA = 0%) to prevent steel overheating. The control loop also includes a 10-second delay on the heating enable signal to avoid false activation during transient conditions, such as ladle placement or initial gas purging.


### 6.3) Alarm and Fault Handling

The temperature control loop includes high-priority alarms for critical faults. If TT-501.PV exceeds 1650°C, a "High-High Temperature" alarm (TT-501.HH) is triggered, and the system initiates an emergency shutdown sequence, retracting the electrodes (SM-501.EA = 0%) and isolating power to the furnace. A "Low Temperature" alarm (TT-501.L) is activated if TT-501.PV falls below 1500°C, indicating potential process inefficiency or sensor malfunction.

Sensor faults, such as a loss of signal from TT-501, are detected by monitoring the 4-20mA signal range. If TT-501.PV < 3.8mA or TT-501.PV > 20.2mA, a "Sensor Fault" alarm (TT-501.FLT) is raised, and the PID controller output (MV) is frozen at its last known value to prevent abrupt process changes. In the event of actuator failure (SM-501.EA_POS feedback deviates by >5% from MV for more than 5 seconds), a "Control Actuator Fault" alarm (SM-501.EA.FLT) is generated, and the system transitions to manual mode for operator intervention.

All alarms are logged in the distributed control system (DCS) with timestamps and operator acknowledgment requirements. The control system also provides a trend display of TT-501.PV, TT-501.SP, and TT-501.MV for real-time monitoring and post-event analysis.


## 7 ** Continuous Casting ** 
|Tagname | Type | Description |
|---------|------|-------------|
|CC-601   | Equipment         | Continuous casting machine for steel solidification process |
|CC-603   | Equipment         | Secondary continuous casting machine for steel processing    |
|FT-601   | Flow Transmitter  | Measures flow rate of molten steel into the mold             |
|LIC-101  | Level Controller  | Regulates mold level using PID control logic                 |
|LIT-101  | Level Transmitter | Measures mold level in millimeters                           |
|MV-101   | Control Valve     | Modulates flow of molten steel into the mold                 |
|TT-601   | Temperature Transmitter | Monitors temperature of molten steel during casting process |


### 7.1) Control Strategy Description

The continuous casting process in CC-601 requires precise mold level control to ensure uniform solidification of liquid steel. The primary control loop regulates the mold level (PV) using the signal from LIT-101, which measures the mold level in millimeters. The target setpoint (SP) for the mold level is 150 mm. The final control element is the mold inlet valve (MV-101), which modulates the flow of molten steel into the mold.

The PID controller LIC-101 is configured for reverse-acting control, as an increase in the mold level (PV) requires a reduction in the valve opening (MV). The tuning parameters are set as follows: Kp = 3.0, Ki = 1.2 min, and Kd = 0.1 min. The controller output is clamped between 0% and 100% to prevent overdriving the valve. Anti-windup logic is implemented to limit integral action during output saturation.

The LIT-101 transmitter has a calibrated range of 0-300 mm, with a 4-20 mA signal representing this span. The signal is scaled to engineering units before entering LIC-101. The mold inlet valve MV-101 is a fail-closed valve, ensuring flow stops in the event of a control system failure. The response time of the control loop is tuned to achieve a settling time of less than 10 seconds under normal operating conditions.

Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes. In manual mode, the operator directly adjusts the valve position, and the controller bias is updated continuously to match the manual output.


### 7.2) Interlocks and Permissives

The mold level control loop LIC-101 is interlocked with the cooling water system (CC-603) to ensure safe operation. The control loop is inhibited if the cooling water flow, as measured by FT-601, falls below 50% of its nominal flow rate (SP = 75 m³/h). Additionally, the mold level control is disabled if the mold temperature, measured by TT-601, exceeds 950°C, as this indicates a potential overheating condition.

A permissive is in place to prevent the mold inlet valve MV-101 from opening unless the mold level, as measured by LIT-101, is below 250 mm. This ensures that the mold does not overflow during startup or transient conditions. The permissive logic is hardwired to the valve actuator to provide an additional layer of safety.


### 7.3) Alarm and Fault Handling

An alarm is triggered if the mold level, as measured by LIT-101, deviates from the setpoint by more than ±20 mm for a duration exceeding 5 seconds. The alarm is classified as high priority and is displayed on the operator interface as "Mold Level Deviation Alarm." If the mold level exceeds 280 mm, a high-high alarm is activated, and the mold inlet valve MV-101 is forced closed to prevent overflow.

If the signal from LIT-101 is lost or falls outside the valid range (4-20 mA), the LIC-101 controller enters a fault state, and the mold inlet valve MV-101 is driven to its fail-closed position. An alarm is generated as "Mold Level Sensor Fault," and the operator is required to investigate and rectify the issue before resuming automatic control.

In the event of a cooling water flow fault, indicated by FT-601 falling below 50% of its nominal flow, the control system shuts down the mold inlet valve MV-101 and activates a "Cooling Water Flow Low" alarm. Similarly, if TT-601 detects a mold temperature exceeding 950°C, the system forces the valve closed and generates a "Mold Overtemperature" alarm. These interlocks ensure safe operation and prevent damage to the equipment.


## 8 ** Rolling Mills ** 
|Tagname | Type | Description |
|---------|------|-------------|
|ALM-701 | Level Alarm | High level alarm for reheating furnace safety. |
|ALM-702 | Level Alarm | Low level alarm for reheating furnace safety. |
|ALM-703 | Level Alarm | High level alarm for fuel storage tank. |
|ALM-704 | Level Alarm | Low level alarm for fuel storage tank. |
|BLS-701 | Burner Safety Interlock | Ensures safe operation of reheating furnace burners. |
|FIC-702 | Flow Controller | Regulates air flow to maintain combustion efficiency. |
|FLT-701 | Level Transmitter | Measures fuel tank level for inventory control. |
|FT-701 | Flow Transmitter | Measures fuel flow rate for combustion control. |
|FT-702 | Flow Transmitter | Measures air flow rate for combustion control. |
|FV-702 | Flow Control Valve | Modulates air flow to achieve combustion setpoint. |
|TT-701 | Temperature Transmitter | Monitors reheating furnace temperature. |


### 8.1) Control Strategy Description

In Section 8, the ratio control strategy for the rolling mills ensures proportional relationships between the reheating furnace fuel flow and combustion air flow to maintain optimal combustion efficiency. The wild flow measurement is provided by FT-701 (Fuel Flow Transmitter) with a calibrated range of 0-5000 kg/hr. The controlled flow measurement is provided by FT-702 (Air Flow Transmitter) with a calibrated range of 0-15000 Nm³/hr. The ratio controller FFIC-701 calculates the air flow setpoint based on the fuel flow measurement and a fixed operator-set ratio of 10:1 (air-to-fuel). The ratio control equation is implemented as FT-702 SP = FT-701 PV × 10, where FT-701 PV represents the process variable of the fuel flow transmitter. The air flow control loop modulates FV-702 (Air Flow Control Valve) via FIC-702 (Air Flow Controller) to achieve the calculated setpoint. Ratio limits are clamped between 8:1 and 12:1 to ensure safe and efficient combustion. Manual bias adjustment is available through FFIC-701 to compensate for variations in fuel quality or reheating furnace temperature deviations, with a bias adjustment range of ±10%. Lead compensation is applied to the air flow controller to account for delays in air delivery. Low flow cutoff logic disables ratio control if FT-701 PV falls below 200 kg/hr to prevent unstable operation during low fuel flow conditions.


### 8.2) Interlocks and Permissives

The ratio control system is interlocked with TT-701 (Reheating Furnace Temperature Transmitter) to ensure safe operation. If TT-701 PV exceeds 1200°C, FFIC-701 automatically reduces the air-to-fuel ratio to 8:1 to prevent overheating. Additionally, FT-701 and FT-702 must both be operational and transmitting valid signals for FFIC-701 to enable ratio control. A permissive condition requires the reheating furnace burner status to be ON, as indicated by BLS-701 (Burner Logic Status), before FFIC-701 can calculate and output the air flow setpoint. Boolean glue logic ensures that FV-702 remains closed if FT-701 PV is below 200 kg/hr or if TT-701 PV is below 800°C, preventing unsafe combustion conditions. Mode selection for FFIC-701 allows operators to switch between automatic ratio control, manual air flow control, and individual fuel flow control.


### 8.3) Alarm and Fault Handling

Alarm conditions are configured to alert operators of deviations in ratio control and equipment faults. If the calculated air-to-fuel ratio exceeds 12:1 or falls below 8:1, FFIC-701 triggers a high/low ratio alarm (ALM-701) and clamps the ratio within safe bounds. FT-701 and FT-702 transmitters are equipped with diagnostic alarms (ALM-702 and ALM-703) to indicate signal loss or sensor malfunction. If either transmitter fails, FFIC-701 transitions to manual control mode and generates a fault alarm (FLT-701) to notify operators. TT-701 high-temperature alarm (ALM-704) activates if the reheating furnace temperature exceeds 1200°C, prompting FFIC-701 to reduce the air-to-fuel ratio and FV-702 to close partially. Deadband logic within FFIC-701 prevents ratio hunting by ignoring minor fluctuations in FT-701 PV below 5 kg/hr, ensuring stable operation. Alarm acknowledgment requires operator intervention to reset the system and resume automatic ratio control.


## 9 ** By-Product Recovery Systems ** 
|Tagname | Type | Description |
|---------|------|-------------|
|AL-801 | Analyzer | Monitors composition of recovered blast furnace gas for process optimization |
|AL-802 | Analyzer | Measures combustion air quality to ensure proper mixing with recovered gas |
|AL-803 | Analyzer | Tracks impurities in off-gases for by-product recovery efficiency |
|AL-804 | Analyzer | Analyzes steam quality in the generation system for operational control |
|FIC-802 | Flow Controller | Regulates air flow to maintain the required gas-to-air ratio for combustion |
|FT-801 | Flow Transmitter | Measures flow rate of recovered blast furnace gas for ratio control |
|FT-802 | Flow Transmitter | Monitors air flow rate for combustion process control |
|FV-802 | Flow Valve | Modulates air flow based on setpoint from FIC-802 for combustion efficiency |
|PT-801 | Pressure Transmitter | Measures pressure of recovered blast furnace gas for permissive interlocks |


### 9.1) Control Strategy Description

The by-product recovery system utilizes ratio control to maintain proportional relationships between recovered off-gases and combustion air for efficient fuel utilization in steam generation. Flow transmitter FT-801 measures the wild flow of recovered blast furnace gas (range: 0-5000 Nm³/hr). Ratio controller FFIC-801 calculates the setpoint for controlled air flow based on a fixed gas-to-air ratio of 1:2.5. The controlled air flow setpoint is determined as FT-801 × 2.5 and is transmitted to flow controller FIC-802, which modulates control valve FV-802 to maintain the required air flow. The ratio setpoint is adjustable between 2.0:1 and 3.0:1 via manual operator input on FFIC-801. Input signals from FT-801 and PT-801 are scaled linearly from 4-20 mA to match the controller input range of 0-100%. A low flow cutoff is implemented to disable ratio control when FT-801 measures less than 100 Nm³/hr, switching FIC-802 to manual mode.


### 9.2) Interlocks and Permissives

The ratio control loop FFIC-801 is interlocked with permissive conditions to ensure safe operation. FT-801 must register a valid signal above 100 Nm³/hr for FFIC-801 to enable ratio control; otherwise, the system defaults to manual control of FIC-802. PT-801 monitors the pressure of recovered gas and must remain within the range of 0.5-2.0 bar for operation; pressures outside this range trigger a permissive lockout that closes FV-802. Boolean interlocks ensure that combustion air flow measured by FT-802 does not exceed 6000 Nm³/hr, clamping the FFIC-801 output to prevent unsafe air-to-gas ratios. A hysteresis of 1% is applied to FT-801 and PT-801 signals to avoid rapid toggling between permissive states near the cutoff thresholds.


### 9.3) Alarm and Fault Handling

The system generates alarms for deviations from the configured ratio or failure of critical transmitters. A high ratio deviation alarm (AL-801) is triggered if the calculated air-to-gas ratio exceeds 3.0:1 for more than 5 seconds, indicating potential over-aeration. A low ratio deviation alarm (AL-802) is triggered if the ratio falls below 2.0:1, signaling insufficient air supply for combustion. FT-801 and PT-801 transmitter faults are monitored by diagnostic alarms (AL-803 and AL-804, respectively), which initiate automatic fallback to manual control mode for FIC-802. In the event of a fault, FV-802 is positioned to a default fail-safe setting of 50% open to maintain minimum air flow. All alarms are logged in the plant's distributed control system (DCS) for operator review and corrective action.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 9

- Total Tagnames: 74

- Word Count: 5288
