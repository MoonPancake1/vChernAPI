from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from src.config.project_config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.service.utils import crud, OAuth2, schemas
from src.service.utils.OAuth2 import oauth2_scheme, verify_password
from src.service.utils.db import get_db

router = APIRouter(prefix="/login", tags=["auth"])


async def decode_token(db, token):
    """
    Функция для декодированя bearer token
    :param db: активная сессия с базой данных
    :param token: токен для декодирования
    :return: объект пользователя
    """
    user = await crud.get_user_by_token(db=db, token=token)
    return user


async def authenticate_user(db, nickname: str, password: str):
    """
    Функция для аунтефикации пользователя
    :param db: активная сессия с базой данных
    :param nickname: имя пользователя
    :param password: пароль пользователя
    :return: объект пользователя
    """
    user = await crud.get_user_by_nickname(db, nickname)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    """
    Функция для получения текущего пользователя после декодирования
    bearer token
    :param token: токен авторизации
    :param db: активная сессия с базой данных
    :return: объект пользователя
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.get_user_by_nickname(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Функция для создания JWT токена авторизации
    :param data: данные о пользователе
    :param expires_delta: длительность жизни токена в минутах
    :return: JWT токен авторизации
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    """
    Функция проверяет аккаунт пользователя на деактивацию
    :param current_user: объект пользователя
    :return: Если пользователь активен, то объект пользователя, иначе ошибку
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:
    """
    Функция для авторизации пользователя
    :param form_data: данные о пользователе
    :param db: активная сессия с базой данных
    :return: JWT токен авторизации
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nickname}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
