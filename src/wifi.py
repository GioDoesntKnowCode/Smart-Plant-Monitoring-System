import network
import time

from secrets import WIFI_SSID, WIFI_PASSWORD

_wlan = None


def ensure_connected(timeout=20):
    global _wlan
    if _wlan is None:
        _wlan = network.WLAN(network.STA_IF)
        _wlan.active(True)
    if _wlan.isconnected():
        return
    _wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    deadline = time.time() + timeout
    while not _wlan.isconnected():
        if time.time() > deadline:
            raise RuntimeError("wifi connect timed out")
        time.sleep(0.5)
