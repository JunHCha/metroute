from pydantic import BaseSettings


class Settings(BaseSettings):
    ODSAY_API_KEY: str


settings = Settings()
