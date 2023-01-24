from PIL import Image

from chapter14.chapter14_text_to_image import TextToImage


def test_chapter_14_text_to_image():
    text_to_image = TextToImage()
    text_to_image.load_model()
    image = text_to_image.generate(
        "a photo of squirrels partying in a night club", num_steps=1
    )
    assert isinstance(image, Image.Image)
