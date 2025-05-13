from serial import Serial, serialutil
with Serial(port='/dev/ttyACM0', baudrate=115200) as ser:
    print(ser.is_open)
    # print(ser.readline())
    ser.writelines([
        b"from config import wifi_config\r\n",
        # f'wifi_config.save_wifi_config("{input('SSID:')}","{input('PASSWD:')}")\r\n'.encode("UTF-8"),
        b'wifi_config.save_wifi_config("HUAWEI-2.4G-3FGn","wdGUHgy5")\r\n'
    ])
    ser.writelines([b"import machine\r\n", b"machine.Pin(43,machine.Pin.OUT).on()\r\n"])

#HAUWEI-2.4G-3FGn
#wdGUHgy5

#wifi_config.save_wifi_config("HUAWEI-2.4G-3FGn","wdGUHgy5")