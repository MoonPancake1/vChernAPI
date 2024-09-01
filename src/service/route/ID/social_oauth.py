from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import hashlib
import hmac
import requests

from src.config.project_config.config import settings
from src.service.utils.ID import schemas, crud
from src.service.utils.ID.OAuth2 import create_tokens
from src.service.utils.db import get_db
from src.service.utils.ID.vk_auth_utils import get_code_verifier

BOT_TOKEN_HASH = hashlib.sha256(settings.PROD_TELEGRAM_BOT_TOKEN.encode())
http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/oauth",
                   tags=["oauth"],
                   dependencies=[Depends(http_bearer)])


# id=611845316
# first_name=Влад
# username=p1n0k10
# photo_url=https%3A%2F%2Ft.me%2Fi%2Fuserpic%2F320%2F9tYstrI3uJIKzzDJCps-YqHbc7cs_GyO7TLj8cjw_Kg.jpg
# photo_url_formated=https://t.me/i/userpic/320/9tYstrI3uJIKzzDJCps-YqHbc7cs_GyO7TLj8cjw_Kg.jpg
# auth_date=1725012189
# hash=a3ce3852544a5830f5db75a0ad8a94ed59a2e40d99ebe1311df6e6e19e92b6b9

@router.get("/telegram/", response_model=schemas.Token)
async def auth_tg_user(id: str,
                      first_name: str,
                      username: str,
                      photo_url: str,
                      auth_date: int,
                      hash: str,
                      db: Session = Depends(get_db)):
    user_tg = schemas.UserTelegram(
        id=id,
        first_name=first_name,
        username=username,
        photo_url=photo_url,
        auth_date=auth_date,
        hash=hash
    )
    if user_tg.username:
        query_hash = user_tg.hash
        data_check_string = '\n'.join(
            sorted(f'{x}={y}' for x, y in user_tg if x not in ('hash', 'next'))
        )
        computed_hash = hmac.new(
            BOT_TOKEN_HASH.digest(),
            data_check_string.encode(),
            'sha256').hexdigest()
        is_correct = hmac.compare_digest(computed_hash, query_hash)
        if not is_correct:
            raise HTTPException(status_code=403, detail='Telegram HASH problem')
    user = await crud.get_user_by_uuid(db, user_tg.id)
    if not user:
        user = await crud.create_user_telegram(db=db, user_tg=user_tg)
    access_token, refresh_token = create_tokens(user_tg.id)
    return RedirectResponse(f"https://vchern.me/auth?access_token={access_token}&refresh_token={refresh_token}")


@router.get('/vk/')
async def auth_vk(code: str,
                  expires_in: int,
                  device_id: str,
                  state: str,
                  ext_id: str,
                  type: str):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = {
        "grant_type": "authorization_code",
        "code_verifier": get_code_verifier(),
        "redirect_uri": settings.VK_ID_AUTH_REDIRECT,
        "code": code,
        "client_id": settings.VK_ID_CLIENT,
        "device_id": device_id,
        "state": state,
    }
    r = requests.post("https://id.vk.com/oauth2/auth", params=params, headers=headers)
    print(r.json())
    raise HTTPException(status_code=404, detail='Тестирую... Пока можно войти с помощью тг)')
