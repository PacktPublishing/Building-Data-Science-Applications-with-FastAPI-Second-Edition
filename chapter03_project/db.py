from chapter03_project.schemas.post import Post
from chapter03_project.schemas.user import User


class DummyDatabase:
    users: dict[int, User] = {}
    posts: dict[int, Post] = {}


db = DummyDatabase()
