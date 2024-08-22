from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from src.service.route.ID.auth import get_current_active_user
from src.service.utils.Main import schemas, crud
from src.service.utils.db import get_db

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/{project_id}/")
async def read_comments(project_id: int,
        db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return await crud.get_comments(db, project.id)


@router.post("/")
async def create_comment(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                         comment: schemas.CommentCreate,
                         db: Session = Depends(get_db)):
    project = await crud.get_project_by_id(db, comment.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return await crud.create_comment(db, comment, current_user)


@router.put("/")
async def update_comment(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                         new_comment: schemas.CommentUpdate,
                         db: Session = Depends(get_db)):
    comment = await crud.get_comment_by_id(db, new_comment.comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден!")
    if comment.user_uuid == current_user.uuid or current_user.is_admin:
        return await crud.update_comment(db, comment, new_comment)
    raise HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")


@router.delete("/{comment_id}/")
async def delete_comment(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        comment_id: int,
                        db: Session = Depends(get_db)):
    comment = await crud.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден!")
    if comment.user_uuid == current_user.uuid or current_user.is_admin:
        return await crud.delete_comment_by_id(db, comment)
    raise HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
