from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION_NAME: str
    SQS_QUEUE_URL: AnyUrl


settings = Settings()
