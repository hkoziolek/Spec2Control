# Wastewater Treatment Facility Process Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Influent & Headworks**
3. **Flow Equalization**
4. **Primary Treatment**
5. **Chemical Conditioning**
6. **Secondary (Biological) Treatment**
7. **Secondary Clarification**
8. **Tertiary/Advanced Treatment**
9. **Disinfection**
10. **Influent Lift Station**
11. **Utilities, Chemicals & Controls**
12. **Sludge/Biosolids Management**

---


## 1 **Process Overview and Scope**

The wastewater treatment facility is designed to process municipal flows through a series of integrated treatment phases, ensuring safe and efficient removal of contaminants while meeting regulatory discharge standards. The process begins with influent handling and headworks, where incoming wastewater is screened and grit is removed before flow equalization smooths variations in hydraulic loading. Primary treatment facilitates the removal of settleable solids and scum, followed by chemical conditioning to adjust pH and alkalinity as needed. Secondary treatment employs a biological activated-sludge process to degrade organic matter, supported by precise dissolved oxygen control in anoxic and aerobic zones. Secondary clarification and tertiary treatment further refine the effluent, with advanced filtration polishing turbidity and solids, while disinfection—via UV or chlorination—achieves pathogen reduction prior to discharge.

Throughout the process, centralized control strategies are implemented to optimize performance and maintain operational stability. Plant-wide PLC/DCS systems with SCADA integration coordinate automation, interlocks, and manual overrides, ensuring seamless transitions between treatment phases. Feedforward strategies such as flow-paced chemical dosing and influent-bias aeration control enhance efficiency, while feedback loops continually adjust critical parameters like dissolved oxygen and effluent quality. Sludge and biosolids management is conducted in parallel, leveraging thickening, digestion, and dewatering systems with safeguards for storage capacity and odor control. The facility’s hydraulic continuity is further supported by redundant pump systems and interlocks at critical points.

Safety and reliability are integral to the control philosophy, with interlocks preventing equipment starts under unsafe conditions and permissives ensuring proper sequencing. The modular design of the process phases allows critical systems to function independently while maintaining interdependencies for effective overall operation. By integrating advanced process control strategies, the facility ensures compliance with environmental regulations, operational consistency, and protection of downstream ecosystems.


## 2 **Influent & Headworks**
|Tagname | Type | Description |
|---------|------|-------------|
|BS-101   | Interlock         | Prevents pump operation under unsafe conditions       |
|FT-101   | Flow Transmitter  | Measures influent flow rate                           |
|LS-101   | Level Transmitter | Monitors wet well level                               |
|P-101A   | Pump              | Primary influent pump for wet well level control      |
|P-101B   | Pump              | Standby influent pump activated upon P-101A failure   |
|PIC-101  | Level Controller  | Regulates wet well level via pump speed control       |
|VG-101   | Vacuum Gauge      | Measures vacuum pressure in associated equipment      |
|XV-101   | On-Off Valve      | Controls flow isolation in the influent line          |


### 2.1) Control Strategy Description

The influent wet well level is maintained using a PID control loop centered on LS-101 (Wet Well Level Transmitter) as the process variable (PV). LS-101 measures the wet well level in the range of 0 to 10 meters, transmitting a 4-20 mA signal to PIC-101 (Wet Well Level Controller). The target setpoint (SP) for the wet well level is 5.5 meters, ensuring optimal pump operation and preventing overflow or pump cavitation.

PIC-101 is configured as a reverse-acting controller, where an increase in PV results in a decrease in the manipulated variable (MV) to maintain the SP. The PID tuning parameters are set as follows: proportional gain (Kp) = 2.0, integral time (Ki) = 1.5 minutes, and derivative time (Kd) = 0.3 minutes. The controller output (MV) ranges from 0% to 100%, corresponding to the speed control of P-101A/B (Influent Pumps). Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes.

The final control element is the pump speed control for P-101A/B, which adjusts influent flow to maintain the wet well level. P-101A is the primary pump, and P-101B serves as the standby pump, automatically starting upon failure of P-101A. The pump speed is modulated based on the MV from PIC-101, with a minimum speed limit of 30% to prevent pump stalling and a maximum limit of 90% to avoid excessive wear.


### 2.2) Interlocks and Permissives

The operation of P-101A/B is governed by interlocks tied to LS-101 and FT-101 (Influent Flow Transmitter). P-101A/B will not start unless LS-101 indicates a level above 2.0 meters to prevent dry running. Similarly, if LS-101 exceeds 9.0 meters, both pumps will shut down to prevent overflow. FT-101 measures influent flow in the range of 0 to 500 m³/h, transmitting a 4-20 mA signal to the PLC. The PLC ensures that the combined flow rate from P-101A/B does not exceed 450 m³/h, clamping the MV from PIC-101 accordingly.

Bar screens BS-101 and vortex grit unit VG-101 are interlocked with the wet well level logic. BS-101 will stop operation if LS-101 falls below 2.0 meters to prevent damage due to insufficient flow. VG-101 will not start unless FT-101 confirms a minimum influent flow rate of 50 m³/h to ensure proper grit removal functionality.


### 2.3) Alarm and Fault Handling

