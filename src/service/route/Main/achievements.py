from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.service.route.ID.auth import get_current_active_user
from src.service.utils.Main import schemas, crud
from src.service.utils.db import get_db

router = APIRouter(prefix="/achievement", tags=["achievement"])


@router.post('/')
async def create_achievement(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                             achievement: schemas.Achievement,
                             db: Session = Depends(get_db)):
    if current_user:
        if current_user.is_admin:
            return await crud.create_achievement(db=db, achievement=achievement)
        else:
            return HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    else:
        return HTTPException(status_code=404, detail="Пользователь не найден!")


@router.get('/')
async def get_achievements(db: Session = Depends(get_db)):
    return await crud.get_achievements(db=db)


@router.get('/{achievement_id}/')
async def get_achievement(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                          achievement_id: int,
                          db: Session = Depends(get_db)):
    db_achievement = await crud. get_achievement_by_id(db, achievement_id)
    if not db_achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено!")
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    return db_achievement


@router.put('/{achievement_id}/')
async def update_achievement(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                             achievement_id: int,
                             new_achievement: schemas.AchievementUpdate,
                             db: Session = Depends(get_db)):
    achievement = await crud.get_achievement_by_id(db, achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено!")
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    return await crud.update_achievement(db, achievement, new_achievement)


@router.delete('/{achievement_id}/')
async def delete_achievement(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                             achievement_id: int,
                             db: Session = Depends(get_db)):
    achievement = await crud.get_achievement_by_id(db, achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Достижение не найдено!")
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Данный пользователь не обладает нужными правами доступа!")
    return await crud.delete_achievement_by_id(db, achievement)
