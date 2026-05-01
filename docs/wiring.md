# Wiring

## Pico W pinout reference

```
                            USB
                     ┌──────────┐
             GP0 →  1│          │40  VBUS
             GP1 →  2│          │39  VSYS
              GND   3│          │38  GND ─────────────────── Moisture sensor GND
             GP2 →  4│          │37  3V3 EN
             GP3 →  5│          │36  3V3(OUT) ────┬────────── Moisture sensor VCC
             GP4 →  6│          │35               └────────── Light sensor VCC
             GP5 →  7│          │34
              GND   8│          │33  GND ─────────────────── Light sensor GND
             GP6 →  9│          │32  GP27                    (spare)
             GP7 → 10│          │31  GP26                    (spare)
             GP8 → 11│          │30  RUN
             GP9 → 12│          │29  GP22 ─────────────────── Light sensor SIG
              GND  13│          │28  GP28 / ADC2 ──────────── Moisture sensor SIG
            GP10 → 14│          │27  GP21
            GP11 → 15│          │26  GP20
            GP12 → 16│          │25  GP19
            GP13 → 17│          │24  GP18
              GND  18│          │23  GND                    (spare)
            GP14 → 19│          │22  GP17  (reserved — reservoir level sensor)
            GP15 → 20│          │21  GP16
                     └──────────┘

```

## Connections per device

### Soil moisture sensor (Grove)

| Wire | Pico pin | Label |
|---|---|---|
| VCC (red) | Pin 36 | 3V3(OUT) |
| GND (black) | Pin 38 | GND |
| SIG (yellow) | Pin 34 | GP28 / ADC2 |

---

### Ambient light sensor (SENS1016)

| Wire | Pico pin | Label |
|---|---|---|
| VCC | Pin 36 | 3V3(OUT) |
| GND | Pin 33 | GND |
| AO | Pin 29 | GP22 |

---

### GND pin assignments

| Device | Pico pin |
|---|---|
| Moisture sensor GND | Pin 38 |
| Light sensor GND | Pin 33 |
| Spare | Pins 3, 8, 13, 18, 23, 28 |
