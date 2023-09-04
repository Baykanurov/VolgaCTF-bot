import gspread
import mongoengine
from functools import lru_cache
from pathlib import Path
from .config import Config
from .logger import logger_conf


@lru_cache()
def get_config() -> Config:
    return Config()


configuration = get_config()

gc = gspread.service_account(filename=str(Path(configuration.table.config)))
sh = gc.open(title=configuration.table.name)
worksheet = sh.worksheet(configuration.table.worksheet)

mongoengine.connect(
    host=f'mongodb://{configuration.mongo.host}:'
         f'{configuration.mongo.port}/{configuration.mongo.db}'
)
