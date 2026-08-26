// Preliminary pulse-monitor firmware.
//
// Scope for this step: MAX30102 (simulated) -> ESP32 over I2C -> ESP32
// prints IR reading + estimated BPM over Serial (USB cable). No Wi-Fi /
// network transmission yet - that comes once the traffic contract
// (interval, payload, protocol, destination) is settled with Aki. See
// device/README.md.

#include <Wire.h>

#define MAX30102_ADDR 0x57
#define SDA_PIN 21
#define SCL_PIN 22

const uint32_t SAMPLE_INTERVAL_MS = 10;     // matches the sensor's ~100 Hz sim rate
const uint16_t BEAT_DIP_THRESHOLD = 300;    // how far below baseline counts as a beat
const uint32_t MIN_BEAT_INTERVAL_MS = 300;  // refractory period, caps detection at ~200 bpm
const uint32_t PRINT_INTERVAL_MS = 1000;

uint16_t baseline = 50000;
uint32_t lastBeatMs = 0;
uint32_t lastSampleMs = 0;
uint32_t lastPrintMs = 0;
float bpm = 0;

uint16_t readIrSample() {
  Wire.requestFrom(MAX30102_ADDR, 2);
  uint16_t value = 0;
  if (Wire.available() >= 2) {
    value = (uint16_t)(Wire.read()) << 8;
    value |= Wire.read();
  }
  return value;
}

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  delay(200);
  Serial.println("Pulse monitor starting (preliminary - serial only, no network yet)");
}

void loop() {
  uint32_t now = millis();
  if (now - lastSampleMs < SAMPLE_INTERVAL_MS) {
    return;
  }
  lastSampleMs = now;

  uint16_t ir = readIrSample();

  // Slow-moving baseline so we can detect a beat as a dip below "normal".
  baseline = (uint16_t)((baseline * 15UL + ir) / 16);

  if (ir < baseline - BEAT_DIP_THRESHOLD && now - lastBeatMs > MIN_BEAT_INTERVAL_MS) {
    if (lastBeatMs != 0) {
      float instantBpm = 60000.0f / (now - lastBeatMs);
      bpm = (bpm == 0) ? instantBpm : (bpm * 0.7f + instantBpm * 0.3f);
    }
    lastBeatMs = now;
  }

  if (now - lastPrintMs >= PRINT_INTERVAL_MS) {
    lastPrintMs = now;
    Serial.print("IR=");
    Serial.print(ir);
    Serial.print("\tBPM=");
    Serial.println(bpm, 1);
  }
}
