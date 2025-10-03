# Coking Refinery Process Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Atmospheric Distillation Unit (ADU)**
3. **Vacuum Distillation Unit (VDU)**
4. **Fluid Catalytic Cracking (FCC) Unit**
5. **Delayed Coking Unit**
6. **Hydrotreating Units**
7. **Petroleum Coke Handling System**
8. **Utilities and Offsites**
9. **Flare and Relief Systems**

---


## 1 **Process Overview and Scope**

The refinery is designed to process heavy and sour crude oils into high-value products, including high-octane gasoline, ultra-low sulfur diesel, jet fuel, LPG, and petrochemical feedstocks, while minimizing residual fuel oil output. The process begins with crude oil separation in the atmospheric distillation unit (ADU), producing lighter fractions and atmospheric residue. The atmospheric residue is further processed in the vacuum distillation unit (VDU), yielding vacuum gas oil (VGO) for catalytic conversion and vacuum residue for thermal cracking. Downstream units, including fluid catalytic cracking (FCC), delayed coking, and hydrotreating systems, enhance product yield and quality by converting intermediate streams into targeted fuel products and by-products such as petroleum coke.

Key control strategies focus on maintaining process stability and optimizing yields through temperature, pressure, and flow management across all major units. Interdependencies between process stages ensure a seamless flow of materials, with each unit providing critical feedstocks for subsequent operations. For example, VGO from the VDU feeds the FCC for gasoline and LPG production, while vacuum residue is thermally cracked in the delayed coking unit to generate additional light fractions and petroleum coke. Hydrotreating units ensure compliance with stringent fuel specifications by removing sulfur and improving combustion characteristics. Supporting utilities, including steam, cooling water, and fuel gas systems, sustain continuous operations, while flare and relief systems ensure safe disposal of excess gases and pressure relief during emergencies.

The refinery configuration prioritizes operational flexibility, enabling adaptation to varying crude oil qualities and market demands. Safety and reliability are integral to the design, with automated controls, alarms, and interlocks safeguarding critical operations. By emphasizing deep conversion and product quality, the facility achieves economic optimization while meeting environmental standards and production targets.


## 2 **Atmospheric Distillation Unit (ADU)**
|Tagname | Type | Description |
|---------|------|-------------|
|FIC-104 | Flow Controller | Modulates reflux flow to achieve desired setpoint based on ratio control logic |
|FT-101 | Flow Transmitter | Measures crude oil feed flow rate for ratio control calculations |
|FT-102 | Flow Transmitter | Measures reflux stream flow rate for ratio control and monitoring |
|FV-104 | Flow Valve | Adjusts reflux flow rate to maintain the setpoint provided by FIC-104 |
|PIC-102 | Pressure Controller | Regulates pressure within the system to ensure stable operation |
|PIT-106 | Pressure Transmitter | Monitors system pressure for control and safety purposes |
|TIT-104 | Temperature Transmitter | Measures temperature at a specific point for process monitoring |
|TIT-105 | Temperature Transmitter | Monitors temperature for control and operational adjustments |
|TIT-107 | Temperature Transmitter | Provides temperature data for process optimization and safety checks |


### 2.1) Control Strategy Description

The Atmospheric Distillation Unit (ADU) employs ratio control to maintain precise proportional relationships between the crude oil feed stream and the reflux stream to ensure optimal separation efficiency within the distillation column. The wild flow measurement is provided by FT-101, which monitors the crude oil feed rate in the range of 0-5000 kg/hr. The controlled flow measurement is provided by FT-102, which monitors the reflux stream flow rate in the range of 0-2500 kg/hr. The ratio controller FFIC-103 calculates the reflux flow setpoint (SP) as a function of the crude oil feed flow, using the defined ratio setpoint of 0.5:1 (reflux-to-feed ratio).

The ratio control logic is implemented as follows: FFIC-103 receives the real-time crude oil feed flow signal from FT-101 and calculates the reflux flow SP using the formula SP = FT-101 × 0.5. This setpoint is transmitted to FIC-104, which modulates the reflux flow control valve FV-104 to achieve the desired flow rate. The ratio controller FFIC-103 is configured with ratio adjustment limits between 0.4:1 and 0.6:1 to allow for operational flexibility while maintaining safe and efficient column operation.

