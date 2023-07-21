from fastapi import APIRouter

from .auth.routers import auth_router, user_router
from .social.routers import router as social_router
from .tasks.routers import router as tasks_router

routers = APIRouter()

routers.include_router(auth_router, prefix="/auth", tags=["authentication"])
routers.include_router(user_router, prefix="/users", tags=["users"])
routers.include_router(
    social_router, prefix="/posts", tags=["social_networking"]
)
routers.include_router(tasks_router, prefix="/tasks", tags=["celery_tasks"])
