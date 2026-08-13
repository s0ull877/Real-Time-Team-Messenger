from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent.parent.parent.parent / ".env"
    )
    
    app_name: str = Field(alias="APP_NAME")
    app_env: str = Field(alias="APP_ENV")

settings: Settings | None = None


def get_settings() -> Settings:
    """
    Возвращает глобальные настройки проекта
    """
    global settings

    if not settings:
        settings = Settings()
    return settings