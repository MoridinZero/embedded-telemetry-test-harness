import csv
import os
import sys
from datetime import datetime

import serial


PORT = "/dev/tty.usbserial-10"
BAUD_RATE = 115200
OUTPUT_FILE = "sensor_data.csv"


def main() -> None:
    file_exists = os.path.exists(OUTPUT_FILE)

    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as exc:
        print("Could not open serial port:", exc)
        sys.exit(1)

    print("Connected to", PORT)
    print("Logging to", OUTPUT_FILE)
    print("Press Ctrl+C to stop.\n")

    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists or os.path.getsize(OUTPUT_FILE) == 0:
            writer.writerow([
                "logged_at",
                "time_s",
                "temperature_c",
                "humidity_pct",
                "pressure_hpa"
            ])

        try:
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()

                if not line:
                    continue

                if line.startswith("ERROR:"):
                    print(line)
                    continue

                if line == "time_s,temperature_c,humidity_pct,pressure_hpa":
                    print("Header received from ESP32.")
                    continue

                parts = line.split(",")

                if len(parts) != 4:
                    print("Skipping malformed line:", line)
                    continue

                logged_at = datetime.now().isoformat(timespec="seconds")
                row = [logged_at] + parts

                writer.writerow(row)
                csvfile.flush()

                print("Logged:", row)

        except KeyboardInterrupt:
            print("\nStopped logging.")
        finally:
            ser.close()


if __name__ == "__main__":
    main()