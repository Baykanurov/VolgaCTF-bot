from mongoengine.errors import DoesNotExist
from .models import User


def create_user(**data) -> None:
    User(**data).save()


def get_user(telegram_id: str) -> User | None:
    try:
        user = User.objects.get(telegram_id=telegram_id)
        return user
    except DoesNotExist:
        return


def update_user(user: User, **kwargs) -> None:
    user.update(**kwargs)


def get_users():
    return User.objects()
