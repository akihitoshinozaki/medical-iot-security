# Script emulator (Phase A fallback)

Phase A's second option from [`device/README.md`](../README.md): a plain
Python script that publishes contract-conformant readings over **real
MQTT** to a real broker. No Wokwi, no physical hardware — the packets it
produces are genuinely real, even though the reading values are
synthetic. This is what makes it useful for testing the
[capture/export pipeline](../../capture/README.md) right now, and it's
what actually gets handed to Aki if Wokwi's network tier doesn't pan out.

## Files

- `simulate_device.py` — the emulated device. Publishes `{device_id,
  timestamp, bpm, spo2}` as JSON to an MQTT topic on a timer.
- `local_test_subscriber.py` — a throwaway local subscriber for testing.
  **Not Aki's real subscriber/backend** — just enough to prove the
  simulator and capture pipeline work before that exists.

## Setup

```
python3 -m venv .venv          # from repo root, if not already done
.venv/bin/pip install -r requirements.txt
brew install mosquitto         # local broker for testing
```

## Try it

```
# terminal 1: local broker
mosquitto -p 1883

# terminal 2: subscriber
.venv/bin/python3 device/simulator/local_test_subscriber.py

# terminal 3: emulated device
.venv/bin/python3 device/simulator/simulate_device.py
```

Once Aki's real broker/topic exist, point `--broker-host`/`--broker-port`/
`--topic` at them instead — nothing else changes.

## Status vs. the traffic contract

Protocol (MQTT) is confirmed by Aki. Broker host/port, topic name, and
auth/TLS are still open — see the table in
[`device/README.md`](../README.md). Defaults here (`localhost:1883`,
`devices/<device_id>/readings`, QoS 1, no auth) are placeholders for local
testing, not the real destination.
