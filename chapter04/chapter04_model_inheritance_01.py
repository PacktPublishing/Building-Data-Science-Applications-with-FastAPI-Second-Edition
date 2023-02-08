from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostRead(BaseModel):
    id: int
    title: str
    content: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    nb_views: int = 0
