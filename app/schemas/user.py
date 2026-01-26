from pydantic import BaseModel, EmailStr, validator, Field, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    full_name: str = Field(max_length=20)
    is_active: bool = True
        
class UserCreate(UserBase):
    password: constr = Field(min_length=8, max_length=128)
    @validator('username')
    def username_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserUpdate(UserBase):
    password: Optional[constr] = Field(None, min_length=8, max_length=128)

class UserInDB(UserBase):
    id: int
    hashed_password: str
    class Config:
        orm_mode = True