Raw sensor data from FT-101 and FT-102 undergoes linear scaling to ensure calibrated flow values are used in control calculations. The control system clamps the reflux flow SP within the range of 0-2500 kg/hr to prevent unsafe conditions. Lead compensation is applied to FFIC-103 to account for dynamic delays in the reflux flow response relative to crude oil feed changes. Three operating modes are available for FFIC-103: Auto (automatic ratio control), Manual (operator-defined reflux flow SP), and Off (isolated control).


### 2.2) Interlocks and Permissives

To ensure safe operation, the ratio control system integrates interlocks and permissives. The reflux flow control valve FV-104 will not open unless the crude oil feed flow measured by FT-101 exceeds 500 kg/hr, preventing excessive reflux flow during low feed conditions. Additionally, FFIC-103 is interlocked with PIC-102 to ensure that column pressure remains within the operational range of 0.5-1.5 bar. If column pressure deviates beyond these limits, FFIC-103 will suspend automatic ratio control and revert to manual mode.

Low flow cutoff logic is implemented such that FFIC-103 disables ratio calculation if FT-101 reports a crude oil feed flow below 100 kg/hr, preventing erroneous control actions during startup or shutdown conditions. Boolean interlocks are configured to ensure that FV-104 remains closed if TIT-104, TIT-105, or TIT-107 report column temperatures outside the safe operating range of 120°C to 350°C.


### 2.3) Alarm and Fault Handling

The ratio control system generates alarms for the following conditions: deviation of the reflux-to-feed ratio beyond the defined adjustment limits (0.4:1 to 0.6:1), loss of signal from FT-101 or FT-102, and failure of FV-104 to respond to control signals from FIC-104. In the event of a fault, FFIC-103 will automatically transition to manual mode, allowing the operator to define the reflux flow SP directly.

If the crude oil feed flow measured by FT-101 falls below 100 kg/hr, a low flow alarm will be triggered, and FFIC-103 will suspend ratio control. Similarly, if column pressure measured by PIT-106 exceeds 1.5 bar or falls below 0.5 bar, FFIC-103 will disable automatic control and alert the operator. Temperature faults from TIT-104, TIT-105, or TIT-107 will also trigger alarms and prompt a system-wide shutdown of reflux flow control to prevent thermal damage to the column.

All alarm conditions are logged in the Distributed Control System (DCS) for operator review, and fault diagnostics are available to assist in troubleshooting sensor or actuator failures.


## 3 **Vacuum Distillation Unit (VDU)**
|Tagname | Type | Description |
|---------|------|-------------|
|PIC-102 | Pressure Controller | Controls vacuum column pressure in the VDU using PID feedback loop. |
|PIT-103 | Pressure Transmitter | Measures vacuum column pressure and provides 4-20 mA signal to controller. |
|PV-101 | Pressure Valve | Modulates position to maintain column pressure within the desired range. |


### 3.1) Control Strategy Description

The vacuum column pressure in the Vacuum Distillation Unit (VDU) is controlled via a single-loop feedback PID control strategy implemented on PIC-102. The process variable (PV) is the column pressure measured by PIT-103, with a transmitter range of 0-760 mmHg absolute, providing a 4-20 mA signal to the controller. The target setpoint (SP) for the column pressure is maintained at 50 mmHg absolute to optimize separation efficiency and prevent column flooding.

PIC-102 is configured as a reverse-acting controller, where an increase in the PV results in a decrease in the manipulated variable (MV) to reduce pressure. The PID tuning parameters are set as follows: proportional gain (Kp) = 1.8, integral time (Ki) = 2.0 minutes, and derivative time (Kd) = 0.5 minutes. The controller output (MV) ranges from 0% to 100% and is scaled to modulate the position of PV-101, a pneumatically actuated pressure control valve.

The final control element, PV-101, is a fail-closed valve with a linear flow characteristic. The valve position is adjusted based on the MV signal from PIC-102, which is transmitted as a 4-20 mA signal to the valve positioner. The valve's operating range is calibrated to correspond to a pressure control range of 10-100 mmHg absolute. Anti-windup logic is implemented in PIC-102 to prevent integral windup during valve saturation conditions, and bumpless transfer is enabled to ensure smooth transitions between manual and automatic modes.

A signal scaling block normalizes the 4-20 mA input from PIT-103 to a 0-100% range for the controller. The setpoint is clamped between 30 mmHg and 70 mmHg to ensure safe operating conditions. A hysteresis of 1 mmHg is applied to the control output to prevent oscillations near the setpoint.


### 3.2) Interlocks and Permissives

