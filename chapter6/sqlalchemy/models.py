from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    publication_date: datetime = Column(DateTime, nullable=False, default=datetime.now)
    title: str = Column(String(255), nullable=False)
    content: str = Column(Text, nullable=False)
