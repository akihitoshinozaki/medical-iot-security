#!/usr/bin/env python3
"""Script emulator for the ESP32 pulse monitor.

Publishes contract-conformant readings over real MQTT to a real broker, so
the traffic on the wire is genuine (real sockets, real MQTT framing, real
timing) even though the reading values are synthetic. See ../README.md for
the traffic contract and why this exists as a fallback to the Wokwi sim.

Requires paho-mqtt (see ../../requirements.txt) — the repo venv at .venv/
has it installed.

Usage:
    python3 simulate_device.py
    python3 simulate_device.py --broker-host localhost --topic devices/pulse-monitor-01/readings
"""

import argparse
import json
import random
import time

import paho.mqtt.client as mqtt

DEFAULT_BROKER_HOST = "localhost"
DEFAULT_BROKER_PORT = 1883
DEFAULT_TOPIC = "devices/{device_id}/readings"
DEFAULT_QOS = 1
DEFAULT_DEVICE_ID = "pulse-monitor-01"
DEFAULT_INTERVAL_S = 1.0


def next_reading(state):
    # Random walk so bpm/spo2 drift plausibly instead of jumping every tick.
    state["bpm"] = max(50, min(110, state["bpm"] + random.uniform(-1.5, 1.5)))
    state["spo2"] = max(94.0, min(100.0, state["spo2"] + random.uniform(-0.3, 0.3)))
    return {
        "device_id": state["device_id"],
        "timestamp": time.time(),
        "bpm": round(state["bpm"], 1),
        "spo2": round(state["spo2"], 1),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broker-host", default=DEFAULT_BROKER_HOST)
    parser.add_argument("--broker-port", type=int, default=DEFAULT_BROKER_PORT)
    parser.add_argument("--topic", default=None, help="defaults to devices/<device-id>/readings")
    parser.add_argument("--qos", type=int, default=DEFAULT_QOS, choices=[0, 1, 2])
    parser.add_argument("--device-id", default=DEFAULT_DEVICE_ID)
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL_S, help="seconds between sends")
    parser.add_argument("--count", type=int, default=0, help="stop after N sends (0 = run forever)")
    args = parser.parse_args()

    topic = args.topic or DEFAULT_TOPIC.format(device_id=args.device_id)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=args.device_id)
    client.connect(args.broker_host, args.broker_port)
    client.loop_start()

    state = {"device_id": args.device_id, "bpm": 72.0, "spo2": 98.0}
    sent = 0
    print(f"Publishing to {args.broker_host}:{args.broker_port} topic '{topic}' "
          f"(QoS {args.qos}) every {args.interval}s (Ctrl+C to stop)")
    try:
        while args.count == 0 or sent < args.count:
            reading = next_reading(state)
            payload = json.dumps(reading)
            info = client.publish(topic, payload, qos=args.qos)
            info.wait_for_publish(timeout=5)
            print(f"published {reading} -> mid={info.mid} rc={info.rc}")
            sent += 1
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\nStopped after {sent} sends")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
