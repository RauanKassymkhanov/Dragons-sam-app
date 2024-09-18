from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AWS_REGION_NAME: str
    SQS_QUEUE_URL: AnyUrl

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