The operation of PIC-102 and PV-101 is subject to the following interlocks and permissives to ensure safe and reliable control. The control loop is enabled only when the VDU column is in operation, verified by the column startup permissive logic. The permissive signal (VDU_START_OK) must be active for PIC-102 to operate in automatic mode.

A high-pressure trip interlock is configured to override the controller output and fully close PV-101 if the column pressure exceeds 120 mmHg absolute, as indicated by PIT-103. This interlock is hardwired and latches until manually reset. Additionally, a low-pressure permissive ensures that PIC-102 is disabled if the column pressure falls below 5 mmHg absolute to prevent vacuum pump cavitation.

The control system includes a maintenance bypass permissive (MAINT_BYPASS_OK) for PV-101, which allows manual operation during maintenance activities. When this permissive is active, PIC-102 is forced into manual mode, and the operator is required to manually adjust the valve position.


### 3.3) Alarm and Fault Handling

The control system generates alarms for deviations in the column pressure and equipment faults. A high-pressure alarm (PIT-103_HI) is triggered if the column pressure exceeds 80 mmHg absolute, while a low-pressure alarm (PIT-103_LO) is activated if the pressure drops below 20 mmHg absolute. Both alarms are configured with a 2-second delay to filter out transient fluctuations.

In the event of a transmitter fault, such as a loss of signal from PIT-103 (signal < 3.6 mA or > 21 mA), PIC-102 transitions to manual mode, and an alarm (PIT-103_FAULT) is raised. The operator is required to manually control PV-101 until the fault is resolved. A fault in PV-101, such as a positioner failure, triggers an alarm (PV-101_FAULT) and forces the valve to its fail-closed position.

The control system includes diagnostic logic to detect excessive oscillations in the control loop. If the oscillation amplitude exceeds 5 mmHg for more than 60 seconds, an alarm (PIC-102_OSC) is raised, and the controller tuning should be reviewed.


## 4 **Fluid Catalytic Cracking (FCC) Unit**
|Tagname | Type | Description |
|---------|------|-------------|
|P-301A | Pump | Lead pump for fluid circulation in the system |
|PAH-301 | Pressure Alarm High | High-pressure alarm for regenerator safety |
|PAL-301 | Pressure Alarm Low | Low-pressure alarm for regenerator safety |
|PC-301 | Pressure Controller | Regulates regenerator pressure via control valve |
|PT-301 | Pressure Transmitter | Measures regenerator pressure for control feedback |
|PT-302 | Pressure Transmitter | Auxiliary pressure measurement for system monitoring |
|PT-303 | Pressure Transmitter | Backup pressure measurement for redundancy |
|PTF-301 | Pressure Transmitter | Measures filtered pressure in the system |
|PV-105 | Pressure Valve | Controls regenerator pressure; fail-closed type |
|PV-106 | Pressure Valve | Secondary pressure control valve for system regulation |
|TT-301 | Temperature Transmitter | Measures temperature in the regenerator system |
|XV-108 | On-Off Valve | Isolation valve for emergency or maintenance purposes |


### 4.1) Control Strategy Description

The primary control objective for the FCC unit reactor-regenerator system is to maintain the regenerator pressure at a stable setpoint of 2.5 barg, ensuring optimal catalyst circulation and reaction stability. This is achieved by implementing a PID control loop on the regenerator pressure control valve, PV-105.

The PID controller, designated as PC-301, operates in reverse-acting mode to regulate the manipulated variable (MV), which is the position of PV-105. The process variable (PV) is the regenerator pressure, measured by PT-301, with a transmitter range of 0 to 5.0 barg and a 4-20 mA signal output. The setpoint (SP) is clamped between 2.0 and 3.0 barg to prevent unsafe pressure excursions.

The PID tuning parameters for PC-301 are configured as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.1 minutes. The controller output is scaled to a range of 0% to 100%, corresponding to the fully closed and fully open positions of PV-105. The control valve PV-105 is a fail-closed type to ensure containment in the event of a system failure.

To prevent control hunting, a deadband of ±0.05 barg is applied to the pressure signal. Bumpless transfer logic is implemented to ensure smooth transitions between automatic and manual modes. The expected control performance includes a response time of less than 10 seconds and a settling time of under 30 seconds for a step change in setpoint.


### 4.2) Interlocks and Permissives

The operation of PC-301 and PV-105 is subject to the following interlocks and permissives. The control valve PV-105 will not open unless the regenerator temperature, measured by TT-301, is above 650°C and the air blower, P-301A, is running with a discharge pressure above 3.5 barg as verified by PT-302. Additionally, the setpoint of PC-301 is locked at 2.5 barg during startup until the regenerator achieves stable operation, as determined by a steady-state condition on PT-301 for a continuous 60-second period.

