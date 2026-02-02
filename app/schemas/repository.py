from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from pydantic import StringConstraints
from typing_extensions import Annotated
from typing import Optional
import re

RepositoryName = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9._-]+$',
        strip_whitespace=True
    )
]

RepositoryOwner = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=39,  # GitHub limit
        pattern=r'^[a-zA-Z0-9-]+$',
        strip_whitespace=True
    )
]

RepositoryUrl = Annotated[
    HttpUrl,
    StringConstraints(
        pattern=r'^https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9._-]+$'
    )
]


class RepositoryBase(BaseModel):
    name: RepositoryName
    owner: RepositoryOwner
    url: RepositoryUrl

    @field_validator("name", "owner", mode="before")
    @classmethod
    def to_lowercase(cls, value: str) -> str:
        return value.lower()

    @model_validator(mode="after")
    def validate_url_matches_fields(self):
        expected_url = f"https://github.com/{self.owner}/{self.name}"
        if str(self.url) != expected_url:
            raise ValueError(
                f"url должен быть '{expected_url}'"
            )
        return self
    
class RepositoryCreate(RepositoryBase):
    pass
class RepositoryUpdate(BaseModel):
    name: Optional[RepositoryName] = None
    owner: Optional[RepositoryOwner] = None
    url: Optional[RepositoryUrl] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not any([self.name, self.owner, self.url]):
            raise ValueError("Нужно передать хотя бы одно поле")
        return self
