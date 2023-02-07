import uuid

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.middleware import Middleware

from chapter14.basic.text_to_image import TextToImage


class TextToImageMiddleware(Middleware):
    def __init__(self) -> None:
        super().__init__()
        self.text_to_image = TextToImage()

    def after_process_boot(self, broker):
        self.text_to_image.load_model()
        return super().after_process_boot(broker)


text_to_image_middleware = TextToImageMiddleware()
redis_broker = RedisBroker(host="localhost")
redis_broker.add_middleware(text_to_image_middleware)
dramatiq.set_broker(redis_broker)


@dramatiq.actor()
def text_to_image_task(
    prompt: str, *, negative_prompt: str | None = None, num_steps: int = 50
):
    image = text_to_image_middleware.text_to_image.generate(
        prompt, negative_prompt=negative_prompt, num_steps=num_steps
    )
    image.save(f"{uuid.uuid4()}.png")
