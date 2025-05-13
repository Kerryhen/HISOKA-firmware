from machine import UART
import machine 
from time import sleep
class Serial:
    def __init__(self):
        self.ssid = None
        self.password = None

    def begin(self, baudrate = 115200):
        self.uart = UART(1)#, rx=1, tx=3)
        self.uart.init(baudrate = baudrate)
        self.uart.irq(self.ask_wifi_credentials, trigger=UART.IRQ_RXIDLE)

    def ask_wifi_credentials(self, serial):
        print("Configuração de Wi-Fi via serial:")
        self.ssid = serial.read()
        self.password = serial.readline()
        # return ssid, password
