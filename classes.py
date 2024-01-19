from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class NameUserCallback(CallbackData, prefix='name'):
    name: str


class TypeCallbackFactory(CallbackData, prefix='type'):
    type: str


class DaysCallbackFactory(TypeCallbackFactory, prefix='day'):
    day: str


class RehearsalCallbackFactory(DaysCallbackFactory, prefix='rehearsal'):
    hourStart: int
    hourEnd: int


class ChooseTime(StatesGroup):
    choosing_time = State()


class RequestState(StatesGroup):
    send_request = State()
