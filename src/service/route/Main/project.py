from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.service.utils.Main import schemas, crud
from src.service.utils.db import get_db

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/project/{project_id}")
async def get_project(project_id: int,
        db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id)
    return project


@router.post("/project/", response_model=schemas.PreGetProject)
async def create_project(project: schemas.ProjectCreate,
                         db: Session = Depends(get_db)):
    return await crud.create_project(db=db, project=project)