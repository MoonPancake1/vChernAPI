from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware

from src.config.project_config.config import settings
from src.service.route.routes import get_apps_router
from src.service.utils.db import initialize_database

initialize_database()

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    # openapi_url=settings.API_URL,
    # docs_url=settings.API_URL + 'docs/',
) # Объект API всего приложения

app.mount("/static", StaticFiles(directory="static"), name="static")

# origins = [
#     "http://api.vchern.me",
#     "https://api.vchern.me",
#     "http://localhost",
#     "http://localhost:8080",
# ]
#
# origins_regex = [
#     "http://*\.vchern\.me",
#     "https://*\.vchern\.me",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_origin_regex=origins_regex,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(get_apps_router()) # включение маршрутизатора в основное приложение