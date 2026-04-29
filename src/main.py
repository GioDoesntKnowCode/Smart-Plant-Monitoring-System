import time

from config import (
    PI_NAME,
    MOISTURE_PIN,
    MOISTURE_DRY_THRESHOLD,
    MOISTURE_DRY_VALUE,
    MOISTURE_WET_VALUE,
    PUMP_PIN,
    PUMP_DOSE_SECONDS,
    READ_INTERVAL_SECONDS,
)
import wifi
import firebase_client
import moisture
import pump


def cycle():
    value = moisture.read(MOISTURE_PIN)
    percent = moisture.to_percent(value, MOISTURE_DRY_VALUE, MOISTURE_WET_VALUE)
    print("moisture: {} ({}%)".format(value, percent))

    wifi.ensure_connected()
    ts = firebase_client.now_iso()
    firebase_client.push_reading(PI_NAME, ts, value, percent)

    remote = firebase_client.fetch_config(PI_NAME) or {}
    dry_threshold = remote.get("dry_threshold", MOISTURE_DRY_THRESHOLD)
    dose_seconds = remote.get("pump_dose_seconds", PUMP_DOSE_SECONDS)
    print("config: dry_threshold={} dose={}s".format(dry_threshold, dose_seconds))

    if value > dry_threshold:
        print("dry — running pump for", dose_seconds, "s")
        pump.dose(PUMP_PIN, dose_seconds)
        firebase_client.push_event(
            PI_NAME, ts, {"event": "watered", "duration_s": dose_seconds}
        )


def main():
    while True:
        try:
            cycle()
        except Exception as e:
            print("cycle error:", e)
        time.sleep(READ_INTERVAL_SECONDS)


main()
