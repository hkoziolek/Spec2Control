# Benzene Distillation Process Control Narrative

---


## Table of Contents

1. **Process Overview and Scope**
2. **Distillation Column (T-101)**
3. **Reboiler Heat Exchanger (E-106)**
4. **Overhead Condenser and Accumulator (E-104 and V-104)**
5. **Benzene Product Pumps (P-102A/B)**
6. **Bottoms Product Handling**

---


## 1 **Process Overview and Scope**

The benzene distillation process is designed to efficiently separate benzene from toluene using thermal distillation principles while maintaining operational safety and system reliability. The primary objective is to achieve high-purity benzene recovery and toluene removal by employing precise control of temperature, pressure, and flow across interconnected process stages. The process flow begins with the vaporization of the benzene-toluene mixture in the distillation column (T-101) through controlled heat input from the reboiler. Overhead vapors are condensed and collected in an accumulator for product recovery, while the toluene-rich bottoms are directed to storage. The system is optimized to ensure continuous operation with minimal downtime through strategic equipment redundancy and robust control methodologies.

The process is divided into several critical phases, including vaporization in the reboiler, separation within the distillation column, overhead condensation, and product handling for benzene and toluene. Key control strategies include maintaining stable column pressure and temperature profiles, regulating reboiler heat input, and ensuring proper flow and level control in condensers and accumulators. The interdependency between these phases is central to achieving process objectives, as the effectiveness of separation relies on precise coordination of heat transfer, vapor condensation, and fluid movement. Safety measures such as alarms, interlocks, and high/low level limits are integrated across the system to mitigate operational risks and protect equipment and personnel.

Overall, the control system prioritizes efficiency, reliability, and safety. Automated monitoring and regulation ensure consistent product quality while maintaining equipment integrity and conserving energy. The design incorporates redundancy in critical components, such as pumps, to guarantee uninterrupted operation. Operational safeguards, combined with an emphasis on precise process control, support the system’s ability to meet both production targets and safety requirements under varying conditions.


## 2 **Distillation Column (T-101)**
|Tagname | Type | Description |
|---------|------|-------------|
|LAH-101 | Level Alarm High | High level alarm for tank overflow protection |
|LAL-101 | Level Alarm Low | Low level alarm for tank level monitoring |
|LIT-101 | Level Transmitter | Measures liquid level in the tank |
|PIT-102 | Pressure Transmitter | Monitors column pressure for safe operation |
|PV-103 | Pressure Valve | Modulates heat input to the reboiler |
|T-101 | Distillation Column | Separates benzene and toluene |
|TE-101 | Temperature Transmitter | Measures temperature at the base of the column |
|TIC-104 | Temperature Controller | Regulates reboiler temperature for optimal separation |
|XV-105 | On-Off Valve | Isolation valve for process safety |


### 2.1) Control Strategy Description

The primary control objective for the distillation column (T-101) is to regulate the reboiler temperature using TIC-104 to maintain a stable separation of benzene and toluene. TIC-104 operates in a single-loop feedback configuration, controlling the temperature at the base of T-101 via TE-101 and modulating the heat input through PV-103. The process variable (PV) is the temperature measured by TE-101, which has a calibrated range of 50°C to 200°C and outputs a 4-20mA signal. The setpoint (SP) for TIC-104 is configured at 150°C to optimize the separation process. TIC-104 is configured as a reverse-acting controller with tuning parameters set to Kp=3.0, Ki=0.5 min, and Kd=0.1 min to ensure precise control and minimize overshoot. The manipulated variable (MV) is the position of PV-103, which is a fail-closed control valve with an actuator signal range of 0-100%. Bumpless transfer logic is implemented to allow seamless switching between manual and automatic modes without disrupting process stability. Signal scaling ensures TE-101 output is normalized to match the controller input range, while the control output from TIC-104 is clamped between 10% and 90% to prevent excessive heating.


