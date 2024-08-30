from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, APIRouter, status, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from fastapi.responses import HTMLResponse

from src.config.project_config.config import settings
from src.service.utils.ID import schemas, crud
from src.service.utils.ID.OAuth2 import oauth2_scheme, verify_password, create_access_token, create_tokens
from src.service.utils.db import get_db
from src.templates.template_init import templates

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/login",
                   tags=["auth"],
                   dependencies=[Depends(http_bearer)])


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


async def get_current_user_by_token(token: Annotated[str, Depends(oauth2_scheme)],
                                    token_type: str,
                                    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные пользователя!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    incorrect_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Некорректный тип токена авторизации!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") == token_type:
            uuid: str = payload.get("sub")
            if uuid is None:
                raise credentials_exception
            token_data = schemas.TokenData(uuid=uuid)
        else:
            raise incorrect_token_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.get_user_by_uuid(db, token_data.uuid)
    if user is None:
        print(user)
        raise credentials_exception
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
    user = await get_current_user_by_token(token, token_type="access", db=db)
    return user


async def get_current_user_for_refresh(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    """
        Функция для получения текущего пользователя после декодирования
        bearer token
        :param token: токен авторизации
        :param db: активная сессия с базой данных
        :return: объект пользователя
        """
    user = await get_current_user_by_token(token, token_type="refresh", db=db)
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    """
    Функция проверяет аккаунт пользователя на деактивацию
    :param current_user: объект пользователя
    :return: Если пользователь активен, то объект пользователя, иначе ошибку
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь деактивирован!")
    return current_user


@router.post("/refresh/",
             response_model=schemas.Token,
             response_model_exclude_none=True)
async def auth_refresh_jwt(user: Annotated[schemas.User, Depends(get_current_user_for_refresh)], ):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"type": "access",
              "sub": user.nickname,
              "email": user.email},
        expires_delta=access_token_expires)

    return schemas.Token(access_token=access_token)


@router.post("/tokens/")
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
            detail="Неверный логин или пароль!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = create_tokens(user.uuid)

    return schemas.Token(access_token=access_token,
                         refresh_token=refresh_token)


@router.get("/", response_class=HTMLResponse)
async def form_for_auth(request: Request):
    return templates.TemplateResponse(
        request=request, name="login_page.html"
    )