import network
import time

def connect_wifi(ssid, password, timeout=10):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        for _ in range(timeout * 2):
            if wlan.isconnected():
                return True
            time.sleep(0.5)
        return False
    except OSError as e:
        print(e)
        return False


def disconnect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)

def get_mac():
    wlan = network.WLAN(network.STA_IF)
    return wlan.config('mac')
