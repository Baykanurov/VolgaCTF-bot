import mongoengine
from aiogram import Bot, Dispatcher
from functools import lru_cache
from config import Config
from bot import router


@lru_cache()
def get_config():
    return Config()


def mongo_init(config: Config):
    return mongoengine.connect(
        host=f'mongodb://{config.mongo.host}:{config.mongo.port}/{config.mongo.db}'
    )


def run_bot(config: Config):
    bots = [Bot(token) for token in [config.bot.token]]
    dp = Dispatcher()
    dp.include_router(router)
    dp.run_polling(*bots, polling_timeout=1)


if __name__ == '__main__':
    try:
        configuration = get_config()
        mongo_init(configuration)
        run_bot(configuration)
    except Exception as error:
        raise
