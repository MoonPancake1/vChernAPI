from hashlib import sha256

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_bearer_token(nickname: str, password: str) -> str:
    """
    Функция для генерации bearer token
    :param nickname: имя пользователя
    :param password: пароль
    :return: bearer token
    """
    hash_first_lvl = sha256(str(nickname).encode('utf-8')).hexdigest()
    hash_second_lvl = sha256(str(password).encode('utf-8')).hexdigest()
    hash_bearer_token = sha256(str(hash_first_lvl + hash_second_lvl).encode('utf-8')).hexdigest()
    return hash_bearer_token


def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
