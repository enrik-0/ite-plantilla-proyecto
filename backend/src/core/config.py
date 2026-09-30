from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://app_user:app_password@localhost:5432/app_db"


settings = Settings()
