from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class LanguageCallback(CallbackData, prefix="language"):
    data: str


language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Русский",
                callback_data=LanguageCallback(data="russian").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="English",
                callback_data=LanguageCallback(data="english").pack()
            )
        ]
    ]
)


class RankCallback(CallbackData, prefix="rank"):
    data: str


def get_rank_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Участник 👨‍💻"
                    if language == "russian" else "Participant 👨‍💻",
                    callback_data=RankCallback(data="participant").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Гость 👀"
                    if language == "russian" else "Guest 👀",
                    callback_data=RankCallback(data="guest").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Организатор или Волонтер 🦸‍♂️"
                    if language == "russian" else "Organizer or Volunteer 🦸‍♂️",
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


def get_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Задать вопрос организаторам ✉️"
                    if language == "russian" else "Ask a question to the organizer ✉️",
                    callback_data=MenuCallback(data="question_org").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Задать вопрос спикеру 💬"
                    if language == "russian" else "Ask a question to the speaker 💬",
                    callback_data=MenuCallback(data="question_spiker").pack()
                )
            ]
        ]
    )
