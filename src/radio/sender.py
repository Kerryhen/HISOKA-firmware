from radio.espnow_comm import ESPNOW_BASE
from primitives.queue import Queue
import asyncio

import time
import math

class Sender(ESPNOW_BASE):
    def __init__(self, range=100):
        super().__init__()
        self.receiver_mac = None
        self.range = range
        self.data = Queue() #2x Max_freq?

    async def listen_for_receiver(self):
        """Listen for broadcast messages from the receiver containing its MAC address."""
        while not self.receiver_mac:
            async for sensor_host, msg in self.esp:
                if self.receiver_mac != sensor_host:
                    self.receiver_mac = sensor_host
                    self.esp.add_peer(sensor_host)
                    print(f"Receiver MAC registered {sensor_host} {msg}")
            await asyncio.sleep(0)

    async def collect_data(self):
        """Send sensor data to the registered receiver."""
        while True:
            for i in range(self.range):
                await self.data.put(f"{time.ticks_ms()}:{math.sin(i / self.range):.2f}")
                # await asyncio.sleep_ms(10)

    async def send_data(self):
        """Send sensor data to the registered receiver."""

        while True:
            if not self.receiver_mac:
                print("No receiver MAC registered. Waiting...")
                await asyncio.sleep(5)
            else:
                if not self.data.empty():
                    data = await self.data.get()
                    send_ok = await self.esp.asend(self.receiver_mac, data.encode("utf-8"))
                    while not send_ok:
                        send_ok = await self.esp.asend(self.receiver_mac, data.encode("utf-8"))
                    self.data.task_done()
                await asyncio.sleep(0)

    def get_async(self):
        return self.listen_for_receiver, self.collect_data, self.send_data