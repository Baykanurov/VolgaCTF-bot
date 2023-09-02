from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Status(str, Enum):
    shipped = "отправлено"
    waiting = "ожидает"
    cancelled = "отменено"


class Task(BaseModel):
    time: str = Field(alias="Дата и время")
    text: str | None = Field(alias="Текст")
    id_photo: str | None = Field(alias="ID изображения")
    status: str | None = Field(alias="Статус")


class Tasks(BaseModel):
    tasks: List[Task] = []
