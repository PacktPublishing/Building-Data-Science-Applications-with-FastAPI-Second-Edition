from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


class Post(PostBase):
    id: int
    nb_views: int = 0
