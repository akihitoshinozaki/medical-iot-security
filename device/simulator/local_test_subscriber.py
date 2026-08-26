#!/usr/bin/env python3
"""Throwaway local subscriber for testing the simulator + capture pipeline.

This is NOT Aki's real subscriber/backend - it's a stand-in so the traffic
contract, simulator, and capture/export pipeline can be exercised
end-to-end against a local broker before Aki's real broker/topic exist.

Requires a local MQTT broker running (e.g. `brew install mosquitto` then
`mosquitto -p 1883`) and paho-mqtt (in ../../requirements.txt).

Usage:
    python3 local_test_subscriber.py
    python3 local_test_subscriber.py --topic 'devices/#'
"""

import argparse
import json

import paho.mqtt.client as mqtt

DEFAULT_BROKER_HOST = "localhost"
DEFAULT_BROKER_PORT = 1883
DEFAULT_TOPIC = "devices/#"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"connected (rc={reason_code}), subscribing to '{userdata['topic']}'")
    client.subscribe(userdata["topic"])


def on_message(client, userdata, msg):
    try:
        reading = json.loads(msg.payload)
        print(f"[{msg.topic}] received {reading}")
    except json.JSONDecodeError:
        print(f"[{msg.topic}] received non-JSON payload ({len(msg.payload)} bytes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broker-host", default=DEFAULT_BROKER_HOST)
    parser.add_argument("--broker-port", type=int, default=DEFAULT_BROKER_PORT)
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="MQTT topic filter to subscribe to")
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata={"topic": args.topic})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.broker_host, args.broker_port)

    print(f"Listening on {args.broker_host}:{args.broker_port} (Ctrl+C to stop)")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nStopped")
        client.disconnect()


if __name__ == "__main__":
    main()
