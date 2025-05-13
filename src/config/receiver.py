class Receiver:
    def __init__(self):
        self.ssid = None
        self.ssid_password = None
        self.sensors = []

    def set_wifi_network(self, ssid, password ):
        self.ssid = ssid
        self.ssid_password = password

    def add_sensor(self, mac):
        self.mac.append(mac)