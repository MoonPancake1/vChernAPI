import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.service.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid_user = Column(String, unique=True)
    nickname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, default=None)
    create_date = Column(String, index=True, default=str(datetime.datetime.today()))
    icon = Column(Boolean, default= False)
    images = Column(Boolean, default=False)
    link = Column(String, default='https://vchern.me')
    author_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")