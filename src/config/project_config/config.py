from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool
    VERSION: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DB_ENGINE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    API_URL: str
    # TEST DATA
    TEST_DB_HOST: str

    model_config = SettingsConfigDict(env_file=".env")


class DataBaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # TEST DATA
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env.db")


settings = Settings()
database = DataBaseSettings()

