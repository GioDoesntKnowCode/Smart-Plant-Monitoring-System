# Identifies this device in Firebase. Use a unique name per Pico.
PI_NAME = "pico-plant-tomato-1"

# Signal pins — must be GP26/27/28 (only ADC-capable pins on Pico).
MOISTURE_PIN = 27  # GP27 / ADC1 — moisture sensor SIG
LIGHT_PIN = 26     # GP26 / ADC0 — light sensor SIG

# Both sensor VCCs are wired directly to Pin 36 (3V3 OUT) — always on.

# Calibrated sensor extremes (from bench tests).
# 0% = fully dry (air), 100% = fully wet (submerged in water).
MOISTURE_DRY_VALUE = 65535
MOISTURE_WET_VALUE = 34954

# Grove resistive sensor: higher = drier, lower = wetter.
# Pump triggers when value > threshold.
MOISTURE_DRY_THRESHOLD = 57000

# Main loop period.
READ_INTERVAL_SECONDS = 4 * 60 * 60  # 4 hours
