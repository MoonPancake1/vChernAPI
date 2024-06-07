import uuid
from typing import Annotated

import aiofiles
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

import crud
import models
import schemas
from db import SessionLocal, engine
from src.config.project_config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


############################ Code for Users ##############################

@app.post("/users/", response_model=schemas.User)
async def create_user(token: Annotated[str, Depends(oauth2_scheme)],
    user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = await crud.get_user_by_email(db, email=user.email)
    db_user_nickname = await crud.get_user_by_nickname(db, nickname=user.nickname)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Почта уже привязана!")
    if db_user_nickname:
        raise HTTPException(status_code=400, detail="Никнейм уже существует")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователя не существует!")
    return db_user

##########################################################################

########################### Code for Project #############################

@app.post("/users/{user_id}/project/", response_model=schemas.Project)
async def create_project_for_user(
    author_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return crud.create_user_project(db=db, project=project, author_id=author_id)


@app.get("/project/", response_model=list[schemas.Project])
async def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = await crud.get_projects(db, skip=skip, limit=limit)
    return projects

##########################################################################

############################ Code for Files ##############################

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"result": "error",
                "message": "No upload file sent"}
    else:
        file_path = "src/static/img/"
        file_name = f"{uuid.uuid4()}.{file.content_type.split('/')[1]}"
        full_file_name = file_path + file_name
        async with aiofiles.open(full_file_name, "wb") as out_file:
            content = await file.read()  # Асинхронно читаем данные из файла
            await out_file.write(content)  # Асинхронно записываем файл на сервер
        return {"result": "ok"}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    if len(files) == 0:
        return {"result": "error",
        "message": "No upload files sent"}
    else:
        for file in files:
            file_path = "src/static/img/"
            file_name = f"{uuid.uuid4()}.{file.content_type.split('/')[1]}"
            full_file_name = file_path + file_name
            async with aiofiles.open(full_file_name, "wb") as out_file:
                content = await file.read()  # Асинхронно читаем данные из файла
                await out_file.write(content)  # Асинхронно записываем файл на сервер
        return {"result": "ok"}

##########################################################################

############################## Test Code #################################

@app.get("/test_upload_files/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

##########################################################################