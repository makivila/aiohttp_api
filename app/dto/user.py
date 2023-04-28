import datetime
from pydantic import BaseModel, Field


class UserDTORequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    second_name: str = Field(min_length=1, max_length=255)
    login: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)
    born: datetime.date
    role: str


class UserDTOResponse(BaseModel):
    id: int
    first_name: str
    second_name: str
    login: str
    born: datetime.date
    registration_date: datetime.date
    role_id: int


class LoginDTO(BaseModel):
    login: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)
