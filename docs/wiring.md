# Wiring

## Pico W pinout reference

```
                            USB
                     ┌──────────┐
             GP0 →  1│          │40  VBUS ────────────────── Relay VCC
             GP1 →  2│          │39  VSYS
              GND   3│          │38  GND ─────────────────── Moisture sensor GND
             GP2 →  4│          │37  3V3 EN
             GP3 →  5│          │36  3V3(OUT) ────┬────────── Moisture sensor VCC
             GP4 →  6│          │35               └────────── Light sensor VCC
             GP5 →  7│          │34
              GND   8│          │33  GND ─────────────────── Light sensor GND
             GP6 →  9│          │32  GP27 / ADC1 ──────────── Moisture sensor SIG
             GP7 → 10│          │31  GP26 / ADC0 ──────────── Light sensor SIG
             GP8 → 11│          │30  RUN
             GP9 → 12│          │29  GP22
              GND  13│          │28  GND ─────────────────── Pump supply GND
            GP10 → 14│          │27  GP21
            GP11 → 15│          │26  GP20
            GP12 → 16│          │25  GP19
            GP13 → 17│          │24  GP18
              GND  18│          │23  GND ─────────────────── Relay GND
            GP14 → 19│          │22  GP17  (reserved — reservoir level)
            GP15 → 20│●        ●│21  GP16
                     └──────────┘
                       Relay IN1
```

## Connections per device

### Soil moisture sensor (Grove)

| Wire | Pico pin | Label |
|---|---|---|
| VCC (red) | Pin 36 | 3V3(OUT) |
| GND (black) | Pin 38 | GND |
| SIG (yellow) | Pin 32 | GP27 / ADC1 |

---

### Ambient light sensor (SENS1016)

| Wire | Pico pin | Label |
|---|---|---|
| VCC | Pin 36 | 3V3(OUT) |
| GND | Pin 33 | GND |
| AO | Pin 31 | GP26 / ADC0 |

---

### Relay module (4-channel, logic side)

| Wire | Pico pin | Label |
|---|---|---|
| VCC | Pin 40 | VBUS (5 V) |
| GND | Pin 23 | GND |
| IN1 | Pin 20 | GP15 |

---

### Pump (load side via relay)

```
  Separate USB adapter
  ┌─────────────┐
  │  5 V (+)  ──┼──► Relay COM (channel 1)
  │             │         │
  │             │    Relay NO ──► Pump (+) red wire
  │             │
  │  GND (–)  ──┼──► Pump (–) black wire
  │             │         │
  └─────────────┘         └──► Pico pin 28 (GND)  ← ties grounds together
```

> ⚠️ The pump GND and Pico GND must be connected together. Pin 28 is used for this.
> Do NOT power the pump from the Pico's VBUS — pump inrush can brown out the Pico.

---

### GND pin assignments summary

| Device | Pico pin | 
|---|---|
| Moisture sensor GND | Pin 38 |
| Light sensor GND | Pin 33 |
| Pump supply GND | Pin 28 |
| Relay GND | Pin 23 |
| Spare | Pins 3, 8, 13, 18 |

### 3V3 note

Both sensors share **pin 36** (3V3 OUT) for VCC. This is fine — the Pico's 3V3 regulator can supply up to 300 mA and the two sensors draw only a few mA combined.
