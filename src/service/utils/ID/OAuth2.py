from datetime import timedelta, datetime, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.config.project_config.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/id/login/tokens")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta | None = None):
    """
    Функция для создания JWT
    :param data: данные о пользователе
    :param expires_delta: длительность жизни токена в минутах
    :return: JWT токен авторизации
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict,
                        expires_delta: timedelta | None = None):
    """
    Функция для создания access_token
    """
    if expires_delta:
        expires_delta = timedelta(minutes=
                                  settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expires_delta = timedelta(minutes=60)
    return create_token(data, expires_delta)


def create_refresh_token(data: dict,
                         expires_delta: timedelta | None = None):
    """
    Функция для создания refresh_token
    """
    if expires_delta:
        expires_delta = timedelta(days=
                                  settings.REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        expires_delta = timedelta(days=30)
    return create_token(data, expires_delta)


def create_tokens(user_uuid: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"type": "access",
              "sub": user_uuid},
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"type": "refresh",
              "sub": user_uuid}, expires_delta=refresh_token_expires
    )
    return access_token, refresh_token