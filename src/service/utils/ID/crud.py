from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from src.service.utils.ID import models, OAuth2, schemas
from src.service.utils.ID.OAuth2 import oauth2_scheme


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


async def get_user_by_uuid(db: Session, uuid: str):
    """
    Функция возвращает пользователя с определённыйм uuid
    """
    return db.query(models.User).filter(models.User.uuid == uuid).first()


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
    uuid = str(uuid4())
    hashed_password = OAuth2.get_password_hash(user.password)
    db_user = models.User(
        uuid=uuid,
        email=user.email,
        nickname=user.nickname,
        hashed_password=hashed_password,
        ip=user.ip,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user_data(db: Session,
                           current_user: schemas.UserUpdate) -> [bool, str]:
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user.nickname = current_user.nickname
    user.email = current_user.email
    user.avatar = current_user.avatar
    db.commit()
    return user


async def get_user_by_social_id(db: Session, social_id: str, social: str):
    """
    Функция возвращает пользователя с определённыйм social_id
    """

    if social == 'vk':
        return db.query(models.User).filter(models.User.vk_id == social_id).first()
    elif social == 'tg':
        return db.query(models.User).filter(models.User.tg_id == social_id).first()


async def create_user_oauth(db: Session, user: schemas.UserTelegram | schemas.UserVK,
                            social: str):
    uuid = str(uuid4())
    if social == 'vk':
        db_user = models.User(
            uuid=uuid,
            nickname=user.username,
            avatar=user.photo_url,
            vk_id=str(user.id),
        )
    elif social == 'tg':
        db_user = models.User(
            uuid=uuid,
            nickname=user.username,
            avatar=user.photo_url,
            tg_id=str(user.id),
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