LS-101 provides high and low-level alarms at 8.5 meters and 1.5 meters, respectively. A high-level alarm triggers an immediate shutdown of P-101A/B and closes XV-101 (Shut-off Valve) to isolate the wet well. A low-level alarm disables BS-101 and VG-101 to prevent damage to equipment operating without sufficient flow.

PIC-101 includes anti-windup logic to prevent integral accumulation during pump shutdown conditions. If LS-101 detects a level below 2.0 meters, the PID controller output is clamped at 0%, and the integral term is reset to avoid overshooting upon restart. Similarly, a deadband of ±0.1 meters around the SP is implemented to prevent control hunting when the level is stable.

Fault conditions for LS-101, FT-101, or P-101A/B are monitored by the PLC. If LS-101 or FT-101 fails, the system switches to manual mode, allowing operators to control pump speed directly. If P-101A fails, P-101B automatically starts, and an alarm is sent to the SCADA system for operator intervention.


## 3 **Flow Equalization**
|Tagname | Type | Description |
|---------|------|-------------|
|FIT-102 | Flow Transmitter | Measures flow rate in the pipeline for monitoring and control purposes |
|LIC-101 | Level Controller | Regulates tank level using PID control to maintain operator-defined setpoint |
|LS-201 | Level Switch | Detects tank level for interlock and permissive functions |
|LV-103 | Level Valve | Controls tank inlet flow to maintain desired level |
|LV-104 | Level Valve | Regulates outlet flow from the tank for downstream processes |
|MX-201 | Mixer | Ensures homogeneity in the tank by continuous mixing at fixed speed |
|P-201A | Pump | Lead pump for transferring fluid from the equalization tank |
|P-201B | Pump | Backup pump for transferring fluid from the equalization tank |


### 3.1) Control Strategy Description

The Flow Equalization system utilizes LIC-101 to maintain the level in the equalization tank by modulating the operation of P-201A/B and MX-201. LIC-101 employs a single-loop PID control algorithm to regulate the tank level (PV) to the operator-defined setpoint (SP). The setpoint for LIC-101 is adjustable between 12% and 87% of tank level, corresponding to a range of 1.2 meters to 8.7 meters, with the transmitter LS-201 providing a 4-20mA signal scaled to this range. LIC-101 is configured for reverse-acting control, ensuring pump speed decreases as the tank level approaches the setpoint. The PID tuning parameters are set as follows: Kp = 3.0, Ki = 0.5 min, and Kd = 0.1 min. The controller output (MV) modulates the speed of P-201A/B between 20% and 100% of their rated capacity, ensuring consistent downstream flow. Anti-windup logic is implemented to limit integral accumulation when the pumps are at their minimum or maximum speed. Bumpless transfer is enabled for smooth transitions between manual and automatic operation. MX-201 is operated continuously to maintain homogeneity in the tank, with the mixer speed fixed at 75% capacity.


### 3.2) Interlocks and Permissives

P-201A/B operation is interlocked with LS-201 to prevent dry running. If LS-201 detects a tank level below 10% (1.0 meters), LIC-101 disables pump operation and generates a permissive fault signal. MX-201 is interlocked with LS-201 to ensure mixing is disabled if the tank level falls below 5% (0.5 meters). Additionally, pump operation is interlocked with downstream flow permissives from FIT-102 to ensure that flow does not exceed 95% of the downstream process capacity. The pumps are configured with automatic switchover logic, ensuring that P-201A operates as the primary pump, with P-201B starting automatically if P-201A fails or if demand exceeds the capacity of a single pump. LV-103 and LV-104 are interlocked with LIC-101 to ensure that any level deviations exceeding 90% (9.0 meters) trigger an emergency drain sequence.


### 3.3) Alarm and Fault Handling

LIC-101 generates high-level and low-level alarms based on LS-201 measurements. A high-level alarm is triggered at 90% (9.0 meters), while a low-level alarm is triggered at 5% (0.5 meters). If LS-201 fails or provides an invalid signal, LIC-101 enters a fault state, disabling P-201A/B and MX-201 operation, and activating LV-103 to drain the tank to a safe level of 50% (5.0 meters). Fault conditions are latched until manually reset by the operator. FIT-102 is monitored for flow deviation alarms, with high-flow alarms triggered at 95% of capacity and low-flow alarms triggered at 5% of capacity. Alarm conditions are displayed on the SCADA system, with audible and visual indicators provided to alert operators.


## 4 **Primary Treatment**
|Tagname | Type | Description |
|---------|------|-------------|
|CL-301A | Clarifier | Primary clarifier for sludge separation (Unit A) |
|CL-301B | Clarifier | Primary clarifier for sludge separation (Unit B) |
|FFIC-303 | Flow Controller | Calculates sludge withdrawal flow setpoint based on influent flow ratio |
|FT-301 | Flow Transmitter | Measures influent flow rate to primary clarifiers |
|FT-302 | Flow Transmitter | Measures sludge withdrawal flow rate |
|FV-102 | Flow Valve | Modulates sludge withdrawal flow to maintain setpoint |
|LS-301 | Level Transmitter | Monitors weir level in primary clarifiers |
|PS-301 | Pressure Transmitter | Measures pressure in sludge withdrawal system |
|SS-301 | Speed Switch | Monitors rotational speed of associated equipment |


### 4.1) Control Strategy Description

