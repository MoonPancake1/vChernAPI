from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from src.service.utils import crud, OAuth2, schemas
from src.service.utils.OAuth2 import oauth2_scheme
from src.service.utils.db import get_db

router = APIRouter(prefix="/login", tags=["auth"])


async def decode_token(db, token):
    # This doesn't provide any security at all
    # Check the next version
    user = await crud.get_user_by_token(db=db, token=token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    user = await decode_token(db=db, token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2.OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    user = await crud.get_user_by_nickname(db=db, nickname=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = OAuth2.get_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    bearer_token = OAuth2.get_bearer_token(user.nickname, user.hashed_password)
    return {"access_token": bearer_token, "token_type": "bearer"}