If the emergency shut-off valve XV-108 is closed, PC-301 will immediately force its output to 0%, driving PV-105 to the fully closed position. A permissive ensures that PV-105 cannot open if the fractionator overhead pressure, measured by PT-303, exceeds 0.8 barg, to avoid overpressurization of downstream equipment.


### 4.3) Alarm and Fault Handling

High and low-pressure alarms are configured on PT-301 to alert the operator of deviations from the normal operating range. A high-pressure alarm (PAH-301) is triggered at 2.8 barg, while a low-pressure alarm (PAL-301) is activated at 2.2 barg. If the regenerator pressure exceeds 3.0 barg, an emergency trip signal is sent to XV-108, closing the valve to isolate the regenerator.

In the event of a transmitter fault on PT-301, the controller PC-301 will enter manual mode, and the operator will be required to manually adjust PV-105 until the transmitter fault is resolved. A fault alarm (PTF-301) will be displayed on the control interface, and the system will log the event for maintenance review. Anti-windup logic is implemented in PC-301 to freeze the integral term during transmitter faults, preventing output saturation.

In the case of a power failure to PV-105, the valve will fail closed to isolate the regenerator. An auxiliary pressure relief valve, PV-106, is designed to open at 3.5 barg to protect the system from overpressure in such scenarios.


## 5 **Delayed Coking Unit**
|Tagname | Type | Description |
|---------|------|-------------|
|FT-401A | Flow Transmitter | Measures flow rate of process fluid. |
|FV-401 | Flow Valve | Modulates fuel gas flow to furnace burners. |
|P-401A | Pump | Primary pump for fluid circulation. |
|P-401B | Pump | Backup pump for fluid circulation. |
|PC-401 | Pressure Controller | Maintains pressure setpoint in the system. |
|PT-402 | Pressure Transmitter | Measures pressure in the process line. |
|PT-403 | Pressure Transmitter | Monitors pressure downstream of equipment. |
|TC-401 | Temperature Controller | Regulates furnace outlet temperature. |
|TIT-101 | Temperature Transmitter | Measures furnace outlet temperature. |


### 5.1) Control Strategy Description

The primary control objective for the delayed coking unit is to maintain the furnace outlet temperature at a precise setpoint to ensure optimal thermal cracking of the vacuum residue feedstock. The process variable (PV) is the furnace outlet temperature measured by TIT-101, with a target setpoint (SP) of 495°C. The temperature control loop is implemented using PID controller TC-401.

TC-401 is configured as a reverse-acting controller, where an increase in PV results in a decrease in manipulated variable (MV) to maintain stability. The PID tuning parameters are set as follows: proportional gain (Kp) = 3.2, integral time (Ki) = 0.9 minutes, and derivative time (Kd) = 0.3 minutes. The controller output (MV) adjusts the control valve FV-401, which modulates the flow of fuel gas to the furnace burners. The control valve FV-401 is specified as fail-closed to ensure safe shutdown in the event of a loss of instrument air.

The measurement signal from TIT-101 is transmitted as a 4-20mA signal corresponding to a temperature range of 400°C to 550°C. The signal is scaled linearly within the controller to normalize the PV between 0-100%. The output of TC-401 is clamped between 0% and 100%, corresponding to the fully closed and fully open positions of FV-401. Bumpless transfer logic is implemented to ensure smooth transitions between manual and automatic modes, with the manual bias value synchronized to the current MV during mode switching.

To prevent control hunting, a deadband of ±2°C is applied around the SP. This ensures that minor fluctuations in PV do not result in unnecessary control actions. The control loop is designed to achieve a response time of less than 30 seconds and a settling time of under 2 minutes for typical process disturbances.


### 5.2) Interlocks and Permissives

The operation of TC-401 is subject to several interlocks and permissives to ensure safe and reliable control of the furnace. The control loop will not engage unless the following conditions are met: the fuel gas pressure, monitored by PC-401, is within the range of 2.5-4.0 bar; the furnace draft pressure, measured by PT-402, is between -0.1 and -0.5 kPa; and the feed pump P-401A or P-401B is running with a discharge pressure above 8.0 bar, as verified by PT-403.

