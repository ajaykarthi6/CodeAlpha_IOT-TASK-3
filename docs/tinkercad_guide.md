# Tinkercad Simulation Guide

## Prerequisites
- Free account at [tinkercad.com](https://www.tinkercad.com)
- No hardware required

---

## Step-by-Step Setup

### Step 1 — Create Circuit
1. Log in to Tinkercad
2. Click **Circuits** in the left panel
3. Click **Create new Circuit**
4. Rename it: `IoT-Sensor-LED-Control`

### Step 2 — Place Arduino UNO
- Search "Arduino UNO" in the Components panel
- Drag it onto the canvas

### Step 3 — Add TMP36 Temperature Sensor
- Search "TMP36" → drag onto canvas
- Wire connections:
  - **VCC** → Arduino **5V**
  - **GND** → Arduino **GND**
  - **VOUT** → Arduino **A0**

### Step 4 — Add LDR (Photoresistor) + 10kΩ Resistor
- Search "Photoresistor" → drag onto canvas
- Search "Resistor" → set value to **10 kΩ** → drag onto canvas
- Voltage divider wiring:
  - LDR pin 1 → Arduino **5V**
  - LDR pin 2 → junction node → Arduino **A1**
  - 10 kΩ resistor between junction node → Arduino **GND**

### Step 5 — Add PIR Sensor
> Tinkercad doesn't have PIR HC-SR501 natively. Use these alternatives:
- **Option A**: Use a **push-button** on D2 to simulate motion (HIGH when pressed)
- **Option B**: Use Tinkercad's "Ultrasonic Distance Sensor" for proximity trigger
- **Option C**: Use Proteus for authentic PIR simulation

PIR Wiring (if available):
  - **VCC** → Arduino **5V**
  - **GND** → Arduino **GND**
  - **OUT** → Arduino **D2**

### Step 6 — Add Red LED (Temperature Alert)
- Search "LED" → choose **Red**
- Add a **220Ω resistor** in series
- **Anode (+)** through 220Ω → Arduino **D9**
- **Cathode (-)** → Arduino **GND**

### Step 7 — Add Blue LED (Night Light)
- Search "LED" → choose **Blue**
- Add a **220Ω resistor** in series
- **Anode (+)** through 220Ω → Arduino **D10**
- **Cathode (-)** → Arduino **GND**

### Step 8 — Add Yellow LED (Motion Alert)
- Search "LED" → choose **Yellow**
- Add a **220Ω resistor** in series
- **Anode (+)** through 220Ω → Arduino **D11**
- **Cathode (-)** → Arduino **GND**

### Step 9 — Upload the Code
1. Click **Code** in the toolbar
2. Switch to **Text** mode
3. Delete any existing code
4. Paste the full contents of `src/sketch.ino`
5. Click **Done**

### Step 10 — Run the Simulation
1. Click **Start Simulation** (green button)
2. Click the **Serial Monitor** tab (bottom panel)
3. Set baud rate to **9600**
4. You should see: `IoT System Initialized.`

---

## Testing Each Sensor

### Test Temperature (Red LED)
- Click the **TMP36** sensor in the circuit
- Drag the temperature slider **above 30°C**
- ✅ **Red LED turns ON**
- Drag back below 30°C → Red LED turns OFF

### Test Light (Blue LED)
- Click the **Photoresistor**
- Set the light level to a low value (< 300 ADC equivalent)
- ✅ **Blue LED turns ON**
- Increase light → Blue LED turns OFF

### Test Motion (Yellow LED)
- Click the **push-button** on D2 (or PIR trigger)
- Press / hold button
- ✅ **Yellow LED turns ON**
- Release → Yellow LED turns OFF

---

## Expected Serial Monitor Output

```
IoT System Initialized.
Sensors: TMP36 | LDR | PIR
[ 0s] Temp: 24.3C | LDR: 620 | Motion: NO
[ 1s] Temp: 25.1C | LDR: 580 | Motion: NO
[ 2s] Temp: 31.4C | LDR: 570 | Motion: NO    << LED_TEMP ON (D9 HIGH)
[ 3s] Temp: 31.4C | LDR: 570 | Motion: YES   << LED_PIR ON (D11 HIGH)
[ 4s] Temp: 31.4C | LDR: 250 | Motion: YES   << LED_LDR ON (D10 HIGH)
[ 5s] Temp: 28.9C | LDR: 250 | Motion: NO    << LED_TEMP OFF, LED_PIR OFF
[ 6s] Temp: 22.0C | LDR: 890 | Motion: NO    << LED_LDR OFF (bright again)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| LED never turns on | Check anode/cathode orientation; verify resistor value |
| Temperature reading wrong | Confirm VOUT → A0; check TMP36 formula in code |
| LDR not responding | Verify voltage divider: LDR → 5V, 10kΩ → GND, midpoint → A1 |
| Serial Monitor blank | Confirm baud rate = 9600; click Start Simulation first |
| Code errors | Ensure Text mode is selected; paste sketch fresh |
