from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    gemini_api_key: str = Field(min_length=1)
    filename: str = Field("娛樂新聞爬蟲結果.csv")


config = Config()
