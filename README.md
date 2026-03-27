# DesertSense Telemetry System

This project demonstrates a real-time telemetry system using an ESP32 and a BME280 environmental sensor. The system collects environmental data and visualizes it through a simple data pipeline.

## Features

- Reads temperature, humidity, and pressure from a BME280 sensor
- Uses I2C communication (ESP32 SDA: GPIO 21, SCL: GPIO 22)
- Outputs formatted data over serial
- Logs data using a Python script
- Stores data in CSV format
- Visualizes data using Google Sheets

## System Overview

BME280 → ESP32 → Serial → Python Logger → CSV → Google Sheets Chart

## Repository Structure

- `firmware/` → ESP32 code for reading sensor data
- `collector/` → Python script for logging serial data
- `data/` → Sample CSV output
- `analysis/` → Data visualization or processing (optional)
- `docs/` → System diagrams and documentation

## Getting Started

1. Connect BME280 to ESP32 via I2C  
2. Upload firmware to ESP32  
3. Run Python logger:
   ```bash
   python3 log_sensor_data.py
4.	Open CSV in Google Sheets to generate charts
