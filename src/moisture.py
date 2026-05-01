from machine import ADC, Pin
import time


def read(sig_pin, power_pin, samples=8):
    """
    Power the sensor, wait for it to settle, take averaged ADC reading, power off.
    Returns 0..65535.
    """
    pwr = Pin(power_pin, Pin.OUT)
    pwr.value(1)
    time.sleep_ms(20)  # settle time before reading

    adc = ADC(Pin(sig_pin))
    total = 0
    for _ in range(samples):
        total += adc.read_u16()

    pwr.value(0)
    return total // samples


def to_percent(value, dry_value, wet_value):
    """Convert raw ADC value to moisture percentage. Clamped to 0-100."""
    percent = (dry_value - value) / (dry_value - wet_value) * 100
    return max(0, min(100, round(percent)))
