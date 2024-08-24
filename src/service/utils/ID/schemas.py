from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class TokenData(BaseModel):
    uuid: str | None = None


class UserBase(BaseModel):
    """
    Базовая модель для таблицы с пользователями
    """
    nickname: str
    email: str


class UserCreate(UserBase):
    """
    Модель для создания записи в базе данных
    """
    ip: str | None = None
    password: str


class UserBase(BaseModel):
    """
    Модель для базового представления объекта в коде
    """
    uuid: str
    nickname: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    avatar: str

    class Config:
        from_attributes = True

class User(UserBase):
    """
    Модель для полного представления объекта в коде
    """
    ip: str | None = None


class UserUpdate(BaseModel):
    """
    Update user data
    """
    nickname: str | None = None
    email: str | None = None
    avatar: str | None = None
