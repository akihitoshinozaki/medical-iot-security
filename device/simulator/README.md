# Script emulator (Phase A fallback)

Phase A's second option from [`device/README.md`](../README.md): a plain
Python script that sends contract-conformant readings over **real HTTP**
to a real server. No Wokwi, no physical hardware, no external Python
dependencies (stdlib only) — the packets it produces are genuinely real,
even though the reading values are synthetic. This is what makes it
useful for testing the [capture/export pipeline](../../capture/README.md)
right now, and it's what actually gets handed to Aki if Wokwi's network
tier doesn't pan out.

## Files

- `simulate_device.py` — the emulated device. Sends `{device_id,
  timestamp, bpm, spo2}` as JSON via HTTP POST on a timer.
- `local_test_receiver.py` — a throwaway local endpoint for testing.
  **Not Aki's real receiving server** — just enough to prove the
  simulator and capture pipeline work before that exists.

## Try it

```
python3 device/simulator/local_test_receiver.py --port 8765
# in another terminal:
python3 device/simulator/simulate_device.py --url http://localhost:8765/ingest
```

Once Aki's real server exists, point `--url` at it instead — nothing else
changes.

## Status vs. the traffic contract

Protocol is HTTP POST here as a **default assumption**, not yet confirmed
by Aki (see the open decision in [`device/README.md`](../README.md)). If
Aki picks MQTT instead, only `send()` in `simulate_device.py` needs to
change — the reading generation and CLI stay the same.
