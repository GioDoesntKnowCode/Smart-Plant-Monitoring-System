"""Calibration mode: prints moisture + light readings every 500ms. No WiFi, no Firebase, no pump.

Run this in Thonny (open file, press F5). Stop with Ctrl+C.
"""
import time
import moisture
from config import MOISTURE_PIN, LIGHT_PIN, MOISTURE_DRY_VALUE, MOISTURE_WET_VALUE

while True:
    m_raw = moisture.read(MOISTURE_PIN)
    m_pct = moisture.to_percent(m_raw, MOISTURE_DRY_VALUE, MOISTURE_WET_VALUE)
    l_raw = moisture.read(LIGHT_PIN)

    print("moisture: {} ({}%)  |  light: {}".format(m_raw, m_pct, l_raw))
    time.sleep_ms(500)
