import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ProjectBase(BaseModel):
    """
    Базовая модель для таблицы с проектами
    """
    title: str
    description: str | None = None
    create_project_date: str = str(datetime.datetime.today())
    icon: bool = False
    images: bool = False
    link: str = None


class ProjectCreate(ProjectBase):
    """
    Модель для создания записи проекта
    """
    pass


class Project(ProjectBase):
    """
    Модель полной записи для таблицы
    """
    id: int
    author_id: int

    class Config:
        orm_mode = True


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


class User(UserBase):
    """
    Модель для полного представления объекта в коде
    """
    id: int
    uuid_user: str
    is_active: bool = True
    hashed_password: str
    projects: list[Project] = []

    class Config:
        orm_mode = True
