from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str


class UserRead(UserBase):
    id: int