### 2.2) Interlocks and Permissives

The operation of TIC-104 is interlocked with the column pressure control system to ensure safe operation. PIT-102 monitors the column pressure, and if the pressure exceeds 150 psig or falls below 90 psig, TIC-104 is forced into manual mode with the output held constant to prevent unsafe temperature excursions. XV-105, a shut-off valve downstream of PV-103, is interlocked to close automatically if the column level, as measured by LIT-101, falls below 20% or exceeds 80%, as indicated by LAL-101 and LAH-101 respectively. The permissive logic ensures TIC-104 can only operate in automatic mode if LIT-101 is within the safe operating range and XV-105 is confirmed open. Additionally, TE-101 signal integrity is continuously monitored, and any deviation beyond the calibrated range triggers a permissive block to inhibit TIC-104 operation.


### 2.3) Alarm and Fault Handling

TIC-104 generates a high-temperature alarm if TE-101 detects a temperature above 180°C, and a low-temperature alarm if the temperature falls below 130°C. These alarms are displayed to the operator with priority levels to prompt immediate corrective action. In the event of TE-101 signal failure (4-20mA signal loss or out-of-range values), TIC-104 enters a fault state where the output is frozen at the last known value, and an alarm is triggered. If PV-103 fails to respond to control signals, TIC-104 generates a control valve fault alarm and switches to manual mode. A deadband of ±2°C is implemented in the control logic to prevent hunting around the setpoint. Settling time for the temperature control loop is designed to be within 5 minutes under normal operating conditions, ensuring rapid stabilization after disturbances.


## 3 **Reboiler Heat Exchanger (E-106)**
|Tagname | Type | Description |
|---------|------|-------------|
|E-106   | Heat Exchanger       | Provides heat to the distillation column via steam. |
|FAH-104 | Flow Alarm High      | High steam flow alarm for safety interlock.         |
|FIC-104 | Flow Controller      | Regulates steam flow to maintain reboiler temperature. |
|FIT-101 | Flow Transmitter     | Measures steam flow rate to the reboiler.           |
|LIC-002 | Level Controller     | Monitors and controls condensate level in the reboiler. |
|PT-101  | Pressure Transmitter | Measures pressure in the steam line.                |
|T-101   | Distillation Column  | Separates toluene and benzene via vaporization.     |
|TAH-106 | Temperature Alarm High | High temperature alarm for reboiler safety.         |
|TAL-106 | Temperature Alarm Low | Low temperature alarm for reboiler operation.       |
|TCV-106 | Temperature Control Valve | Regulates steam flow to the reboiler.             |
|TI-106  | Temperature Transmitter | Measures reboiler temperature for feedback control. |


### 3.1) Control Strategy Description

The reboiler heat exchanger (E-106) is controlled using a single-loop PID feedback system to regulate the steam flow rate via the control valve TCV-106, ensuring the desired temperature at the bottom of the distillation column T-101. The process variable (PV) is the temperature measured by TI-106, with a setpoint (SP) of 180°C for optimal toluene-benzene vaporization. The PID controller FIC-104 is configured as reverse-acting to decrease steam flow when the measured temperature exceeds the setpoint.

The PID tuning parameters are set as follows: proportional gain (Kp) = 3.0, integral time (Ki) = 1.2 minutes, and derivative time (Kd) = 0.3 minutes. The controller output (MV) is scaled to drive TCV-106 within its operating range of 0-100% open. The temperature transmitter TI-106 provides a 4-20mA signal corresponding to a measurement span of 100°C to 250°C. Bumpless transfer is implemented to allow seamless switching between manual and automatic modes without disturbing the process. Anti-windup logic is enabled to prevent integral accumulation during saturation of the control valve.


### 3.2) Interlocks and Permissives

