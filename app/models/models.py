from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    born = Column(Date, nullable=False)
    registration_date = Column(Date, nullable=False)
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    role = relationship("Role", back_populates="users", lazy="selectin")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, unique=True)
    users = relationship("User", back_populates="role")
    permissions = Column(ARRAY(String), nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", lazy="selectin", uselist=False)
    last_activity = Column(DateTime, nullable=False)
