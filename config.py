import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pyrogram import Client


class Config(BaseSettings):
    DB_URL: str
    FOLDER_ID: int
    clients: list
    api_id: int | None 
    api_hash: str | None 

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__name__), ".env"),
        env_file_encoding="utf-8"
    )


config = Config()