The steam flow control loop is interlocked to ensure safe operation of E-106. The control valve TCV-106 will remain closed (fail-closed position) under the following conditions:
1. Low condensate level in the reboiler, detected by LIC-002, with a trip setpoint of 20% level.
2. High temperature in the reboiler shell, detected by TI-106, exceeding 200°C.
3. Loss of signal from TI-106 or FIC-104, indicated by a transmitter fault.

Permissive logic ensures that the control loop is active only when the distillation column T-101 is operational, verified by a minimum column pressure of 50 psig as measured by PT-101.


### 3.3) Alarm and Fault Handling

Alarm conditions are configured to alert operators of deviations from normal operation. A high-temperature alarm (TAH-106) is triggered when TI-106 exceeds 190°C, while a low-temperature alarm (TAL-106) is activated if TI-106 drops below 170°C. Additionally, a flow failure alarm (FAH-104) is generated if the steam flow measured by FIT-101 falls below 10% of the maximum flow rate.

In the event of a fault in TI-106 or FIC-104, the control valve TCV-106 will default to its fail-closed position, and the system will transition to manual mode. Operators are required to verify the integrity of the temperature measurement and controller output before reactivating automatic control. Hysteresis of 1% is applied to prevent frequent toggling between alarm states near the threshold values.


## 4 **Overhead Condenser and Accumulator (E-104 and V-104)**
|Tagname | Type | Description |
|---------|------|-------------|
|E-104   | Heat Exchanger     | Condenses overhead vapor stream          |
|FIC-107 | Flow Controller    | Regulates condensate flow rate           |
|FT-107  | Flow Transmitter   | Measures condensate flow rate            |
|LAH-104 | Level Alarm High   | High level alarm for accumulator         |
|LAL-104 | Level Alarm Low    | Low level alarm for accumulator          |
|LIC-104 | Level Controller   | Controls liquid level in accumulator     |
|LT-105  | Level Transmitter  | Measures liquid level in accumulator     |
|LV-107  | Level Valve        | Modulates condensate flow rate           |
|PIC-104 | Pressure Controller| Controls pressure in accumulator         |
|PT-104  | Pressure Transmitter| Measures pressure in accumulator         |
|V-104   | Vessel             | Accumulator for condensed liquid         |
|XV-103  | On-Off Valve       | Isolation valve for process line         |


### 4.1) Control Strategy Description

The cascade control system for the overhead condenser and accumulator (E-104 and V-104) utilizes a primary loop to regulate the liquid level in the accumulator (V-104) and a secondary loop to control the flow rate of condensate through the level control valve LV-107. The primary controller, LIC-104, receives input from level transmitter LT-105, which measures the liquid level in V-104. LIC-104 maintains the accumulator level at a setpoint of 65% and outputs a remote setpoint (RSP) to the secondary controller FIC-107.

The secondary controller, FIC-107, regulates the flow rate of condensate by modulating LV-107. FIC-107 receives its process variable from flow transmitter FT-107, which measures the condensate flow rate. The secondary loop is tuned to respond 5 times faster than the primary loop, ensuring rapid disturbance rejection. Tuning parameters are set as follows: LIC-104 (Kp=1.5, Ki=2.5 min) and FIC-107 (Kp=4.0, Ki=0.5 min). The cascade configuration ensures that the primary controller output dynamically adjusts the secondary controller setpoint, maintaining stable operation under varying process conditions.

Signal scaling is implemented between LIC-104 and FIC-107 to ensure compatibility between the primary output range (0-100%) and the secondary setpoint range (0-50 GPM). The system operates in cascade mode by default, with provisions for local and manual modes. Manual setpoints for FIC-107 are clamped between 12 and 79 GPM to prevent saturation of LV-107 and ensure operational safety.


### 4.2) Interlocks and Permissives

The cascade control system is permitted to operate only when the following conditions are satisfied: PT-104 indicates accumulator pressure is within the range of 15-30 psig, and LT-105 confirms the liquid level is above the low alarm threshold set by LAL-104 (10%). Additionally, XV-103, the upstream shut-off valve, must be fully open to allow vapor flow to E-104. If any of these conditions are violated, the cascade control system transitions to manual mode, and the operator is alerted to take corrective action.

