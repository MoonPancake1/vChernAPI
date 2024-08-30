import uuid

from sqlalchemy import Boolean, Column, String, Integer, MetaData

from src.service.utils.db import Base


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True)
    nickname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, default=None)
    hashed_password = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    avatar = Column(String, default='static/avatars/default.png')
    ip = Column(String, default='127.0.0.1')
    role = Column(String, default='user')
