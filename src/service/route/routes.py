from fastapi import APIRouter

from .ID import routes as IDRoutes
from .Main import routes as MainRoutes


def get_apps_router():
    """
    Функция для формировния маршрутизатора из разных модулей
    :return: маршрутизатор
    """
    router = APIRouter()
    router.include_router(IDRoutes.router)
    router.include_router(MainRoutes.router)
    return router
