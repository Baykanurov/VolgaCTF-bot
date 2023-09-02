from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Bot(BaseModel):
    token: str


class Mongo(BaseModel):
    host: str
    port: str
    db: str


class Table(BaseModel):
    config: str
    name: str
    worksheet: str


class Config(BaseSettings):
    bot: Bot
    mongo: Mongo
    table: Table

    class Config:
        env_nested_delimiter = '_'
