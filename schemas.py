from datetime import datetime
from pydantic import BaseModel , ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1,max_length=50)
    email: EmailStr = Field(max_length=100)

class UserCreate(UserBase):
    ...


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    image_file : str | None
    image_path : str

class UserUpdate(BaseModel):
    username: str | None = Field(default=None,min_length=1,max_length=50)
    email: EmailStr | None = Field(default=None,max_length=100)
    image_file: str | None = Field(default=None,max_length=100)

class PostBase(BaseModel):
    title: str = Field(min_length=1,max_length=100)
    content: str = Field(min_length=1)
    
class PostUpdate(BaseModel):
    # prevent the caller of adding extra attributes
    # model_config = ConfigDict(extra='forbid')
    title: str | None = Field(min_length=1,max_length=100,default=None)
    content: str | None = Field(min_length=1,default=None)
    
class PostCreate(PostBase):
    user_id: int
    
class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    date_posted : datetime
    author : UserResponse