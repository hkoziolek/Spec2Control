# LNG Production Train Process Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Feed-Gas Reception and Pretreatment**
3. **Acid Gas Removal (Amine Absorber System)**
4. **Molecular-Sieve Dehydration and Mercury Removal**
5. **Heavy-Hydrocarbon and NGL Recovery**
6. **Liquefaction and Refrigerant System**
7. **LNG Storage and Ship-Loading**

---


## 1 **Process Overview and Scope**

The LNG production train is designed to process pipeline natural gas into liquefied natural gas (LNG) suitable for storage and export. The overarching objectives include maximizing hydrocarbon recovery, achieving optimal liquefaction performance, and ensuring safe, reliable operations across all process phases. The system is segmented into distinct stages: feed-gas reception and pretreatment, acid gas removal, dehydration and mercury removal, heavy-hydrocarbon recovery, liquefaction, and LNG storage and ship-loading. Each stage is interconnected to create a seamless flow of materials and energy, supported by a comprehensive control strategy that integrates real-time monitoring, automated adjustments, and safety interlocks.

The process begins with feed-gas reception, where liquids are separated, and gas pressure is stabilized to facilitate downstream processing. Acid gas removal follows, targeting H₂S and CO₂ extraction to meet product specifications while maintaining optimal absorber performance. Dehydration and mercury removal eliminate water and trace contaminants, ensuring the gas is conditioned for cryogenic temperatures. Heavy hydrocarbons are then recovered through controlled cooling and separation, optimizing liquid yields while preserving methane for liquefaction. The liquefaction phase employs a dual-mixed-refrigerant system to progressively cool the gas to −160 °C, converting it into LNG. This stage is critical, as it balances thermal efficiency with high compressor throughput.

Throughout the process, advanced control strategies such as cascade loops, alarm-driven sequencing, and dynamic pressure-temperature adjustments are employed to maintain stable operation. Safety considerations are paramount, with automated shutdowns, high-integrity pressure protection systems, and tank-overfill prevention safeguarding personnel and equipment. The final LNG product is stored in full-containment tanks before being loaded onto ships for export, completing the production cycle. The system design ensures operational reliability, product quality, and compliance with environmental and safety standards.


## 2 **Feed-Gas Reception and Pretreatment**
|Tagname | Type | Description |
|---------|------|-------------|
|DP-101 | Differential Pressure Transmitter | Measures differential pressure across a process component |
|DP-102 | Differential Pressure Transmitter | Monitors pressure drop for system diagnostics |
|FT-101 | Flow Transmitter | Measures feed-gas flow rate (0–5000 Nm³/hr) |
|IIC-101 | Ratio Controller | Calculates liquid separation flow setpoint based on feed-gas flow and ratio |
|IT-102 | Flow Transmitter | Monitors liquid separation flow rate (0–2000 Nm³/hr) |
|LCV-101 | Level Control Valve | Modulates liquid flow to maintain separation ratio |
|LT-101 | Level Transmitter | Measures liquid level in a vessel or separator |


### 2.1) Control Strategy Description

The feed-gas reception and pretreatment section employs ratio control to maintain a precise proportional relationship between the pipeline gas flow rate and the liquid separation rate. The wild flow measurement is provided by FT-101, which measures the feed-gas flow rate within a range of 0–5000 Nm³/hr. This value is used as the input to the ratio controller IIC-101, which calculates the controlled flow setpoint for the liquid separation stream based on a fixed ratio of 2.5:1. The controlled flow measurement is derived from IT-102, which monitors the liquid separation flow rate within a range of 0–2000 Nm³/hr. IIC-101 computes the liquid separation flow setpoint as the product of the feed-gas flow rate and the ratio setpoint, ensuring the liquid separation stream maintains the desired proportional relationship to the feed-gas flow.

The output of IIC-101 modulates the liquid control valve LCV-101 to achieve the calculated setpoint. The ratio setpoint can be adjusted manually within the range of 2.0:1 to 3.0:1 via the operator interface, allowing flexibility for process optimization. Signal scaling is applied to both FT-101 and IT-102 measurements to ensure accurate ratio calculations. Lead-lag compensation is implemented within IIC-101 to account for delays in the liquid separation process, ensuring stable control. Low flow cutoff logic disables ratio control if FT-101 measures a feed-gas flow below 100 Nm³/hr to prevent erroneous operation during low-flow conditions.


### 2.2) Interlocks and Permissives

