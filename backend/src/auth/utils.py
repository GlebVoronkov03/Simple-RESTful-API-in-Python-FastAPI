import random
import string

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_async_session
from .models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def generate_password(length: int) -> str:
    characters = string.ascii_letters + string.digits
    password = random.sample(characters, length)
    return ''.join(password)


def get_verify_message(token: str) -> str:
    return """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Verify Token</title>
        <script
          src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js">
        </script>
        <script>
            function verifyToken() {
            var url = 'http://localhost:8000/auth/verify';
            var token = '%s';

            $.ajax({
                type: 'POST',
                url: url,
                headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
                },
                data: JSON.stringify({ token: token }),
                success: function(response) {
                console.log(response);
                // Handle the response here
                },
                error: function(error) {
                console.error(error);
                // Handle the error here
                }
            });
            }
        </script>
        </head>
        <body>
        Подтвердите свой email нажав на кнопку
        <button onclick="verifyToken()">Verify Token</button>
        </body>
        </html>
    """ % token
