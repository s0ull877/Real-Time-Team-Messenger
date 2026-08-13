import logging
from pathlib import Path


from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):


    # для локальной
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[5] / ".env"
    )
    # для Docker compose
    # model_config = SettingsConfigDict( 
    #     env_file=".env", extra="ignore", 
    # )
    
    app_name: str = Field(alias="APP_NAME")
    app_env: str = Field(alias="APP_ENV")
    app_host: str = Field(alias="APP_HOST")
    app_port: int = Field(alias="APP_PORT")
    debug: bool = Field(alias="DEBUG")

settings: Settings | None = None


def get_settings() -> Settings:
    """
    Возвращает глобальные настройки проекта
    """
    global settings

    if not settings:
        logging.warning(Path(__file__))
        settings = Settings()
    return settings