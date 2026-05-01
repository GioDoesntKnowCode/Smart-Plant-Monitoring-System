# Identifies this device in Firebase. Use a unique name per Pico.
PI_NAME = "pico-plant-tomato-1"

# GPIO numbers (not physical pins).
MOISTURE_PIN = 27        # GP27 / ADC1  (soldered) — signal
MOISTURE_POWER_PIN = 22  # GP22 / pin 29 — powers moisture sensor during reads only
LIGHT_PIN = 26           # GP26 / ADC0  (soldered) — signal
LIGHT_POWER_PIN = 28     # GP28 / pin 34 — powers light sensor during reads only

# Calibrated sensor extremes (from your bench tests).
# 0% = fully dry (air reading), 100% = fully wet (submerged in water).
MOISTURE_DRY_VALUE = 65535   # air reading
MOISTURE_WET_VALUE = 34954   # fully submerged reading

# Grove resistive sensor is INVERTED: higher = drier, lower = wetter.
# Triggers when value > threshold. Set to midpoint between dry/wet soil readings.
MOISTURE_DRY_THRESHOLD = 57000

# Main loop period.
READ_INTERVAL_SECONDS = 4 * 60 * 60  # 4 hours
