// ================================================================
// IoT Sensor-Based LED Control — Arduino Sketch
// Simulation Platform : Tinkercad / Proteus
// Sensors            : TMP36 (Temp) | LDR (Light) | PIR HC-SR501 (Motion)
// Author             : Task 2 — IoT Sensor Simulation
// Version            : 1.0.0
// ================================================================

// ── Pin Definitions ─────────────────────────────────────────────
const int TEMP_PIN  = A0;   // TMP36  — analog temperature sensor
const int LDR_PIN   = A1;   // LDR    — analog light sensor
const int PIR_PIN   = 2;    // PIR    — digital motion sensor

const int LED_TEMP  = 9;    // Red    LED — temperature alert
const int LED_LDR   = 10;   // Blue   LED — darkness / night indicator
const int LED_PIR   = 11;   // Yellow LED — motion alert

// ── Threshold Constants ──────────────────────────────────────────
const float TEMP_THRESHOLD = 30.0;   // °C  — trigger RED LED above this
const int   LDR_THRESHOLD  = 300;    // ADC — trigger BLUE LED below this

// ── setup() — runs once on power-on / reset ──────────────────────
void setup() {
  Serial.begin(9600);               // Start serial at 9600 baud

  pinMode(PIR_PIN,  INPUT);         // PIR  as digital input
  pinMode(LED_TEMP, OUTPUT);        // LED pins as outputs
  pinMode(LED_LDR,  OUTPUT);
  pinMode(LED_PIR,  OUTPUT);

  Serial.println("========================================");
  Serial.println("  IoT Sensor-LED System — Initialized  ");
  Serial.println("  Sensors : TMP36 | LDR | PIR HC-SR501 ");
  Serial.println("  Polling interval : 500 ms             ");
  Serial.println("========================================");
}

// ── loop() — runs continuously ───────────────────────────────────
void loop() {

  // 1. READ TEMPERATURE (TMP36 on A0)
  int   rawADC  = analogRead(TEMP_PIN);
  float voltage = rawADC * (5.0 / 1023.0);   // ADC → volts
  float tempC   = (voltage - 0.5) * 100.0;   // TMP36 formula → °C

  // 2. READ LIGHT LEVEL (LDR voltage divider on A1)
  int ldrValue = analogRead(LDR_PIN);         // 0 = dark, 1023 = bright

  // 3. READ PIR MOTION SENSOR (D2)
  int motionDetected = digitalRead(PIR_PIN);  // HIGH = motion present

  // 4. CONTROL LEDs BASED ON THRESHOLDS
  digitalWrite(LED_TEMP, tempC          > TEMP_THRESHOLD ? HIGH : LOW);
  digitalWrite(LED_LDR,  ldrValue       < LDR_THRESHOLD  ? HIGH : LOW);
  digitalWrite(LED_PIR,  motionDetected == HIGH           ? HIGH : LOW);

  // 5. SERIAL MONITOR OUTPUT
  Serial.print("Temp: ");
  Serial.print(tempC, 1);
  Serial.print("C | LDR: ");
  Serial.print(ldrValue);
  Serial.print(" | Motion: ");
  Serial.println(motionDetected ? "YES" : "NO");

  delay(500);   // poll every 500 ms
}