The ratio control loop is governed by interlocks and permissives to ensure safe operation. The liquid separation valve LCV-101 is permitted to modulate only when the feed-gas flow rate measured by FT-101 exceeds 100 Nm³/hr and the liquid separation flow rate measured by IT-102 is within its operational range of 0–2000 Nm³/hr. A Boolean interlock ensures that the ratio controller IIC-101 is active only when the slug catcher level transmitter LT-101 indicates a level below 80% to prevent overfilling. Additionally, a permissive signal from DP-101 and DP-102 ensures that the differential pressure across the inlet separators does not exceed 10 kPa, preventing filter damage or excessive pressure drop. Mode selection logic allows bumpless transfer between automatic ratio control and manual operation, ensuring smooth transitions without process disturbances.


### 2.3) Alarm and Fault Handling

The ratio control system includes comprehensive alarm and fault handling mechanisms to maintain operational integrity. If FT-101 fails or reports a feed-gas flow rate outside its calibrated range of 0–5000 Nm³/hr, an alarm is triggered in the DCS, and the ratio controller IIC-101 clamps the liquid separation flow setpoint to a default value of 500 Nm³/hr. Similarly, if IT-102 fails or reports a liquid separation flow rate outside its calibrated range of 0–2000 Nm³/hr, the control system disables LCV-101 modulation and activates a high-priority alarm. A deviation alarm is triggered if the calculated ratio deviates by more than 10% from the setpoint, prompting operator intervention. Deadband logic within IIC-101 prevents hunting by ignoring ratio deviations smaller than 1%. All alarms are logged and displayed on the operator interface, and fault conditions are latched until manually cleared by the operator.


## 3 **Acid Gas Removal (Amine Absorber System)**
|Tagname | Type | Description |
|---------|------|-------------|
|AI-201 | Analyzer | Monitors and analyzes process variables for acid gas removal system efficiency |
|FV-101 | Flow Valve | Regulates steam flow to the reboiler for temperature control |
|LT-201 | Level Transmitter | Measures liquid level in the amine absorber |
|PT-201 | Pressure Transmitter | Monitors flash tank pressure for permissive interlock conditions |
|TIC-201 | Temperature Controller | PID controller for maintaining absorber temperature setpoint |
|TT-201 | Temperature Transmitter | Measures absorber temperature for feedback to TIC-201 |


### 3.1) Control Strategy Description

The Acid Gas Removal system utilizes PID control to regulate lean-amine circulation temperature within the amine absorber (TIC-201). The controlled variable (PV) is the absorber temperature measured by TT-201, with a target setpoint (SP) of 45°C. The PID controller TIC-201 is configured as reverse-acting to maintain temperature stability by manipulating the steam flow through the reboiler control valve (FV-101).

The transmitter TT-201 has a calibrated range of 0–100°C, outputting a 4–20mA signal to TIC-201. The controller tuning parameters are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.5 minutes, and derivative time (Kd) = 0.0 minutes. The controller output (MV) is scaled to operate FV-101 within a range of 0–100% valve position. FV-101 is a fail-closed valve to ensure safe operation during system faults. Bumpless transfer logic is implemented to allow smooth transitions between manual and automatic modes, with anti-windup protection to prevent integral term saturation during manual operation. A 4% deadband is applied to the controller output to reduce valve wear during stable operation.


### 3.2) Interlocks and Permissives

The PID control loop for TIC-201 is interlocked with low-pressure and high-temperature permissives to protect equipment and ensure safe operation. Steam flow to FV-101 is permitted only when the flash tank pressure (PT-201) is above 0.5 MPa and the absorber temperature (TT-201) is below 50°C. If TT-201 exceeds 50°C, TIC-201 output is clamped to 0% to close FV-101, preventing further heating. Additionally, FV-101 is interlocked with the flash tank level transmitter (LT-201) to ensure sufficient lean-amine inventory; if LT-201 indicates a level below 20%, the valve is forced closed.


### 3.3) Alarm and Fault Handling

High-priority alarms are generated if TT-201 measures a temperature exceeding 50°C or if PT-201 drops below 0.5 MPa. These alarms trigger immediate closure of FV-101 and disengage the PID control loop to prevent equipment damage. A secondary alarm is activated if TIC-201 detects a deviation between SP and PV exceeding 5°C for more than 30 seconds, indicating potential control instability.

