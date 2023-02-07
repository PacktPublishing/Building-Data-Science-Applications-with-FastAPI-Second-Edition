from dramatiq import Message
from fastapi import FastAPI, status
from pydantic import UUID4, BaseModel, Field

from chapter14.basic.worker import text_to_image_task


class ImageGenerationInput(BaseModel):
    prompt: str
    negative_prompt: str | None
    num_steps: int = Field(50, gt=0, le=50)


class ImageGenerationOutput(BaseModel):
    task_id: UUID4


app = FastAPI()


@app.post(
    "/image-generation",
    response_model=ImageGenerationOutput,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_image_generation(input: ImageGenerationInput) -> ImageGenerationOutput:
    task: Message = text_to_image_task.send(
        input.prompt, negative_prompt=input.negative_prompt, num_steps=input.num_steps
    )
    return ImageGenerationOutput(task_id=task.message_id)
