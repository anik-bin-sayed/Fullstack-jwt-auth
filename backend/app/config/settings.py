from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str

    JWT_SECRET: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
