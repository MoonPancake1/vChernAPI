from datetime import date

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


class PreGetProject(BaseModel):
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


class GetProject(PreGetProject):
    rate: float
