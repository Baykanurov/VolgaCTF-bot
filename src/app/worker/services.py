import asyncio
import logging
from aiogram import Bot
from aiogram.exceptions import AiogramError
from aiogram.client.session.aiohttp import AiohttpSession
from gspread import Worksheet
from ..mongo import get_users
from ..table import Tasks, check_task, update_status


logger = logging.getLogger(__name__)


class BaseTelegramError(Exception):
    pass


class TelegramManager:
    def __init__(self, token: str):
        session = AiohttpSession()
        self.bot = Bot(token=token, session=session)

    def get_bot(self):
        try:
            return self.bot
        except KeyError:
            raise BaseTelegramError

    def send_message(self, chat_id: int, text: str, photo: str | None = None):
        if photo:
            task = self._send_message(bot=self.get_bot(),
                                      chat_id=chat_id,
                                      text=text,
                                      photo=photo)
        else:
            task = self._send_message(bot=self.get_bot(),
                                      chat_id=chat_id,
                                      text=text)
        return asyncio.get_event_loop().run_until_complete(task)

    def tasks(self, worksheet: Worksheet):
        users = get_users()
        tasks = Tasks(tasks=worksheet.get_all_records()).tasks
        actual_task, result = None, None
        for task in tasks:
            if check_task(task):
                actual_task = task
                break
        if actual_task:
            for user in users:
                if actual_task.id_photo:
                    result = self.send_message(
                        chat_id=user.telegram_id,
                        text=actual_task.text,
                        photo=actual_task.id_photo
                    )
                else:
                    result = self.send_message(
                        chat_id=user.telegram_id,
                        text=actual_task.text
                    )
            update_status(worksheet, actual_task)
            return result

    @staticmethod
    async def _send_message(bot: Bot, chat_id: int, text: str, photo: str | None = None):
        try:
            if photo:
                message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=text
                )
            else:
                message = await bot.send_message(
                    chat_id=chat_id,
                    text=text
                )
            return message.__dict__
        except AiogramError as error:
            logger.error(str(error))
            return
        finally:
            await bot.session.close()


class TasksProcess:
    def __init__(self, telegram_manager: TelegramManager):
        self.telegram_manager = telegram_manager

    def send_message(self, worksheet: Worksheet):
        message = self.telegram_manager.tasks(worksheet)
        if message:
            return {
                "result": "success"
            }
