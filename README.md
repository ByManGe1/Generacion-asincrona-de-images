### simula una situación donde hay un hilo que actualiza una imagen en segundo plano y un generador asíncrono que espera y consume esas imágenes en el hilo principal. Este es solo un ejemplo didáctico y no necesariamente representa un caso de uso práctico.

### Codigo Python 3.12.2

```python
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
```

### ImageUpdater:

- update_image: Este método se ejecuta en un hilo separado (update_thread). Simula la creación de una nueva imagen cada 0.6 segundos y notifica al generador asíncrono (image_generator) que hay una nueva imagen disponible.
- image_generator: Este método es un generador asíncrono que espera hasta que se haya creado una nueva imagen. Luego, devuelve la imagen y señaliza que la imagen ha sido utilizada.

### main: 
- Inicia la instancia de ImageUpdater.
- Inicia un hilo (update_thread) que ejecuta update_image para crear y notificar nuevas imágenes.
- Utiliza asyncio para ejecutar el generador asíncrono image_generator que consume las imágenes creadas.

### Funcionamiento: 
- Mientras update_image crea una nueva imagen cada 0.6 segundos, image_generator espera activamente hasta que se notifica sobre una nueva imagen.
- Cuando una nueva imagen está disponible, image_generator la devuelve y señaliza que la imagen ha sido utilizada.
- El bucle continúa, y el proceso se repite.
