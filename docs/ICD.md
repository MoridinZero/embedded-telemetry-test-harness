# Interface Control Document (ICD)
## Telemetry Test Harness

**Project:** Embedded Telemetry Test Harness  
**Transport:** UART (ESP32 → Host)  
**Sensor Bus:** I2C (BME280)  
**Status:** Draft

---

## 1. Overview
This document defines the telemetry interface between the ESP32 device and the host PC collector.
Telemetry is transmitted as framed binary packets over UART and is validated using CRC16 and
sequence tracking.

---

## 2. UART Configuration
- **Baud rate:** 115200
- **Data bits:** 8
- **Parity:** None
- **Stop bits:** 1
- **Flow control:** None

---

## 3. Packet Framing
All packets use a fixed framing header and a variable-length payload.

### 3.1 Frame Layout
| Field | Size (bytes) | Description |
|------|--------------:|-------------|
| SOF1 | 1 | Start-of-frame byte 1 (0xAA) |
| SOF2 | 1 | Start-of-frame byte 2 (0x55) |
| LEN  | 1 | Number of bytes from TYPE through end of PAYLOAD |
| TYPE | 1 | Packet type identifier |
| SEQ  | 1 | Sequence number (0–255, wraps) |
| TS_MS | 4 | Timestamp in milliseconds since boot (uint32, little-endian) |
| PAYLOAD | LEN - 6 | Payload bytes (TYPE+SEQ+TS_MS are 6 bytes) |
| CRC16 | 2 | CRC16 over [LEN..end of PAYLOAD] |

### 3.2 CRC
- **Algorithm:** CRC-16/CCITT-FALSE
- **Polynomial:** 0x1021
- **Init:** 0xFFFF
- **XOROut:** 0x0000
- **RefIn/RefOut:** False
- **CRC byte order:** Little-endian (LSB first)
---
## 4. Packet Types

### 4.1 TYPE = 0x01 (Sensor Sample)
Payload fields are scaled integers for deterministic logging.

| Field | Type | Size | Units | Notes |
|------|------|-----:|-------|------|
| temp_c_x100 | int16 | 2 | °C * 100 | Example: 2345 = 23.45°C |
| hum_pct_x100 | uint16 | 2 | %RH * 100 | Example: 5025 = 50.25% |
| press_hpa_x10 | uint16 | 2 | hPa * 10 | Example: 10132 = 1013.2 hPa |

**Total payload size:** 6 bytes

---
### 4.2 Reserved Packet Types
Packet types 0x80-0xFF are reserved for future diagnostic or control messages.

---
## 5. Timing Requirements
- **Nominal sample rate:** 10 Hz (one TYPE 0x01 packet every 100 ms)
- **Allowed jitter:** ±20 ms
- **Stale-data threshold (host):** 1.0 s without a valid packet triggers stale alarm

---

## 6. Error Handling (Host Expectations)
The host collector should:
- Reject frames with invalid SOF or LEN
- Reject frames with CRC mismatch and increment `crc_fail_count`
- Detect missing sequence numbers and increment `drop_count`
- Trigger a stale alarm if no valid packet is received for > 1.0 s

---

## 7. I2C Sensor Interface (BME280)
- **Bus:** I2C
- **SDA:** GPIO21
- **SCL:** GPIO22
- **Address:** 0x76 or 0x77 (board dependent)
- **Update rate:** 10 Hz (aligned with telemetry)

