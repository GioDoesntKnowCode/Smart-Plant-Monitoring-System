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


def collect_readings(duration_s, interval_ms):
    """
    Sample both sensors every interval_ms for duration_s seconds.
    Returns (moisture_avg, light_avg).
    """
    m_samples = []
    l_samples = []
    deadline = time.ticks_add(time.ticks_ms(), duration_s * 1000)

    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        m_samples.append(moisture.read(MOISTURE_PIN))
        l_samples.append(moisture.read(LIGHT_PIN))
        time.sleep_ms(interval_ms)

    m_avg = sum(m_samples) // len(m_samples)
    l_avg = sum(l_samples) // len(l_samples)
    print("samples collected: {}  |  moisture avg: {}  |  light avg: {}".format(
        len(m_samples), m_avg, l_avg))
    return m_avg, l_avg


def cycle():
    wifi.ensure_connected()
    cfg = remote_config.load()

    sample_dur = cfg["sample_duration_s"]
    sample_int = cfg["sample_interval_ms"]
    print("sampling for {}s every {}ms...".format(sample_dur, sample_int))
    m_avg, l_avg = collect_readings(sample_dur, sample_int)

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