In the event of TT-201 signal failure (4 mA or less), TIC-201 enters manual mode with its output frozen at the last known value, while FV-101 defaults to fail-closed position. Operators are notified via DCS with a "Sensor Fault" alarm. The CO₂ analyzer AI-201 continuously monitors absorber outlet gas composition; if CO₂ exceeds 1% by volume, TIC-201 triggers a system-wide shutdown sequence to prevent off-spec product.


## 4 **Molecular-Sieve Dehydration and Mercury Removal**
|Tagname | Type | Description |
|---------|------|-------------|
|AI-302 | Analyzer | Measures outlet H₂O concentration for process monitoring. |
|AI-303 | Analyzer | Monitors mercury concentration in the gas stream. |
|AI-304 | Analyzer | Provides H₂O concentration data for ratio control optimization. |
|DI-301 | Discrete Input | Provides status signal for bed switching sequence. |
|DP-301 | Differential Pressure Transmitter | Measures pressure drop across dehydration beds. |
|FIC-302 | Flow Controller | Adjusts regeneration gas flow based on ratio control setpoint. |
|FT-301 | Flow Transmitter | Measures feed gas flow entering dehydration beds. |
|FV-302 | Flow Valve | Modulates regeneration gas flow for precise control. |


### 4.1) Control Strategy Description

The molecular-sieve dehydration beds operate in a sequenced configuration to remove water from the gas stream, while mercury guard beds ensure mercury concentrations remain below acceptable limits. Ratio control is implemented to maintain proportional flow relationships between the feed gas entering the dehydration beds and the regeneration gas used during bed switching. Feed gas flow is measured by FT-301 (wild flow) with a range of 0–10,000 Nm³/hr. Regeneration gas flow is controlled by FIC-302, which adjusts the setpoint based on the ratio controller FFIC-303. FFIC-303 calculates the regeneration gas flow setpoint as \( \text{SP}_{\text{regen}} = \text{PV}_{\text{feed}} \times R \), where \( R \) is the ratio setpoint configured to 0.25:1. The regeneration gas flow is modulated by FV-302 to ensure precise control.

The ratio setpoint \( R \) is adjustable within limits of 0.20:1 to 0.30:1, allowing operators to optimize regeneration gas consumption based on bed performance and outlet H₂O concentration measured by AI-304. A deadband of ±3% is applied to the calculated setpoint to prevent unnecessary valve modulation during stable operation. Additionally, FFIC-303 includes manual bias adjustment capability, enabling operators to trim the ratio during transitions or abnormal conditions. Signal scaling ensures all flow measurements are normalized to a 0–100% engineering scale for accurate ratio calculation.


### 4.2) Interlocks and Permissives

The ratio control system is interlocked with bed sequencing logic to prevent regeneration gas flow during active dehydration cycles. The permissive signal for FFIC-303 activation is tied to the bed regeneration status, indicated by DI-301. If DI-301 signals that the bed is in dehydration mode, FFIC-303 output is clamped to zero, overriding the ratio calculation. Additionally, the system includes a low-flow cutoff for FT-301, set at 500 Nm³/hr, below which FFIC-303 disables regeneration gas flow to prevent excessive dilution or waste.

Pressure interlocks from DP-301 ensure that excessive differential pressure across the molecular-sieve beds does not initiate regeneration gas flow. If DP-301 exceeds 20 kPa, the ratio control output is disabled, and an alarm is generated. Mercury guard bed analyzers AI-302 and AI-303 provide permissive signals for regeneration gas flow; if mercury concentrations exceed 0.01 µg/Nm³, FFIC-303 output is clamped to zero, preventing further contamination of the regeneration stream.


### 4.3) Alarm and Fault Handling

Alarm thresholds are configured for critical measurements to ensure safe operation of the ratio control system. If FT-301 (wild flow) falls below 500 Nm³/hr, a low-flow alarm is triggered, and FFIC-303 enters a fault state, disabling regeneration gas flow. Similarly, if DP-301 exceeds 20 kPa, a high differential pressure alarm is activated, and the ratio controller output is forced to zero. Outlet H₂O concentration measured by AI-304 has an alarm setpoint at 10 ppm; if exceeded, FFIC-303 ratio setpoint is automatically adjusted to the upper limit of 0.30:1 to increase regeneration gas flow.

In the event of a mercury analyzer fault from AI-302 or AI-303, the system triggers a high-mercury alarm and clamps FFIC-303 output to zero. Ratio controller FFIC-303 includes fault detection logic to monitor signal integrity from FT-301 and FIC-302; if either signal is lost or outside the configured range, FFIC-303 enters manual mode, allowing operators to directly control FV-302. All alarms are logged in the DCS and require operator acknowledgment before the system resumes automatic control.


