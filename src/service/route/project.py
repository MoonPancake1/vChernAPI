from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.service.utils import schemas, crud
# from src.service.utils.OAuth2 import oauth2_scheme
from src.service.utils.db import get_db

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/", response_model=list[schemas.Project])
async def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = await crud.get_projects(db, skip=skip, limit=limit)
    return projects
