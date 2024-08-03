from sqlalchemy import Boolean, Column, String, Integer

from src.service.utils.db import Base


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid_user = Column(String, unique=True)
    nickname = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    avatar = Column(String, default='static/avatars/default.png')