During startup, a timer delay of 30 seconds ensures that the secondary loop (FIC-107) stabilizes before the primary loop (LIC-104) begins operation. This prevents interaction-induced hunting and ensures smooth cascade mode transitions.


### 4.3) Alarm and Fault Handling

Alarm handling for the cascade control system includes high and low level alarms from LAH-104 and LAL-104, respectively. If LT-105 detects a level above 90% or below 10%, LIC-104 enters an alarm state and outputs a fixed setpoint to FIC-107 to maintain minimum flow through LV-107. Similarly, if PT-104 detects accumulator pressure exceeding 30 psig, PIC-104 overrides LIC-104 and closes LV-107 to prevent overpressure conditions.

In the event of secondary loop failure, such as FT-107 signal loss or LV-107 actuator malfunction, the system automatically switches to manual mode. LIC-104 outputs a fixed setpoint of 40% to maintain safe operation, and the operator is notified via the control system interface. Deadband logic is applied to LIC-104 to prevent oscillations during recovery from fault conditions.


## 5 **Benzene Product Pumps (P-102A/B)**
|Tagname | Type | Description |
|---------|------|-------------|
|FI-102   | Flow Transmitter     | Measures flow rate for pump operation logic and interlocks. |
|LCV-102  | Level Control Valve  | Regulates level in the accumulator (V-104).                |
|LIC-102  | Level Controller     | Maintains desired level in the accumulator (V-104).        |
|P-102A   | Pump                 | Lead pump for benzene transfer to product storage.         |
|P-102B   | Pump                 | Standby pump for benzene transfer to product storage.      |
|PI-102   | Pressure Transmitter | Monitors suction and discharge pressure for pump control.  |
|V-104    | Vessel               | Accumulator for benzene prior to product storage transfer. |


### 5.1) Control Strategy Description

The benzene product pumps P-102A (duty) and P-102B (standby) operate in a duty/standby configuration to ensure continuous transfer of benzene from the accumulator (V-104) to the product storage. In AUTO mode, P-102A is designated as the lead pump, while P-102B remains in standby. The switchover logic activates P-102B automatically if P-102A fails to maintain adequate discharge pressure, as measured by PI-102, or if a motor fault is detected. The failure condition is defined as PI-102 reading less than 25 psig for 10 seconds. A switchover delay of 5 seconds is incorporated to prevent nuisance switching during transient conditions.

The pumps are equipped with runtime hour meters to facilitate manual rotation of the duty and standby roles. In MANUAL mode, the operator can designate either pump as lead or standby via the local control panel. TEST mode allows both pumps to operate simultaneously for system verification or during high-demand scenarios, initiated when FI-102 exceeds 500 gpm.

A minimum runtime of 30 minutes is enforced for the active pump to prevent hunting. Both pumps will operate concurrently when the flow rate, as measured by FI-102, exceeds 700 gpm, with P-102B starting automatically regardless of the operating mode.


### 5.2) Interlocks and Permissives

Pumps P-102A and P-102B will only start if the suction pressure at V-104, as measured by PI-102, is greater than 15 psig. The discharge valve associated with the pump must be fully open, as confirmed by limit switches, before the pump is energized. Additionally, the high-level permissive from V-104, provided by LIC-102, ensures the pump will not start if the liquid level in the accumulator falls below 20%.

During switchover, the failed pump is isolated by closing its associated discharge valve, and the standby pump is started after a 5-second delay. The switchover sequence bypasses the suction pressure interlock for 10 seconds to ensure the standby pump can establish flow. The system prevents simultaneous starting of both pumps unless FI-102 exceeds 700 gpm, in which case the interlock is overridden.


### 5.3) Alarm and Fault Handling

