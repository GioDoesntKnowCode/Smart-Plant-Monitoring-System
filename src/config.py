# Identifies this device in Firebase. Use a unique name per Pico.
PI_NAME = "pico-plant-tomato-1"

# GPIO numbers (not physical pins).
MOISTURE_PIN = 27        # GP27 / ADC1  (soldered) — signal
MOISTURE_POWER_PIN = 22  # GP22 / pin 29 — powers moisture sensor during reads only
LIGHT_PIN = 26           # GP26 / ADC0  (soldered) — signal
LIGHT_POWER_PIN = 28     # GP28 / pin 34 — powers light sensor during reads only
PUMP_PIN = 15            # GP15

# Calibrated sensor extremes (from your bench tests).
# 0% = fully dry (air reading), 100% = fully wet (submerged in water).
MOISTURE_DRY_VALUE = 65535   # air reading
MOISTURE_WET_VALUE = 34954   # fully submerged reading

# `moisture.read()` returns a 16-bit value (0..65535).
# Grove resistive sensor is INVERTED: higher = drier, lower = wetter.
# Pump triggers when value > this threshold (too dry).
# Calibrate: fully submerged in water ~32419, dry air ~65535.
# Set to midpoint between dry-soil and wet-soil readings.
MOISTURE_DRY_THRESHOLD = 57000

# How long to run the pump per "dose". Calibrate by measuring mL/s.
# Kit pump is rated ~1.67 L/min ≈ 28 mL/s, so 2 s ≈ 56 mL — adjust for your plant.
# Never test for more than ~1 s with the pump in air; it must not run dry.
PUMP_DOSE_SECONDS = 2

# Main loop period.
READ_INTERVAL_SECONDS = 4 * 60 * 60  # 4 hours
