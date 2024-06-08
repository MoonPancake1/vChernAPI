from hashlib import sha256
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from src.service.utils import models, schemas, OAuth2
from src.service.utils.OAuth2 import get_bearer_token, oauth2_scheme


async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_nickname(db: Session, nickname: str):
    return db.query(models.User).filter(models.User.nickname == nickname).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_token(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    return db.query(models.User).filter(models.User.bearer_token == token).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: schemas.UserCreate):
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
    return db.query(models.Project).offset(skip).limit(limit).all()


async def create_user_project(db: Session, project: schemas.ProjectCreate, author_id: int):
    db_project = models.Project(**project.dict(), author_id=author_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
