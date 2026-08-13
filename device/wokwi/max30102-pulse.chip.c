// Wokwi Custom Chip - preliminary MAX30102 pulse simulator
//
// This does NOT implement the real MAX30102 register map (FIFO, mode
// config, part ID, etc). It's a minimal stand-in so we can get a pulse
// waveform onto the I2C bus before real hardware is available: on every
// I2C read it returns a 2-byte IR sample that dips once per simulated
// heartbeat, riding on a noisy baseline, at a fixed I2C address (0x57,
// same as the real chip).
//
// Protocol: master does Wire.requestFrom(0x57, 2) and gets back the
// current IR sample, MSB first. Writes are accepted (ACKed) but ignored,
// since there is only one thing this stub can return.
//
// SPDX-License-Identifier: MIT

#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define I2C_ADDRESS 0x57
#define SAMPLE_INTERVAL_US 10000  // 10ms -> 100 Hz, same rate as the real MAX30102 default
#define BASELINE 50000.0
#define PULSE_AMPLITUDE 3000.0
#define PULSE_DECAY 18.0  // higher = sharper, shorter dip per beat
#define NOISE_RANGE 200
#define SIM_BPM 72.0

typedef struct {
  i2c_dev_t i2c;
  timer_t sample_timer;
  uint16_t ir_value;
  uint8_t read_byte_index;
} chip_state_t;

static void update_ir_sample(chip_state_t *chip) {
  double t_ms = get_sim_nanos() / 1e6;
  double period_ms = 60000.0 / SIM_BPM;
  double phase = fmod(t_ms, period_ms) / period_ms;  // 0..1 within the current beat

  double pulse = PULSE_AMPLITUDE * exp(-phase * PULSE_DECAY);
  double noise = (rand() % (2 * NOISE_RANGE + 1)) - NOISE_RANGE;

  double value = BASELINE - pulse + noise;
  if (value < 0) value = 0;
  if (value > 65535) value = 65535;

  chip->ir_value = (uint16_t)value;
}

static void on_sample_timer(void *user_data) {
  update_ir_sample((chip_state_t *)user_data);
}

static bool on_i2c_connect(void *user_data, uint32_t address, bool read) {
  chip_state_t *chip = (chip_state_t *)user_data;
  if (read) {
    chip->read_byte_index = 0;  // restart MSB/LSB sequence for this transaction
  }
  return true;  // ACK
}

static uint8_t on_i2c_read(void *user_data) {
  chip_state_t *chip = (chip_state_t *)user_data;
  uint8_t byte = (chip->read_byte_index == 0)
                     ? (uint8_t)(chip->ir_value >> 8)
                     : (uint8_t)(chip->ir_value & 0xFF);
  if (chip->read_byte_index < 1) {
    chip->read_byte_index++;
  }
  return byte;
}

static bool on_i2c_write(void *user_data, uint8_t data) {
  // Register-select byte would go here if we emulated more than one
  // register. Nothing to do yet - just ACK so the master's transaction
  // completes normally.
  return true;
}

void chip_init(void) {
  chip_state_t *chip = malloc(sizeof(chip_state_t));
  chip->ir_value = (uint16_t)BASELINE;
  chip->read_byte_index = 0;

  srand(42);  // deterministic waveform across runs

  const i2c_config_t i2c_config = {
      .address = I2C_ADDRESS,
      .scl = pin_init("SCL", INPUT_PULLUP),
      .sda = pin_init("SDA", INPUT_PULLUP),
      .connect = on_i2c_connect,
      .read = on_i2c_read,
      .write = on_i2c_write,
      .user_data = chip,
  };
  chip->i2c = i2c_init(&i2c_config);

  const timer_config_t timer_config = {
      .callback = on_sample_timer,
      .user_data = chip,
  };
  chip->sample_timer = timer_init(&timer_config);
  timer_start(chip->sample_timer, SAMPLE_INTERVAL_US, true);

  printf("max30102-pulse: simulating ~%.0f bpm on I2C address 0x%02X\n", SIM_BPM, I2C_ADDRESS);
}
