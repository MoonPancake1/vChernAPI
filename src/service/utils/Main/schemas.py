from datetime import date
from typing import Annotated

from pydantic import BaseModel


# Project

class ProjectCreate(BaseModel):
    title: str
    description: str
    realize_project: date
    stack: dict
    status: str
    link_logo: str | None = None
    github_link: str | None = None
    project_link: str | None = None


class Project(BaseModel):
    id: int
    title: str
    description: str
    realize_project: date
    stack: dict
    status: str
    view: int
    link_logo: str | None = None
    github_link: str | None = None
    project_link: str | None = None


class ProjectFull(Project):
    rate: float


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    realize_project: date | None = None
    stack: dict | None = None
    status: str | None = None
    view: int | None = None
    link_logo: str | None = None
    github_link: str | None = None
    project_link: str | None = None


# User

class User(BaseModel):
    """
    Модель для полного представления объекта в коде
    """
    uuid: str
    nickname: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    avatar: str
    ip: str | None = None

    class Config:
        from_attributes = True


# Grades

class GradeCreate(BaseModel):
    project_id: int
    grade: int


class GradeUpdate(BaseModel):
    grade_id: int
    grade: int


class Grade(GradeCreate):
    user_uuid: str

class Grades(GradeCreate):
    pass


# Comment

class CommentCreate(BaseModel):
    project_id: int
    comment: str


class CommentUpdate(BaseModel):
    comment_id: int
    comment: str


class Comment(BaseModel):
    user_uuid: int


class Comments(CommentCreate):
    pass