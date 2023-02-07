import torch
from diffusers import StableDiffusionPipeline
from PIL import Image


class TextToImage:
    pipe: StableDiffusionPipeline | None = None

    def load_model(self) -> None:
        # Enable CUDA GPU
        if torch.cuda.is_available():
            device = "cuda"
            torch_dtype = torch.float16
        # Enable Apple Silicon (M1) GPU
        elif torch.backends.mps.is_available():
            device = "mps"
            torch_dtype = torch.float16
        # Fallback to CPU
        else:
            device = "cpu"
            torch_dtype = None

        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=torch_dtype
        )
        pipe.to(device)
        self.pipe = pipe

    def generate(
        self, prompt: str, *, negative_prompt: str | None = None, num_steps: int = 50
    ) -> Image.Image:
        if not self.pipe:
            raise RuntimeError("Pipeline is not loaded")
        return self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_steps,
            guidance_scale=9.0,
        ).images[0]


if __name__ == "__main__":
    text_to_image = TextToImage()
    text_to_image.load_model()
    image = text_to_image.generate(
        "A Renaissance castle in the Loire Valley", negative_prompt="low quality, ugly"
    )
    image.save("output.png")
