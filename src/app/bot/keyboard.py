from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class RankCallback(CallbackData, prefix="rank"):
    data: str


rank_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Участник",
                callback_data=RankCallback(data="participant").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Гость",
                callback_data=RankCallback(data="guest").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Организатор или Волонтер",
                callback_data=RankCallback(data="organizer").pack()
            )
        ]
    ]
)

contacts_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Website🌐",
                url="https://volgactf.ru/"
            ),
            InlineKeyboardButton(
                text="Github💠",
                url="https://github.com/volgactf"
            )
        ],
        [
            InlineKeyboardButton(
                text="VKontakte🔷",
                url="https://vk.com/volgactf"
            ),
            InlineKeyboardButton(
                text="Twitter📖",
                url="https://twitter.com/volgactf"
            )
        ],
        [
            InlineKeyboardButton(
                text="Instagram💬",
                url="https://instagram.com/volga_ctf?utm_medium=copy_link"
            ),
            InlineKeyboardButton(
                text="Youtube🛑",
                url="https://www.youtube.com/channel/UCTbjY5Xys-CgMBN8jgLazPA"
            )
        ]
    ]
)


class MenuCallback(CallbackData, prefix="menu"):
    data: str


menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Задать вопрос организаторам ✉️",
                callback_data=MenuCallback(data="question_org").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Задать вопрос спикеру 💬",
                callback_data=MenuCallback(data="question_spiker").pack()
            )
        ]
    ]
)
