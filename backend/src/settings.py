from pydantic import ConfigDict
from pydantic.v1 import BaseSettings

from settings.config import DB_USER, DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME


class Settings(BaseSettings):
    model_config = ConfigDict(extra='allow')
    server_host: str = 'localhost'
    server_port: int = 8000
    database_url: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
