from radio.espnow_comm import ESPNOW_BASE
from primitives.queue import Queue
import asyncio

from config import wifi_config
import ujson

class Receiver(ESPNOW_BASE):
    def __init__(self, queue_size=10):
        super().__init__()
        self.queues = {}  # CircularQueue for each sensor MAC
        self.queue_size = queue_size
       
        self.config = ""
        if wifi_config.has_config():
            self.config = ujson.dumps(wifi_config.load_wifi_config())

    async def broadcast_mac(self):
        """Broadcast the receiver's MAC address to all sensors."""
        while True:
            self.broadcast(self.config.encode("utf-8"))
            print(f"Broadcasting MAC address {self.mac}")
            await asyncio.sleep(5) #every 5 seconds

    async def listen_for_data(self):
        """Listen for sensor data and store it in queues."""
        while True:
            # sensor_host, msg = await self.esp.airecv(timeout_ms=0)
            async for sensor_host, msg in self.esp:
                if sensor_host not in self.queues:
                    print(f"New sensor detected: {sensor_host}")
                    self.queues[sensor_host] = Queue(self.queue_size)
                    self.esp.add_peer(sensor_host)
                await self.queues[sensor_host].put(msg.decode("utf-8"))
            await asyncio.sleep_ms(0)

    async def plot_data(self):
        """Periodically process and plot values from the queues."""
        while True:
            for mac, queue in self.queues.items():
                if not queue.empty():
                    data = await queue.get()
                    print(f">{mac.hex()}:{data}")
                    queue.task_done()
            await asyncio.sleep(0)

    def get_async(self):
        return self.broadcast_mac, self.listen_for_data, self.plot_data
    