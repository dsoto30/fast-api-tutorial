from pydantic import BaseModel, EmailStr, conint, ValidationError
from datetime import datetime
from typing import Annotated
from pydantic.functional_validators import AfterValidator



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):
    Post: Post
    votes: int


def is_binary_int(value: int) -> int:
    if value not in (0, 1):
        raise ValueError(f"value must be 0 or 1")
    return value



class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, AfterValidator(is_binary_int)]






class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None