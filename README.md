# Medical IoT Security

A network-based anomaly detection system for identifying attacks and
malfunctions in connected medical IoT devices.

## Project Goal

Monitor how a medical IoT device communicates over a network, learn its
normal communication pattern, and detect deviations caused by attacks or
malfunctions.

## Architecture

ESP32 Medical Device
        ↓
Network Traffic
        ↓
Packet Capture
        ↓
Feature Extraction
        ↓
Anomaly Detection
        ↓
Alert + Explanation
        ↓
Dashboard

## Team

- Jun — Hardware and traffic generation
- Aki — Data, ML, anomaly detection, alert logic
- Toma — Attack simulation and validation

## Planning

Progress is tracked per person in [docs/planning](docs/planning) — one file
each, edited by its owner.

Internal discussion (concerns, opinions, direction after v1) lives in the team
Google Doc, shared privately between the three of us. This repo is public, so
keep anything sensitive out of it.

## V1

1. ESP32 generates realistic medical-device network traffic
2. Capture normal network traffic
3. Extract traffic features
4. Train baseline anomaly detector
5. Simulate attacks
6. Detect attacks
7. Explain alerts
8. Display results in a simple dashboard