def get_photo_token() -> dict:
    return {
        'start': 'AgACAgIAAxkBAAIsGmT3oDwIR4A8dVtjC0UDWSWLnN'
                 'OdAAId0jEbXwXAS-HT4Z90ykC2AQADAgADeAADMAQ',
        'menu': 'AgACAgIAAxkBAAIsGmT3oDwIR4A8dVtjC0UDWSWLnNO'
                'dAAId0jEbXwXAS-HT4Z90ykC2AQADAgADeAADMAQ'
    }


def get_start_text() -> str:
    return """
Привет!
Для начала выбери язык интерфейса

//

Hello!
First, select the interface language
"""


def get_welcome_text(name: str, language: str) -> str:
    if language == "russian":
        return f"""
{name}, добро пожаловать на VolgaCTF 2023!

Я бот-волонтер который будет помогать тебе ориентироваться на данных соревнованиях.

Я буду напоминать тебе о лекциях и других мероприятиях,
которые будут проходить во время VolgaCTF 2023.

🟡 Узнать обо всех моих возможностях можно вызвав команду /menu
⚫️ Если ты что-то забудешь, я всегда буду рад напомнить тебе командой /help
🟠 Посмотреть наши контакты можно командой /contacts

Теперь давай определимся с твоим статусом на данном мероприятии,
выбери один вариант из предложенного списка.
"""
    else:
        return f"""
{name}, welcome to VolgaCTF 2023!

I am a volunteer bot that will help you navigate during the whole competition.

I will remind you about all the lectures and other events during VolgaCTF 2023.

🟡 tap /menu to check what I can offer you
⚫️ If you forget anything, I will always be happy to remind with simple command /help
🟠 Check contacts page with command /contacts

Let’s confirm your status on this competition. Pick an option below.
"""


def get_no_auth_text() -> str:
    return """
Ты ещё не познакомился с ботом!
Введи команду /start, чтобы начать.

//

You haven't met the bot yet!
Enter the /start command to start.
"""


def get_no_rank_text(language: str) -> str:
    if language == "russian":
        return """
Ты не выбрал свой статус на данных соревнованиях!
Вернись к приветственному сообщению и нажми на один из статусов.
"""
    else:
        return """
You didn't choose your status at these competitions!
Go back to the welcome message and click on one of the statuses.
"""


def get_retry_start_text() -> str:
    return """
Мы с тобой уже знакомились!
Позволь мне напомнить тебе, как я могу помочь. 
Выполнить команду /help

//

We've already met!
Let me remind you how I can help you. 
Execute command /help
"""


def get_not_text_error(language: str) -> str:
    if language == "russian":
        return """
Сообщение должно быть текстом!
Попробуй ещё раз.
"""
    else:
        return """
The message must be text!
Try again.
"""


def get_command_error(language: str) -> str:
    if language == "russian":
        return """
Сообщение не может быть командой!
Попробуй ещё раз.
"""
    else:
        return """
The message cannot be a command!
Try again.
"""


def get_key_error(language: str) -> str:
    if language == "russian":
        return """
Неверный ключ!
"""
    else:
        return """
Wrong key!
"""


def get_answer_team_text(language: str) -> str:
    if language == "russian":
        return """
Напиши название своей команды
"""
    else:
        return """
Write the name of your team
"""


def get_answer_key_text(language: str) -> str:
    if language == "russian":
        return """
Введи секретный ключ
"""
    else:
        return """
Enter the secret key
"""


def get_registration_text(language: str) -> str:
    if language == "russian":
        return """
Вы успешно зарегистрированы!
"""
    else:
        return """
You have successfully registered!
"""


def get_contacts_text(language: str) -> str:
    if language == "russian":
        return """
Наши контакты!
"""
    else:
        return """
Our contacts!
"""


def get_bear_gif_url() -> str:
    return "http://gifki-gifki.ru/go?http://i.imgur.com/7jws4xS.gif"


def get_bear_all_text() -> str:
    return "Запускаю рассылку медведя..."


def get_menu_text(language: str) -> str:
    if language == "russian":
        return """
🔶 Ты можешь задать вопрос организаторам или спикеру, который ведет лекцию!

🔶 Выбери один из пунктов меню и напиши свой вопрос.
"""
    else:
        return """
🔶 Feel free to ask the leading speaker the question or contact the organizer

🔶 Pick any option from the list below and ask a question.
"""


def get_question_org_text(language: str) -> str:
    if language == "russian":
        return """
Напиши свой вопрос организаторам!
Для выхода введи: Отмена
"""
    else:
        return """
Write your question to the organizers!
To exit, enter: Cancel
"""


def get_question_spiker_text(language: str) -> str:
    if language == "russian":
        return """
Напиши свой вопрос спикер!
Для выхода введи: Отмена
"""
    else:
        return """
Write your question to the spiker!
To exit, enter: Cancel
"""


def get_cancel_question_text(language: str) -> str:
    if language == "russian":
        return """
Сообщение отменено!
"""
    else:
        return """
The message is canceled!
"""


def get_send_question_text(language: str) -> str:
    if language == "russian":
        return """
Сообщение отправлено!
"""
    else:
        return """
The message has been sent!
"""


def get_not_organizer_text(language: str) -> str:
    if language == "russian":
        return """
Ты не организатор или волонтёр!
"""
    else:
        return """
You are not an organizer or a volunteer!
"""


def get_help_text(language: str) -> str:
    if language == "russian":
        return """
⚠️В течении всего времени соревнований я буду напоминать тебе о лекциях и других мероприятиях.

🟡Чтобы открыть меню возможностей выполни команду /menu

🟨Узнать всегда о нас и посмотреть наши контакты можно с помощью команды /contacts

🔆На этом мои полномочия все!
Если тебе есть что предложить или как улучшить мою работу, смело задавай вопрос организаторам!
"""
    else:
        return """
⚠️During the whole competition I will send reminders of lectures and other events.

🟡To open the options menu, run the command /menu

🟨Check our contacts by using the command /contacts

🔆That’s it!
In case you have any suggestions on how to improve my work, 
feel free to share your ideas by using command /contacts
"""


def get_all_text(language: str) -> str:
    if language == "russian":
        return """
Вызови /help, чтобы посмотреть, что я могу!
"""
    else:
        return """
Call /help to see what I can do!
"""
