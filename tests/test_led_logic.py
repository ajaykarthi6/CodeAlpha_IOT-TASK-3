#!/usr/bin/env python3
"""
Unit Tests — IoT Sensor LED Logic
Tests the threshold-based LED control logic mirrored from sketch.ino
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../simulation"))

from simulate import control_leds, TMP36, LDR, PIR

# ── ANSI helpers ─────────────────────────────────────────────────
PASS = "\033[92m✓ PASS\033[0m"
FAIL = "\033[91m✗ FAIL\033[0m"

passed = 0
failed = 0

def check(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  {PASS}  {name}")
        passed += 1
    else:
        print(f"  {FAIL}  {name}  |  expected={expected}  got={got}")
        failed += 1

# ── LED Control Logic Tests ──────────────────────────────────────
print("\n🔬 LED Control Logic")
print("─" * 50)

r, b, y = control_leds(temp=24.0, ldr=620, motion=False)
check("Normal room:  all LEDs OFF",        (r, b, y), (False, False, False))

r, b, y = control_leds(temp=31.4, ldr=570, motion=False)
check("Temp=31.4°C:  RED LED ON",          r,          True)
check("Temp=31.4°C:  BLUE LED OFF",        b,          False)

r, b, y = control_leds(temp=24.0, ldr=150, motion=False)
check("LDR=150:      BLUE LED ON (dark)",  b,          True)
check("LDR=150:      RED LED OFF",         r,          False)

r, b, y = control_leds(temp=24.0, ldr=620, motion=True)
check("Motion=YES:   YELLOW LED ON",       y,          True)

r, b, y = control_leds(temp=35.0, ldr=150, motion=True)
check("All triggers: all LEDs ON",         (r, b, y), (True, True, True))

r, b, y = control_leds(temp=30.0, ldr=300, motion=False)
check("Exact threshold (=): all OFF",      (r, b, y), (False, False, False))

r, b, y = control_leds(temp=30.01, ldr=299, motion=True)
check("Just above threshold: all ON",      (r, b, y), (True, True, True))

# ── TMP36 ADC Conversion Test ────────────────────────────────────
print("\n🌡  TMP36 Sensor Model")
print("─" * 50)
sensor = TMP36(base_temp=25.0)
adc = sensor.to_adc()
expected_adc = int(((25.0 / 100.0) + 0.5) * 1023 / 5.0)
check(f"25°C → ADC ≈ {expected_adc}", adc, expected_adc)

# ── Boundary Checks ──────────────────────────────────────────────
print("\n📏  Boundary / Edge Cases")
print("─" * 50)

r, b, y = control_leds(temp=-10.0, ldr=1023, motion=False)
check("Extreme cold + bright:  all OFF", (r, b, y), (False, False, False))

r, b, y = control_leds(temp=100.0, ldr=0, motion=True)
check("Extreme hot + dark + motion: all ON", (r, b, y), (True, True, True))

# ── Summary ──────────────────────────────────────────────────────
total = passed + failed
print(f"\n{'─'*50}")
print(f"  Results: {passed}/{total} tests passed", end="")
if failed == 0:
    print("  \033[92m— ALL TESTS PASSED ✓\033[0m\n")
    sys.exit(0)
else:
    print(f"  \033[91m— {failed} FAILED ✗\033[0m\n")
    sys.exit(1)
