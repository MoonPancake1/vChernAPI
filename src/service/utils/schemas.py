from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str | None = None


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
    password: str


class User(BaseModel):
    """
    Модель для полного представления объекта в коде
    """
    uuid_user: str
    nickname: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    avatar: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    """

    """
    avatar: str | None = None
