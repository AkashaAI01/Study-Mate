from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Study Mate"
    agent_name: str = "AK"
    app_version: str = "1.0.0"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
