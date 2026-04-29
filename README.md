# Smart Plant Monitoring System

A Raspberry Pi Pico W reads soil moisture every 4 hours, logs the reading to a Firebase Realtime Database, and runs a small water pump for a fixed dose whenever the soil is too dry.

---

## Present requirements (scope of this repo)

- Pico W is mains-powered (USB).
- Every 4 hours:
  1. Read the analog soil moisture sensor.
  2. Connect WiFi (if not already) and push the reading to Firebase RTDB at `<pi_name>/<timestamp>` with the value.
  3. If the reading is below a configurable dryness threshold, switch a relay to run the pump for a fixed number of seconds (= one "dose").
- Loop forever, surviving WiFi/network errors without crashing.

## Future-proofing (not implemented, but the design accommodates them)

- **Grow lamp** via Shelly Gen 1 mini — controlled over LAN HTTP, just another actuator module alongside `pump.py`.
- **Ambient light sensor** — extra ADC channel; a second sensor module that runs in the same 4h cycle.
- **Reservoir water-level sensor** — float switch on a free GPIO, read in the same cycle, refuse to pump if empty.

The code is organized so each new sensor or actuator is a small new module + a few lines in `main.py` and `config.py`. No central rewrite needed.

---

## Hardware

From your order:

| Part | Role |
|------|------|
| Raspberry Pi Pico W | Microcontroller |
| Grove Soil Moisture Sensor (resistive, analog) | Moisture reading |
| Breadboard 400 tie points | Prototyping |
| Jumper wires M/M and F/F | Connections |
| Soldering kit + tin + holder | If permanent later |

From the Amazon kit (RUNCCI-YUN B088T64ZT2):

| Part | Used? | Role |
|------|-------|------|
| 5 V mini submersible pump (~1.67 L/min) | yes | Moves water |
| 4-channel 5 V relay module | yes — channel 1 only | Switches the pump from a GPIO |
| 50 cm silicone tubing | yes | Pump → plant |
| USB-to-bare-wire cable | yes | Feeds 5 V to the relay/pump rail from a USB adapter |
| YL-69 / HL-69 soil sensor + comparator board | not used | Backup if the Grove sensor fails — has both analog (AO) and digital (DO) outputs |
| 2×AA battery holder | not used | Insufficient for the relay coil and pump |

**Pump constraints from the manufacturer:**
- Never run the pump dry — it overheats fast. Always submerge it before powering on.
- Flow is ~28 mL/s, so doses are short. Default `PUMP_DOSE_SECONDS = 2` (≈ 50 mL) — calibrate for your plant.

**Power:** Pico W from USB (your computer or a wall adapter). The relay module + pump get 5 V from the kit's USB cable plugged into a separate USB adapter. Tie all grounds together with the Pico's GND. Don't power the pump from the Pico's VBUS — pump inrush can brown out the Pico.

---

## Wiring (quick reference)

Detailed pinout & diagram: [docs/wiring.md](docs/wiring.md).

| Wire | From | To Pico W (physical pin) | GPIO |
|------|------|--------------------------|------|
| Sensor power | Moisture VCC (red) | Pin 36 | 3V3(OUT) |
| Sensor ground | Moisture GND (black) | Pin 38 or 33 | GND |
| Sensor signal | Moisture SIG (yellow) | Pin 31 | GP26 / ADC0 |
| Relay power | Relay VCC | Pin 40 | VBUS (5 V) |
| Relay ground | Relay GND | Pin 23 | GND |
| Relay signal | Relay IN | Pin 20 | GP15 |
| Pump (+) | Pump red | Relay COM | — |
| Pump (–) | Pump black | External 5 V GND | — |
| Pump supply (+) | External 5 V + | Relay NO | — |

Common ground between Pico, relay, and pump supply is mandatory.

---

## Setup

1. **Flash MicroPython** on the Pico W
   - Hold BOOTSEL, plug in USB → it mounts as `RPI-RP2`.
   - Drop the latest Pico W MicroPython UF2 onto it (https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

2. **Install Thonny** (or `mpremote`) to talk to the board.

3. **Firebase project**
   - Firebase console → new project → enable **Realtime Database** (pick a region near you, e.g. `europe-west1`).
   - Copy the database URL.
   - For the simplest auth path on a microcontroller, use a **database secret** (Project settings → Service accounts → Database secrets). Paste the secret as `FIREBASE_AUTH`.
   - Recommended starting rules (locks down reads, allows authed writes):
     ```json
     { "rules": { ".read": false, ".write": "auth != null" } }
     ```

4. **Configure secrets**
   ```
   cp src/secrets_example.py src/secrets.py
   # edit src/secrets.py with your WiFi + Firebase values
   ```

5. **Upload code to the Pico**
   - Copy every file in `src/` to the root of the Pico filesystem (Thonny → "Save copy → Raspberry Pi Pico").
   - `main.py` runs automatically on boot.

6. **Tune thresholds** — see validation step 1 below.

---

## Validation

Detailed runbook: [docs/validation.md](docs/validation.md). Short version:

1. **Sensor sanity** — temporarily set `READ_INTERVAL_SECONDS = 5` and comment out the Firebase + pump calls in `main.py`. Watch values: dry sensor in air vs. dipped in a glass of water. Pick `MOISTURE_DRY_THRESHOLD` halfway between dry-soil and wet-soil readings (not air vs. water — soil values are narrower).
2. **Relay + pump bench test** — uncomment pump call only; put pump in a cup of water with the outlet aimed at another cup. Confirm relay clicks and water moves. Measure how many mL come out per second to set `PUMP_DOSE_SECONDS`.
3. **WiFi + Firebase write** — uncomment Firebase calls. Confirm a node appears at `<pi_name>/<timestamp>` in the Firebase console.
4. **End-to-end on a fast cycle** — keep the interval short (e.g. 30 s) and the threshold high enough that the pump fires. Watch a few cycles.
5. **Restore production settings** — `READ_INTERVAL_SECONDS = 4 * 60 * 60`, real threshold, real dose. Plant it.

---

## Repo layout

```
smart-plant-monitoring-system/
├── README.md
├── .gitignore
├── docs/
│   ├── wiring.md
│   └── validation.md
└── src/
    ├── main.py              # entry point + 4h loop
    ├── config.py            # pins, thresholds, intervals
    ├── secrets_example.py   # copy to secrets.py and fill in
    ├── wifi.py              # WiFi connect helper
    ├── firebase_client.py   # RTDB writes + NTP timestamp
    ├── moisture.py          # ADC read with smoothing
    └── pump.py              # relay-driven dose
```
