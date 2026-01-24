from pydantic import BaseModel, EmailStr, ConfigDict, conint
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserOutResponse(BaseModel):
    id: int
    email: EmailStr
    # This acccpet the SQLAlchemy ORM object as object, not just dictionaries
    model_config = ConfigDict(from_attributes=True) 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PostOutResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutResponse

class PostOutResponseVote(BaseModel):
    Posts: PostOutResponse
    Votes: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class DoVoting(BaseModel):
    post_id: int
    dir: conint(le=1)

class TokenOutResponse(BaseModel):
    access_token: str
    token_type: str