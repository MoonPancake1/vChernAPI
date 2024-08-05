from datetime import date
from typing import Annotated

from pydantic import BaseModel


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
