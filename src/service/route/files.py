import uuid

import aiofiles
from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/uploadfile/")
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


@router.post("/uploadfiles/")
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

