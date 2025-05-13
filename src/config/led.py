import machine, neopixel

class Color:
    RED = [255,0,0]
    GREEN = [0,255,0]
    BLUE = [0,0,255]
    OFF = [0,0,0]

class LedRGB:
    def __init__(self, pin=48, qtd=1):
        self.np = neopixel.NeoPixel(machine.Pin(pin), qtd)
    
    def set(self, color:Color, pixel=0):
        self.np[pixel] = color
        self.np.write()