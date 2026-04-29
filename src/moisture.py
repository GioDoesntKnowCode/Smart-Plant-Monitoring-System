from machine import ADC, Pin


def read(pin_num, samples=8):
    """Average a few ADC samples to smooth jitter. Returns 0..65535."""
    adc = ADC(Pin(pin_num))
    total = 0
    for _ in range(samples):
        total += adc.read_u16()
    return total // samples


def to_percent(value, dry_value, wet_value):
    """Convert raw ADC value to moisture percentage. Clamped to 0-100."""
    percent = (dry_value - value) / (dry_value - wet_value) * 100
    return max(0, min(100, round(percent)))