An interlock is configured to immediately close FV-401 if TIT-101 detects a temperature exceeding 550°C, indicating a high-temperature trip condition. Additionally, the control logic includes a permissive that prevents the opening of FV-401 if the furnace pilot burners are not confirmed lit by flame detectors FT-401A/B. This ensures that fuel gas is not introduced into the furnace without proper ignition.

A timer delay of 5 seconds is applied to the fuel gas flow interlock to account for transient conditions during startup. This prevents nuisance trips while maintaining safety.


### 5.3) Alarm and Fault Handling

The control system generates high and low temperature alarms based on the PV from TIT-101. A high-temperature alarm (TIT-101 > 510°C) alerts the operator to potential overheating, while a low-temperature alarm (TIT-101 < 480°C) indicates insufficient thermal cracking conditions. Both alarms are configured with a 3-second delay to avoid spurious triggers due to transient fluctuations.

In the event of a sensor fault or signal loss from TIT-101, the control loop enters a fail-safe mode, driving FV-401 to its fail-closed position. The fault is indicated by a system alarm, and the PV is flagged as invalid. Operators are required to manually intervene and switch TC-401 to manual mode until the fault is resolved.

Anti-windup logic is implemented in TC-401 to prevent integral action from accumulating during periods when the valve is at its output limit. This ensures stable control performance when the loop returns to normal operation.


## 6 **Hydrotreating Units**
|Tagname | Type | Description |
|---------|------|-------------|
|E-501   | Heat Exchanger       | Transfers heat to process fluid for temperature control in reactor system |
|ESD-501 | Emergency Stop       | Shuts down the system during emergency conditions for safety |
|FC-103  | Flow Controller      | Regulates hydrogen feed flow to maintain setpoint within specified range |
|FT-103  | Flow Transmitter     | Measures hydrogen flow rate and provides signal to controller |
|FV-103  | Flow Valve           | Controls hydrogen flow to the reactor; fail-closed for safety |
|PC-501  | Pressure Controller  | Maintains reactor pressure within operational limits |
|PT-501  | Pressure Transmitter | Measures reactor pressure for monitoring and control purposes |
|PT-502  | Pressure Transmitter | Provides additional pressure measurement for redundancy or specific locations |
|TC-501  | Temperature Controller | Regulates reactor outlet temperature by controlling heating medium flow |
|TT-101  | Temperature Transmitter | Measures reactor outlet temperature for control and monitoring |
|TV-501  | Temperature Valve    | Adjusts heating medium flow to maintain desired reactor temperature |


### 6.1) Control Strategy Description

The hydrotreating unit employs PID control to regulate hydrogen feed flow, reactor pressure, and reactor outlet temperature to ensure optimal sulfur removal and fuel specification compliance. The primary control loop for hydrogen feed is configured on flow control valve FV-103, with the process variable (PV) measured by flow transmitter FT-103. The setpoint (SP) for hydrogen flow is operator-adjustable within the range of 500 to 1500 Nm³/h, constrained to prevent excessive hydrogen consumption or insufficient feed. The PID controller (FC-103) is configured as reverse-acting to decrease the valve opening when the measured flow exceeds the setpoint.

The PID tuning parameters for FC-103 are set as follows: proportional gain (Kp) = 1.8, integral time (Ki) = 0.5 min, and derivative time (Kd) = 0.1 min. The controller output (MV) is clamped between 0% and 100% to match the stroke range of FV-103. FV-103 is a fail-closed valve to ensure hydrogen flow is automatically cut off during a fault condition. The transmitter FT-103 provides a 4-20 mA signal corresponding to a measurement span of 0 to 2000 Nm³/h.

Reactor temperature control is implemented on temperature control valve TV-501, which regulates the flow of heating medium to heat exchanger E-501. The process variable is measured by temperature transmitter TT-101, with a control range of 300°C to 400°C. The temperature setpoint is fixed at 375°C. The PID controller (TC-501) is configured as direct-acting, with tuning parameters Kp = 2.5, Ki = 0.8 min, and Kd = 0.2 min. TV-501 is a fail-open valve to ensure reactor cooling in the event of a control failure.

A bumpless transfer algorithm is implemented in both FC-103 and TC-501 to allow seamless switching between manual and automatic modes without introducing process disturbances. Additionally, a 1% deadband is applied to both loops to minimize wear on the control valves during steady-state operation.


### 6.2) Interlocks and Permissives

The hydrogen feed control loop (FC-103) is interlocked with the reactor pressure control loop (PC-501) to ensure safe operation. If the reactor pressure, as measured by PT-501, exceeds 50 bar, the hydrogen feed setpoint is automatically reduced to 50% of its current value. Similarly, if the reactor outlet temperature, measured by TT-101, exceeds 410°C, the hydrogen feed control loop is disabled, and FV-103 is forced to a fully closed position.

