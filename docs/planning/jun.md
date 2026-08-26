# Jun — Hardware and traffic generation

**Owns:** getting the device running and producing real, capturable network
traffic.

**Target device:** ESP32 + MAX30102 pulse / heart-rate sensor (locked in).

## Current status

Back at school. MAX30102 ordered, arriving in a few days. Rather than sit
idle until then, I'm splitting my work in two:

- **Phase A (now):** simulate the device so it emits the same *shape* of
  traffic a real one would, and hand that to Aki so feature extraction and the
  baseline model can start immediately.
- **Phase B (once back):** swap in the real hardware. If Phase A defines the
  traffic contract properly, this should be close to zero rework.

## Phase A — simulated device

- [x] Draft the **traffic contract** in [`device/README.md`](../../device/README.md):
      1s interval, JSON `{device_id, timestamp, bpm, spo2}`, ~80-120 bytes.
      Protocol defaulted to **HTTP POST** rather than waiting on Aki — still
      needs their sign-off, but not a blocker anymore since swapping to MQTT
      later only touches one function.
- [x] Build the simulated device — two paths now exist:
      - **Wokwi** (wokwi.com), in [`device/wokwi/`](../../device/wokwi). Sensor
        is a stub custom chip (not a real MAX30102 register emulation — Wokwi
        has no built-in one), producing a 2-byte IR reading over I2C that dips
        once per simulated heartbeat. ESP32 firmware reads it, estimates BPM,
        prints over Serial. **Still no network leg** — Wokwi's free-tier
        outbound-network question is still open, and is now lower priority
        since the script emulator below already unblocks traffic.
      - **Script emulator**, in [`device/simulator/`](../../device/simulator).
        `simulate_device.py` sends real HTTP POSTs with contract-shaped
        readings; `local_test_receiver.py` is a throwaway endpoint to test
        against. Smoke-tested locally — works end to end.
- [x] Document the **capture/export pipeline** in
      [`capture/README.md`](../../capture/README.md): tcpdump to `.pcap`,
      tshark to a per-packet CSV. Same pipeline Phase B will use, so it's not
      thrown away once real hardware arrives.
- [ ] Confirm Aki has a receiving server up; swap `simulate_device.py --url`
      to point at it instead of the local test receiver.
- [ ] Run a real capture (tcpdump + tshark export) against the emulator and
      hand the CSV to Aki so Steps 3-4 can start.
- [ ] Add Wi-Fi + send-to-server on top of the Wokwi sketch, if it turns out
      the network tier works and it's worth having both paths.

## Phase B — real hardware

- [ ] Buy MAX30102, confirm the ESP32 board still flashes.
- [ ] Wire sensor to ESP32, flash firmware.
- [ ] **Verify real traffic matches the Phase A contract** — interval, payload
      size, destination. If it drifts, Aki's baseline was trained on the wrong
      distribution and needs a retrain.
- [ ] Live capture handoff to Aki (project Step 2) with real packets.

## Blocked on

- **Aki:** confirm HTTP POST (or override to MQTT) — no longer blocking, just
  needs sign-off before calling the contract final.
- **Aki:** where do I send to — what's the receiving server / endpoint? Using
  a local throwaway receiver until this exists.

## Notes for the team

Steps 3 and 4 will be running on *simulated* traffic for about two weeks. That
should be fine for building the pipeline, but we need a re-validation pass on
real traffic in Phase B before we trust any numbers.

## Log

- _2026-08-08_ — Set up this planning folder. Device locked in as ESP32 +
  MAX30102. Waiting on protocol decision before starting the simulator.
- _2026-08-13_ — First Wokwi slice working: simulated MAX30102 (stub chip,
  I2C) -> ESP32 -> Serial. No network yet, that's next once protocol is
  decided. See [`device/wokwi/`](../../device/wokwi).
- _2026-08-26_ — Back at school, MAX30102 ordered (arriving in a few days).
  Prepping while I wait: built the script emulator
  ([`device/simulator/`](../../device/simulator)) so there's real,
  capturable traffic today instead of waiting on Wokwi's network tier or
  the board. Defaulted the protocol to HTTP POST rather than staying
  blocked on Aki. Documented the tcpdump/tshark capture-to-CSV pipeline in
  [`capture/README.md`](../../capture/README.md) — same pipeline Phase B
  reuses. Next: get a real capture running against the emulator and hand
  the CSV to Aki.
