# Wokwi pulse-monitor simulation (preliminary)

A Wokwi simulation of the ESP32 + MAX30102 device, standing in for real
hardware while I'm away from it. This is the first slice of Phase A from
[docs/planning/jun.md](../../docs/planning/jun.md): get *a* pulse reading
flowing from sensor to ESP32, before wiring up the network side.

## What this is (and isn't)

- **Sensor:** `max30102-pulse.chip.c` is a custom Wokwi chip, not a real
  MAX30102 emulation. It doesn't implement the actual register map (FIFO,
  mode config, part ID, etc.) - Wokwi has no built-in MAX30102, and the
  reference project I started from used an empty chip stub that wouldn't
  actually respond on the I2C bus. Instead, this chip answers a simple
  `Wire.requestFrom(0x57, 2)` with a 2-byte IR value that dips once per
  simulated heartbeat (fixed at 72 bpm) on top of a noisy baseline. Good
  enough to exercise the ESP32 side end-to-end; not physiologically
  accurate.
- **ESP32 (`sketch.ino`):** reads that value over I2C at ~100 Hz, runs a
  simple threshold + refractory-period beat detector to estimate BPM, and
  **prints both to Serial** (i.e. over the USB cable / Serial Monitor).
- **No Wi-Fi, no network transmission yet.** That's intentionally out of
  scope for this step - it starts once Aki and I settle the traffic
  contract (interval, payload shape, protocol, destination) documented in
  [device/README.md](../README.md). This step only proves sensor -> ESP32
  -> "somewhere I can see the data."

## Running it in Wokwi

There's no automated way to publish a project directly to wokwi.com from
here, so:

1. Go to [wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32)
   to create a blank ESP32 project.
2. Replace the default `sketch.ino` content with this folder's
   `sketch.ino`.
3. Open the diagram editor, click the code view (`</>` icon) on the
   diagram panel, and replace its contents with this folder's
   `diagram.json`.
4. Click the "+" button in the diagram editor, choose "Custom Chip", name
   it `max30102-pulse`. It will generate a `.chip.json` and `.chip.c` -
   replace both with this folder's `max30102-pulse.chip.json` and
   `max30102-pulse.chip.c`.
5. Run the simulation and open the Serial Monitor - you should see
   `IR=...  BPM=...` lines once per second, with BPM converging toward
   ~72 after a few beats.

If Wokwi's file panel supports drag-and-drop in your browser, you can
likely just drag all four files (`diagram.json`, `sketch.ino`,
`max30102-pulse.chip.json`, `max30102-pulse.chip.c`) onto the project's
file sidebar instead of copy-pasting each one.

## Next steps

- Tune the beat detector / waveform if the BPM estimate looks noisy in
  practice (thresholds are constants at the top of `sketch.ino` and
  `max30102-pulse.chip.c`).
- Once the traffic contract is settled, add the Wi-Fi + send-to-server
  step on top of this (Phase A network step), still simulated.
- Phase B: same firmware structure, but reading a real MAX30102 over real
  I2C instead of this stub, once I'm back with hardware.
