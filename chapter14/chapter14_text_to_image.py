# pip install diffusers accelerate
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cpu")

prompt = "squirrel wearing a hat"
image = pipe(prompt).images[0]

image.save("squirrel.png")
