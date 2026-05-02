import machine
import time

from config import (
    PI_NAME, MOISTURE_PIN, LIGHT_PIN,
    SENSOR_INTERVAL, SAMPLE_DURATION_S, SAMPLE_INTERVAL_MS,
)
import wifi
import firebase_client
import moisture
import remote_config


def collect_readings():
    """
    Sample both sensors every SAMPLE_INTERVAL_MS for SAMPLE_DURATION_S seconds.
    Returns (moisture_avg, light_avg).
    """
    m_samples = []
    l_samples = []
    deadline = time.ticks_add(time.ticks_ms(), SAMPLE_DURATION_S * 1000)

    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        m_samples.append(moisture.read(MOISTURE_PIN))
        l_samples.append(moisture.read(LIGHT_PIN))
        time.sleep_ms(SAMPLE_INTERVAL_MS)

    m_avg = sum(m_samples) // len(m_samples)
    l_avg = sum(l_samples) // len(l_samples)
    print("samples collected: {}  |  moisture avg: {}  |  light avg: {}".format(
        len(m_samples), m_avg, l_avg))
    return m_avg, l_avg


def cycle():
    wifi.ensure_connected()
    cfg = remote_config.load()

    print("sampling for {}s...".format(SAMPLE_DURATION_S))
    m_avg, l_avg = collect_readings()

    m_pct = moisture.to_percent(
        m_avg, cfg["moisture_dry_value"], cfg["moisture_wet_value"]
    )
    print("moisture: {} ({}%)  |  light: {}".format(m_avg, m_pct, l_avg))

    ts = firebase_client.now_iso()
    firebase_client.push_reading(PI_NAME, ts, m_avg, m_pct, l_avg)

    return cfg["sensor_interval"]


def main():
    interval = SENSOR_INTERVAL  # fallback if cycle fails
    try:
        interval = cycle()
    except Exception as e:
        print("cycle error:", e)

    print("deep sleeping for {}s...".format(interval))
    machine.deepsleep(interval * 1000)


main()
