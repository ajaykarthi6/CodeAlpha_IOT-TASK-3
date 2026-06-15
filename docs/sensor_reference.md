# Sensor Reference Sheet

## TMP36 — Analog Temperature Sensor

| Parameter         | Value          |
|-------------------|----------------|
| Supply voltage    | 2.7 V – 5.5 V |
| Output voltage    | 0.1 V – 2.0 V |
| Temp range        | −40°C to +125°C|
| Scale factor      | 10 mV / °C    |
| Accuracy          | ±2°C typical  |
| Formula           | T(°C) = (Vout − 0.5) × 100 |

### ADC Lookup Table (Arduino 5 V, 10-bit)
| Temp (°C) | Vout (V) | ADC Value |
|-----------|----------|-----------|
| 0         | 0.500    | 102       |
| 10        | 0.600    | 123       |
| 20        | 0.700    | 143       |
| 25        | 0.750    | 153       |
| 30        | 0.800    | 164       |
| 35        | 0.850    | 174       |
| 40        | 0.900    | 184       |
| 50        | 1.000    | 205       |

---

## LDR — Light Dependent Resistor (with 10 kΩ voltage divider)

| Condition    | LDR Resistance | ADC Value (approx) |
|--------------|----------------|--------------------|
| Direct sun   | ~200 Ω         | ~1000              |
| Bright room  | ~5 kΩ          | ~700               |
| Dim room     | ~20 kΩ         | ~400               |
| Dark room    | ~100 kΩ        | ~90                |
| Complete dark| >1 MΩ          | ~5                 |

Threshold used: **ADC < 300 → Dark → BLUE LED ON**

---

## PIR HC-SR501 — Passive Infrared Motion Sensor

| Parameter      | Value                        |
|----------------|------------------------------|
| Supply voltage | 4.5 V – 20 V               |
| Output         | Digital HIGH (3.3 V) / LOW  |
| Detection range| Up to 7 m                   |
| Cone angle     | ~110°                        |
| Hold time      | 0.5 s – 200 s (pot adjust)  |
| Trigger mode   | Repeatable (H) / Single (L) |

Output: **HIGH = motion detected, LOW = no motion**

---

## LED Resistor Calculator

```
R = (Vcc - Vf) / If

Red LED:    Vf ≈ 1.8–2.2 V,  R = (5.0 - 2.0) / 0.015 = 200 Ω → 220 Ω ✓
Blue LED:   Vf ≈ 2.5–3.5 V,  R = (5.0 - 3.0) / 0.015 = 133 Ω → 220 Ω ✓
Yellow LED: Vf ≈ 1.8–2.2 V,  R = (5.0 - 2.0) / 0.015 = 200 Ω → 220 Ω ✓
```
