from fastapi import APIRouter
from src.service.route.Main.project import router as project_router


router = APIRouter(prefix="/main", tags=["Main"])

router.include_router(project_router)