The ratio control logic for the Primary Treatment section ensures precise proportional relationships between the sludge withdrawal flow and the influent flow entering the primary clarifiers, CL-301A and CL-301B. Flow measurement FT-301 monitors the influent flow rate, designated as the wild flow variable, with a range of 0-500 GPM. The controlled variable, sludge withdrawal flow, is measured by FT-302, with a range of 0-200 GPM. The ratio controller FFIC-303 calculates the sludge withdrawal flow setpoint (FT-302 SP) as a function of the influent flow measurement (FT-301) multiplied by the operator-defined ratio setpoint, which is adjustable between 0.2:1 and 0.4:1. For example, at an influent flow of 400 GPM, FFIC-303 sets FT-302 SP to 120 GPM based on a ratio of 0.3:1. The flow control valve FV-102 modulates to maintain FT-302 at the calculated setpoint. Ratio adjustments can be manually biased via operator input or automatically trimmed based on downstream sludge quality measurements. Low flow cutoff logic disables ratio control if FT-301 drops below 50 GPM to prevent operational instability.


### 4.2) Interlocks and Permissives

The ratio control loop FFIC-303 is interlocked with LS-301, which monitors the weir level in the primary clarifiers. If LS-301 detects a weir level outside the operational range of 2.0-5.0 feet, the ratio control loop is disabled, and FV-102 is commanded to close. Additionally, permissives ensure that sludge withdrawal pumps PS-301 are operational and that scum skimmers SS-301 are not actively engaged before enabling ratio control. Boolean logic verifies that FT-301 is within its calibrated range (0-500 GPM) and that FT-302 does not exceed its maximum capacity of 200 GPM before allowing FFIC-303 to calculate and apply the sludge withdrawal setpoint. A manual override mode is available to bypass ratio control during maintenance or abnormal operating conditions.


### 4.3) Alarm and Fault Handling

An alarm is triggered if FT-301 deviates from its expected range or if the calculated sludge withdrawal flow setpoint exceeds the allowable ratio limits (0.2:1 to 0.4:1). FFIC-303 generates a fault signal if the ratio calculation fails due to invalid inputs or if FV-102 cannot achieve the commanded setpoint within 5% accuracy. LS-301 generates a high-level alarm if the weir level exceeds 5.0 feet, initiating a shutdown of the sludge withdrawal pumps PS-301 and disabling ratio control. Similarly, a low-level alarm at LS-301 below 2.0 feet disables ratio control and closes FV-102 to prevent air entrainment in the sludge withdrawal system. All alarms and faults are logged in the SCADA system and require operator acknowledgment before resuming normal operation.


## 5 **Chemical Conditioning**
|Tagname | Type | Description |
|---------|------|-------------|
|AC-401 | Alkalinity Transmitter | Measures alkalinity in mg/L for chemical conditioning control |
|CD-401 | Pump | Doses chemicals for pH adjustment in the process |
|FT-101 | Flow Transmitter | Measures flow rate in the system |
|LT-401 | Level Transmitter | Monitors liquid level in the tank or vessel |
|PH-401 | pH Analyzer | Measures process pH for chemical conditioning control |
|PIC-401 | pH Controller | Regulates chemical dosing to maintain pH setpoint |
|PIC-402 | Alkalinity Controller | Adjusts chemical dosing to maintain alkalinity setpoint |
|TS-401 | Temperature Sensor | Monitors temperature in the process system |


### 5.1) Control Strategy Description

The Chemical Conditioning section implements PID control to regulate pH and alkalinity upstream of biological treatment. The process variable (PV) for pH control is measured by PH-401, a pH analyzer with a transmitter range of 0-14 pH units, outputting a 4-20mA signal normalized to a 0-100% scale. The setpoint (SP) for pH adjustment is operator-configurable within the range of 6.5 to 7.5 pH units, with the default setpoint set to 7.0 pH units. The PID controller, designated as PIC-401, is configured for reverse-acting control to increase chemical dosing when the measured pH falls below the setpoint. Tuning parameters are set as follows: proportional gain (Kp) = 2.0, integral time (Ki) = 1.0 min, and derivative time (Kd) = 0.2 min. The manipulated variable (MV) drives the chemical dosing pumps, CD-401, with an output range of 0-100% corresponding to pump flow rates between 0 and 50 L/min. The pumps are fail-closed to prevent chemical overdosing during fault conditions.

For alkalinity control, AC-401 measures alkalinity in mg/L with a transmitter range of 0-500 mg/L, outputting a 4-20mA signal. The SP for alkalinity adjustment is set to 150 mg/L, constrained within the operating range of 100-200 mg/L. The PID controller, designated as PIC-402, is configured for direct-acting control to increase dosing when alkalinity falls below the setpoint. Tuning parameters are set as follows: Kp = 1.5, Ki = 0.8 min, and Kd = 0.1 min. The MV adjusts the chemical dosing pumps, CD-401, with output limits constrained to prevent pump flow exceeding 75% capacity during normal operation. Anti-windup logic is enabled to prevent integral accumulation during saturation conditions. Bumpless transfer logic ensures smooth transitions between manual and automatic modes.


### 5.2) Interlocks and Permissives

