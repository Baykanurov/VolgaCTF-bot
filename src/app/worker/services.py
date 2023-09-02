from aiogram import Bot
from .. import worksheet
from ..mongo import get_users
from ..table import Tasks, check_task, update_status


async def _send_task(bot: Bot):
    users = get_users()
    tasks = Tasks(tasks=worksheet.get_all_records()).tasks
    actual_task = None
    for task in tasks:
        if check_task(task):
            actual_task = task
            break
    if actual_task:
        for user in users:
            if actual_task.id_photo:
                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=actual_task.id_photo,
                    caption=actual_task.text
                )
            else:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=actual_task.text
                )
            update_status(worksheet, actual_task)
            await bot.session.close()
            return "success"
    else:
        await bot.session.close()
        return "skip"
