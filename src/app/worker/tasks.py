import asyncio
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from .services import _send_task
from ...worker import celery
from .. import configuration


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(25, send_task.s())


@celery.task
def send_task(*args, **kwargs):
    session = AiohttpSession()
    task = _send_task(Bot(token=configuration.bot.token, session=session))
    return asyncio.get_event_loop().run_until_complete(task)
