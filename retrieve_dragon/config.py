from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION_NAME: str
    TABLE_NAME: str


settings = Settings()