Chemical dosing is permitted only when influent flow is verified by FT-101, with a minimum flow threshold of 50 m³/h. The permissive condition is satisfied when FT-101 outputs a signal above 4.5mA. Additionally, chemical storage tanks (TS-401) must report a minimum level of 20% via LT-401 to enable dosing operations. If LT-401 detects a level below 20%, the permissive signal to CD-401 is removed, and dosing is inhibited. Both PH-401 and AC-401 transmitters must be operational, with valid signals within their respective ranges, for the PID controllers PIC-401 and PIC-402 to execute control. A deadband of ±0.1 pH units is applied to pH control to prevent hunting, while a deadband of ±5 mg/L is applied to alkalinity control.

Mode selection logic allows operators to switch between automatic and manual control. In manual mode, the operator directly sets the MV for CD-401, bypassing PID control. Automatic mode is enabled only when all permissives are satisfied, and the controllers are in a healthy state. Timer delays of 10 seconds are implemented to prevent rapid cycling of permissive signals during transient conditions.


### 5.3) Alarm and Fault Handling

Alarms are generated if PH-401 or AC-401 transmitters report signals outside their calibrated ranges (e.g., <4mA or >20mA). A high-priority alarm is triggered if pH exceeds 8.0 or falls below 6.0, or if alkalinity exceeds 300 mg/L or falls below 50 mg/L. In such cases, CD-401 dosing pumps are immediately stopped, and operators are notified via the SCADA system. A fault condition in TS-401, such as a level reading below 10%, triggers a chemical storage alarm and inhibits dosing operations.

PID controllers PIC-401 and PIC-402 enter fault mode if their respective transmitters fail or if the MV reaches saturation for more than 30 seconds. In fault mode, the controllers freeze their outputs and switch to manual mode, with bumpless transfer logic ensuring no abrupt changes in pump operation. Operators are required to acknowledge alarms before resuming automatic control.


## 6 **Secondary (Biological) Treatment**
|Tagname | Type | Description |
|---------|------|-------------|
|B-501A | Blower | Provides air pressure for biological treatment system |
|B-501B | Blower | Backup blower for air pressure delivery in treatment system |
|FFIC-102 | Ratio Controller | Calculates airflow setpoint based on influent flow ratio |
|FIC-101 | Flow Controller | Monitors influent flow rate to biological treatment system |
|FIC-103 | Flow Controller | Modulates airflow delivery to maintain setpoint ratio |
|FV-102 | Flow Valve | Regulates airflow to biological treatment zones |
|MX-501 | Mixer | Ensures uniform mixing in treatment zones |
|PT-501 | Pressure Transmitter | Monitors air pressure from blowers for system interlocks |
|XV-105 | On-Off Valve | Ensures airflow continuity by verifying open position |


### 6.1) Control Strategy Description

In the Secondary (Biological) Treatment segment, ratio control is implemented to maintain proportional airflow delivery to the anoxic and aerobic zones based on influent flow rate. The wild flow measurement is provided by FIC-101, which monitors influent flow within a calibrated range of 0-5000 m³/hr. The ratio controller FFIC-102 calculates the required airflow setpoint for FIC-103, maintaining a fixed ratio of 2.0:1 (airflow-to-influent flow). The calculated setpoint for FIC-103 is determined using the formula: Airflow SP = Influent Flow × 2.0. FIC-103 modulates FV-102 to achieve the desired airflow, ensuring sufficient oxygen delivery for biological treatment. The ratio controller FFIC-102 incorporates manual bias adjustment within ±0.5 of the ratio setpoint, allowing operational flexibility during transient conditions. Ratio limits are clamped between 1.5:1 and 2.5:1 to prevent excessive or insufficient aeration.


### 6.2) Interlocks and Permissives

The ratio control loop is interlocked with air header availability and blower operational status. FFIC-102 will not issue a setpoint to FIC-103 unless B-501A or B-501B is confirmed running and delivering air pressure above 3.0 bar (monitored by PT-501). Additionally, FV-102 will not open unless XV-105 is verified in the open position, ensuring airflow continuity. Low flow cutoff logic disables FFIC-102 when influent flow measured by FIC-101 drops below 100 m³/hr, preventing unnecessary blower operation during low-load conditions. Mixing equipment MX-501 must be operational before FFIC-102 is activated to ensure proper zone circulation.


### 6.3) Alarm and Fault Handling

A deviation alarm is triggered if the actual airflow measured by FIC-103 deviates from the calculated setpoint by more than 10% for a duration exceeding 30 seconds. FFIC-102 generates a fault alarm if the ratio exceeds the clamped limits of 1.5:1 or 2.5:1 due to erroneous inputs or manual bias adjustments. In the event of a blower failure (B-501A or B-501B), FFIC-102 transitions to manual mode, allowing operators to directly control FV-102 to maintain minimum airflow. If influent flow measured by FIC-101 falls below 100 m³/hr for more than 5 minutes, FFIC-102 will disable the ratio control loop and shut FV-102, generating a low-flow alarm.


