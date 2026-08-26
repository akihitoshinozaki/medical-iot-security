#!/usr/bin/env python3
"""Script emulator for the ESP32 pulse monitor.

Sends contract-conformant readings over real HTTP to a real server, so the
traffic on the wire is genuine (real sockets, real headers, real timing)
even though the reading values are synthetic. See ../README.md for the
traffic contract and why this exists as a fallback to the Wokwi sim.

Usage:
    python3 simulate_device.py
    python3 simulate_device.py --url http://localhost:8765/ingest --interval 1.0
"""

import argparse
import json
import random
import time
import urllib.error
import urllib.request

DEFAULT_URL = "http://localhost:8765/ingest"
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


def send(url, reading):
    body = json.dumps(reading).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="destination endpoint")
    parser.add_argument("--device-id", default=DEFAULT_DEVICE_ID)
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL_S, help="seconds between sends")
    parser.add_argument("--count", type=int, default=0, help="stop after N sends (0 = run forever)")
    args = parser.parse_args()

    state = {"device_id": args.device_id, "bpm": 72.0, "spo2": 98.0}
    sent = 0
    print(f"Sending to {args.url} every {args.interval}s (Ctrl+C to stop)")
    try:
        while args.count == 0 or sent < args.count:
            reading = next_reading(state)
            try:
                status = send(args.url, reading)
                print(f"sent {reading} -> {status}")
            except urllib.error.URLError as exc:
                print(f"send failed: {exc}")
            sent += 1
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\nStopped after {sent} sends")


if __name__ == "__main__":
    main()
