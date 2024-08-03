from fastapi import APIRouter

from .ID import routes


def get_apps_router():
    """
    Функция для формировния маршрутизатора из разных модулей
    :return: маршрутизатор
    """
    router = APIRouter()
    router.include_router(routes.router)
    return router
