# Device — ESP32 heart-rate monitor

**Owner:** Jun

Target device for v1: **ESP32 + MAX30102** pulse / heart-rate sensor. Cheap,
easy to get running, and it streams continuously — so we get real
physiological data rather than fake numbers.

## Traffic contract (DRAFT — broker/topic still needed from Aki)

This is the agreement about what the device puts on the wire. It matters more
than it looks: as long as the simulated device and the real device both honour
it, Aki's feature extraction and baseline model don't care which one is
running, and we can swap hardware in without redoing the pipeline.

| Field | Proposed | Status |
|-------|----------|--------|
| Send interval | 1s | proposed |
| Payload | JSON — `{device_id, timestamp, bpm, spo2}` | proposed |
| Payload size | ~80-120 bytes | follows from the above |
| Protocol | **MQTT** | confirmed by Aki |
| Broker | `localhost:1883` (local test broker) for now | **needed — Aki's broker host/port** |
| Topic | `devices/<device_id>/readings`, e.g. `devices/pulse-monitor-01/readings` | **needs Aki's sign-off** |
| QoS | 1 (at-least-once) | proposed default, low-stakes to change |
| Auth / TLS | none (open local broker) | **needed — does Aki's broker require creds or TLS?** |

Once Aki answers broker/topic/auth, only the CLI flags to
[`device/simulator/simulate_device.py`](simulator/simulate_device.py) change
(`--broker-host`, `--broker-port`, `--topic`) — the publish logic itself
doesn't need rework.

## Phases

Jun is back at school and has ordered the MAX30102 (arriving in a few days),
so the device comes up in two stages:

**Phase A — simulated.** Emit contract-conformant traffic without physical
hardware, so Aki isn't blocked for two weeks. Two options, in order of
preference:

1. **Wokwi** (wokwi.com) — online ESP32 simulator with a MAX30102 part. The
   firmware written here transfers to real hardware unchanged, which is why
   it's first choice. Open question: whether outbound network calls work on
   the free tier.
   **Status:** first slice done in [`device/wokwi/`](wokwi) — simulated
   sensor over I2C, ESP32 estimates BPM, prints over Serial. No network leg
   yet; that's added once the protocol/destination below are decided.
2. **Script emulator** (`device/simulator/`) — generates plausible readings
   (random walk, 60-100 bpm, with noise) and publishes them on the
   contract's interval. Not real firmware, but it unblocks Aki immediately.
   **Status:** done — [`device/simulator/simulate_device.py`](simulator/simulate_device.py)
   publishes real MQTT messages (via `paho-mqtt`, see `requirements.txt`);
   [`device/simulator/local_test_subscriber.py`](simulator/local_test_subscriber.py)
   is a throwaway subscriber to test against on a local broker
   (`brew install mosquitto`) until Aki's real broker/topic exist.
   Paired with the [capture/export pipeline](../capture/README.md), this is
   enough to produce and hand off real traffic today, independent of Wokwi's
   network-tier question or the physical board's arrival.

**Phase B — real hardware.** MAX30102 wired to the ESP32, real firmware, real
packets. The important check here is that real traffic actually matches the
contract — if the interval or payload size drifts, the baseline model was
trained on the wrong distribution and needs a retrain before any numbers from
it mean anything.

See [docs/planning/jun.md](../docs/planning/jun.md) for current status.
