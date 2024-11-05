from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str


def get_settings() -> Settings:
    return Settings()
