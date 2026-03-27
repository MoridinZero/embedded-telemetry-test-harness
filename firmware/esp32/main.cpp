#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// ESP32 default I2C pins are often SDA=21, SCL=22
static const int SDA_PIN = 21;
static const int SCL_PIN = 22;

Adafruit_BME280 bme;

uint8_t i2cRead8(uint8_t dev, uint8_t reg) {
  Wire.beginTransmission(dev);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom((int)dev, 1);
  return Wire.available() ? Wire.read() : 0xFF;
}

void setup() {
  Serial.begin(115200);
  delay(500); // give serial a moment to come up (and for monitor to attach)

  Wire.begin(SDA_PIN, SCL_PIN);

  Serial.println("\n--- Telemetry Harness: BME280 Readings ---");

  if (!bme.begin(0x76)) {
    Serial.println("Could not find BME280 at 0x76");
    while (1){
      delay(1000);
    }
  }
  Serial.println("time_s,temperature_c,humidity_pct,pressure_hpa");
}

void loop() {
  unsigned long timeSeconds = millis() / 1000;
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  Serial.print(timeSeconds);
  Serial.print(",");
  Serial.print(temperature, 2);
  Serial.print(",");
  Serial.print(humidity, 2);
  Serial.print(",");
  Serial.println(pressure, 2);

  delay(2000);
}