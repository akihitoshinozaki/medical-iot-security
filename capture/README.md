# Capture — packets to structured data

How raw network traffic (from the [simulator](../device/simulator/) now,
the real ESP32 later) becomes something Aki's feature extraction
([`src/features/`](../src/features/)) can load. Capturing at the packet
level rather than trusting the sender's own JSON logs matters because
Phase B (real hardware) won't hand Aki clean logs either — building the
same pipeline now means Phase B is a source swap, not a rewrite.

## 1. Capture with tcpdump

While the device (simulator or, later, real ESP32) is sending:

```
sudo tcpdump -i any -w capture/session1.pcap host <server-host> and port <port>
```

Testing locally against `local_test_receiver.py`, replace `-i any` with
`-i lo0` (macOS loopback) since traffic to `localhost` doesn't appear on
a regular interface.

## 2. Export pcap -> CSV with tshark

```
tshark -r capture/session1.pcap -T fields \
  -e frame.time_epoch -e ip.src -e ip.dst \
  -e tcp.srcport -e tcp.dstport -e frame.len \
  -E header=y -E separator=, > capture/session1.csv
```

This is the actual "export" step — a small, git-friendly CSV with one row
per packet: timestamp, src/dst, ports, and size. That's the raw material
Step 3 (traffic -> features) works from.

## What's committed, what isn't

`.gitignore` already excludes `*.pcap`/`*.pcapng` and `artifacts/` — raw
captures are bulky and can carry incidental noise, so they stay local (or
shared via Drive if Aki needs the raw file). The exported CSV is small
enough to commit directly if it's a short sample; larger runs go through
the same Drive/shared-folder path as the raw pcap, referenced here rather
than committed.

## Requires

`tcpdump` ships with macOS/Linux. `tshark` comes with Wireshark
(`brew install wireshark` on macOS installs both the GUI and the CLI
tools).