## 7 **Secondary Clarification**
|Tagname | Type | Description |
|---------|------|-------------|
|CL-601A | Clarifier | Primary duty clarifier for secondary clarification system in AUTO mode. |
|CL-601B | Clarifier | Standby clarifier for secondary clarification system, activated upon failure of CL-601A. |
|HM-601A | Hour Meter | Tracks runtime hours for CL-601A clarifier. |
|HM-601B | Hour Meter | Tracks runtime hours for CL-601B clarifier. |
|HM-602A | Hour Meter | Tracks runtime hours for PS-601A pump. |
|HM-602B | Hour Meter | Tracks runtime hours for PS-601B pump. |
|LS-601 | Level Switch | Monitors blanket level in clarifiers to ensure process stability. |
|PS-601A | Pump | Primary duty pump for return sludge operation in AUTO mode. |
|PS-601B | Pump | Standby pump for return sludge operation, activated upon failure of PS-601A. |
|PT-601A | Pressure Transmitter | Measures discharge pressure of PS-601A pump. |
|PT-601B | Pressure Transmitter | Measures discharge pressure of PS-601B pump. |
|VS-601A | Valve | Controls flow associated with PS-601A pump operation. |
|VS-601B | Valve | Controls flow associated with PS-601B pump operation. |


### 7.1) Control Strategy Description

The secondary clarification system employs redundant duty/standby control for the operation of the secondary clarifiers (CL-601A and CL-601B) and return sludge pumps (PS-601A and PS-601B). Under normal conditions, CL-601A and PS-601A are designated as duty (lead) equipment, while CL-601B and PS-601B are designated as standby (lag) equipment. The system operates in three distinct modes: AUTO, MANUAL, and TEST.

In AUTO mode, CL-601A is the primary clarifier, and PS-601A operates to maintain blanket level setpoint as measured by LS-601. If CL-601A fails (e.g., LS-601 detects blanket level > 2.5 meters for 15 seconds or PS-601A discharge pressure PT-601A < 25 psig for 10 seconds), CL-601B and PS-601B automatically start after a switchover delay of 10 seconds. The failed equipment is stopped immediately upon switchover, and the standby equipment assumes lead operation. A minimum runtime of 30 minutes is enforced for both clarifiers and pumps to prevent hunting.

In MANUAL mode, operators can select either CL-601A or CL-601B as the lead clarifier and PS-601A or PS-601B as the lead pump via HMI. Standby equipment remains idle unless manually started. In TEST mode, both clarifiers and pumps operate simultaneously for performance verification, with LS-601 providing blanket-level supervision to ensure process stability.

Runtime management is implemented using hour meters HM-601A and HM-601B for the clarifiers and HM-602A and HM-602B for the pumps. Automatic rotation between duty and standby equipment occurs every 72 hours to equalize runtime and wear, ensuring long-term reliability.


### 7.2) Interlocks and Permissives

The operation of CL-601A and CL-601B is interlocked with LS-601 to ensure blanket level remains within acceptable limits. CL-601A cannot start unless LS-601 detects a blanket level < 2.0 meters, and CL-601B cannot start unless LS-601 detects a blanket level < 2.0 meters. Additionally, PS-601A and PS-601B are interlocked with PT-601A and PT-601B, respectively, requiring discharge pressure > 25 psig for continued operation.

During switchover, permissives bypass interlocks for 10 seconds to allow standby equipment to ramp up without immediate shutdown due to transient conditions. A 5-second on-delay timer ensures proper sequencing of equipment startup, while a 57-second off-delay timer prevents premature shutdown during temporary process upsets. Both clarifiers and pumps are locked out if LS-601 detects blanket level > 3.0 meters, triggering a process halt to prevent overflow.

Manual overrides are permitted only in MANUAL mode, with interlock bypasses requiring operator confirmation via HMI. TEST mode bypasses all interlocks and permissives, allowing unrestricted operation for system testing purposes.


### 7.3) Alarm and Fault Handling

Fault conditions for CL-601A and CL-601B are monitored using LS-601 and vibration sensors VS-601A and VS-601B. If LS-601 detects blanket level > 2.5 meters for 15 seconds or VS-601A/VS-601B detects vibration exceeding 5 mm/s for 10 seconds, an alarm is generated, and the affected equipment is stopped. Similarly, PS-601A and PS-601B are monitored using PT-601A and PT-601B; if discharge pressure falls below 25 psig for 10 seconds, an alarm is generated, and the affected pump is stopped.

In AUTO mode, switchover to standby equipment occurs automatically upon fault detection. In MANUAL mode, operators must manually acknowledge alarms and initiate switchover. All alarms are displayed on the HMI and logged in the SCADA system for operator review.

Critical faults, such as LS-601 detecting blanket level > 3.0 meters or PT-601A/PT-601B detecting discharge pressure < 15 psig, trigger a system-wide shutdown and lockout until the fault is resolved. Operators must reset alarms via HMI before restarting equipment.


## 8 **Tertiary/Advanced Treatment**
|Tagname | Type | Description |
|---------|------|-------------|
|FFIC-703 | Flow Controller | Performs ratio control for backwash flow rate adjustment based on influent flow rate. |
|FIC-702  | Flow Controller | Controls backwash flow rate setpoint for FV-702 based on ratio calculation. |
|FT-701   | Flow Transmitter | Measures influent flow rate to the tertiary filtration system. |
|FV-702   | Flow Valve | Regulates backwash flow rate as per FIC-702 setpoint. |
|TF-701   | Temperature Transmitter | Measures temperature in the tertiary filtration system. |
|TT-701   | Temperature Transmitter | Monitors temperature for process control and safety. |


### 8.1) Control Strategy Description

