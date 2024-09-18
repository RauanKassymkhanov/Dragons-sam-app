from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AWS_REGION_NAME: str
    TABLE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
