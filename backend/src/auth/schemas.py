import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from fastapi_users import schemas
from pydantic import Field, validator

from .utils import generate_password


class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    email: str
    first_name: str
    last_name: str
    birthdate: Optional[datetime.date]
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    email: str = Field("string@string.py", min_length=5)
    password: str = Field(generate_password(10), min_length=5)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    @validator('password')
    def validate_password(password: str):
        simple_passwords = ['password', '123456', 'qwerty', 'admin']
        if password.lower() in simple_passwords:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too simple"
            )

        if len(set(password)) < len(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot have repeated characters"
            )
        return password


class UserUpdate(schemas.BaseUserUpdate):
    password: str
    email: str
    first_name: str
    last_name: str
    birthdate: Optional[datetime.date]
