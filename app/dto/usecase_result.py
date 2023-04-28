from enum import Enum
from dataclasses import dataclass
from typing import Any


class UsecaseStatus(Enum):
    SUCCESS = 1
    INTERNAL_ERROR = 2
    UNAUTHORIZED = 3
    NOT_FOUND = 4
    BAD_REQUEST = 5


@dataclass
class UsecaseResult:
    status: UsecaseStatus = UsecaseStatus.SUCCESS
    data: Any = None
