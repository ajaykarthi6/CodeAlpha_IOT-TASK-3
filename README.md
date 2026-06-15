# 🌡️💡👁️ IoT Sensor-LED Simulation
### Arduino UNO · TMP36 · LDR · PIR HC-SR501 · Tinkercad / Proteus

[![Tests](https://github.com/YOUR_USERNAME/iot-led-sensor-sim/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/iot-led-sensor-sim/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Arduino](https://img.shields.io/badge/Arduino-UNO-00979D?logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Tinkercad%20%7C%20Proteus-blue)](https://www.tinkercad.com)

> **A complete, hardware-free IoT simulation** demonstrating threshold-based LED control via three sensor types — all running in Tinkercad or your terminal. Every file is documented, tested, and CI-verified.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Repository Structure](#-repository-structure)
- [System Architecture](#-system-architecture)
- [Sensors & Actuators](#-sensors--actuators)
- [Threshold Logic](#-threshold-logic)
- [Quick Start](#-quick-start)
  - [Option A — Tinkercad (browser, no install)](#option-a--tinkercad-browser-no-install)
  - [Option B — Python Simulator (terminal)](#option-b--python-simulator-terminal)
  - [Option C — Real Hardware](#option-c--real-hardware)
- [Arduino Code](#-arduino-code)
- [Serial Monitor Output](#-serial-monitor-output)
- [Python Tools](#-python-tools)
- [Running Tests](#-running-tests)
- [Key Learnings](#-key-learnings)
- [Possible Extensions](#-possible-extensions)
- [Contributing](#-contributing)

---

## 🔭 Project Overview

This project simulates a **complete IoT sensor-actuator loop** using an Arduino UNO connected to three sensor types. Each sensor triggers a dedicated LED, demonstrating three fundamental IoT design patterns:

| Pattern | Sensor | LED | Trigger |
|---------|--------|-----|---------|
| **Threshold Alert** | TMP36 Temperature | 🔴 Red | temp > 30 °C |
| **Adaptive Automation** | LDR Light | 🔵 Blue | ADC < 300 (dark) |
| **Event-Driven Response** | PIR HC-SR501 Motion | 🟡 Yellow | motion HIGH |

All sensor readings stream to the **Serial Monitor at 9600 baud** every 500 ms for real-time telemetry.

---

## 📁 Repository Structure

```
iot-led-sensor-sim/
│
├── 📂 src/                        # Arduino sketches
│   ├── sketch.ino                 # ★ Core sketch — TMP36 + LDR + PIR → 3 LEDs
│   ├── sketch_extended.ino        # Advanced: multi-threshold + buzzer support
│   └── serial_logger.py           # Real-hardware: logs serial data to CSV
│
├── 📂 simulation/                 # Software-only simulation
│   └── simulate.py                # Pure-Python IoT sensor simulator (5 scenarios)
│
├── 📂 tests/                      # Automated tests
│   └── test_led_logic.py          # 12 unit tests for LED threshold logic
│
├── 📂 diagrams/                   # Circuit documentation
│   └── wiring_diagram.txt         # Full ASCII wiring schematic + pin table
│
├── 📂 docs/                       # Guides & references
│   ├── tinkercad_guide.md         # Step-by-step Tinkercad simulation walkthrough
│   └── sensor_reference.md        # TMP36 / LDR / PIR data tables & formulas
│
├── 📂 .github/workflows/
│   └── test.yml                   # CI: auto-runs tests on every push
│
├── README.md                      # You are here
├── CHANGELOG.md                   # Version history
└── LICENSE                        # MIT
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Arduino UNO                          │
│                                                         │
│  INPUTS                          OUTPUTS                │
│  ───────                         ───────                │
│  TMP36 ──► A0  ─────────────►  D9  ──► 🔴 Red LED     │
│                 Threshold        (heat alert)           │
│                 > 30.0 °C                               │
│                                                         │
│  LDR   ──► A1  ─────────────►  D10 ──► 🔵 Blue LED    │
│                 Threshold        (night mode)           │
│                 < 300 ADC                               │
│                                                         │
│  PIR   ──► D2  ─────────────►  D11 ──► 🟡 Yellow LED  │
│                 Digital          (motion alert)         │
│                 HIGH = motion                           │
│                                                         │
│  Serial Monitor (9600 baud) ◄── all readings / 500 ms  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔩 Sensors & Actuators

### TMP36 — Temperature Sensor (Analog, A0)

```
ADC_raw  = analogRead(A0)              //  0 – 1023
Voltage  = ADC_raw × (5.0 / 1023.0)   //  0 – 5 V
Temp_°C  = (Voltage − 0.5) × 100      //  temperature
```

| Temp | ADC | Red LED |
|------|-----|---------|
| 24 °C | ~563 | OFF |
| **31 °C** | **~737** | **ON** |

### LDR — Light Dependent Resistor (Analog, A1, with 10kΩ divider)

- Bright → high resistance drops → higher ADC  
- Dark   → resistance rises → lower ADC  
- **Threshold: ADC < 300 → Blue LED ON**

### PIR HC-SR501 — Motion Sensor (Digital, D2)

- Detects infrared radiation from warm moving bodies  
- Outputs **HIGH** for adjustable hold-time after motion  
- **HIGH → Yellow LED ON**

---

## ⚙️ Threshold Logic

```cpp
// From sketch.ino
const float TEMP_THRESHOLD = 30.0;   // °C
const int   LDR_THRESHOLD  = 300;    // ADC

digitalWrite(LED_TEMP, tempC        > TEMP_THRESHOLD ? HIGH : LOW);
digitalWrite(LED_LDR,  ldrValue     < LDR_THRESHOLD  ? HIGH : LOW);
digitalWrite(LED_PIR,  motionDetect == HIGH           ? HIGH : LOW);
```

| Scenario | Sensor Value | LED State | Meaning |
|----------|-------------|-----------|---------|
| Room temp = 24 °C | ADC ~563 | 🔴 OFF | Normal |
| Temp rises to 32 °C | ADC ~737 | 🔴 **ON** | Heat alert |
| Bright daylight | ADC ~800 | 🔵 OFF | Sufficient light |
| Dark room | ADC ~150 | 🔵 **ON** | Night mode |
| No movement | LOW (0) | 🟡 OFF | Unoccupied |
| Person detected | HIGH (1) | 🟡 **ON** | Motion alert |

---

## 🚀 Quick Start

### Option A — Tinkercad (browser, no install)

1. Go to [tinkercad.com](https://www.tinkercad.com) → **Circuits → Create new**
2. Place: **Arduino UNO · TMP36 · Photoresistor · 10kΩ resistor · Push button · 3× LEDs · 3× 220Ω resistors**
3. Wire as shown in [`diagrams/wiring_diagram.txt`](diagrams/wiring_diagram.txt)
4. Paste [`src/sketch.ino`](src/sketch.ino) into Code → Text mode
5. Click **Start Simulation** → open **Serial Monitor** (9600 baud)
6. Interact with sensors to trigger LEDs

> Full walkthrough: [`docs/tinkercad_guide.md`](docs/tinkercad_guide.md)

---

### Option B — Python Simulator (terminal)

No Arduino required. Runs entirely in Python.

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/iot-led-sensor-sim.git
cd iot-led-sensor-sim

# Run the default (normal) scenario
python3 simulation/simulate.py

# Available scenarios
python3 simulation/simulate.py --scenario heatwave        # temp climbs past 30°C
python3 simulation/simulate.py --scenario night_intruder  # dark + frequent motion
python3 simulation/simulate.py --scenario cooling         # temp drops
python3 simulation/simulate.py --scenario bright          # full daylight
python3 simulation/simulate.py --scenario normal          # realistic random drift

# Run for N cycles then stop
python3 simulation/simulate.py --scenario heatwave --cycles 20
```

**Sample output:**
```
══════════════════════════════════════════════════════
  🔌 IoT Sensor Simulator  |  Scenario: HEATWAVE
══════════════════════════════════════════════════════
  Thresholds → Temp > 30.0°C | LDR < 300 ADC

  🌡  27.4°C  💡 LDR: 612  👁 Motion:NO    ○ RED  ○ BLUE  ○ YEL
  🌡  28.1°C  💡 LDR: 598  👁 Motion:NO    ○ RED  ○ BLUE  ○ YEL
  🌡  29.6°C  💡 LDR: 574  👁 Motion:YES   ○ RED  ○ BLUE  ◉ YEL
  🌡  30.4°C  💡 LDR: 560  👁 Motion:NO    ◉ RED  ○ BLUE  ○ YEL
  🌡  31.2°C  💡 LDR: 210  👁 Motion:YES   ◉ RED  ◉ BLUE  ◉ YEL
```

---

### Option C — Real Hardware

1. Wire components to Arduino UNO per [`diagrams/wiring_diagram.txt`](diagrams/wiring_diagram.txt)
2. Upload `src/sketch.ino` via Arduino IDE
3. Open Serial Monitor at 9600 baud

**Optional — log to CSV:**
```bash
pip install pyserial
python3 src/serial_logger.py --port /dev/ttyUSB0 --out log.csv
```

---

## 🖥️ Arduino Code

Core sketch — `src/sketch.ino`:

```cpp
const float TEMP_THRESHOLD = 30.0;   // °C
const int   LDR_THRESHOLD  = 300;    // ADC

void loop() {
  // Read sensors
  int   rawADC = analogRead(TEMP_PIN);
  float voltage = rawADC * (5.0 / 1023.0);
  float tempC   = (voltage - 0.5) * 100.0;
  int   ldrValue       = analogRead(LDR_PIN);
  int   motionDetected = digitalRead(PIR_PIN);

  // Control LEDs
  digitalWrite(LED_TEMP, tempC          > TEMP_THRESHOLD ? HIGH : LOW);
  digitalWrite(LED_LDR,  ldrValue       < LDR_THRESHOLD  ? HIGH : LOW);
  digitalWrite(LED_PIR,  motionDetected == HIGH           ? HIGH : LOW);

  // Telemetry
  Serial.print("Temp: "); Serial.print(tempC, 1);
  Serial.print("C | LDR: "); Serial.print(ldrValue);
  Serial.print(" | Motion: "); Serial.println(motionDetected ? "YES" : "NO");

  delay(500);
}
```

Also available: `src/sketch_extended.ino` — adds buzzer, multi-level thresholds, uptime logging, and LED flickering for warning states.

---

## 📡 Serial Monitor Output

```
========================================
  IoT Sensor-LED System — Initialized
  Sensors : TMP36 | LDR | PIR HC-SR501
  Polling interval : 500 ms
========================================
Temp: 24.3C | LDR: 620 | Motion: NO
Temp: 25.1C | LDR: 580 | Motion: NO
Temp: 31.4C | LDR: 570 | Motion: NO    << LED_TEMP ON  (D9  HIGH)
Temp: 31.4C | LDR: 570 | Motion: YES   << LED_PIR  ON  (D11 HIGH)
Temp: 31.4C | LDR: 250 | Motion: YES   << LED_LDR  ON  (D10 HIGH)
Temp: 28.9C | LDR: 250 | Motion: NO    << LED_TEMP OFF, LED_PIR OFF
Temp: 22.0C | LDR: 890 | Motion: NO    << LED_LDR  OFF (bright again)
```

---

## 🐍 Python Tools

| Script | Purpose |
|--------|---------|
| `simulation/simulate.py` | Software sensor simulator — 5 scenarios, no hardware |
| `src/serial_logger.py` | Reads live Arduino serial output → CSV log |
| `tests/test_led_logic.py` | 12 unit tests verifying LED threshold logic |

---

## 🧪 Running Tests

```bash
python3 tests/test_led_logic.py
```

Expected output:
```
🔬 LED Control Logic
──────────────────────────────────────────────────
  ✓ PASS  Normal room:  all LEDs OFF
  ✓ PASS  Temp=31.4°C:  RED LED ON
  ✓ PASS  Temp=31.4°C:  BLUE LED OFF
  ✓ PASS  LDR=150:      BLUE LED ON (dark)
  ✓ PASS  Motion=YES:   YELLOW LED ON
  ✓ PASS  All triggers: all LEDs ON
  ✓ PASS  Exact threshold (=): all OFF
  ✓ PASS  Just above threshold: all ON

🌡  TMP36 Sensor Model
  ✓ PASS  25°C → ADC ≈ 153

📏  Boundary / Edge Cases
  ✓ PASS  Extreme cold + bright:  all OFF
  ✓ PASS  Extreme hot + dark + motion: all ON

──────────────────────────────────────────────────
  Results: 12/12 tests passed — ALL TESTS PASSED ✓
```

Tests also run automatically on every push via **GitHub Actions** (`.github/workflows/test.yml`).

---

## 📚 Key Learnings

| Concept | Implementation |
|---------|----------------|
| Analog-to-digital conversion | TMP36: ADC → Voltage → Celsius formula |
| Voltage divider circuit | LDR + 10kΩ for light level measurement |
| Digital I/O | PIR HIGH/LOW driving LED state directly |
| Threshold-based logic | Ternary `condition ? HIGH : LOW` |
| Serial telemetry | 9600 baud real-time IoT monitoring |
| Simulation fidelity | Tinkercad matches real Arduino behaviour |
| Sensor diversity | Combining analog (A0, A1) + digital (D2) |
| Software simulation | Python mirrors Arduino logic without hardware |

---

## 🔧 Possible Extensions

| Extension | How to Implement |
|-----------|------------------|
| 🔊 Buzzer alert | Add piezo on D8; `tone(8, 1000)` when temp > 35 °C |
| 📺 LCD display | 16×2 I²C LCD to show live sensor values |
| 🌀 Fan/relay | Replace LED with relay module; drive DC fan |
| ☁️ Wi-Fi upload | Swap UNO for ESP8266/ESP32; push data to cloud |
| 📊 Multiple thresholds | Warning + critical levels with different LED colours |
| 📈 Data dashboard | Feed `serial_logger.py` CSV into Grafana or Excel |

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make changes and run `python3 tests/test_led_logic.py`
4. Commit: `git commit -m "Add: your feature"`
5. Push and open a Pull Request

---

## 📜 License

[MIT](LICENSE) — free to use, modify, and distribute.

---

<p align="center">
  <strong>Built for Task 2 — IoT Sensor-Based LED Simulation</strong><br>
  Arduino UNO · TMP36 · LDR · PIR HC-SR501 · Tinkercad / Proteus
</p>
