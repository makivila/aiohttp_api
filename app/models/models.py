import datetime
from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import (
    MetaData,
    UniqueConstraint,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    ARRAY,
    DateTime,
    Table,
)


metadata = MetaData()


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("second_name", String, nullable=False),
    Column("login", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("born", Date, nullable=False),
    Column("registration_date", Date, nullable=False),
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    ),
)


roles_table = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("role", String, nullable=False, unique=True),
    Column("permissions", ARRAY(String)),
)


sessions_table = Table(
    "sessions",
    metadata,
    Column("id", String, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("last_activity", DateTime, nullable=False),
)


users_roles_rel_table_unique = UniqueConstraint(
    "user_id", "role_id", name="user_role_unique_idx"
)


@dataclass
class Role:
    role: str
    permissions: List[str]
    id: Optional[int] = None


@dataclass
class User:
    first_name: str
    second_name: str
    login: str
    password: str
    born: datetime.date
    registration_date: datetime.date
    role_id: int
    id: Optional[int] = None
    role: Optional[str] = None


@dataclass
class Session:
    user_id: int
    last_activity: datetime.date
    id: Optional[int] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = None
