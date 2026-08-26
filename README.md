# Medical IoT Security

A network-based anomaly detection system for identifying attacks and
malfunctions in connected medical IoT devices.

## Project Goal

Monitor how a medical IoT device communicates over a network, learn its
normal communication pattern, and detect deviations caused by attacks or
malfunctions.

## Architecture

The team works remotely through a private Tailscale network. Jun's simulated
medical device publishes readings using MQTT to a Mosquitto broker hosted on
Aki's computer. Aki captures and analyzes the traffic, while Toma uses the
same authorized lab network to generate controlled attack traffic.

```text
Jun's simulated device (ESP32 later)
        |
        | MQTT readings
        v
Private Tailscale network
        |
        v
Aki's computer
  Mosquitto MQTT broker (port 1883)
        |
        v
Packet/message capture
        |
        v
Feature extraction -> Anomaly detection -> Alert + explanation -> Dashboard

Toma's attack simulator
        |
        | authorized replay/injection tests
        v
Private Tailscale network -> Aki's MQTT broker
```

The broker is bound to Aki's private Tailscale address and requires separate
MQTT credentials for Aki, Jun, and Toma. It is not exposed through public
router port forwarding. All testing uses synthetic data and team-owned systems.

## Team

- Jun — Hardware and traffic generation
- Aki — Data, ML, anomaly detection, alert logic
- Toma — Attack simulation and validation

## V1

1. ESP32 generates realistic medical-device network traffic
2. Capture normal network traffic
3. Extract traffic features
4. Train baseline anomaly detector
5. Simulate attacks
6. Detect attacks
7. Explain alerts
8. Display results in a simple dashboard