A low-pressure alarm (PI-102 < 25 psig for 5 seconds) triggers an alert to the operator, indicating potential pump failure. If the pressure remains low for 10 seconds, the system initiates switchover to the standby pump. A motor fault alarm is generated if the motor current exceeds 150% of the rated value, as detected by the motor protection relay.

If both pumps fail to start or maintain discharge pressure, a high-priority alarm is triggered, and the control valve LCV-102 is closed to prevent backflow. An operator acknowledgment is required to reset the alarm and re-enable the pumps. All alarms are logged in the distributed control system (DCS) for maintenance and troubleshooting purposes.


## 6 **Bottoms Product Handling**
|Tagname | Type | Description |
|---------|------|-------------|
|FT-105 | Flow Transmitter | Measures column feed flow rate for ratio control loop |
|FT-106 | Flow Transmitter | Measures bottoms product flow rate for ratio control loop |
|FV-101 | Flow Valve | Modulates to control bottoms product flow rate |
|IIC-104 | Ratio Controller | Calculates setpoint for bottoms flow based on feed flow and ratio setpoint |
|LIC-002 | Level Controller | Maintains column bottoms level and interlocks with ratio control loop |


### 6.1) Control Strategy Description

The bottoms product handling section employs ratio control to maintain a precise proportional relationship between the toluene-rich bottoms flow rate and the column feed flow rate. Flow transmitter FT-106 measures the bottoms product flow rate, while flow transmitter FT-105 measures the column feed flow rate, which serves as the wild flow for the ratio control loop. The ratio controller IIC-104 calculates the setpoint for the controlled flow (FT-106) based on the measured feed flow (FT-105) and a configurable ratio setpoint.

The ratio setpoint is maintained at 1.5:1, ensuring that the bottoms flow rate is 1.5 times the feed flow rate. The ratio controller output is used as the setpoint for flow controller FV-101, which modulates the control valve to maintain the desired bottoms flow rate. The ratio control equation is defined as:

\[ SP_{FT-106} = FT-105 \times 1.5 \]

The ratio controller IIC-104 includes a manual adjustment feature, allowing operators to modify the ratio setpoint within a range of 1.2:1 to 1.8:1. Low flow cutoff logic is implemented to disable the ratio control loop when FT-105 measures a flow below 50 kg/hr, preventing instability during low feed conditions. The flow measurement ranges for FT-105 and FT-106 are 0-1000 kg/hr.


### 6.2) Interlocks and Permissives

The ratio control loop is interlocked with the column level controller (LIC-002) to ensure safe operation. If the column bottoms level, as measured by LIC-002, falls below 10%, the ratio control loop is disabled, and FV-101 is set to a fail-safe position to prevent damage to downstream equipment. Additionally, the ratio control loop is only active when both FT-105 and FT-106 are operational and providing valid signals.

A permissive is included to ensure that the ratio control loop cannot be activated unless the column feed pump and bottoms pump are running. The status of the pumps is monitored via discrete inputs, and the ratio control loop is inhibited if either pump is offline.


### 6.3) Alarm and Fault Handling

An alarm is triggered if the ratio setpoint deviates beyond the configured limits of 1.2:1 to 1.8:1. The alarm is displayed on the operator interface with the tagname IIC-104-ALM. Additionally, a low flow alarm (FT-105-LAL) is activated if the column feed flow rate falls below 50 kg/hr, indicating that the ratio control loop is no longer in operation.

In the event of a fault in FT-105 or FT-106, the ratio controller IIC-104 switches to manual mode, and FV-101 is set to maintain a fixed position based on the last valid flow measurement. Fault conditions are indicated by diagnostic alarms FT-105-FAH and FT-106-FAH, which alert operators to investigate and resolve the issue promptly.

---


## Document Information

*This document was automatically generated using AI.*

Generation Statistics:

- Total Sections: 6

- Total Tagnames: 41

- Word Count: 3189
