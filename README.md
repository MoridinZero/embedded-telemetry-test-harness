# Telemetry Test Harness

This project implements a real-time telemetry and instrumentation harness using an ESP32
and I2C sensors. The system captures sensor data, transmits framed telemetry over UART,
logs and monitors the data on a host PC, and verifies communication using a logic analyzer.

## Features
- I2C sensor data acquisition (BME280)
- Framed binary telemetry with sequence numbers and CRC
- Real-time monitoring and logging via Python
- Interface documentation (ICD) and test plan
- Logic analyzer verification of I2C and UART traffic

## Status
Hardware acquisition and bring-up in progress.
