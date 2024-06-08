from fastapi import APIRouter

from . import users, project, files, testing, auth


def get_apps_router():
    router = APIRouter()
    router.include_router(auth.router)
    router.include_router(users.router)
    router.include_router(project.router)
    router.include_router(files.router)
    router.include_router(testing.router)
    return router
