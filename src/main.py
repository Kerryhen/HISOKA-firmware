import network
import espnow
import asyncio
import time
import math
from collections import deque
from config import wifi_config
import ujson
from radio.espnow_comm import ESPNOW_BASE

class logger:
    def __init__(self, name=None, unit=None, _type=None):
        self.name = name
        self.unit = f"§{unit}" if unit else ""
        self._type = f"|{_type}" if _type else ""

    def print(self, value, name=None):
        print(f">{name or self.name}:{time.time_ns()}:{value}{self.unit}{self._type}")

# class CircularQueue:
#     """Circular queue implementation for storing sensor data."""
#     def __init__(self, size):
#         self.queue = 

#     def add(self, item):
#         self.queue.append(item)

#     def get_all(self):
#         return list(self.queue)

#     def is_empty(self):
#         return len(self.queue) == 0


class Receiver(ESPNOW_BASE):
    def __init__(self, queue_size=10):
        super().__init__()
        self.logger = logger("Receiver", _type="t")
        self.data_logger = logger()
        self.queues = {}  # CircularQueue for each sensor MAC
        self.queue_size = queue_size

        self.config = ""
        if wifi_config.has_config():
            self.config = ujson.dumps(wifi_config.load_wifi_config())

    async def broadcast_mac(self):
        """Broadcast the receiver's MAC address to all sensors."""
        receiver_mac = self.wlan.config('mac')
        self.broadcast(self.config.encode("utf-8"))
        self.logger.print(f"Broadcasting MAC address {receiver_mac}")
        await asyncio.sleep_ms(1)

    async def listen_for_data(self):
        """Listen for sensor data and store it in queues."""
        while True:
            host, msg = self.esp.recv()
            if msg:
                sensor_mac = host
                if sensor_mac not in self.queues:
                    self.queues[sensor_mac] = deque((),self.queue_size)
                    self.logger.print(f"New sensor detected: {sensor_mac}")
                    self.esp.add_peer(host)
                self.queues[sensor_mac].append(msg.decode("utf-8"))
                self.logger.print(f"Received from {sensor_mac} {msg.decode("utf-8")}")
            await asyncio.sleep_ms(1)

    async def plot_data(self):
        """Periodically process and plot values from the queues."""
        while True:
            for mac, queue in self.queues.items():
                if not len(queue) == 0:
                    data = queue.pop()
                    print(f">{mac.hex()}:{data}")
            await asyncio.sleep_ms(1)  # Simulate plotting delay


class Sender(ESPNOW_BASE):
    def __init__(self, range=100):
        super().__init__()
        self.logger = logger("SenderLogger", _type="t")
        self.data_logger = logger("SenderData")
        self.receiver_mac = None
        self.range = range

    async def listen_for_receiver(self):
        """Listen for broadcast messages from the receiver containing its MAC address."""
        while True:
            host, msg = self.esp.recv()
            if msg and self.receiver_mac is None:
                self.receiver_mac = host
                self.esp.add_peer(host)

                self.logger.print(f"Receiver MAC registered {host} {msg}")
            await asyncio.sleep_ms(1)

    async def send_data(self):
        """Send sensor data to the registered receiver."""

        while True:
            if not self.receiver_mac:
                self.logger.print("No receiver MAC registered. Waiting...")
                await asyncio.sleep_ms(1)
            else:
                for i in range(self.range):
                    data = f"{time.time_ns()}:{math.sin(i / self.range):.2f}"
                    self.esp.send(self.receiver_mac, data.encode("utf-8"))
                    self.data_logger.print(data)
                    await asyncio.sleep_ms(1)


async def main():
    # Receiver workflow
    # receiver = Receiver(queue_size=1000)
    # await receiver.init()    
    # return await asyncio.gather(receiver.broadcast_mac(), receiver.listen_for_data(),receiver.plot_data())

    # # Sender workflow
    sender = Sender(range=100)
    await sender.init()
    results = await asyncio.gather(sender.listen_for_receiver(),sender.send_data() )


    


if __name__ == "__main__":
    try:
        asyncio.run(main())
        # loop = asyncio.get_event_loop()  
        # loop.create_task(main())
        # loop.run_forever()

    except KeyboardInterrupt:
        print("Program stopped.")