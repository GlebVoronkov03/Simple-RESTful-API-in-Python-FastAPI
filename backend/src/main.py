from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from .config import settings
from .routers import routers
from .tasks.tasks import celery
from .utils import create_roles

description = """
Simple RESTfull API using FastAPI for a social networking application. 🚀
"""

app = FastAPI(
    title="Social networking",
    description=description,
    version="1.0.0",
    terms_of_service="http://localhost:8000/",
    contact={
        "name": "Borokin Andrey",
        "url": "https://github.com/exp-ext",
        "email": "ext77@yandex.ru",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PATCH",
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"
    ],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_roles()


@app.on_event("startup")
def configure_celery():
    if settings.debug:
        celery.conf.task_always_eager = True
        celery.conf.task_eager_propagates = True
        celery.conf.task_ignore_result = True


app.include_router(routers)
