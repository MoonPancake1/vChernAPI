from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.service.utils.Main import models, schemas


async def get_project_by_id(db: Session, project_id: int) -> schemas.Project:
    return db.query(models.Projects).filter(models.Projects.id == project_id).first()


async def update_project(db: Session, new_project_data: schemas.ProjectUpdate) -> schemas.Project:
    current_project = await get_project_by_id(db, new_project_data.id)
    if not current_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if new_project_data.title:
        current_project.title = new_project_data.title
    if new_project_data.description:
        current_project.description = new_project_data.description
    if new_project_data.realize_project:
        current_project.realize_project = new_project_data.realize_project
    if new_project_data.stack:
        current_project.stack = new_project_data.stack
    if new_project_data.status:
        current_project.status = new_project_data.status
    if new_project_data.view:
        current_project.view = new_project_data.view
    if new_project_data.link_logo:
        current_project.link_logo = new_project_data.link_logo
    if new_project_data.github_link:
        current_project.github_link = new_project_data.github_link
    if new_project_data.project_link:
        current_project.project_link = new_project_data.project_link
    db.commit()
    db.refresh(current_project)
    return current_project


async def delete_project(db: Session, project_id: int) -> dict[str, bool]:
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {'result': True}


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
