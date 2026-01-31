from pydantic import BaseModel, EmailStr, Field
from pydantic import StringConstraints
from typing_extensions import Annotated
from typing import Optional

Username = Annotated[str, StringConstraints(
    min_length=1,
    max_length=20,
    pattern=r'^[a-zA-Z0-9]+$'
)]

Password = Annotated[str, StringConstraints(
    min_length=8,
    max_length=128
)]

class UserBase(BaseModel):
    username: Username
    email: EmailStr
    full_name: str = Field(max_length=20)
    is_active: bool = True


class UserCreate(UserBase):
    password: Password

class UserUpdate(UserBase):
    password: Optional[Password] = None
