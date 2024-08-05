from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.config.project_config.config import settings
from src.service.utils.Main import schemas, crud, auth
from src.service.utils.db import get_db

router = APIRouter(prefix="/projects", tags=["project"])


@router.get("/{project_id}")
async def get_project(project_id: int,
        db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.view:
        project.view = 1
    else:
        project.view += 1
    return await crud.update_project(db, project)


@router.put("/{project_id}/{token}")
async def update_project(token: str,
                         project: schemas.ProjectUpdate,
                         db: Session = Depends(get_db)):
    check = await auth.check_permissions(token, [settings.OWNER])
    if isinstance(check, bool):
        if check:
            return await crud.update_project(db, project)
        else:
            return HTTPException(status_code=403, detail="Not enough permissions")
    else:
        return check



@router.delete("/{project_id}/{token}")
async def delete_project(token: str,
                         project_id: int,
                         db: Session = Depends(get_db)):
    check = await auth.check_permissions(token, [settings.OWNER])
    if isinstance(check, bool):
        if check:
            return await crud.delete_project(db, project_id)
        else:
            return HTTPException(status_code=403, detail="Not enough permissions")
    else:
        return check



@router.post("/{token}")
async def create_project(
        token: str,
        project: schemas.ProjectCreate,
        db: Session = Depends(get_db)):
    check = await auth.check_permissions(token, [settings.OWNER])
    if isinstance(check, bool):
        if check:
            return await crud.create_project(db=db, project=project)
        else:
            return HTTPException(status_code=403, detail="Not enough permissions")
    else:
        return check


@router.get("/")
async def get_projects(db: Session = Depends(get_db)):
    return await crud.get_projects(db=db)
