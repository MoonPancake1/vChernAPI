from fastapi import APIRouter
from src.service.route.ID.auth import router as auth_router
from src.service.route.ID.files import router as files_router
from src.service.route.ID.users import router as users_router
from src.service.route.ID.testing import router as testing_router
from src.service.route.ID.social_oauth import router as social_oauth_router

router = APIRouter(prefix="/id", tags=["ID"])

router.include_router(auth_router)
router.include_router(files_router)
router.include_router(users_router)
router.include_router(testing_router)
router.include_router(social_oauth_router)
