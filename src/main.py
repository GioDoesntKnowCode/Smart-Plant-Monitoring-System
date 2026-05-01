import time

from config import PI_NAME, MOISTURE_PIN, MOISTURE_POWER_PIN, LIGHT_PIN, LIGHT_POWER_PIN, READ_INTERVAL_SECONDS
import wifi
import firebase_client
import moisture
import remote_config


def cycle():
    wifi.ensure_connected()
    cfg = remote_config.load()

    value = moisture.read(MOISTURE_PIN, MOISTURE_POWER_PIN)
    percent = moisture.to_percent(
        value, cfg["moisture_dry_value"], cfg["moisture_wet_value"]
    )
    l_raw = moisture.read(LIGHT_PIN, LIGHT_POWER_PIN)
    print("moisture: {} ({}%)  |  light: {}".format(value, percent, l_raw))

    ts = firebase_client.now_iso()
    firebase_client.push_reading(PI_NAME, ts, value, percent, l_raw)

    return cfg["read_interval_seconds"]


def main():
    interval = READ_INTERVAL_SECONDS
    while True:
        try:
            interval = cycle()
        except Exception as e:
            print("cycle error:", e)
        time.sleep(interval)


main()
