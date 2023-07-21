from fastapi import APIRouter

from .auth_config import auth_backend, fastapi_users
from .schemas import UserCreate, UserRead, UserUpdate

auth_router = APIRouter()
user_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)

auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

user_router.include_router(
    fastapi_users.get_users_router(
        UserRead, UserUpdate, requires_verification=True
    ),
)
