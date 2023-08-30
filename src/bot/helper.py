def get_photo_token() -> dict:
    return {
        'start': 'AgACAgIAAxkBAAMUZO-bsOsI0_7Dv61bXETQ9SpPpW'
                 'kAAtvPMRv2WIBLZ8N_7m9fWT4BAAMCAAN4AAMwBA'
    }


def get_start_text(name: str) -> str:
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

//

{name}, welcome to VolgaCTF 2023!

I am a volunteer bot that will help you navigate during the whole competition.

I will remind you about all the lectures and other events during VolgaCTF 2023.

🟡 tap /menu to check what I can offer you
⚫️ If you forget anything, I will always be happy to remind with simple command /help
🟠 Check contacts page with command /contacts

Let’s confirm your status on this competition. Pick an option below.
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


def get_contacts_text() -> str:
    return """
Наши контакты!

//

Our contacts!
"""