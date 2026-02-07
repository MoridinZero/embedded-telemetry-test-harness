# Test Plan
## Embedded Telemetry Test Harness

**Project:** Embedded Telemetry Test Harness  
**Document Type:** Verification Test Plan  
**Status:** Draft

---

## 1. Purpose
This test plan defines the procedures used to verify correct operation of the
telemetry test harness, including I2C sensor communication, UART telemetry
transmission, data integrity, timing performance, and fault detection.

---

## 2. Test Environment

### 2.1 Hardware
- ESP32-DevKitC-32 (ESP32-WROOM-32)
- BME280 environmental sensor (I2C)
- USB logic analyzer (8-channel, Saleae-compatible)
- Host PC (Linux/Windows/macOS)

### 2.2 Software
- ESP32 firmware (Arduino framework)
- Python-based telemetry collector
- Saleae Logic 2 software

---

## 3. Interfaces Under Test
- I2C bus (ESP32 ↔ BME280)
- UART telemetry stream (ESP32 → host)

---

## 4. Test Cases

### TC-01: I2C Communication Verification
**Objective:** Verify correct I2C communication with the BME280 sensor.

**Procedure:**
1. Connect logic analyzer to SDA and SCL lines.
2. Power the ESP32 and start firmware.
3. Capture I2C traffic during sensor reads.

**Expected Results:**
- Sensor address (0x76 or 0x77) acknowledged.
- No repeated NACK conditions during normal operation.
- Read transactions occur at the expected rate (~10 Hz).

---

### TC-02: Telemetry Frame Structure
**Objective:** Verify correct telemetry framing over UART.

**Procedure:**
1. Capture UART TX line with logic analyzer.
2. Decode byte stream.
3. Inspect frame boundaries and field order.

**Expected Results:**
- SOF bytes (0xAA 0x55) precede each frame.
- LEN field matches payload size.
- TYPE, SEQ, and TS_MS fields are present and ordered correctly.

---

### TC-03: CRC Validation
**Objective:** Verify CRC detection of corrupted frames.

**Procedure:**
1. Introduce intentional CRC corruption in firmware (debug mode).
2. Observe host-side telemetry processing.

**Expected Results:**
- Corrupted frames are rejected.
- CRC failure counter increments.
- No corrupted data is logged as valid.

---

### TC-04: Sequence Drop Detection
**Objective:** Verify detection of dropped telemetry frames.

**Procedure:**
1. Temporarily pause telemetry transmission.
2. Resume normal operation.

**Expected Results:**
- Missing sequence numbers are detected.
- Drop counter increments appropriately.

---

### TC-05: Timing and Stale Data Detection
**Objective:** Verify timing performance and stale-data detection.

**Procedure:**
1. Run telemetry at nominal 10 Hz for ≥30 minutes.
2. Pause telemetry for >1 second.

**Expected Results:**
- Stable packet rate at ~10 Hz.
- Stale-data alarm triggers after >1.0 s without valid packets.

---

## 5. Test Artifacts
The following artifacts will be retained:
- Logic analyzer captures (I2C and UART)
- Telemetry log files (CSV/JSONL)
- Summary statistics and plots

---

## 6. Pass/Fail Criteria
The system is considered passing if all expected results are met without
uncorrected errors or unexplained data loss.