The tertiary filtration system utilizes a ratio control strategy to maintain a precise proportional relationship between the influent flow rate and the backwash flow rate to ensure consistent turbidity removal and filter bed integrity. The influent flow rate is measured by FT-701, which serves as the wild flow variable. The backwash flow rate is controlled by FIC-702, which adjusts the setpoint of FV-702 based on the ratio calculation performed by ratio controller FFIC-703.

The ratio control is configured to maintain a backwash-to-influent flow ratio of 0.1:1 under normal operating conditions. The setpoint for the controlled backwash flow rate is calculated as:

\[ \text{Backwash Flow SP (FIC-702)} = \text{Influent Flow (FT-701)} \times 0.1 \]

The ratio setpoint is adjustable within a range of 0.05:1 to 0.2:1 to accommodate varying influent characteristics and operational requirements. Flow measurement ranges are 0–5000 m³/h for FT-701 and 0–500 m³/h for FIC-702. A 5% deadband is implemented in FFIC-703 to minimize control valve hunting during stable operation.


### 8.2) Interlocks and Permissives

The ratio control loop is enabled only when FT-701 confirms an influent flow rate above 50 m³/h. If the influent flow rate falls below this threshold, FFIC-703 will automatically disable the backwash flow control by setting FIC-702 to its minimum output of 0%. Additionally, the backwash flow control valve FV-702 will not open unless the tertiary filter TF-701 is in operation and the turbidity sensor TT-701 indicates a turbidity level below 5 NTU.

A permissive ensures that the ratio control loop is overridden, and FV-702 is fully closed if a high-high turbidity alarm (10 NTU) is triggered by TT-701, indicating potential filter breakthrough. This condition requires operator intervention to assess and resolve the issue before resuming ratio control.


### 8.3) Alarm and Fault Handling

The ratio controller FFIC-703 generates a deviation alarm if the actual backwash-to-influent flow ratio deviates by more than ±0.02 from the setpoint for a duration exceeding 30 seconds. This alarm is logged as "Ratio Deviation Alarm" and prompts inspection of FT-701, FIC-702, and FV-702 for potential faults.

A low flow alarm is triggered if FT-701 measures an influent flow rate below 50 m³/h, labeled as "Low Influent Flow Alarm." Under this condition, FFIC-703 transitions to manual mode, and FIC-702 is set to its fail-safe position of 0% output.

In the event of a sensor fault in FT-701 or TT-701, FFIC-703 will generate a "Sensor Fault Alarm" and automatically switch to manual mode. Operators are required to manually adjust the backwash flow rate via FIC-702 until the fault is resolved.


## 9 **Disinfection**
|Tagname | Type | Description |
|---------|------|-------------|
|CL-801 | Chlorination System | Provides chlorine dosage for effluent disinfection |
|DC-801 | Dechlorination System | Supplies dechlorination agent to neutralize chlorine residuals |
|FIC-101 | Flow Controller | Maintains chlorination dosage ratio to effluent flow rate |
|FIC-102 | Flow Controller | Maintains dechlorination dosage ratio to effluent flow rate |
|FT-801 | Flow Transmitter | Measures effluent flow rate for ratio control calculations |
|LV-105 | Level Valve | Regulates level control in associated process equipment |
|UV-801 | Ultraviolet System | Provides UV disinfection for effluent treatment |
|XV-106 | On-Off Valve | Isolates or permits flow in the associated pipeline |


### 9.1) Control Strategy Description

The disinfection process employs ratio control to maintain a proportional relationship between the effluent flow rate measured by FT-801 and the disinfectant dosing systems, including chlorination (CL-801) and dechlorination (DC-801). The effluent flow rate, measured by FT-801, serves as the wild flow variable, while the controlled flow setpoints for CL-801 and DC-801 are calculated using ratio controllers FIC-101 and FIC-102, respectively. FIC-101 maintains a chlorination dosage ratio of 2.5:1 (chlorine dosage to effluent flow), while FIC-102 maintains a dechlorination dosage ratio of 1.2:1 (dechlorination agent to effluent flow). For example, if FT-801 measures an effluent flow rate of 500 m³/hr, FIC-101 adjusts the chlorine flow setpoint to 1250 m³/hr, and FIC-102 adjusts the dechlorination agent flow setpoint to 600 m³/hr. Ratio limits are clamped between 2.0:1 and 3.0:1 for chlorination and 1.0:1 to 1.5:1 for dechlorination to ensure safe operation. Both ratio controllers include manual bias adjustment capabilities for operator intervention and automatic trim adjustments based on effluent quality feedback. Signal scaling ensures all flow measurements are normalized to a 0-100% scale, with engineering units converted to m³/hr for accurate ratio calculations.


### 9.2) Interlocks and Permissives

The ratio control logic for disinfection is interlocked with permissives to ensure safe and reliable operation. Chlorination via CL-801 is inhibited unless FT-801 confirms a minimum effluent flow rate of 50 m³/hr, and XV-106 verifies the shut-off valve is fully open. Similarly, dechlorination via DC-801 is permitted only when FT-801 measures an effluent flow greater than 50 m³/hr and the chlorination system (CL-801) is operational. If FT-801 detects a flow rate below the low-flow cutoff of 50 m³/hr, both FIC-101 and FIC-102 output signals are forced to zero to prevent overdosing. Additionally, an interlock ensures that UV-801 remains active unless both chlorination and dechlorination systems are disabled, preventing simultaneous operation of UV and chemical disinfection systems. Ratio controllers FIC-101 and FIC-102 are disabled if effluent flow exceeds 1000 m³/hr to prevent system overload.


