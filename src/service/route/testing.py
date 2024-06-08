import datetime

from fastapi import APIRouter, Cookie
from starlette.responses import HTMLResponse, JSONResponse

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/cookie")
async def read_items(last_visit: str | None = Cookie(default=None)):
    response = JSONResponse(content={"last_execute": last_visit})
    response.set_cookie(key="last_visit", value=datetime.datetime.now())
    return response


@router.get("/test_upload_files/")
async def main():
    """
    Какая-то тестовая форма для загрузки файлов на сервер
    :return:
    """
    content = """
<body>
<form action="/files/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
<form action="/files/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)