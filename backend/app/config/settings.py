from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str

    JWT_SECRET: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    SECRET_KEY: str
    ALGORITHM: str

    FRONTEND_URL: str = "http://localhost:3000"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    class Config:
        env_file = ".env"


settings = Settings()
