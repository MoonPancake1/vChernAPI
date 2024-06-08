from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from src.config.project_config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.service.utils import crud, OAuth2, schemas
from src.service.utils.OAuth2 import oauth2_scheme, verify_password
from src.service.utils.db import get_db

router = APIRouter(prefix="/login", tags=["auth"])


async def decode_token(db, token):
    # This doesn't provide any security at all
    # Check the next version
    """
    Функция для декодированя bearer token
    :param db: активная сессия с базой данных
    :param token: токен для декодирования
    :return: объект пользователя
    """
    user = await crud.get_user_by_token(db=db, token=token)
    return user


async def authenticate_user(db, nickname: str, password: str):
    user = await crud.get_user_by_nickname(db, nickname)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
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
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
#                            db: Session = Depends(get_db)):
#     """
#     Функция для получения текущего пользователя после декодирования
#     bearer token
#     :param token: токен авторизации
#     :param db: активная сессия с базой данных
#     :return: объект пользователя
#     """
#     user = await decode_token(db=db, token=token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


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
    form_data: Annotated[OAuth2.OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:
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


# @router.post("/token")
# async def login(form_data: Annotated[OAuth2.OAuth2PasswordRequestForm, Depends()],
#                 db: Session = Depends(get_db)):
#     """
#     Функция аунтификации пользователя в системе
#     :param form_data: данные из формы
#     :param db: активная сессия с базой данных
#     :return: bearer_token
#     """
#     user = await crud.get_user_by_nickname(db=db, nickname=form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     hashed_password = OAuth2.get_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     bearer_token = OAuth2.get_bearer_token(user.nickname, user.hashed_password)
#     return {"access_token": bearer_token, "token_type": "bearer"}

