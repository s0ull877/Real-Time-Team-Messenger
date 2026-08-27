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

    db_password: str = Field(alias="POSTGRES_PASSWORD")
    db_user: str = Field(alias="POSTGRES_USER")
    db_name: str = Field(alias="POSTGRES_DB")
    db_host: str = Field(alias="POSTGRES_HOST")
    db_port: str = Field(alias="POSTGRES_PORT")
    db_engine: str = Field(alias="DB_ENGINE")

    @property
    def database_url(self) -> str:
        return f"{self.db_engine}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    
settings: Settings | None = None


def get_settings() -> Settings:
    """
    Возвращает глобальные настройки проекта
    """
    global settings

    if not settings:
        settings = Settings()

    return settings