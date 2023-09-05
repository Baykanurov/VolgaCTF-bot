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
    get_rank_keyboard,
    RankCallback,
    contacts_keyboard,
    MenuCallback,
    language_keyboard,
    LanguageCallback
)
from .services import check_auth_message, send_question, get_menu, edit_welcome
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
async def team_participant(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()
    user = get_user(telegram_id=str(message.from_user.id))
    if not message.text:
        await message.answer(text=get_not_text_error(user.language))
        await state.set_state(ParticipantState.team)
    elif str(message.text).startswith("/"):
        await message.answer(text=get_command_error(user.language))
        await state.set_state(ParticipantState.team)
    else:
        update_user(user=user, rank="Participant", team=message.text)
        await message.answer(text=get_registration_text(user.language))
        await get_menu(bot=bot, message=message)


@router.message(AdminKeysState.keys)
async def admin_keys(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()
    user = get_user(telegram_id=str(message.from_user.id))
    if not message.text:
        await message.answer(text=get_not_text_error(user.language))
        await state.set_state(AdminKeysState.keys)
    elif str(message.text).startswith("/"):
        await message.answer(text=get_command_error(user.language))
        await state.set_state(AdminKeysState.keys)
    elif not compare_digest(str(message.text), configuration.admin.key):
        await message.answer(
            text=get_key_error(user.language),
            reply_markup=get_rank_keyboard(user.language)
        )
    else:
        update_user(user=user, rank="Organizer or Volunteer")
        await message.answer(text=get_registration_text(user.language))
        await get_menu(bot=bot, message=message)


@router.message(Command("start"))
async def start(message: types.Message):
    if not get_user(telegram_id=str(message.from_user.id)):
        await message.answer(text=get_start_text(), reply_markup=language_keyboard)
    else:
        await message.answer(text=get_retry_start_text())


@router.callback_query(LanguageCallback.filter())
async def welcome(callback: types.CallbackQuery, bot: Bot):
    chat_id = str(callback.message.chat.id)
    await bot.delete_message(
        chat_id=chat_id,
        message_id=callback.message.message_id
    )
    language = "russian" if callback.data == "language:russian" else "english"
    create_user(
        telegram_id=chat_id,
        name=callback.from_user.full_name,
        language=language
    )
    await bot.send_photo(
        chat_id=chat_id,
        photo=get_photo_token()['start'],
        caption=get_welcome_text(callback.from_user.full_name, language),
        reply_markup=get_rank_keyboard(language)
    )


@router.callback_query(RankCallback.filter(F.data == "participant"))
async def rank_participant(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user = get_user(telegram_id=str(callback.message.chat.id))
    await edit_welcome(callback, bot, user.language)
    await state.set_state(ParticipantState.team)
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text=get_answer_team_text(user.language)
    )


@router.callback_query(RankCallback.filter(F.data == "guest"))
async def rank_guest(callback: types.CallbackQuery, bot: Bot):
    user = get_user(telegram_id=str(callback.message.chat.id))
    await edit_welcome(callback, bot, user.language)
    update_user(user=user, rank="Guest")
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text=get_registration_text(user.language)
    )
    await get_menu(bot=bot, callback=callback)


@router.callback_query(RankCallback.filter(F.data == "organizer"))
async def rank_organizer(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user = get_user(telegram_id=str(callback.message.chat.id))
    await edit_welcome(callback, bot, user.language)
    await state.set_state(AdminKeysState.keys)
    await bot.send_message(
        chat_id=str(callback.message.chat.id),
        text=get_answer_key_text(user.language)
    )


@router.message(Command("menu"))
@check_auth_message
async def menu(message: types.Message, bot: Bot):
    await get_menu(bot=bot, message=message)


@router.callback_query(MenuCallback.filter())
async def question_org(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    user = get_user(telegram_id=str(callback.message.chat.id))
    await bot.delete_message(
        chat_id=str(callback.message.chat.id),
        message_id=callback.message.message_id
    )
    if callback.data == "menu:question_org":
        await state.set_state(ContactOrgState.question)
        await bot.send_message(
            chat_id=str(callback.message.chat.id),
            text=get_question_org_text(user.language)
        )
    elif callback.data == "menu:question_spiker":
        await state.set_state(ContactSpikerState.question)
        await bot.send_message(
            chat_id=str(callback.message.chat.id),
            text=get_question_spiker_text(user.language)
        )


@router.message(Command("contacts"))
@check_auth_message
async def contacts(message: types.Message, bot: Bot):
    user = get_user(telegram_id=str(message.from_user.id))
    await message.answer(
        text=get_contacts_text(user.language),
        reply_markup=contacts_keyboard
    )


@router.message(Command("help"))
@check_auth_message
async def helper(message: types.Message, bot: Bot):
    user = get_user(telegram_id=str(message.from_user.id))
    await message.answer(
        text=get_help_text(user.language)
    )


@router.message(Command("count"))
@check_auth_message
async def count(message: types.Message, bot: Bot):
    user = get_user(telegram_id=str(message.from_user.id))
    if user in get_organizer():
        users = get_users()
        await message.answer(text=f'Пользователей: {len(users)}')
    else:
        await message.answer(text=get_not_organizer_text(user.language))


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
    user = get_user(telegram_id=str(message.from_user.id))
    if user in get_organizer():
        await message.answer(text=get_bear_all_text())
        users = get_users()
        for user in users:
            await bot.send_video(
                chat_id=user.telegram_id,
                video=get_bear_gif_url()
            )
    else:
        await message.answer(text=get_not_organizer_text(user.language))


@router.message(Command("my_id"))
async def my_id(message: types.Message):
    await message.answer(text=str(message.from_user.id))


@router.message(F.photo)
async def get_id_photo(message: types.Message):
    await message.answer(message.photo[-1].file_id)


@router.message()
@check_auth_message
async def all_text(message: types.Message):
    user = get_user(telegram_id=str(message.from_user.id))
    await message.answer(text=get_all_text(user.language))
