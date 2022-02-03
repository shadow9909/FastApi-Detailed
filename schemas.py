from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    # used for Response Model-> to map DB data to objects

    class Config():
        orm_mode = True
