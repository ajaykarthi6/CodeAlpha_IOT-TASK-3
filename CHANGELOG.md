# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2025-06-15

### Added
- `src/sketch.ino` — core Arduino sketch (TMP36 + LDR + PIR → 3 LEDs)
- `src/sketch_extended.ino` — multi-threshold version with buzzer support
- `src/serial_logger.py` — real-hardware serial data logger to CSV
- `simulation/simulate.py` — pure-Python sensor simulator (5 scenarios)
- `tests/test_led_logic.py` — 12 unit tests for LED threshold logic
- `diagrams/wiring_diagram.txt` — full ASCII wiring schematic
- `docs/tinkercad_guide.md` — step-by-step Tinkercad setup guide
- `docs/sensor_reference.md` — TMP36, LDR, PIR data tables
- `.github/workflows/test.yml` — CI pipeline for automated testing
- `README.md` — comprehensive project documentation

### Tested
- All 12 unit tests passing
- Simulator verified across all 5 scenarios
- CI workflow verified locally
