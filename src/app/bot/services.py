import functools
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from .states import ContactOrgState
from ..mongo import get_user, get_message, create_message, update_message, get_organizer
from .data import *


def check_auth_message(func):
    @functools.wraps(func)
    async def wrapper(message: types.Message, bot: Bot | None = None):
        if not get_user(telegram_id=str(message.from_user.id)):
            await message.answer(text=get_no_auth_text())
        else:
            return await func(message, bot or None)

    return wrapper


def check_auth_callback(func):
    @functools.wraps(func)
    async def wrapper(callback: types.CallbackQuery, bot: Bot):
        if not get_user(telegram_id=str(callback.message.from_user.id)):
            await bot.send_message(
                chat_id=str(callback.message.from_user.id),
                text=get_no_auth_text()
            )
        else:
            return await func(callback, bot)

    return wrapper


def delete_message(func):
    @functools.wraps(func)
    async def wrapper(message: types.Message, bot: Bot):
        messages = get_message(telegram_id=str(message.from_user.id))
        if not messages:
            new_message = await func(message, bot or None)
            create_message(
                telegram_id=str(message.from_user.id),
                message_id=new_message.message_id
            )
        else:
            await bot.delete_message(
                chat_id=str(message.from_user.id),
                message_id=messages.message_id
            )
            new_message = await func(message, bot or None)
            update_message(messages, message_id=new_message.message_id)

    return wrapper


async def send_question(message: types.Message, bot: Bot, state: FSMContext, _type: str):
    await state.clear()
    if str(message.text).lower() == "отмена":
        await message.answer(
            text="Сообщение отменено"
        )
    elif str(message.text).startswith("/"):
        await message.answer(
            text="Сообщение не может быть командой\nПопробуй ещё раз"
        )
        await state.set_state(ContactOrgState.question)
    else:
        source_user = get_user(telegram_id=str(message.from_user.id))

        if source_user.rank == "Guest":
            title = f"гостя {source_user.name}"
        elif source_user.rank == "Participant":
            title = f"участника {source_user.name} из команды {source_user.team}"
        elif source_user.rank == "Organizer or Volunteer":
            title = f"организатора или волонтера {source_user.name}"
        else:
            title = None

        if _type == "organizer":
            type_text = "организаторам"
        elif _type == "spiker":
            type_text = "спикеру"
        else:
            type_text = None

        for user in get_organizer():
            await bot.send_message(
                chat_id=user.telegram_id,
                text=f"Вопрос {type_text} от {title}: {message.text}"
            )
        await message.answer(
            text="Сообщение отправлено"
        )

