#!/usr/bin/env python3
"""
IoT Sensor Simulator — Pure Python
Simulates TMP36 + LDR + PIR sensor behaviour and LED responses
without any hardware or Tinkercad dependency.

Usage:  python3 simulate.py
        python3 simulate.py --scenario heatwave
        python3 simulate.py --scenario night_intruder
"""

import time
import random
import argparse
import math

# ── ANSI colour helpers ──────────────────────────────────────────
RED    = "\033[91m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def led(state: bool, colour: str, label: str) -> str:
    return f"{colour}{'◉' if state else '○'} {label}{RESET}"

# ── Sensor Models ────────────────────────────────────────────────
class TMP36:
    """Simulates TMP36 temperature sensor with realistic drift."""
    def __init__(self, base_temp=24.0):
        self.temp = base_temp

    def read(self, scenario="normal") -> float:
        if scenario == "heatwave":
            self.temp += random.uniform(0.2, 0.8)
            self.temp = min(self.temp, 45.0)
        elif scenario == "cooling":
            self.temp -= random.uniform(0.1, 0.5)
            self.temp = max(self.temp, 18.0)
        else:
            self.temp += random.uniform(-0.3, 0.3)
            self.temp = max(15.0, min(self.temp, 40.0))
        return round(self.temp, 1)

    def to_adc(self) -> int:
        voltage = (self.temp / 100.0) + 0.5
        return int(voltage * 1023 / 5.0)


class LDR:
    """Simulates LDR (light dependent resistor) via voltage divider."""
    def __init__(self, base_adc=600):
        self.adc = base_adc

    def read(self, scenario="normal") -> int:
        if scenario in ("night_intruder", "night"):
            target = random.randint(50, 250)
        elif scenario == "bright":
            target = random.randint(700, 1023)
        else:
            # Sinusoidal day/night cycle
            t   = time.time()
            mid = 512
            amp = 400
            self.adc = int(mid + amp * math.sin(t / 30.0))
        self.adc = max(0, min(1023, self.adc))
        return self.adc


class PIR:
    """Simulates PIR HC-SR501 motion sensor with hold-time."""
    def __init__(self, hold_time=3.0):
        self.hold_time      = hold_time
        self.motion_until   = 0.0
        self.trigger_chance = 0.08   # 8 % chance per poll

    def read(self, scenario="normal") -> bool:
        now = time.time()
        if scenario == "night_intruder":
            self.trigger_chance = 0.4
        else:
            self.trigger_chance = 0.08
        if random.random() < self.trigger_chance:
            self.motion_until = now + self.hold_time
        return now < self.motion_until


# ── Arduino Logic (mirrored from sketch.ino) ────────────────────
TEMP_THRESHOLD = 30.0
LDR_THRESHOLD  = 300

def control_leds(temp: float, ldr: int, motion: bool):
    return temp > TEMP_THRESHOLD, ldr < LDR_THRESHOLD, motion


# ── Main Simulation Loop ─────────────────────────────────────────
def run(scenario: str, cycles: int):
    tmp = TMP36(base_temp=24.0 if scenario != "heatwave" else 27.0)
    ldr = LDR(base_adc=600)
    pir = PIR()

    print(f"\n{BOLD}{'═'*54}{RESET}")
    print(f"{BOLD}  🔌 IoT Sensor Simulator  |  Scenario: {scenario.upper()}{RESET}")
    print(f"{BOLD}{'═'*54}{RESET}")
    print(f"  Thresholds → Temp > {TEMP_THRESHOLD}°C | LDR < {LDR_THRESHOLD} ADC")
    print(f"  Polling    → 500 ms  |  Cycles: {'∞' if cycles == 0 else cycles}\n")

    count = 0
    try:
        while cycles == 0 or count < cycles:
            temp   = tmp.read(scenario)
            light  = ldr.read(scenario)
            motion = pir.read(scenario)

            r_led, b_led, y_led = control_leds(temp, light, motion)

            print(f"  🌡  {temp:5.1f}°C  "
                  f"💡 LDR:{light:4d}  "
                  f"👁 Motion:{'YES' if motion else 'NO '}"
                  f"   {led(r_led, RED, 'RED')}  "
                  f"{led(b_led, BLUE, 'BLUE')}  "
                  f"{led(y_led, YELLOW, 'YEL')}")

            count += 1
            time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n{GREEN}[Simulator stopped]{RESET}  Total cycles: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IoT Sensor Simulator")
    parser.add_argument("--scenario", default="normal",
                        choices=["normal", "heatwave", "cooling", "night_intruder", "bright"],
                        help="Simulation scenario")
    parser.add_argument("--cycles", type=int, default=0,
                        help="Number of cycles to run (0 = infinite)")
    args = parser.parse_args()
    run(args.scenario, args.cycles)
