#!/usr/bin/env python3
"""
IoT Sensor Serial Logger
Reads live data from Arduino over USB serial and logs to CSV + console.
Usage: python3 serial_logger.py --port /dev/ttyUSB0 --baud 9600
"""

import serial
import csv
import argparse
import time
import re
from datetime import datetime
from pathlib import Path

# ── Argument Parsing ─────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Arduino IoT Serial Logger")
parser.add_argument("--port",  default="/dev/ttyUSB0", help="Serial port (default: /dev/ttyUSB0)")
parser.add_argument("--baud",  type=int, default=9600,  help="Baud rate (default: 9600)")
parser.add_argument("--out",   default="sensor_log.csv", help="Output CSV filename")
parser.add_argument("--duration", type=int, default=0, help="Seconds to log (0 = infinite)")
args = parser.parse_args()

# ── Regex to parse serial output ────────────────────────────────
PATTERN = re.compile(r"Temp:\s*([\d.]+)C\s*\|\s*LDR:\s*(\d+)\s*\|\s*Motion:\s*(YES|NO)")

def parse_line(line: str):
    m = PATTERN.search(line)
    if m:
        return float(m.group(1)), int(m.group(2)), m.group(3) == "YES"
    return None

def led_states(temp, ldr, motion):
    return {
        "RED_LED":    "ON" if temp  > 30.0 else "OFF",
        "BLUE_LED":   "ON" if ldr   < 300  else "OFF",
        "YELLOW_LED": "ON" if motion        else "OFF",
    }

# ── Main Logger ──────────────────────────────────────────────────
def main():
    out_path = Path(args.out)
    print(f"[IoT Logger] Connecting to {args.port} @ {args.baud} baud …")
    print(f"[IoT Logger] Logging to    {out_path}")
    print("─" * 60)

    start = time.time()

    with serial.Serial(args.port, args.baud, timeout=2) as ser, \
         open(out_path, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "temp_c", "ldr_adc", "motion",
                          "RED_LED", "BLUE_LED", "YELLOW_LED"])

        while True:
            if args.duration and (time.time() - start) >= args.duration:
                print("\n[IoT Logger] Duration reached. Stopping.")
                break

            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue

            parsed = parse_line(raw)
            if parsed:
                temp, ldr, motion = parsed
                leds = led_states(temp, ldr, motion)
                ts   = datetime.now().isoformat(timespec="seconds")

                writer.writerow([ts, temp, ldr, "YES" if motion else "NO",
                                  leds["RED_LED"], leds["BLUE_LED"], leds["YELLOW_LED"]])
                csvfile.flush()

                # Pretty console output
                r = "\033[91m█\033[0m" if leds["RED_LED"]    == "ON" else "□"
                b = "\033[94m█\033[0m" if leds["BLUE_LED"]   == "ON" else "□"
                y = "\033[93m█\033[0m" if leds["YELLOW_LED"] == "ON" else "□"
                print(f"{ts}  🌡 {temp:5.1f}°C  💡 LDR:{ldr:4d}  👁 {'YES' if motion else 'NO '}"
                      f"   RED:{r} BLUE:{b} YEL:{y}")

if __name__ == "__main__":
    main()
