from secrets import compare_digest
from aiogram import (
    Router,
    types,
    Bot,
    F
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..mongo import get_user, create_user, get_users, update_user, get_organizer
from .keyboard import (
    rank_keyboard,
    RankCallback,
    contacts_keyboard,
    menu_keyboard,
    MenuCallback
)
from .services import check_auth_message, send_question
from .states import ContactOrgState, ContactSpikerState, ParticipantState, AdminKeysState
from .data import *
from .. import configuration

router = Router()


@router.message(ContactOrgState.question)
async def org_question(message: types.Message, bot: Bot, state: FSMContext):
    await send_question(message=message, bot=bot, state=state, _type="organizer")


@router.message(ContactSpikerState.question)
async def spiker_question(message: types.Message, bot: Bot, state: FSMContext):
    await send_question(message=message, bot=bot, state=state, _type="spiker")


@router.message(ParticipantState.team)
async def team_participant(message: types.Message, state: FSMContext):
    await state.clear()
    if str(message.text).startswith("/"):
        await message.answer(
            text="Сообщение не может быть командой\nПопробуй ещё раз"
        )
        await state.set_state(ParticipantState.team)
    else:
        user = get_user(telegram_id=str(message.from_user.id))
        update_user(user=user, rank="Participant", team=message.text)
        await message.answer(
            text="Вы успешно зарегистрированы!"
        )


@router.message(AdminKeysState.keys)
async def admin_keys(message: types.Message, state: FSMContext):
    await state.clear()
    if str(message.text).startswith("/"):
        await message.answer(
            text="Сообщение не может быть командой\nПопробуй ещё раз"
        )
        await state.set_state(AdminKeysState.keys)
    elif compare_digest(str(message.text), configuration.admin.key):
        user = get_user(telegram_id=str(message.from_user.id))
        update_user(user=user, rank="Organizer or Volunteer")
        await message.answer(
            text="Вы успешно зарегистрированы!"
        )
    else:
        await message.answer(
            text="Ключ неверный"
        )


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
            caption=get_start_text(message.from_user.full_name),
            reply_markup=rank_keyboard
        )
    else:
        await message.answer(
            text=get_retry_start_text()
        )


@router.callback_query(RankCallback.filter(F.data == "participant"))
async def rank_participant(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(ParticipantState.team)
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text="""
Введи название своей команды
        """
    )


@router.callback_query(RankCallback.filter(F.data == "guest"))
async def rank_guest(callback: types.CallbackQuery, bot: Bot):
    user = get_user(telegram_id=str(callback.message.chat.id))
    update_user(user=user, rank="Guest")
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text="""
Вы успешно зарегистрированы!
        """
    )


@router.callback_query(RankCallback.filter(F.data == "organizer"))
async def rank_organizer(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(AdminKeysState.keys)
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text="""
Введи секретный ключ
            """
    )


@router.message(Command("menu"))
@check_auth_message
async def menu(message: types.Message, bot: Bot):
    await bot.send_photo(
        chat_id=str(message.from_user.id),
        photo=get_photo_token()['menu'],
        caption=get_menu_text(),
        reply_markup=menu_keyboard
    )


@router.callback_query(MenuCallback.filter())
async def question_org(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == "menu:question_org":
        await state.set_state(ContactOrgState.question)
        await bot.send_message(
            chat_id=str(callback.message.chat.id),
            text=get_question_org_text()
        )
    elif callback.data == "menu:question_spiker":
        await state.set_state(ContactSpikerState.question)
        await bot.send_message(
            chat_id=str(callback.message.chat.id),
            text=get_question_spiker_text()
        )


@router.message(Command("contacts"))
@check_auth_message
async def contacts(message: types.Message):
    return await message.answer(
        text=get_contacts_text(),
        reply_markup=contacts_keyboard
    )


@router.message(Command("count"))
@check_auth_message
async def count(message: types.Message):
    users = get_users()
    return await message.answer(
        text=f'Пользователей: {len(users)}'
    )


@router.message(Command("bear"))
@check_auth_message
async def bear(message: types.Message, bot: Bot):
    await bot.send_video(
        chat_id=str(message.from_user.id),
        video=get_bear_gif_url()
    )


@router.message(Command("bear_all"))
@check_auth_message
async def bear_all(message: types.Message, bot: Bot):
    await message.answer(text=get_bear_all_text())
    users = get_users()
    for user in users:
        await bot.send_video(
            chat_id=user.telegram_id,
            video=get_bear_gif_url()
        )


@router.message(Command("my_id"))
async def my_id(message: types.Message):
    await message.answer(text=str(message.from_user.id))


@router.message(Command("test"))
async def test(message: types.Message):
    for user in get_organizer():
        await message.answer(text=user.telegram_id)


@router.message(F.photo)
async def get_id_photo(message: types.Message):
    await message.answer(message.photo[-1].file_id)
