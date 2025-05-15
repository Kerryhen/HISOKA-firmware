import asyncio
from collections import deque

store = deque((), 1000)

main_queue = asyncio.Queue()
failed_queue = asyncio.Queue()

async def task_bd():
    d = 0
    while True:
        await main_queue.put(d)
        d+=1
        await asyncio.sleep(0.5)

async def task_bd2():
    while True:
        if not main_queue.empty():
            data = await main_queue.get()
            print(data)
        await asyncio.sleep(1)

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(task_bd())
    loop.create_task(task_bd2())
    loop.run_forever()
    # await asyncio.sleep(15)



main()