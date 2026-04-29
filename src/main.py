import time

from config import PI_NAME, MOISTURE_PIN, PUMP_PIN, READ_INTERVAL_SECONDS
import wifi
import firebase_client
import moisture
import pump
import remote_config


def cycle():
    cfg = remote_config.load()

    value = moisture.read(MOISTURE_PIN)
    percent = moisture.to_percent(
        value, cfg["moisture_dry_value"], cfg["moisture_wet_value"]
    )
    print("moisture: {} ({}%)".format(value, percent))

    wifi.ensure_connected()
    ts = firebase_client.now_iso()
    firebase_client.push_reading(PI_NAME, ts, value, percent)

    if value > cfg["dry_threshold"]:
        print("dry — running pump for {}s".format(cfg["pump_dose_seconds"]))
        pump.dose(PUMP_PIN, cfg["pump_dose_seconds"])
        firebase_client.push_event(
            PI_NAME, ts, {"event": "watered", "duration_s": cfg["pump_dose_seconds"]}
        )

    return cfg["read_interval_seconds"]


def main():
    interval = READ_INTERVAL_SECONDS  # use local default for the very first sleep
    while True:
        try:
            interval = cycle()
        except Exception as e:
            print("cycle error:", e)
        time.sleep(interval)


main()
