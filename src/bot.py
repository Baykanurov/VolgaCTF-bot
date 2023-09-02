from aiogram import Bot, Dispatcher
from app.config import Config
from app.bot import router
from app import configuration


def run_bot(config: Config):
    bots = [Bot(token) for token in [config.bot.token]]
    dp = Dispatcher()
    dp.include_router(router)
    dp.run_polling(*bots, polling_timeout=1)


if __name__ == '__main__':
    try:
        run_bot(configuration)
    except Exception as error:
        raise
