from mongoengine import (
    Document,
    StringField,
)


class User(Document):
    telegram_id = StringField(required=True)
    name = StringField()
