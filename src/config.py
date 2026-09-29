from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int
    # print("\n\n\n\n",BASE_DIR, "\n\n\n\n")
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )


settings = Settings()
