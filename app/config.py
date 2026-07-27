from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    GITHUB_TOKEN: str = ""
    WEBHOOK_SECRET: str = ""
    GITHUB_ORG_NAME: str = "szabist-karachi-campus"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()