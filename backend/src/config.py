import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_host: str = os.getenv("POSTGRES_HOST")
    database_port: int = os.getenv("POSTGRES_PORT")
    database_name: str = os.getenv("POSTGRES_DB")
    database_user: str = os.getenv("POSTGRES_USER")
    database_password: str = os.getenv("POSTGRES_PASSWORD")
    secret_key: str = os.getenv("SECRET_KEY")
    redis_url: str = os.getenv("REDIS_URL")
    smtp_user: str = os.getenv("SMTP_USER")
    smtp_password: str = os.getenv("SMTP_PASSWORD")
    smtp_host: str = os.getenv("SMTP_HOST")
    smtp_port: int = os.getenv("SMTP_PORT")
    is_tests: bool = int(os.getenv("IS_TESTS", default=0))
    debug: bool = int(os.getenv("DEBUG", default=0))
    test_database_port: int = os.getenv("TEST_PORT")

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{quote_plus(self.database_user)}'
            f':{quote_plus(self.database_password)}'
            f'@{self.database_host}:{self.database_port}/{self.database_name}')


settings = Settings()