The reactor temperature control loop (TC-501) includes a permissive that prevents heating medium flow unless the reactor inlet pressure, as measured by PT-502, is above 10 bar. Additionally, a 15-second delay is imposed on the opening of TV-501 after the permissive is satisfied to allow stabilization of upstream flow conditions.

Both control loops are interlocked with the emergency shutdown system (ESD-501). Upon activation of ESD-501, FV-103 and TV-501 are forced to their respective fail-safe positions (closed and open, respectively), and all PID controllers are placed in manual mode to prevent unintended operation during shutdown.


### 6.3) Alarm and Fault Handling

High-priority alarms are configured for both hydrogen flow and reactor temperature control. For FC-103, a high alarm is triggered if the measured flow (FT-103) exceeds 1600 Nm³/h, and a low alarm is triggered if the flow falls below 400 Nm³/h. For TC-501, a high-high alarm is activated if the reactor outlet temperature (TT-101) exceeds 415°C, and a low-low alarm is activated if the temperature drops below 290°C.

In the event of a transmitter fault, such as a loss of signal from FT-103 or TT-101, the associated PID controller is automatically placed in manual mode, and the final control element (FV-103 or TV-501) is driven to its fail-safe position. Diagnostic alarms are generated for failed transmitters, and operators are required to acknowledge these alarms before resetting the control loop.

Anti-windup logic is implemented in both FC-103 and TC-501 to prevent integral term accumulation when the controller output is saturated. This ensures prompt recovery of control performance when the process variable returns to the controllable range.


## 7 **Petroleum Coke Handling System**
|Tagname | Type | Description |
|---------|------|-------------|
|FA-601   | Flow Alarm         | Low flow alarm for system protection            |
|FIC-601  | Flow Controller    | Regulates flow rate of petroleum coke slurry    |
|FT-601   | Flow Transmitter   | Measures flow rate of petroleum coke slurry     |
|LT-601   | Level Transmitter  | Monitors level in the feed silo                 |
|MCC-601  | Motor Control Center | Controls power supply for P-601A pump          |
|MCC-602  | Motor Control Center | Controls power supply for P-601B pump          |
|P-601A   | Pump               | Primary handling pump for petroleum coke slurry |
|P-601B   | Pump               | Backup handling pump for petroleum coke slurry  |
|TAH-104  | Temperature Alarm  | High temperature alarm for system safety        |
|TT-104   | Temperature Transmitter | Measures temperature in the system           |


### 7.1) Control Strategy Description

The petroleum coke handling system utilizes PID control to regulate the flow rate of petroleum coke slurry through the handling pumps (P-601A/B) to ensure stable transport to storage silos. The primary controlled variable is the flow rate measured by flow transmitter FT-601, with the setpoint (SP) defined by operator input through the HMI. The PID controller, FIC-601, operates in reverse-acting mode to modulate the pump speed via a variable frequency drive (VFD). The target setpoint for flow rate is 150 m³/h, with a permissible range of 100-200 m³/h to maintain system stability.

The PID tuning parameters are configured as follows: proportional gain (Kp) = 2.0, integral time (Ki) = 1.5 min, and derivative time (Kd) = 0.3 min. The controller output (MV) is constrained between 20% and 100% to prevent pump cavitation at low speeds and overloading at high speeds. The measurement signal from FT-601 is scaled to a 4-20mA range corresponding to 0-250 m³/h, normalized to a 0-100% scale within FIC-601. Bumpless transfer is implemented to ensure smooth transitions between manual and automatic modes, with anti-windup logic preventing integral term accumulation during manual operation.


### 7.2) Interlocks and Permissives

Interlocks are integrated to protect equipment and ensure safe operation. The handling pumps P-601A/B are interlocked with the level transmitter LT-601 on the feed silo. If the level in the silo drops below 10% (LL), the pumps are automatically stopped to prevent dry running. Additionally, the crusher motor MCC-601 is interlocked with the conveyor belt motor MCC-602 to ensure the crusher only operates when the conveyor is running. A permissive signal from TT-104 ensures that the slurry temperature remains below 80°C before the pumps can start, preventing damage to downstream equipment.

The setpoint for FIC-601 is clamped within the range of 100-200 m³/h to prevent excessive flow rates that could overload the silos. A 5-second delay timer is applied to the pump start command to allow the system to stabilize after interlock conditions are cleared.


