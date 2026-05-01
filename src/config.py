# Identifies this device in Firebase. Use a unique name per Pico.
PI_NAME = "pico-plant-tomato-1"

# GPIO numbers (not physical pins).
MOISTURE_PIN = 28  # GP28 / ADC2 — signal
LIGHT_PIN = 26     # GP26 / ADC0 — signal (must be GP26/27/28 for ADC)

# Calibrated sensor extremes (from your bench tests).
# 0% = fully dry (air reading), 100% = fully wet (submerged in water).
MOISTURE_DRY_VALUE = 65535   # air reading
MOISTURE_WET_VALUE = 34954   # fully submerged reading

# Grove resistive sensor is INVERTED: higher = drier, lower = wetter.
# Triggers when value > threshold. Set to midpoint between dry/wet soil readings.
MOISTURE_DRY_THRESHOLD = 57000

# Main loop period.
READ_INTERVAL_SECONDS = 4 * 60 * 60  # 4 hours
