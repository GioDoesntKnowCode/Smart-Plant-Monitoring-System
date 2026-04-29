"""
Remote config loader.

Fetches per-device config from Firebase and merges it over local defaults.
Local defaults (config.py) are always used as fallback if Firebase is unreachable.

Firebase structure:
  config/<PI_NAME>/
    moisture_dry_value:      65535
    moisture_wet_value:      34954
    dry_threshold:           57000
    pump_dose_seconds:       2
    read_interval_seconds:   14400

To add a new config key in future:
  1. Add the default value to config.py.
  2. Add the key + default to DEFAULTS below.
  3. Set the value in Firebase under config/<PI_NAME>/.
     The Pico picks it up on the next cycle — no code re-upload needed.

Pin assignments (MOISTURE_PIN, LIGHT_PIN, PUMP_PIN) are intentionally
kept local-only — they're hardware and can't change remotely.
"""

import firebase_client
from config import (
    PI_NAME,
    MOISTURE_DRY_VALUE,
    MOISTURE_WET_VALUE,
    MOISTURE_DRY_THRESHOLD,
    PUMP_DOSE_SECONDS,
    READ_INTERVAL_SECONDS,
)

DEFAULTS = {
    "moisture_dry_value":    MOISTURE_DRY_VALUE,
    "moisture_wet_value":    MOISTURE_WET_VALUE,
    "dry_threshold":         MOISTURE_DRY_THRESHOLD,
    "pump_dose_seconds":     PUMP_DOSE_SECONDS,
    "read_interval_seconds": READ_INTERVAL_SECONDS,
}


def load():
    """
    Returns a config dict for this device.
    Firebase values override local defaults where present.
    Falls back to full local defaults if the fetch fails.
    """
    cfg = dict(DEFAULTS)
    try:
        remote = firebase_client.fetch_config(PI_NAME) or {}
        cfg.update(remote)
        if remote:
            print("remote config applied:", remote)
        else:
            print("no remote config found, using defaults")
    except Exception as e:
        print("remote config unavailable, using defaults:", e)
    return cfg
