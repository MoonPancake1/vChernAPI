from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.service.route.auth import get_current_active_user
from src.service.utils import schemas, crud, models
from src.service.utils.OAuth2 import oauth2_scheme
from src.service.utils.db import get_db

router = APIRouter(prefix="/users", tags=["users"])


# Todo: Написать функцию проверки пользователя на администратора
# def is_admin():
#     return User(id=1)


@router.post("/", response_model=schemas.User)
async def create_user(
        # token: Annotated[str, Depends(oauth2_scheme)],
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


@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Функция читает от skip до limit включительно пользователей из базы данных
    и возвращает их в виде списка
    :param skip: сколько пользователей сначала пропустить
    :param limit: сколько всего пользователей вывести
    :param db: активная сессия с базой данных
    :return: Список пользователей
    """
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me")
async def read_users_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    """
    Функция, которая возвращает данные о текущем пользователе
    :param current_user: текущий пользователь из get_current_active_user
    :return: объект user
    """
    return current_user


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


@router.post("/{author_id}/project/", response_model=schemas.Project)
async def create_project_for_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        author_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    """
    Функция для создания проекта пользователя
    :param token: токен авторизации пользователя
    :param author_id: id пользователя
    :param project: объект Project в макете schemas.Project
    :param db: активная сессия с базой данных
    :return: процесс создания проекта в базе данных
    """
    return await crud.create_user_project(db=db, project=project, author_id=author_id)

# @router.get("")
# async def exists_category_for_name(name: str, user: User = Depends(is_admin)) -> bool:
#     try:
#         return await category_service.exists(name)
#     except Exception as e:
#         raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
