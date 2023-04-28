from typing import List
from pydantic import BaseModel


class RoleDTORequest(BaseModel):
    role: str
    permissions: List[str]


class RoleDTOResponse(BaseModel):
    id: int
    role: str
    permissions: List[str]