### 9.3) Alarm and Fault Handling

Alarms are configured for both ratio controllers to alert operators of deviations from the expected ratio setpoints. FIC-101 generates a high-ratio alarm if the chlorination dosage exceeds the upper limit of 3.0:1 or falls below the lower limit of 2.0:1. Similarly, FIC-102 triggers a low-ratio alarm if the dechlorination dosage drops below the minimum limit of 1.0:1 or exceeds the maximum limit of 1.5:1. FT-801 includes a fault alarm for signal loss or measurement outside the calibrated range of 0-1000 m³/hr. In the event of a fault in FT-801, both FIC-101 and FIC-102 enter manual mode, allowing operators to directly adjust dosing rates. Deadband logic is implemented in both ratio controllers to prevent hunting during minor flow fluctuations, with a deadband range of ±0.1 ratio units. If any critical valve, such as XV-106 or LV-105, fails to respond within 5 seconds, an interlock disables the associated dosing system and generates a fault alarm. All alarms are displayed on the SCADA system with priority levels for operator response.


## 10 **Influent Lift Station**
|Tagname | Type | Description |
|---------|------|-------------|
|FT-901   | Flow Transmitter     | Measures discharge flow rate for pump operation validation |
|LS-901   | Level Transmitter    | Monitors wet well level for pump control logic |
|P-901A   | Pump                 | Lead pump for influent lift station operation |
|P-901B   | Pump                 | Standby pump for redundancy in influent lift station |
|XV-102   | On-Off Valve         | Isolation valve for system maintenance or emergency shutdown |


### 10.1) Control Strategy Description

The Influent Lift Station employs a redundant duty/standby pump configuration with automatic switchover and failover integrated into level-based control logic. Pump P-901A is designated as the duty (lead) pump, while pump P-901B is the standby (lag) pump. The control system operates primarily in AUTO mode, with manual and test modes available for operator intervention and maintenance activities. In AUTO mode, P-901A starts when LS-901 indicates a wet well level above 60% and stops when the level falls below 40%. If P-901A fails, as determined by discharge flow FT-901 reading less than 15 GPM for 10 consecutive seconds, P-901B will auto-start after a 5-second delay. Both pumps will operate simultaneously if LS-901 exceeds 85%, ensuring sufficient capacity during high inflow conditions.

Runtime equalization is achieved through automatic rotation of the duty pump based on cumulative runtime. The rotation interval is set to 48 hours, ensuring balanced wear and utilization of both pumps. A minimum runtime of 30 minutes is enforced for each pump to prevent hunting during transient conditions.


### 10.2) Interlocks and Permissives

Pump P-901A and P-901B are interlocked with LS-901 to prevent operation when the wet well level is below 40%, ensuring dry-run protection. Additionally, each pump is interlocked with FT-901 to confirm discharge flow within the acceptable range. If FT-901 detects flow below 15 GPM for more than 10 seconds, the corresponding pump is considered failed, triggering switchover logic.

Startup permissives for both pumps include verified motor availability and absence of high vibration alarms. A 5-second on-delay timer ensures transient signals do not prematurely initiate switchover. During switchover, interlocks bypass the failed pump’s shutdown sequence to allow immediate activation of the standby pump. In TEST mode, both pumps operate simultaneously, bypassing level-based interlocks for diagnostic purposes.


### 10.3) Alarm and Fault Handling

Alarm conditions are monitored continuously for both pumps. A failure alarm is triggered if FT-901 detects flow below 15 GPM for 10 seconds while the pump is running. High vibration detected by motor sensors will result in a fault alarm and immediate shutdown of the affected pump. LS-901 high-level alarms are activated when the wet well level exceeds 90%, prompting simultaneous operation of P-901A and P-901B.

In the event of a fault or failure, the control system logs the alarm and initiates switchover logic to activate the standby pump. Operators are notified via SCADA with detailed alarm messages, including the failed pump’s tagname and fault condition. If both pumps fail, a critical alarm is raised, and the system enters a fail-safe mode, shutting off XV-102 to isolate the wet well and prevent overflow.


## 11 **Utilities, Chemicals & Controls**
|Tagname | Type | Description |
|---------|------|-------------|
|CD-1001 | Pump | Provides chemical dosing based on flow controller setpoint |
|FFIC-107 | Flow Controller | Ratio controller for chemical-to-influent flow adjustment |
|FIC-106 | Flow Controller | Regulates chemical dosing setpoint based on ratio control |
|FIT-104 | Flow Transmitter | Measures influent flow rate for ratio control calculations |
|PV-101 | Pressure Valve | Regulates pressure in the chemical dosing system |
|XV-102 | On-Off Valve | Enables or disables chemical dosing flow path |


### 11.1) Control Strategy Description