## 5 **Heavy-Hydrocarbon and NGL Recovery**
|Tagname | Type | Description |
|---------|------|-------------|
|DA-401A | Pressure Transmitter | Measures pressure in the de-ethanizer system. |
|DA-401B | Pressure Transmitter | Redundant pressure measurement for de-ethanizer system. |
|DA-401C | Pressure Transmitter | Third redundant transmitter for pressure monitoring. |
|DA-402 | Pressure Transmitter | Monitors pressure in the heavy-hydrocarbon recovery system. |
|DA-402A | Pressure Transmitter | Redundant pressure measurement for heavy-hydrocarbon system. |
|DA-402B | Pressure Transmitter | Secondary redundant pressure transmitter. |
|DA-402C | Pressure Transmitter | Third redundant transmitter for pressure monitoring. |
|FA-401 | Flow Transmitter | Measures flow rate in the recovery system. |
|FA-402A | Flow Transmitter | Redundant flow measurement for system reliability. |
|FA-402B | Flow Transmitter | Secondary redundant flow transmitter. |
|FA-402C | Flow Transmitter | Third redundant transmitter for flow monitoring. |
|FV-107 | Flow Valve | Regulates flow in the recovery system. |
|I-401 | Interlock | Prevents PV-102 from opening unless PVT-401 is valid. |
|I-402 | Interlock | Ensures operational safety in the recovery system. |
|MA-401 | General Alarm | Alerts for system malfunctions or deviations. |
|PT-401 | Pressure Transmitter | Measures pressure in the de-ethanizer column. |
|PT-401A | Pressure Transmitter | Redundant pressure measurement for 2oo3 voting logic. |
|PT-401B | Pressure Transmitter | Secondary redundant pressure transmitter for voting logic. |
|PT-401C | Pressure Transmitter | Third redundant transmitter for pressure voting logic. |
|PV-102 | Pressure Valve | Modulates pressure in the de-ethanizer column. |
|PVT-401 | Pressure Voting Transmitter | Voted pressure signal for column control. |
|TT-105 | Temperature Transmitter | Measures temperature in the de-propanizer column. |
|TT-106 | Temperature Transmitter | Redundant temperature measurement for column control. |
|TT-107 | Temperature Transmitter | Third redundant transmitter for temperature monitoring. |
|TVT-402 | Temperature Voting Transmitter | Voted temperature signal for column control. |
|XV-104 | On-Off Valve | Isolation valve for emergency shutdown. |


### 5.1) Control Strategy Description

The heavy-hydrocarbon and NGL recovery system employs redundant pressure transmitters PT-401A, PT-401B, and PT-401C to monitor de-ethanizer column pressure, utilizing a 2oo3 voting scheme for critical pressure control. The voted pressure signal (PVT-401) is used to modulate pressure control valve PV-102, maintaining the column pressure setpoint at 1.8 MPa. The voting logic requires at least two of the three transmitters to agree within a ±5% deviation range to produce a valid output. If two transmitters agree and the third deviates beyond the allowable range, the system automatically excludes the faulty transmitter from the voting calculation. In degraded mode, if one transmitter fails or produces a bad PV signal (<3.8 mA or >20.5 mA), the 2oo3 scheme transitions to a 1oo2 configuration, allowing pressure control to continue using the remaining two transmitters. Median select logic is implemented for temperature transmitters TT-105, TT-106, and TT-107 to determine the de-propanizer column temperature (TVT-402), ensuring robust temperature control at a setpoint of 65 °C.


### 5.2) Interlocks and Permissives

The pressure control interlock I-401 prevents PV-102 from opening unless PVT-401 is valid and within the operational range of 1.6–2.0 MPa. The interlock logic continuously evaluates the health of PT-401A, PT-401B, and PT-401C. If all three pressure transmitters fail or produce bad PV signals simultaneously, the interlock closes shut-off valve XV-104 to isolate the column and triggers a high-pressure shutdown. Similarly, temperature control interlock I-402 prevents the activation of flow control valve FV-107 unless TVT-402 is valid and within the range of 60–70 °C. Permissive logic ensures that maintenance bypass switches for PT-401 and TT-105/106/107 are engaged only during manual override mode, preventing automatic transitions to degraded operation during maintenance activities.


