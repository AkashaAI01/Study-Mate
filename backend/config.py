from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Study Mate"
    agent_name: str = "AK"
    app_version: str = "1.0.0"
    debug: bool = False

    # Secrets and private values. They come from .env only, never from code.
    groq_api_key: SecretStr = SecretStr("")
    drive_api_key: SecretStr = SecretStr("")
    drive_folder_id: str = ""
    owner_number: str = ""
    bot_number: str = ""
    adapter_shared_secret: SecretStr = SecretStr("")
    master_owner_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()