The chemical dosing system employs ratio control to maintain proportional relationships between influent flow and chemical dosing rates for optimal process performance. The wild flow measurement is provided by FIT-104, which measures the influent flow rate within a range of 0-5000 L/min. The controlled flow is regulated by FIC-106, which adjusts the setpoint for the chemical dosing pumps CD-1001 based on the ratio controller FFIC-107. The ratio setpoint is configured to maintain a 2.5:1 chemical-to-influent flow ratio, ensuring precise dosing. The ratio calculation is performed as follows: the controlled flow setpoint from FIC-106 is calculated as the product of the influent flow rate measured by FIT-104 and the ratio setpoint of 2.5. The ratio controller FFIC-107 includes provisions for manual bias adjustments between ±10% of the calculated setpoint to accommodate process variability. Flow measurement signals are scaled linearly from 0-100% to match the input range of FFIC-107, and a deadband of 3% is implemented to reduce wear on CD-1001 during stable operation. Ratio limits are clamped between 2.0:1 and 3.0:1 to ensure safe operation under varying influent conditions.


### 11.2) Interlocks and Permissives

The chemical dosing system interlocks ensure safe operation and prevent overdosing or underdosing. The ratio controller FFIC-107 is interlocked with FIT-104 to disable chemical dosing if the influent flow rate falls below 100 L/min, as measured by FIT-104, to avoid chemical wastage during low-flow conditions. Additionally, the chemical dosing pumps CD-1001 are prevented from starting unless the shut-off valve XV-102 is confirmed open and the pressure control valve PV-101 is maintaining a minimum pressure of 2 bar. The ratio control mode is permissive only when the influent flow measurement from FIT-104 and the chemical dosing pump feedback signals are within acceptable ranges. Manual control mode overrides are allowed but require operator confirmation and supervisory approval.


### 11.3) Alarm and Fault Handling

The ratio controller FFIC-107 generates alarms under the following conditions: if the calculated ratio exceeds the configured limits of 3.0:1 or drops below 2.0:1, or if the influent flow rate measured by FIT-104 is outside the range of 0-5000 L/min. A high-priority alarm is triggered if the chemical dosing pumps CD-1001 fail to respond to control signals from FIC-106 within 5 seconds. If FIT-104 fails to transmit a valid signal, FFIC-107 will enter a fault state and revert to manual control mode with a default chemical dosing rate of 500 L/min until the fault is resolved. Deadband logic prevents nuisance alarms by ignoring deviations within 3% of the setpoint. All alarms are logged in the SCADA system and require operator acknowledgment before resuming automatic ratio control.


## 12 **Sludge/Biosolids Management**
|Tagname | Type | Description |
|---------|------|-------------|
|DG-1101 | Digester | Processes sludge for thickening operations |
|DW-1101 | Dewatering Unit | Removes excess water from sludge |
|IIC-101 | Solids Concentration Transmitter | Measures sludge consistency for control loop |
|IIC-103 | Controller | Regulates process variables for system stability |
|IIC-105 | Controller | Backup or auxiliary control for process adjustments |
|LV-104 | Level Transmitter | Monitors sludge level in digester or dewatering unit |
|OC-1101 | On-Off Valve | Controls flow isolation in sludge processing system |
|PV-102 | Pressure Valve | Modulates flow to maintain target sludge consistency |
|TH-1101 | Thickener | Performs sludge thickening to achieve desired solids concentration |


### 12.1) Control Strategy Description

The sludge thickening process in TH-1101 is regulated using a PID control loop implemented in IIC-101. The control objective is to maintain the sludge consistency at a target setpoint of 6.5% solids by weight (SP=6.5%). The process variable (PV) is measured by a solids concentration transmitter (IIC-101) with a calibrated range of 0-10% solids and a signal output of 4-20mA. The controller is configured for direct-acting operation, where an increase in PV results in an increase in the manipulated variable (MV) to PV-102. The proportional gain (Kp) is set to 3.0, integral time (Ki) to 1.2 minutes, and derivative time (Kd) to 0.3 minutes. The MV output is clamped between 10% and 90% to ensure safe operation of PV-102, which is a modulating valve with a fail-closed position. Bumpless transfer logic is implemented to allow seamless transition between manual and automatic modes, preventing abrupt changes in MV during mode switching. Anti-windup provisions are included to limit integral accumulation when MV saturates.


### 12.2) Interlocks and Permissives

The PID control loop for TH-1101 is interlocked with the operational status of DG-1101 and DW-1101 to prevent overloading downstream units. The IIC-101 controller is disabled if the digester (DG-1101) or dewatering unit (DW-1101) reports a high-level condition via LV-104, which is configured with a level transmitter spanning 0-100% and a high-level alarm threshold set at 85%. Additionally, PV-102 will not open unless odor control system OC-1101 confirms active operation via IIC-105, ensuring that odor emissions are mitigated during sludge processing. Setpoint clamping logic restricts the SP within the range of 4.0% to 8.0% solids to avoid unsafe thickening conditions that could damage TH-1101 or downstream equipment.


### 12.3) Alarm and Fault Handling

Alarm handling for the PID loop controlling TH-1101 is managed by IIC-103, which monitors PV deviations and actuator faults. A high PV alarm is triggered if the solids concentration exceeds 8.0%, while a low PV alarm is activated below 4.0%. In the event of a transmitter fault in IIC-101, the controller transitions to manual mode, maintaining the last known MV value to prevent uncontrolled operation of PV-102. If PV-102 fails to respond to MV adjustments, an actuator fault alarm is raised, and the valve is commanded to its fail-closed position. Settling time for the PID loop is tuned to achieve a response time of less than 60 seconds, ensuring rapid correction of PV deviations.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 12

- Total Tagnames: 84

- Word Count: 6770