### 5.3) Alarm and Fault Handling

Deviation alarms DA-401A, DA-401B, and DA-401C are generated if the pressure readings from PT-401A, PT-401B, or PT-401C differ by more than ±5% from the median pressure value. If a single transmitter produces a bad PV signal (<3.8 mA or >20.5 mA), fault alarm FA-401 is activated, and the transmitter is automatically excluded from the voting calculation. In degraded mode, the system raises a degraded operation alarm DA-402 to notify operators that the 2oo3 voting scheme has transitioned to 1oo2. For temperature control, deviation alarms DA-402A, DA-402B, and DA-402C are triggered if TT-105, TT-106, or TT-107 readings differ by more than ±2 °C from the median temperature. Fault alarms FA-402A, FA-402B, and FA-402C are activated for bad PV signals from any temperature transmitter. All alarms are aggregated into a master alarm MA-401 for centralized operator notification, and diagnostic outputs are logged to the DCS for maintenance tracking.


## 6 **Liquefaction and Refrigerant System**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-504 | Flow Controller | Modulates mixed refrigerant flow to maintain ratio control with propane flow. |
|FT-501 | Flow Transmitter | Measures propane refrigerant flow for ratio control reference. |
|FT-502 | Flow Transmitter | Measures mixed refrigerant flow for ratio control adjustment. |
|FV-501 | Flow Valve | Regulates propane refrigerant flow to the system. |
|FV-502 | Flow Valve | Adjusts mixed refrigerant flow based on FIC-504 output. |
|PT-501 | Pressure Transmitter | Monitors system pressure for operational safety. |
|TIT-102 | Temperature Transmitter | Measures temperature for process monitoring and control. |


### 6.1) Control Strategy Description

The liquefaction and refrigerant system employs ratio control to maintain precise proportional relationships between the propane refrigerant flow and the mixed refrigerant flow to the Main Cryogenic Heat Exchanger (MCHE-501). The propane refrigerant flow, measured by flow transmitter FT-501 (wild flow), is used as the reference variable for the ratio control strategy. The mixed refrigerant flow, measured by flow transmitter FT-502 (controlled flow), is adjusted to maintain a fixed ratio of 2.5:1 (propane flow to mixed refrigerant flow) under normal operating conditions.

The ratio controller, designated as FFIC-503, calculates the setpoint for the mixed refrigerant flow (FIC-504) using the equation:
**FT-502 Setpoint = FT-501 (wild flow) × Ratio Setpoint (2.5)**.

The output of FFIC-503 is clamped between ratio limits of 2.0:1 (minimum) and 3.0:1 (maximum) to ensure safe operation. Flow controller FIC-504 modulates control valve FV-502 to achieve the calculated setpoint. The propane flow signal from FT-501 is scaled within the range of 0-5000 kg/hr, while the mixed refrigerant flow signal from FT-502 is scaled within the range of 0-2000 kg/hr. A low-flow cutoff is implemented to disable ratio control when FT-501 measures less than 500 kg/hr, switching FIC-504 to manual mode with a fixed setpoint of 100 kg/hr to prevent instability.

Ratio bias adjustments are allowed via operator input to FFIC-503, with a manual bias range of ±0.2. Automatic ratio trim is enabled based on the outlet temperature of the MCHE-501, measured by TIT-102. If TIT-102 exceeds the high-temperature limit of -155°C, the ratio is automatically increased by 0.1 to enhance cooling capacity.


### 6.2) Interlocks and Permissives

The ratio control loop is interlocked with the propane compressor anti-surge valves (FV-501). If FV-501 is fully open for more than 5 seconds, FFIC-503 is forced into manual mode, and FIC-504 is set to maintain a fixed flow of 1000 kg/hr to protect the compressors. Additionally, the ratio control loop is disabled if the pressure in the end-flash drum (PT-501) falls below 2.0 MPa, as measured by PT-501. A permissive condition requires the propane flow (FT-501) to be within the range of 500–5000 kg/hr and the mixed refrigerant flow (FT-502) to be within 200–2000 kg/hr for ratio control to be active.


### 6.3) Alarm and Fault Handling

