import ujson

CONFIG_FILE = "wifi.json"

def save_wifi_config(ssid, password):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump({"ssid": ssid, "password": password}, f)

def load_wifi_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    except OSError:
        return None

def has_config():
    try:
        with open(CONFIG_FILE, "r"):
            return True
    except OSError:
        return False
