# Toma — Attack simulation and validation

**Owns:** simulating real attacks and malfunctions against the device, and
checking whether we're actually catching the right threats.

## Current status

_(Toma — fill this in.)_

## Steps

- [ ] **Step 5 — Simulate real attacks and faults.** Run actual techniques
      (replay, man-in-the-middle, injection) or simulate a device malfunction,
      so we get *realistic* abnormal traffic instead of made-up examples.
- [ ] **Step 6 — Detect and test** (with Aki). Validate that what the model
      catches are genuinely the right threats, and that the false alarm rate
      is tolerable.

## Blocked on

_(Toma — what do you need from Jun or Aki?)_

## Notes

The device runs on a simulated source until Jun is back with real hardware
(see [jun.md](jun.md)). Worth thinking about which attacks are meaningful
against a simulated device versus which ones genuinely need the real ESP32 in
the loop — that affects what can start now and what waits.

## Log

_(Dated entries as things get done.)_
