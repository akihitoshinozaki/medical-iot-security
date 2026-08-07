# Aki — Data, ML, anomaly detection, alert logic

**Owns:** turning traffic into data, learning the normal pattern, building the
detection algorithm, and explaining the alerts.

## Current status

_(Aki — fill this in.)_

## Steps

- [ ] **Step 3 — Traffic to features.** Convert packet logs into model-ready
      numbers: packets per minute, average size, unique destinations,
      time-of-day, etc.
- [ ] **Step 4 — Detect pattern.** Train an anomaly detector on baseline
      traffic. Start simple (statistical thresholds / isolation forest), level
      up to an autoencoder later if there's time.
- [ ] **Step 6 — Detect and test** (with Toma). Run the model against Toma's
      attacks. Measure catch rate and false alarms.
- [ ] **Step 7 — Explain the alert.** Make the system say *why* it flagged
      something ("packet size 3x baseline", "new unknown IP").
- [ ] **Step 8 — Demo dashboard.** Small live view: green when normal, red
      when Toma launches an attack.

## Blocked on

_(Aki — what do you need from Jun or Toma?)_

## Open decision — needed by Jun

Jun is blocked on two things before the device simulator can be built:

- **Protocol:** HTTP POST or MQTT?
- **Destination:** what's the receiving server / endpoint the device sends to?

Once decided, it goes in [`device/README.md`](../../device/README.md) as the
shared traffic contract.

## Log

_(Dated entries as things get done.)_
