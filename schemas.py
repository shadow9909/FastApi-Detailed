from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    username: str

    class Config():
        orm_mode = True


class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config:
        orm_mode = True


class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
    # used for Response Model-> to map DB data to objects

    class Config():
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
