import json
import urllib.parse

from conftest import async_session_maker, client
from pytils.translit import slugify
from sqlalchemy import insert, select
from src.auth.models import Role, User
from src.social.models import Post

TOKEN = ''


async def test_add_role():
    async with async_session_maker() as session:
        list_roles = [
            {"id": 1, "name": "admin", "permissions": None},
            {"id": 2, "name": "user", "permissions": None},
        ]
        stmt = insert(Role).values(list_roles)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        result.all() == [(1, 'admin', None), (2, 'user', None)], "Роль не добавилась"


def test_register():
    response = client.post(
        "/auth/register/",
        json={
            "email": "string@string.py",
            "password": "string",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
    )
    assert response.status_code == 201


async def test_create_user():
    async with async_session_maker() as session:
        query = select(User)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        assert 'string@string.py' in user.email, "User не создался"
        user.is_verified = True
        await session.commit()


def test_login():
    global TOKEN
    data = {
        "username": "string@string.py",
        "password": "string",
    }
    form_data = urllib.parse.urlencode(data)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = client.post(
        "/auth/jwt/login/",
        data=form_data,
        headers=headers
    )
    cookie = response.headers.get('set-cookie', '')
    TOKEN = cookie.split('=')[1].split(';')[0]
    assert response.status_code == 204
    assert "social=" in cookie


def test_get_me():
    client.cookies.set("social", TOKEN)
    response = client.get("/users/me/")

    assert response.status_code == 200

    content = response.content.decode("utf-8")
    data = json.loads(content)
    assert data.get("email") == "string@string.py", "Не верный email"


def test_patch_me():
    client.cookies.set("social", TOKEN)

    json_data = {
        "password": "string",
        "email": "string@string.py",
        "first_name": "new first_name",
        "last_name": "new last_name",
        "birthdate": "2000-07-10",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    }
    response = client.patch("/users/me/", json=json_data)
    assert response.status_code == 200

    content = response.content.decode("utf-8")
    data = json.loads(content)
    assert data.get("first_name") == "new first_name", "Не верный first_name"


def test_post_create():
    client.cookies.set("social", TOKEN)
    for i in range(10):
        json_data = {
            "title": f"test string title {i}",
            "text": f"test string text {i}",
        }
        response = client.post("/posts/", json=json_data)
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        data = json.loads(content)
        assert data['data'].get("title") == json_data["title"]
        assert data['data'].get("text") == json_data["text"]
        assert data['data'].get("slug") == slugify(json_data["title"])


async def test_create_posts():
    async with async_session_maker() as session:
        query = select(Post)
        result = await session.execute(query)
        posts = result.all()
        assert len(posts) == 10


def test_post_patch():
    client.cookies.set("social", TOKEN)
    json_data = {
        "title": "patch test string title ",
        "text": "patch test string text",
    }
    response = client.patch("/posts/1/", json=json_data)
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    data = json.loads(content)
    assert data['data'].get("title") == json_data["title"]
    assert data['data'].get("text") == json_data["text"]
    assert data['data'].get("slug") == slugify(json_data["title"])


def test_logout():
    client.cookies.set("social", TOKEN)
    response = client.post("/auth/jwt/logout/")
    assert response.status_code == 204
