from base.config import BaseSettingsConfig


class StreamHandlerSettings(BaseSettingsConfig):
    SQS_QUEUE_URL: str


settings = StreamHandlerSettings()