A high-ratio deviation alarm (FFIC-503.DV.HI) is triggered if the actual ratio exceeds the setpoint by more than 0.2 for 10 seconds. Similarly, a low-ratio deviation alarm (FFIC-503.DV.LO) is triggered if the ratio falls below the setpoint by more than 0.2 for 10 seconds. If the propane flow (FT-501) or mixed refrigerant flow (FT-502) signals are lost or fall outside their valid ranges, FFIC-503 generates a fault signal (FFIC-503.FLT), which disables the ratio control loop and places FIC-504 in manual mode with a fixed setpoint of 500 kg/hr. A deadband of ±1% is applied to the ratio setpoint to prevent hunting during stable operation.


## 7 **LNG Storage and Ship-Loading**
|Tagname | Type | Description |
|---------|------|-------------|
|C-601 | Compressor | Manages boil-off gas (BOG) flow during LNG operations |
|FIC-601B | Flow Controller | Modulates compressor suction valve to maintain desired BOG flow rate |
|FT-601A | Flow Transmitter | Measures LNG flow rate from storage tanks |
|FT-601B | Flow Transmitter | Measures boil-off gas (BOG) flow rate |
|FV-601B | Flow Valve | Controls compressor suction to regulate BOG flow |
|HS-601 | Hand Switch | Interlock for SIL-3 tank-overfill prevention system |
|LIT-601 | Level Transmitter | Measures LNG storage tank level |
|LT-601 | Level Transmitter | Monitors LNG storage tank level for control strategy |


### 7.1) Control Strategy Description

The ratio control strategy for LNG storage and ship-loading operations ensures proportional flow relationships between LNG pumped from the storage tanks (LT-601) and boil-off gas (BOG) managed by compressors (C-601). The wild flow variable is the LNG flow rate measured by flow transmitter FT-601A, with a range of 0–5000 m³/hr. The controlled flow variable is the BOG flow rate measured by FT-601B, with a range of 0–1000 m³/hr. Ratio controller FFIC-601 maintains a fixed ratio of 5:1 between LNG flow and BOG flow. The ratio controller calculates the BOG flow setpoint (FT-601B.SP) as FT-601A.PV × 0.2, where 0.2 represents the inverse of the 5:1 ratio.

The controlled flow setpoint FT-601B.SP is sent to flow controller FIC-601B, which modulates the compressor suction valve FV-601B to maintain the desired BOG flow rate. The ratio is adjustable between 4:1 and 6:1 via operator input to FFIC-601.RSP, with setpoint clamping logic limiting adjustments outside this range. A 3% deadband is applied to FFIC-601 to prevent hunting during stable operation. Signal scaling ensures accurate ratio calculations, with FT-601A and FT-601B outputs normalized to engineering units for precise control.


### 7.2) Interlocks and Permissives

The ratio control loop is interlocked with the SIL-3 tank-overfill prevention system (HS-601). If LT-601 level exceeds 90% (LIT-601.PV > 90%), FFIC-601 is disabled, and FIC-601B closes FV-601B fully to prevent excess BOG generation. Additionally, if FT-601A.PV falls below 100 m³/hr, FFIC-601 transitions to manual mode, and the operator must manually set FT-601B.SP. Compressor C-601 cannot start unless LT-601 level is above 10% (LIT-601.PV > 10%) and FT-601A.PV exceeds 200 m³/hr. These permissives ensure safe startup and operation.

A Boolean interlock prevents ratio control activation if HS-601 is in alarm state, ensuring priority safety actions override normal control logic. Mode selection logic allows operators to switch between ratio control, manual control, or individual flow control modes. The system defaults to manual control during maintenance or abnormal conditions.


### 7.3) Alarm and Fault Handling

Alarm thresholds are configured for both wild and controlled flow measurements. If FT-601A.PV exceeds 4500 m³/hr or drops below 100 m³/hr, an alarm is triggered to alert the operator of abnormal LNG flow conditions. Similarly, if FT-601B.PV exceeds 900 m³/hr or falls below 50 m³/hr, an alarm is generated to indicate potential compressor or valve issues.

In the event of a ratio deviation exceeding ±10% from the setpoint (FFIC-601.DEV > 10%), a high-priority alarm is triggered, and FFIC-601 enters fail-safe mode, holding the last valid setpoint. If FT-601A or FT-601B transmitters fail (FT-601A.STATUS or FT-601B.STATUS = FAIL), FFIC-601 disables ratio control and alerts the operator to switch to manual mode. Compressor C-601 trips if FV-601B fails to respond within 5 seconds of a control signal (FV-601B.STATUS = FAIL), ensuring protection against uncontrolled BOG generation.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 7

- Total Tagnames: 62

- Word Count: 4054
