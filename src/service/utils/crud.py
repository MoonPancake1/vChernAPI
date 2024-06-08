from hashlib import sha256
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from src.service.utils import models, schemas, OAuth2
from src.service.utils.OAuth2 import get_bearer_token, oauth2_scheme


async def get_user(db: Session, user_id: int):
    """
    Функция для нахождения пользователя по его id
    :param db: активная сессия с базой данных
    :param user_id: id пользователя
    :return: запись из базы данных о пользователе или None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_nickname(db: Session, nickname: str):
    """
    Функция для нахождения пользователя по его имени
    :param db: активная сессия с базой данных
    :param nickname: имя пользователя
    :return: запись из базы данных о пользователе или None
    """
    return db.query(models.User).filter(models.User.nickname == nickname).first()


async def get_user_by_email(db: Session, email: str):
    """
    Функция для нахождения пользователя в базе данных по его почте
    :param db: активная сессия с базой данных
    :param email: почта пользователя
    :return: запись из базы данных о пользователе или None
    """
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_token(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Функция для поиска пользователя по его bearer token
    :param db: активная сессия с базой данных
    :param token: токен авторизации пользователя
    :return: запись из базы данных о пользователе или None
    """
    return db.query(models.User).filter(models.User.bearer_token == token).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Функция для выдачи определённого кол-ва пользователей из базы данных
    :param db: активная сессия с базой данных
    :param skip: сколько пользователей пропустить
    :param limit: кол-во пользователей в ответе
    :return: список пользователей
    """
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: schemas.UserCreate):
    """
    Функция для создания пользователя в базе данных
    :param db: активная сессия с базой данных
    :param user: объект user по макету schemas.UserCreate
    :return: данные о пользователе
    """
    hashed_password = OAuth2.get_hash_password(user.password)
    db_user = models.User(
        uuid_user=str(uuid4()),
        email=user.email,
        nickname=user.nickname,
        hashed_password=hashed_password,
        bearer_token=get_bearer_token(user.nickname, hashed_password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """
    Функция для выдачи определённого кол-ва проектов
    :param db: активная сессия с базой данных
    :param skip: сколько проектов с начала пропустить
    :param limit: кол-во проектов в ответе
    :return: список проектов
    """
    return db.query(models.Project).offset(skip).limit(limit).all()


async def create_user_project(db: Session, project: schemas.ProjectCreate, author_id: int):
    """
    Функция для создания проекта
    :param db: активная сессия с базой данных
    :param project: объект project по макету schemas.ProjectCreate
    :param author_id: id пользователя
    :return: данные о проекте по макету schemas.Project
    """
    db_project = models.Project(**project.dict(), author_id=author_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
