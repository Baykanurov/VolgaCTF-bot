from aiogram.fsm.state import State, StatesGroup


class ContactOrgState(StatesGroup):
    question = State()


class ContactSpikerState(StatesGroup):
    question = State()


class ParticipantState(StatesGroup):
    team = State()


class AdminKeysState(StatesGroup):
    keys = State()