### 7.3) Alarm and Fault Handling

Alarms are configured to alert operators of abnormal conditions. A high-level alarm (LAH) is triggered if LT-601 detects a silo level above 90%, indicating potential overflow. A low-flow alarm (FA-601) is generated if FT-601 measures a flow rate below 80 m³/h for more than 10 seconds, suggesting pump or pipeline blockage. High-temperature alarm (TAH-104) is activated if TT-104 detects a slurry temperature exceeding 85°C, requiring immediate operator intervention to prevent equipment damage.

Fault handling includes automatic shutdown sequences. If FT-601 fails to transmit a valid signal (signal loss or out-of-range condition), FIC-601 enters manual mode, and the pump speed is set to 0% output. In the event of a VFD fault on P-601A, the standby pump P-601B is automatically started, provided permissive conditions are met. All faults are logged in the control system for diagnostic purposes, and operators are prompted to investigate and resolve issues before restarting affected equipment.


## 8 **Utilities and Offsites**
|Tagname | Type | Description |
|---------|------|-------------|
|B-701   | Boiler             | Provides steam generation for process heating. |
|FD-701  | Forced Draft Fan   | Supplies combustion air to the boiler.          |
|FIC-702 | Flow Controller    | Controls combustion air flow to maintain ratio. |
|FT-701  | Flow Transmitter   | Measures fuel gas flow to the boiler.           |
|FT-702  | Flow Transmitter   | Measures combustion air flow to the boiler.     |
|FV-701  | Flow Valve         | Regulates fuel gas flow to the boiler.          |
|FV-702  | Flow Valve         | Modulates combustion air flow based on control. |
|LIC-101 | Level Controller   | Maintains liquid level in a specified vessel.   |
|PT-701  | Pressure Transmitter | Measures pressure in the fuel gas line.       |


### 8.1) Control Strategy Description

In the **Utilities and Offsites** section, ratio control is implemented to maintain a precise proportional relationship between the fuel gas flow to the boiler (B-701) and the combustion air flow. The wild flow, measured by FT-701 (fuel gas flow transmitter), is used as the primary input for ratio calculations. The controlled flow, measured by FT-702 (combustion air flow transmitter), is adjusted to maintain a 10:1 air-to-fuel ratio, ensuring optimal combustion efficiency.

The ratio controller FFIC-701 calculates the combustion air flow setpoint (SP) based on the fuel gas flow measurement. The relationship is defined as:
\[ \text{FT-702 SP} = \text{FT-701 PV} \times 10 \]

Here, FT-701 provides a process variable (PV) range of 0–500 kg/hr, while FT-702 adjusts the air flow SP within a range of 0–5000 kg/hr. The flow control valve FV-702 modulates the combustion air flow based on the output of FIC-702 (air flow controller). FFIC-701 includes manual bias adjustment capability, allowing operators to fine-tune the ratio within a range of 9.5:1 to 10.5:1 for specific combustion conditions.

Signal scaling ensures accurate ratio calculation, with FT-701 and FT-702 outputs linearly scaled to engineering units (kg/hr). A low-flow cutoff is implemented such that if FT-701 PV falls below 50 kg/hr, FFIC-701 forces FIC-702 to maintain a minimum air flow of 500 kg/hr to prevent flame instability in B-701.


### 8.2) Interlocks and Permissives

The ratio control logic is interlocked with boiler safety systems to ensure safe operation. FT-701 and FT-702 are continuously monitored for signal validity. If either transmitter fails or provides a signal outside its calibrated range, FFIC-701 automatically disables ratio control and switches FIC-702 to manual mode, maintaining a default air flow of 2500 kg/hr.

A permissive condition requires the boiler flame detector FD-701 to confirm active combustion before FFIC-701 enables ratio control. Additionally, LIC-101 (boiler drum level controller) ensures that the drum level remains within 40–60% before allowing fuel gas flow through FV-701. If LIC-101 detects a level outside this range, FFIC-701 halts fuel gas flow and combustion air flow to B-701.

Boolean interlocks prevent operation if the cooling water supply to B-701 is unavailable, as confirmed by PT-701 (pressure transmitter) indicating cooling water pressure below 2 bar. The system also prevents FV-702 from opening unless the fuel gas flow rate exceeds 50 kg/hr, ensuring air flow does not exceed safe limits during startup.


### 8.3) Alarm and Fault Handling

