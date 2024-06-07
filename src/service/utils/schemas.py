import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    create_date: str = str(datetime.datetime.today())
    icon: bool = False
    images: bool = False
    link: str = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    nickname: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    uuid_user: str
    is_active: bool
    hashed_password: str
    projects: list[Project] = []

    class Config:
        orm_mode = True