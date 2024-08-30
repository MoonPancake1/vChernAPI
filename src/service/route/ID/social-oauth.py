from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import hashlib
import hmac

from src.config.project_config.config import settings
from src.service.utils.ID import schemas, crud
from src.service.utils.db import get_db

BOT_TOKEN_HASH = hashlib.sha256(settings.PROD_TELEGRAM_BOT_TOKEN.encode())
http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/oauth/",
                   tags=["oauth"],
                   dependencies=[Depends(http_bearer)])


# id=611845316
# first_name=Влад
# username=p1n0k10
# photo_url=https%3A%2F%2Ft.me%2Fi%2Fuserpic%2F320%2F9tYstrI3uJIKzzDJCps-YqHbc7cs_GyO7TLj8cjw_Kg.jpg
# photo_url_formated=https://t.me/i/userpic/320/9tYstrI3uJIKzzDJCps-YqHbc7cs_GyO7TLj8cjw_Kg.jpg
# auth_date=1725012189
# hash=a3ce3852544a5830f5db75a0ad8a94ed59a2e40d99ebe1311df6e6e19e92b6b9

@router.post("/telegram/", response_model=schemas.User)
async def create_user(user_tg: schemas.UserCreateTelegram,
                      request: Request,
                      db: Session = Depends(get_db)):
    """
    Функция для создания пользователя в базе данных
    :param user_tg: данные о пользователе в виде макета UserCreate
    :param db: активная сессия с базой данных
    :param request: данные о запросе пользователя
    :return: ошибка (пользователь с почтой или никнеймом уже существует) или процесс создания
    пользователя
    """
    cp_user_tg = user_tg.copy()
    if cp_user_tg.username:
        query_hash = cp_user_tg.hash
        data_check_string = '\n'.join(
            sorted(f'{x}={y}' for x, y in cp_user_tg if x not in
            ('hash', 'next')))
        computed_hash = hmac.new(
            BOT_TOKEN_HASH.digest(),
            data_check_string.encode(),
            'sha256').hexdigest()
        is_correct = hmac.compare_digest(computed_hash, query_hash)
        if not is_correct:
            raise HTTPException(status_code=403, detail='Telegram HASH problem')
    return await crud.create_user_telegram(db=db, user_tg=cp_user_tg)
