from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


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


