from mongoengine import (
    Document,
    StringField,
    IntField
)


class User(Document):
    telegram_id = StringField(required=True)
    name = StringField()
    language = StringField()
    rank = StringField()
    team = StringField()


class Message(Document):
    telegram_id = StringField(required=True)
    message_id = IntField()
