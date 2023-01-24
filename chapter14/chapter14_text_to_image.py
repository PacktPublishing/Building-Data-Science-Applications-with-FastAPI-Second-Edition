from diffusers import StableDiffusionPipeline
from PIL import Image


class TextToImage:
    pipe: StableDiffusionPipeline | None = None

    def load_model(self) -> None:
        """Loads the model"""
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        pipe.to("cpu")
        self.pipe = pipe

    def generate(
        self, prompt: str, *, negative_prompt: str | None = None, num_steps: int = 50
    ) -> Image.Image:
        if not self.pipe:
            raise RuntimeError("Pipeline is not loaded")
        return self.pipe(
            prompt, negative_prompt=negative_prompt, num_inference_steps=num_steps
        ).images[0]


if __name__ == "__main__":
    text_to_image = TextToImage()
    text_to_image.load_model()
    image = text_to_image.generate(
        "A pikachu fine dining with a view to the Eiffel Tower"
    )
    image.save("output.png")
