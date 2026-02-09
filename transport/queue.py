import asyncio

class EventQueue:
    def __init__(self, maxsize=10000):
        self.queue = asyncio.Queue(maxsize=maxsize)

    async def push(self, event):
        try:
            self.queue.put_nowait(event)
        except asyncio.QueueFull:
            pass
