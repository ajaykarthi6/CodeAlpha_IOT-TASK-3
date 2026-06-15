// ================================================================
// IoT Sensor-LED Control — EXTENDED VERSION
// Features: Multi-threshold, Buzzer support, Status LED, Uptime log
// ================================================================

#include <Arduino.h>

// ── Pin Definitions ─────────────────────────────────────────────
const int TEMP_PIN   = A0;
const int LDR_PIN    = A1;
const int PIR_PIN    = 2;
const int LED_TEMP   = 9;
const int LED_LDR    = 10;
const int LED_PIR    = 11;
const int BUZZER_PIN = 8;   // Optional piezo buzzer

// ── Multi-level Thresholds ───────────────────────────────────────
const float TEMP_WARN     = 28.0;   // °C — warning (LED flickers)
const float TEMP_CRITICAL = 35.0;   // °C — critical (buzzer + LED solid)
const int   LDR_DIM       = 500;    // ADC — dim light
const int   LDR_DARK      = 200;    // ADC — full darkness

// ── State Variables ──────────────────────────────────────────────
unsigned long lastPrint  = 0;
unsigned long bootTime   = 0;
int           eventCount = 0;

void setup() {
  Serial.begin(9600);
  bootTime = millis();

  pinMode(PIR_PIN,    INPUT);
  pinMode(LED_TEMP,   OUTPUT);
  pinMode(LED_LDR,    OUTPUT);
  pinMode(LED_PIR,    OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Boot self-test — flash all LEDs once
  digitalWrite(LED_TEMP, HIGH); digitalWrite(LED_LDR, HIGH); digitalWrite(LED_PIR, HIGH);
  delay(400);
  digitalWrite(LED_TEMP, LOW);  digitalWrite(LED_LDR, LOW);  digitalWrite(LED_PIR, LOW);

  Serial.println("╔══════════════════════════════════════╗");
  Serial.println("║  IoT Extended System — ONLINE        ║");
  Serial.println("║  Multi-threshold | Buzzer | Uptime   ║");
  Serial.println("╚══════════════════════════════════════╝");
}

void loop() {
  unsigned long now = millis();

  // ── Sensor Reads ────────────────────────────────────────────
  int   rawADC       = analogRead(TEMP_PIN);
  float voltage      = rawADC * (5.0 / 1023.0);
  float tempC        = (voltage - 0.5) * 100.0;
  int   ldrValue     = analogRead(LDR_PIN);
  bool  motionHigh   = (digitalRead(PIR_PIN) == HIGH);

  // ── Temperature Logic (multi-level) ─────────────────────────
  if (tempC >= TEMP_CRITICAL) {
    digitalWrite(LED_TEMP, HIGH);
    tone(BUZZER_PIN, 1000, 200);          // short beep
  } else if (tempC >= TEMP_WARN) {
    // Flicker the LED for warning
    digitalWrite(LED_TEMP, (now / 250) % 2 == 0 ? HIGH : LOW);
    noTone(BUZZER_PIN);
  } else {
    digitalWrite(LED_TEMP, LOW);
    noTone(BUZZER_PIN);
  }

  // ── Light Logic (two levels) ─────────────────────────────────
  if (ldrValue < LDR_DARK) {
    digitalWrite(LED_LDR, HIGH);         // full night mode
  } else if (ldrValue < LDR_DIM) {
    digitalWrite(LED_LDR, (now / 500) % 2 == 0 ? HIGH : LOW);  // dim flicker
  } else {
    digitalWrite(LED_LDR, LOW);
  }

  // ── Motion Logic ─────────────────────────────────────────────
  if (motionHigh) {
    digitalWrite(LED_PIR, HIGH);
    eventCount++;
  } else {
    digitalWrite(LED_PIR, LOW);
  }

  // ── Serial Output (every 500 ms) ─────────────────────────────
  if (now - lastPrint >= 500) {
    lastPrint = now;
    unsigned long upSec = (now - bootTime) / 1000;
    Serial.print("[");
    Serial.print(upSec);
    Serial.print("s] Temp:");
    Serial.print(tempC, 1);
    Serial.print("C | LDR:");
    Serial.print(ldrValue);
    Serial.print(" | Motion:");
    Serial.print(motionHigh ? "YES" : "NO ");
    Serial.print(" | Events:");
    Serial.println(eventCount);
  }
}
