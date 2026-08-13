# Device — ESP32 heart-rate monitor

**Owner:** Jun

Target device for v1: **ESP32 + MAX30102** pulse / heart-rate sensor. Cheap,
easy to get running, and it streams continuously — so we get real
physiological data rather than fake numbers.

## Traffic contract (DRAFT — needs Aki's sign-off)

This is the agreement about what the device puts on the wire. It matters more
than it looks: as long as the simulated device and the real device both honour
it, Aki's feature extraction and baseline model don't care which one is
running, and we can swap hardware in without redoing the pipeline.

| Field | Proposed | Status |
|-------|----------|--------|
| Send interval | 1s | proposed |
| Payload | JSON — `{device_id, timestamp, bpm, spo2}` | proposed |
| Payload size | ~80-120 bytes | follows from the above |
| Protocol | HTTP POST **or** MQTT | **undecided — Aki** |
| Destination | receiving server run by Aki | **undecided — Aki** |

Two open decisions, both Aki's call, and both block building the simulator.
Once settled, this table stops being a draft and becomes the reference.

## Phases

Jun is away from the hardware until roughly late August, so the device comes
up in two stages:

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
   (random walk, 60-100 bpm, with noise) and sends them on the contract's
   interval. Not real firmware, but no external dependencies and it unblocks
   Aki immediately.

**Phase B — real hardware.** MAX30102 wired to the ESP32, real firmware, real
packets. The important check here is that real traffic actually matches the
contract — if the interval or payload size drifts, the baseline model was
trained on the wrong distribution and needs a retrain before any numbers from
it mean anything.

See [docs/planning/jun.md](../docs/planning/jun.md) for current status.
