from uuid import UUID

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from ..config import settings
from .manager import get_user_manager
from .models import User

cookie_transport = CookieTransport(cookie_name="social", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

current_active_verified_user = fastapi_users.current_user(
    active=True, verified=True
)
