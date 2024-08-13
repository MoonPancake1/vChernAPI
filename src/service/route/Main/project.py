from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.service.route.ID.auth import get_current_active_user
from src.service.utils.Main import schemas, crud
from src.service.utils.db import get_db

router = APIRouter(prefix="/projects", tags=["project"])


@router.get("/{project_id}/")
async def get_project(project_id: int,
        db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.view:
        project.view = 1
    else:
        project.view += 1
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}/")
async def update_project(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                         project_id: int,
                         new_project: schemas.ProjectUpdate,
                         db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id=project_id)
    if not project:
        return HTTPException(status_code=404, detail="Проект не найден!")
    if current_user:
        if current_user.is_admin:
            return await crud.update_project(db, project, new_project)
        else:
            return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    else:
        return HTTPException(status_code=404, detail="Пользователь не найден!")


@router.delete("/{project_id}/")
async def delete_project(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                         project_id: int,
                         db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    if current_user:
        if current_user.is_admin:
            return await crud.delete_project(db, project_id)
        else:
            return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    else:
        return HTTPException(status_code=404, detail="Пользователь не найден!")



@router.post("/")
async def create_project(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        project: schemas.ProjectCreate,
        db: Session = Depends(get_db)):
    if current_user:
        if current_user.is_admin:
            return await crud.create_project(db=db, project=project)
        else:
            return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    else:
        return HTTPException(status_code=404, detail="Пользователь не найден!")


@router.get("/")
async def get_projects(db: Session = Depends(get_db),
                       skip: int = 0, limit: int = 6):
    return await crud.get_projects(db=db, skip=skip, limit=limit)
