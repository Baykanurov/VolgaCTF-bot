from aiogram import (
    Router,
    types,
    Bot,
    F
)
from aiogram.filters import Command
from src.mongo import get_user, create_user
from .helper import (
    get_photo_token,
    get_start_text,
    get_retry_start_text,
    get_contacts_text
)
from .keyboard import (
    contacts_keyboard
)
from pprint import pprint

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, bot: Bot):
    if not get_user(telegram_id=str(message.from_user.id)):
        create_user(
            telegram_id=str(message.from_user.id),
            name=message.from_user.full_name
        )
        await bot.send_photo(
            chat_id=str(message.from_user.id),
            photo=get_photo_token()['start'],
            caption=get_start_text(message.from_user.full_name)
        )
    else:
        await message.answer(
            text=get_retry_start_text()
        )


@router.message(Command("contacts"))
async def contacts(message: types.Message):
    await message.answer(
        text=get_contacts_text(),
        reply_markup=contacts_keyboard
    )


@router.message()
async def test(message: types.Message):
    pprint(message.photo[-1].file_id)