Alarms are configured to notify operators of deviations from the air-to-fuel ratio or equipment faults. FFIC-701 generates a high-priority alarm if the calculated air-to-fuel ratio exceeds 10.5:1 or falls below 9.5:1 for more than 5 seconds, indicating potential combustion inefficiency. FT-701 and FT-702 are equipped with signal fault alarms to detect transmitter failures or calibration errors.

Low-flow alarms are triggered if FT-701 PV drops below 50 kg/hr, prompting operators to verify fuel gas supply. Similarly, a high-flow alarm is activated if FT-701 PV exceeds 450 kg/hr, indicating potential overloading of the boiler. FIC-702 generates a control deviation alarm if the actual air flow deviates from FFIC-701 SP by more than 10% for 10 seconds.

In the event of a fault, FFIC-701 transitions to manual mode, maintaining a default air flow of 2500 kg/hr through FV-702. Operators are required to investigate and clear the fault condition before re-enabling automatic ratio control.


## 9 **Flare and Relief Systems**
|Tagname | Type | Description |
|---------|------|-------------|
|FV-102 | Flow Valve | Regulates flow to maintain pressure in the knockout drum. |
|LC-801 | Level Controller | Maintains liquid level within the specified range. |
|PIC-101 | Pressure Controller | Controls knockout drum pressure to prevent overpressure. |
|PT-106 | Pressure Transmitter | Measures knockout drum pressure and sends signal to controller. |


### 9.1) Control Strategy Description

The flare system is regulated by PIC-101, which maintains the pressure within the knockout drum at a target setpoint of 1.5 barg. The controller operates in reverse-acting mode, ensuring that an increase in process variable (PV) results in a decrease in manipulated variable (MV) to prevent overpressure. The PID tuning parameters are configured as follows: proportional gain (Kp) = 3.2, integral time (Ki) = 0.5 min, and derivative time (Kd) = 0.1 min. The controller output range is limited to 0-100% to match the control valve FV-102's operational range.

The process pressure is measured by PT-106, a pressure transmitter with a calibrated range of 0-5 barg, transmitting a 4-20mA signal to PIC-101. Signal scaling ensures the transmitter output is normalized to the controller input range of 0-100%. FV-102, the final control element, is a pneumatically actuated valve with a fail-open position to ensure safety during controller or power failure scenarios. A 3% deadband is implemented in PIC-101 to minimize valve wear during steady-state operation.

The controller is equipped with bumpless transfer logic to facilitate smooth transitions between manual and automatic modes. Setpoint clamping is applied to restrict operator-entered values within the range of 1.0-2.0 barg to prevent unsafe operating conditions. Anti-windup provisions are included to limit integral action during saturation events, ensuring stable control performance.


### 9.2) Interlocks and Permissives

PIC-101 is interlocked with the flare stack ignition system to ensure proper combustion of vented gases. The controller is disabled if the ignition system fails, preventing uncontrolled gas discharge. FV-102 is equipped with a position feedback transmitter, ensuring the valve responds correctly to controller output. If the valve position deviates by more than 5% from the commanded position, the controller enters fault mode and halts further adjustments.

Permissive logic requires PT-106 to provide a valid signal within its calibrated range before PIC-101 can initiate control. If PT-106 fails or outputs an invalid signal, PIC-101 transitions to manual mode, alerting the operator to take corrective action. Additionally, FV-102 cannot open unless the knockout drum level, monitored by LC-801, is below 80% to avoid liquid carryover into the flare stack.


### 9.3) Alarm and Fault Handling

PIC-101 generates high-pressure and low-pressure alarms when the process pressure exceeds 1.8 barg or drops below 1.2 barg, respectively. These alarms are displayed on the operator interface and logged for historical analysis. If the pressure deviates beyond these thresholds for more than 30 seconds, the controller initiates an emergency shutdown sequence, closing FV-102 to isolate the system.

Fault conditions in PT-106 or FV-102 trigger a system-wide alarm, notifying operators of equipment failure. In the event of a PT-106 signal loss, PIC-101 switches to manual mode and clamps the controller output at its last known value to prevent abrupt process changes. FV-102 is designed to fail open, ensuring continuous gas venting to the flare stack during fault scenarios.

PIC-101 includes diagnostic routines to monitor controller health and performance. If the controller fails to achieve the setpoint within a 60-second settling time, an alarm is raised, and the operator is prompted to investigate potential tuning or equipment issues.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 9

- Total Tagnames: 66

- Word Count: 5901
