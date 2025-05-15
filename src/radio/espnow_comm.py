import aioespnow
import network
import time

class ESPNOW_BASE:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        # self.esp = espnow.ESPNow()
        self.esp = aioespnow.AIOESPNow()
        self.broadcastaddr = b'\xff'*6
        self.mac = network.WLAN(network.STA_IF).config('mac')
    
    def init(self):
        """Initialize Wi-Fi and ESP-NOW."""
        self.wlan.active(True)
        self.esp.active(True)
        self.esp.add_peer(self.broadcastaddr)

    def broadcast(self, message):
        self.esp.send(self.broadcastaddr, message)


class logger:
    def __init__(self, name=None, unit=None, _type=None):
        self.name = name
        self.unit = f"§{unit}" if unit else ""
        self._type = f"|{_type}" if _type else ""

    def print(self, value, name=None):
        print(f">{name or self.name}:{time.time_ns()}:{value}{self.unit}{self._type}")