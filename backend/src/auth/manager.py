from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, UUIDIDMixin, exceptions, models,
                           schemas)

from ..config import settings
from ..tasks.tasks import send_email
from .models import User
from .utils import get_user_db

SECRET = settings.secret_key


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self,
                                user: User,
                                request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 2

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        sending_data = {
            'email': user.email,
            'subject': 'Подтверждение email',
            'massage': (
                "<strong>"
                "Подтвердите адрес электронной почты введя токен по адресу:"
                "</strong>"
                "http://localhost:8000/verify/"
                "<div>&nbsp;</div>"
                f" <strong><em>Verification token:</em></strong> {token}"
            )
        }
        send_email.delay(sending_data)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
