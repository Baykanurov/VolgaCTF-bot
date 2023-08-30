from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Bot(BaseModel):
    token: str


class Mongo(BaseModel):
    host: str
    port: str
    db: str


class Config(BaseSettings):
    bot: Bot
    mongo: Mongo

    class Config:
        env_nested_delimiter = '_'
