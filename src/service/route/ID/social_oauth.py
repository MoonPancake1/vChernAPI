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


# code=vk2.a.8WieYarpcsfYSeDD1nMrSuQB0yCuhlYWdyidsAKm4Gvjvyxz0TExsYywvBCwk80qPDnX4KnzucuTkMDiLaj3JCjLgAacneEKGjCKUzccLnkbt8pVf86zSO7dc_2Jhb9pVapIFNHYV0fub9I_dEDt_vILVoyXcsNW4A3rwQB0O0vUeci3M3lU0qKR5irxMcnccgnSh3MPGhCd73YnMsK7JA
# &expires_in=600
# &device_id=v4l6_5Eex2Tj_X5e23iDixocscvM-ubJLOO99Phb3ZYcKykSh_oMJGDWAoM2lhC_WmKKW2qNkzyiXPDbV6N4qA
# &state=lAMllcvpSo2u-3nQQ7YSOnUhocSt9-MENQo1cXpNhq6Vecc2
# &ext_id=nDEqy33xbzLSRcxwXbTxYyHBdlpbsaR5Ra_RwLo4ODSPjb2N15rjTf-Y9b3D71FN-8Al1aeLdc00oTRemYZzCu1eD0ZgEtSwHwGFqtjOW8_jAdh5CPVk7y7jnG-_8D6ssSaEigQGvyl_7gEWive2T52KIx3uxrUY1YFYMcKm-JYq-A
# &type=code_v2
@router.get('/vk/', response_model=schemas.Token)
async def auth_vk(code: str,
                  expires_in: int,
                  device_id: str,
                  state: str,
                  ext_id: str,
                  type: str):
    params = {
        "client_id": device_id,
        "access_token": code,
    }
    r = requests.post("https://id.vk.com/oauth2/user_info", params=params)
    print(r.json())
    return HTTPException(status_code=404, detail='Тестирую... Пока можно войти с помощью тг)')
