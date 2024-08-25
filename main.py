from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from src.config.project_config.config import settings
from src.service.route.routes import get_apps_router
from src.service.utils.db import initialize_database

initialize_database()

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
) # Объект API всего приложения

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('vChernID.ico')

origins = [
    "https://id.vchern.me",
    "https://vchern.me",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_apps_router()) # включение маршрутизатора в основное приложение