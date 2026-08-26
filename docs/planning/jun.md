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
      **Protocol confirmed by Aki: MQTT.** Broker host/port, topic name, and
      auth/TLS still needed from Aki — see the open table in that file.
- [x] Build the simulated device — two paths now exist:
      - **Wokwi** (wokwi.com), in [`device/wokwi/`](../../device/wokwi). Sensor
        is a stub custom chip (not a real MAX30102 register emulation — Wokwi
        has no built-in one), producing a 2-byte IR reading over I2C that dips
        once per simulated heartbeat. ESP32 firmware reads it, estimates BPM,
        prints over Serial. **Still no network leg** — Wokwi's free-tier
        outbound-network question is still open, and is now lower priority
        since the script emulator below already unblocks traffic.
      - **Script emulator**, in [`device/simulator/`](../../device/simulator).
        `simulate_device.py` publishes real MQTT messages (`paho-mqtt`) with
        contract-shaped readings; `local_test_subscriber.py` is a throwaway
        subscriber to test against on a local broker. Smoke-tested against a
        local `mosquitto` broker — works end to end.
- [x] Document the **capture/export pipeline** in
      [`capture/README.md`](../../capture/README.md): tcpdump to `.pcap`,
      tshark to a per-packet CSV (now with MQTT-specific fields: topic,
      msgtype, QoS). Same pipeline Phase B will use, so it's not thrown away
      once real hardware arrives.
- [ ] Get broker host/port, topic name, and auth/TLS from Aki; swap
      `simulate_device.py`'s `--broker-host`/`--broker-port`/`--topic` to
      point at Aki's real broker instead of the local test one.
- [ ] Run a real capture (tcpdump + tshark export) against the emulator and
      hand the CSV to Aki so Steps 3-4 can start.
- [ ] Add Wi-Fi + publish-to-broker on top of the Wokwi sketch, if it turns
      out the network tier works and it's worth having both paths.

## Phase B — real hardware

- [ ] Buy MAX30102, confirm the ESP32 board still flashes.
- [ ] Wire sensor to ESP32, flash firmware.
- [ ] **Verify real traffic matches the Phase A contract** — interval, payload
      size, destination. If it drifts, Aki's baseline was trained on the wrong
      distribution and needs a retrain.
- [ ] Live capture handoff to Aki (project Step 2) with real packets.

## Blocked on

- **Aki:** MQTT broker host/port. Using `localhost:1883` (local test broker)
  until this exists.
- **Aki:** topic name to publish/subscribe to. Using
  `devices/<device_id>/readings` as a proposed default.
- **Aki:** does the broker need auth (username/password) or TLS?

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
  the board. Documented the tcpdump/tshark capture-to-CSV pipeline in
  [`capture/README.md`](../../capture/README.md) — same pipeline Phase B
  reuses. Aki confirmed **MQTT** as the protocol; rewrote the emulator to
  publish over MQTT (`paho-mqtt`), tested end to end against a local
  `mosquitto` broker. Still need broker host/port, topic, and auth/TLS
  from Aki. Next: get those, then get a real capture running against the
  emulator and hand the CSV to Aki.
