import functools
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from .states import ContactOrgState
from ..mongo import get_user, get_message, create_message, update_message, get_organizer
from .data import *
from .keyboard import get_menu_keyboard


def check_auth_message(func):
    @functools.wraps(func)
    async def wrapper(message: types.Message, bot: Bot | None = None):
        user = get_user(telegram_id=str(message.from_user.id))
        if not user:
            await message.answer(text=get_no_auth_text())
        else:
            if not user.rank:
                await message.answer(text=get_no_rank_text(language=user.language))
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
    source_user = get_user(telegram_id=str(message.from_user.id))
    if not message.text:
        await message.answer(text=get_not_text_error(source_user.language))
        await state.set_state(ContactOrgState.question)
    elif str(message.text).lower() == "отмена" or str(message.text).lower() == "cancel":
        await message.answer(text=get_cancel_question_text(source_user.language))
    elif str(message.text).startswith("/"):
        await message.answer(text=get_command_error(source_user.language))
        await state.set_state(ContactOrgState.question)
    else:
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
        await message.answer(text=get_send_question_text(source_user.language))


async def get_menu(bot: Bot, message: types.Message | None = None,
                   callback: types.CallbackQuery | None = None):
    if message:
        chat_id = str(message.from_user.id)
        user = get_user(telegram_id=str(message.from_user.id))
    elif callback:
        chat_id = str(callback.message.chat.id)
        user = get_user(telegram_id=str(callback.message.chat.id))
    else:
        chat_id, user = None, None
    await bot.send_photo(
        chat_id=chat_id,
        photo=get_photo_token()['menu'],
        caption=get_menu_text(user.language),
        reply_markup=get_menu_keyboard(user.language)
    )


async def edit_welcome(callback: types.CallbackQuery, bot: Bot, language: str):
    chat_id = str(callback.message.chat.id)
    await bot.delete_message(
        chat_id=chat_id,
        message_id=callback.message.message_id
    )
    if callback.message.text in ["Wrong key!", "Неверный ключ!"]:
        await bot.send_message(chat_id=chat_id, text=get_key_error(language))
    else:
        await bot.send_photo(
            chat_id=chat_id,
            photo=get_photo_token()['start'],
            caption=get_welcome_text(callback.from_user.full_name, language)
        )


