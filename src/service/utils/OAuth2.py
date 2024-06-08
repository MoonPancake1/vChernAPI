from hashlib import sha256

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


def get_hash_password(password: str) -> str:
    """
    Функция для генерации hash для пароля
    :param password: пароль пользователя
    :return: hash этого пароля
    """
    hash_first_lvl = sha256(str(password).encode('utf-8')).hexdigest()
    hash_password = sha256(str(hash_first_lvl + "52462595-7682-4132-bf80-cc41ee4086cf")
                           .encode('utf-8')).hexdigest()
    return hash_password


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
