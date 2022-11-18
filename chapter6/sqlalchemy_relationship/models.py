from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    post_id: int = Column(ForeignKey("posts.id"), nullable=False)
    publication_date: datetime = Column(DateTime, nullable=False, default=datetime.now)
    content: str = Column(Text, nullable=False)

    post: "Post" = relationship("Post", back_populates="comments")


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    publication_date: datetime = Column(DateTime, nullable=False, default=datetime.now)
    title: str = Column(String(255), nullable=False)
    content: str = Column(Text, nullable=False)

    comments: list[Comment] = relationship("Comment", cascade="all, delete")
