from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import hashlib
import hmac
import json
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
    user = await crud.get_user_by_social_id(db, user_tg.id, social='tg')
    if not user:
        user = await crud.create_user_oauth(db=db, user=user_tg, social='tg')
    access_token, refresh_token = create_tokens(user_tg.id)
    return RedirectResponse(f"https://vchern.me/auth?access_token={access_token}&refresh_token={refresh_token}")


@router.get('/vk/')
async def auth_vk(
        user_id: str,
        first_name: str,
        last_name: str,
        avatar: str,
        db: Session = Depends(get_db)
):
    user_vk = schemas.UserVK(
        id=user_id,
        username=f"{first_name} {last_name}",
        photo_url=avatar,
    )

    user = await crud.get_user_by_social_id(db, user_vk.id, social='vk')
    if not user:
        user = await crud.create_user_oauth(db=db, user=user_vk, social='vk')
    access_token, refresh_token = create_tokens(user_vk.id)

    return RedirectResponse(f"https://vchern.me/auth?access_token={access_token}&refresh_token={refresh_token}")
