from fastapi import FastAPI, status
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


class Post(PostBase):
    id: int
    nb_views: int = 0


class DummyDatabase:
    posts: dict[int, Post] = {}


db = DummyDatabase()


app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostRead)
async def create(post_create: PostCreate):
    new_id = max(db.posts.keys() or (0,)) + 1

    post = Post(id=new_id, **post_create.dict())

    db.posts[new_id] = post
    return post
