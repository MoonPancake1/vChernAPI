from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/test_upload_files/")
async def main():
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