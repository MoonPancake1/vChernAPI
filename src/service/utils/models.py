import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.service.utils.db import Base


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    uuid_user = Column(String, unique=True)
    nickname = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    bearer_token = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner")


class Project(Base):
    """
    Модель для проектов
    """
    __tablename__ = "projects"

    title = Column(String, index=True)
    description = Column(String, default=None)
    create_project_date = Column(String, index=True, default=str(datetime.datetime.today()))
    icon = Column(Boolean, default= False)
    images = Column(Boolean, default=False)
    link = Column(String, default='https://vchern.me')
    author_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")