from aiogram import html
from aiogram.filters import CommandObject
from classes import NameUserCallback, TypeCallbackFactory, DaysCallbackFactory, RehearsalCallbackFactory
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_name_kb(command: CommandObject):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Всё верно',
        callback_data=NameUserCallback(name=html.code(html.quote(command.args)))
    )
    builder.button(
        text='Хочу переписать имя',
        callback_data='rename'
    )
    return builder.as_markup()


def get_menu_button():
    builder = InlineKeyboardBuilder()
    builder.button(text='Меню', callback_data='menu')
    return builder.as_markup()


def get_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Записаться на репетицию',
        callback_data='choose_type'
    )
    builder.button(
        text='Узнать прайс-лист',
        callback_data='price'
    )
    builder.button(
        text='Поменять имя',
        callback_data='rename'
    )
    builder.button(
        text='Мои репетиции',
        callback_data='my_repetition'
    )
    builder.adjust(1)
    return builder.as_markup()


def get_type_repetition_kb():
    builder = builder = InlineKeyboardBuilder()
    builder.button(
        text='Индивидуальная',
        callback_data=TypeCallbackFactory(type='solo')
    )
    builder.button(
        text='Вдвоём',
        callback_data=TypeCallbackFactory(type='duo')
    )
    builder.button(
        text='Группой',
        callback_data=TypeCallbackFactory(type='group')
    )
    builder.adjust(1)
    return builder.as_markup()


def get_day_kb(callback_data: TypeCallbackFactory):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Понедельник',
        callback_data=DaysCallbackFactory(day='mon', type=callback_data.type)
    )
    builder.button(
        text='Вторник',
        callback_data=DaysCallbackFactory(day='tues', type=callback_data.type)
    )
    builder.button(
        text='Среда',
        callback_data=DaysCallbackFactory(day='wednes', type=callback_data.type)
    )
    builder.button(
        text='Четверг',
        callback_data=DaysCallbackFactory(day='thurs', type=callback_data.type)
    )
    builder.button(
        text='Пятница',
        callback_data=DaysCallbackFactory(day='fri', type=callback_data.type)
    )
    builder.button(
        text='Суббота',
        callback_data=DaysCallbackFactory(day='satur', type=callback_data.type)
    )
    builder.button(
        text='Воскресенье',
        callback_data=DaysCallbackFactory(day='sun', type=callback_data.type)
    )
    builder.button(
        text='Назад',
        callback_data='menu'
    )
    builder.adjust(4)
    return builder.as_markup()


def get_back_button(callback_data: DaysCallbackFactory):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Назад',
        callback_data=TypeCallbackFactory(type=callback_data.type)
    )
    return builder.as_markup()


def get_set_time_kb(day, dict_numbers, num_1, num_2, mod):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Верно',
        callback_data=RehearsalCallbackFactory(day=day,
                                               hourStart=dict_numbers[num_1],
                                               hourEnd=dict_numbers[num_2],
                                               type=mod
                                               )
    )
    builder.button(
        text='Неверно',
        callback_data=DaysCallbackFactory(day=day, type=mod)
    )
    return builder.as_markup()


def get_request_button():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Отправить заявку',
        callback_data='request'
    )
    return builder.as_markup()
