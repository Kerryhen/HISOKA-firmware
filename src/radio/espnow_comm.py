import aioespnow
import network

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