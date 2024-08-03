from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from src.service.utils.Main import models, schemas


async def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Projects).filter(models.Projects.id == project_id).first()


async def get_projects(db: Session):
    return db.query(models.Projects).all()


async def create_project(db: Session, project: schemas.ProjectCreate):
    if not project.link_logo:
        project.link_logo = None
    if not project.github_link:
        project.github_link = None
    if not project.project_link:
        project.project_link = None

    db_project = models.Projects(
        title=project.title,
        description=project.description,
        realize_project=project.realize_project,
        stack=project.stack,
        status=project.status,
        view=0,
        link_logo=project.link_logo,
        github_link=project.github_link,
        project_link=project.project_link,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
