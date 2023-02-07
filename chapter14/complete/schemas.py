from datetime import datetime

from pydantic import BaseModel, Field


class GeneratedImageBase(BaseModel):
    prompt: str
    negative_prompt: str | None
    num_steps: int = Field(50, gt=0, le=50)

    class Config:
        orm_mode = True


class GeneratedImageCreate(GeneratedImageBase):
    pass


class GeneratedImageRead(GeneratedImageBase):
    id: int
    created_at: datetime
    progress: int
    file_name: str | None


class GeneratedImageURL(BaseModel):
    url: str
