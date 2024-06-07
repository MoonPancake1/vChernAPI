from fastapi import FastAPI

from src.config.project_config import settings
from src.service.route.routes import get_apps_router
from src.service.utils.db import initialize_database

initialize_database()

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION
)

app.include_router(get_apps_router())