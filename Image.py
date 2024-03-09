import asyncio
import threading
import time
import random

class ImageUpdater:
    def __init__(self):
        self.image = None
        self.image_used = threading.Event()
        self.image_created = threading.Event()
        self.lock = threading.Lock()

    def update_image(self):
        while True:
            time.sleep(0.6)
            with self.lock:
                self.image = str(random.random())
                self.image_created.set()
                self.image_used.wait()
                self.image_created.clear()

    async def image_generator(self):
        while True:
            with self.lock:
                self.image_created.clear()
                self.image_used.clear()
                print("waiting for new image")
                await asyncio.sleep(0)
                yield self.image
                self.image_used.set()

async def main():
    updater = ImageUpdater()

    update_thread = threading.Thread(target=updater.update_image)
    update_thread.start()


    async for image in updater.image_generator():
        print(f"Received new image: {image}")

if __name__ == "__main__":
    asyncio.run(main())
