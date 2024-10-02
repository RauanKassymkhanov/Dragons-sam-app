from pydantic_settings import BaseSettings


class BaseSettingsConfig(BaseSettings):
    AWS_REGION_NAME: str


settings = BaseSettingsConfig()
