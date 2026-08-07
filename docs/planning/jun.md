# Jun — Hardware and traffic generation

**Owns:** getting the device running and producing real, capturable network
traffic.

**Target device:** ESP32 + MAX30102 pulse / heart-rate sensor (locked in).

## Current status

In Japan until roughly late August. I don't have the MAX30102 yet — buying it
once I'm back. Rather than sit idle for two weeks and block Aki, I'm splitting
my work in two:

- **Phase A (now):** simulate the device so it emits the same *shape* of
  traffic a real one would, and hand that to Aki so feature extraction and the
  baseline model can start immediately.
- **Phase B (once back):** swap in the real hardware. If Phase A defines the
  traffic contract properly, this should be close to zero rework.

## Phase A — simulated device

- [ ] Agree the **traffic contract** with Aki and write it into
      [`device/README.md`](../../device/README.md): send interval, payload
      shape and size, protocol (HTTP POST vs MQTT), destination.
      *This is the piece that makes simulated and real traffic
      interchangeable — everything else depends on it.*
- [ ] Confirm Aki has a receiving server up, so packets actually cross a
      network and are capturable.
- [ ] Build the simulated device. Trying in this order:
  - [ ] **Wokwi** (wokwi.com) — online ESP32 simulator with a MAX30102 part.
        Firmware written here carries over to real hardware unchanged. Need to
        check whether outbound network calls work on the free tier.
  - [ ] **Fallback: script emulator** in `device/simulator/` — generates
        plausible readings (random walk, 60-100 bpm, with noise) and sends
        them on the contract's interval. Less real, but unblocks Aki with no
        external dependencies.
- [ ] Hand simulated traffic to Aki.

## Phase B — real hardware

- [ ] Buy MAX30102, confirm the ESP32 board still flashes.
- [ ] Wire sensor to ESP32, flash firmware.
- [ ] **Verify real traffic matches the Phase A contract** — interval, payload
      size, destination. If it drifts, Aki's baseline was trained on the wrong
      distribution and needs a retrain.
- [ ] Live capture handoff to Aki (project Step 2) with real packets.

## Blocked on

- **Aki:** HTTP POST or MQTT? Blocks the simulator build.
- **Aki:** where do I send to — what's the receiving server / endpoint?

## Notes for the team

Steps 3 and 4 will be running on *simulated* traffic for about two weeks. That
should be fine for building the pipeline, but we need a re-validation pass on
real traffic in Phase B before we trust any numbers.

## Log

- _2026-08-08_ — Set up this planning folder. Device locked in as ESP32 +
  MAX30102. Waiting on protocol decision before starting the simulator.
