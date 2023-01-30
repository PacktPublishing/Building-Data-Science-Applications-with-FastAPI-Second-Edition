import uuid
from celery import Celery
from celery.signals import worker_process_init


from chapter14.text_to_image import TextToImage

app = Celery("worker", broker="redis://localhost:6379/0")
text_to_image = TextToImage()


@worker_process_init.connect()
def init_worker_process(**kwargs):
    """
    load model before running tasks
    :param kwargs:
    :return:
    """
    global text_to_image
    text_to_image.load_model()


@app.task
def text_to_image_task(
    prompt: str, *, negative_prompt: str | None = None, num_steps: int = 50
):
    image = text_to_image.generate(
        prompt, negative_prompt=negative_prompt, num_steps=num_steps
    )
    image.save(f"{uuid.uuid4()}.png")
