from typing import List
from mongoengine.errors import DoesNotExist
from .models import User, Message


def create_user(**data):
    User(**data).save()


def get_user(telegram_id: str, **kwargs) -> User | None:
    try:
        user = User.objects.get(telegram_id=telegram_id, **kwargs)
        return user
    except DoesNotExist:
        return


def update_user(user: User, **kwargs):
    user.update(**kwargs)


def get_users() -> List[User]:
    return User.objects()


def get_organizer() -> List[User]:
    return User.objects(rank="Organizer or Volunteer")


def create_message(**data):
    Message(**data).save()


def get_message(telegram_id: str) -> Message | None:
    try:
        message = Message.objects.get(telegram_id=telegram_id)
        return message
    except DoesNotExist:
        return


def update_message(message: Message, **kwargs):
    message.update(**kwargs)
