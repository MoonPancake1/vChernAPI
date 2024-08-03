from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.service.route.ID.auth import get_current_active_user
from src.service.utils.ID import schemas, crud
from src.service.utils.db import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/check/")
async def check_users(nickname: str | None = None,
                      email: str | None = None,
                      db: Session = Depends(get_db)):
    data = {}
    if nickname:
        username_check = await crud.get_user_by_nickname(db, nickname=nickname)
        data.update({"nickname": bool(username_check)})
    if email:
        email_check = bool(await crud.get_user_by_email(db, email))
        data.update({"email": email_check})
    return data




@router.post("/", response_model=schemas.User)
async def create_user(
        user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Функция для создания пользователя в базе данных
    :param user: данные о пользователе в виде макета UserCreate
    :param db: активная сессия с базой данных
    :return: ошибка (пользователь с почтой или никнеймом уже существует) или процесс создания
    пользователя
    """
    db_user_email = await crud.get_user_by_email(db, email=user.email)
    db_user_nickname = await crud.get_user_by_nickname(db, nickname=user.nickname)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Почта уже привязана!")
    if db_user_nickname:
        raise HTTPException(status_code=400, detail="Никнейм уже существует")
    return await crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User] | dict)
async def read_users(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Функция читает от skip до limit включительно пользователей из базы данных
    и возвращает их в виде списка
    :param skip: сколько пользователей сначала пропустить
    :param limit: сколько всего пользователей вывести
    :param db: активная сессия с базой данных
    :return: Список пользователей
    """
    if current_user.is_admin:
        users = await crud.get_users(db, skip=skip, limit=limit)
        return users
    return {"detail": "Current user is not admin"}


@router.get("/me")
async def read_user_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    """
    Функция, которая возвращает данные о текущем пользователе
    :param current_user: текущий пользователь из get_current_active_user
    :return: объект user
    """
    return current_user


@router.post("/me")
async def update_user_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        new_user_data: schemas.UserUpdate,
        db: Session = Depends(get_db)
):
    check = await check_users(new_user_data.nickname, new_user_data.email, db)
    if new_user_data.nickname:
        if (not check.get("nickname")) and \
                new_user_data.nickname != current_user.nickname:
            current_user.nickname = new_user_data.nickname
        else:
            raise HTTPException(status_code=400,
                                detail="Никнейм уже существует")
    if new_user_data.email:
        if (not check.get("email")) and \
                new_user_data.email != current_user.email:
            current_user.email = new_user_data.email
        else:
            raise HTTPException(status_code=400,
                                detail="Почта уже привязана!")
    if new_user_data.avatar:
        current_user.avatar = new_user_data.avatar
    await crud.update_user_data(db, current_user)
    return {"user": current_user, "result": True}



@router.get("/get/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Функция для просмотра данных о пользователя с определённым id
    :param user_id: пользовательский id
    :param db: активная сессия с базой данных
    :return: найденных пользователь по schemas.User или ошибка (пользователь не найден)
    """
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователя не существует!")
    return db_user
