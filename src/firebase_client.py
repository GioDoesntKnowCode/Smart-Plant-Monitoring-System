import time
import ntptime
import urequests

from secrets import FIREBASE_DB_URL, FIREBASE_AUTH

_synced = False


def _sync_clock():
    global _synced
    if _synced:
        return
    ntptime.settime()
    _synced = True


def now_iso():
    """ISO-8601 UTC timestamp, safe to use as a Firebase key."""
    _sync_clock()
    t = time.gmtime()
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(*t[:6])


def _put(path, payload):
    url = "{}/{}.json?auth={}".format(FIREBASE_DB_URL, path, FIREBASE_AUTH)
    r = urequests.put(url, json=payload)
    try:
        if r.status_code >= 400:
            raise RuntimeError("firebase {}: {}".format(r.status_code, r.text))
    finally:
        r.close()


def _get(path):
    url = "{}/{}.json?auth={}".format(FIREBASE_DB_URL, path, FIREBASE_AUTH)
    r = urequests.get(url)
    try:
        if r.status_code >= 400:
            raise RuntimeError("firebase {}: {}".format(r.status_code, r.text))
        return r.json()
    finally:
        r.close()


def push_reading(pi_name, ts, moisture_raw, moisture_pct, light_raw):
    _put("readings/{}/{}".format(pi_name, ts), {
        "moisture":     moisture_raw,
        "moisture_pct": moisture_pct,
        "light":        light_raw,
    })


def fetch_config(pi_name):
    """Returns the config dict for this Pi, or None if missing."""
    return _get("config/{}".format(pi_name))
