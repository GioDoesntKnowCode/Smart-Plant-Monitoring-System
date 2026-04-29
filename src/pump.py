import time
from machine import Pin

# Flip to False if your relay module is active-low (LED lights when IN is grounded).
ACTIVE_HIGH = True


def dose(pin_num, seconds):
    """Run the pump for `seconds`. Always switches off in `finally`, even on error."""
    pin = Pin(pin_num, Pin.OUT)
    on, off = (1, 0) if ACTIVE_HIGH else (0, 1)
    pin.value(off)
    pin.value(on)
    try:
        time.sleep(seconds)
    finally:
        pin.value(off)
