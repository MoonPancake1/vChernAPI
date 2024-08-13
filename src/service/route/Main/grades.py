from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.service.route.ID.auth import get_current_active_user
from src.service.utils.Main import schemas, crud
from src.service.utils.db import get_db


router = APIRouter(prefix="/grade", tags=["grade"])


@router.post("/")
async def create_grade(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                       grade: schemas.GradeCreate,
                       db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, grade.project_id)
    if not project:
        return HTTPException(status_code=404, detail="Проект не найден!")
    grade = await crud.create_grade_project(db, grade, current_user)
    return grade


@router.get("/{project_id}/")
async def get_grades(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                    project_id: int,
                    db: Session = Depends(get_db)):
    if current_user.is_admin:
        grades = await crud.get_grades_project_by_id(db, project_id)
        return grades
    else:
        return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")


@router.put("/")
async def update_grade(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        new_grade: schemas.GradeUpdate,
                        db: Session = Depends(get_db)):
    grade = await crud.get_grade_by_id(db, new_grade.grade_id)
    if grade.user_uuid == current_user.uuid or current_user.is_admin:
        return await crud.update_grade(db, grade, new_grade)
    else:
        return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")


@router.delete("/{grade_id}/")
async def delete_grade(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                       grade_id: int,
                       db: Session = Depends(get_db)):
    grade = await crud.get_grade_by_id(db, grade_id)
    if grade.user_uuid == current_user.uuid or current_user.is_admin:
        return await crud.delete_grade_by_id(db, grade)
    else:
        return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
