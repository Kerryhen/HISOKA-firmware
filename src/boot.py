from config import wifi_config, led
from net import wifi
from config.receiver import Receiver

ld = led.LedRGB()
receiver = Receiver()

if __name__ == "__main__":

    ld.set(led.Color.OFF)

    if wifi_config.has_config():
        ld.set(led.Color.BLUE)
        config = wifi_config.load_wifi_config()
        if config:
            ssid = config['ssid']
            password = config['password']
            
            if wifi.connect_wifi(ssid, password):
                ld.set(led.Color.GREEN)
                wifi.disconnect_wifi()
                ld.set(led.Color.OFF)
                receiver.set_wifi_network(ssid, password)
            else:
                ld.set(led.Color.RED)
                print("Falha ao conectar no Wi-Fi.")
        else:
            ld.set(led.Color.RED)
            print("Nenhuma configuração de Wi-Fi encontrada.")
    else:
        ld.set(led.Color.RED)