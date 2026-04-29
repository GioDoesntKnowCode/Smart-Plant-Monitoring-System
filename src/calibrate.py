"""Calibration mode: prints moisture readings every 5 s. No WiFi, no Firebase, no pump.

Run this in Thonny (open file, press F5). Stop with Ctrl+C.
"""
import time
import moisture
from config import MOISTURE_PIN

while True:
    value = moisture.read(MOISTURE_PIN)
    print("moisture:", value)
    time.sleep(5)
