import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from datetime import date, timedelta
from aiogram.fsm.context import FSMContext

from keyboards.basic_kb import get_type_repetition_kb, get_day_kb, get_back_button, get_set_time_kb, \
    get_menu_button, get_request_button
from classes import TypeCallbackFactory, DaysCallbackFactory, RehearsalCallbackFactory, ChooseTime, RequestState
from master_db import pg_master
from lib import lists

# Свободные часы, надо обновлять раз в неделю, вместе со скриптом на генерацию дат
hours = {}

for i in range(7):
    hours.update({lists.list_days[i]:
        pg_master.select_hours(
            lists.list_days[i], (date.today() - timedelta(days=date.today().weekday() - i),))})


def get_time_table(dict_hour: tuple):
    str_time = str(dict_hour[0]) + ':00 - '
    for i in range(1, len(dict_hour), 1):
        if dict_hour[i] - dict_hour[i - 1] == 1:
            continue
        else:
            str_time += str(dict_hour[i - 1] + 1) + ':00\n' + str(dict_hour[i]) + ':00 - '
    str_time += str(dict_hour[-1] + 1) + ':00'
    return str_time


def set_time(text: str, pattern: int, day: str, mod: str):
    dict_numbers = re.findall(r'(\d{1,2})', text)
    if pattern == 1:
        num_1 = 0
        num_2 = 1
    elif pattern == 2:
        num_1 = 0
        num_2 = 2
    list_for_return = {'builder': get_set_time_kb(day=day,
                                                  dict_numbers=dict_numbers,
                                                  num_1=num_1,
                                                  num_2=num_2,
                                                  mod=mod), 'date': [dict_numbers[num_1], dict_numbers[num_2]]}
    return list_for_return


def return_list_of_hour(start: int, end: int):
    tmp_list = []
    if end - start > 1:
        for i in range(end - start):
            tmp_list.append(start + i)
    else:
        tmp_list.append(start)
    return tmp_list


router = Router()


@router.callback_query(F.data == 'choose_type')
async def choose_type(callback: CallbackQuery):
    await callback.message.answer(text='Пожалуйста, выберите тип репетиции',
                                  reply_markup=get_type_repetition_kb())
    await callback.answer()


@router.callback_query(TypeCallbackFactory.filter())
async def book_rehearsal(callback: CallbackQuery,
                         callback_data: TypeCallbackFactory):
    await callback.message.answer("В какой день интересует репетиция?:",
                                  reply_markup=get_day_kb(callback_data=callback_data))
    await callback.answer()


@router.callback_query(DaysCallbackFactory.filter())
async def choose_time(callback: CallbackQuery,
                      callback_data: DaysCallbackFactory,
                      state: FSMContext):
    time_table = get_time_table(hours[callback_data.day + 'day'])
    await callback.message.answer(text=f'В {lists.list_of_days[callback_data.day + "day"]} свободно время:\n{time_table}\n'
                                       f'Напишите на сколько Вас записать?',
                                  reply_markup=get_back_button(callback_data=callback_data))
    await state.set_state(ChooseTime.choosing_time)
    await state.update_data(day=callback_data.day, type_rep=callback_data.type)
    await callback.answer()


@router.message(ChooseTime.choosing_time, F.text)
async def get_time(message: Message,
                   state: FSMContext):
    user_data = await state.get_data()
    callback_data = DaysCallbackFactory(day=user_data['day'], type=user_data['type_rep'])
    # Паттерны ввода
    pattern_1 = r'[^\d]*(\d{1,2}[\ ])[^\d]*(\d{1,2})[^\d]*'
    pattern_2 = r'[^\d]*(\d{1,2}[:00])[^\d]*(\d{1,2}[:00])[^\d]*'

    # Если не подходит ни под один, то сообщаем о неверном вводе
    if re.match(pattern_1, message.text) is None and re.match(pattern_2, message.text) is None:
        await message.answer(text='Неверный формат ввода, пожалуйста, попробуйте ещё раз')
    # Если подошёл один из, то выясняем какой и запоминаем в num_pattern
    else:
        if re.match(pattern_1, message.text) is not None:
            num_pattern = 1
        elif re.match(pattern_2, message.text) is not None:
            num_pattern = 2

        # Собираем клавиатуру и сообщение, методу сообщаем в каком виде информация
        list_set_time = set_time(text=message.text, pattern=num_pattern, day=callback_data.day, mod=callback_data.type)
        builder = list_set_time['builder']
        await message.answer(text=f'Репетиция в {lists.list_of_days[callback_data.day + "day"]},'
                                  f' тип репетиции {lists.list_of_types[callback_data.type]}, '
                                  f'с {list_set_time["date"][0]} до {list_set_time["date"][1]}\n'
                                  f'Всё верно?',
                             reply_markup=builder)


@router.callback_query(ChooseTime.choosing_time, RehearsalCallbackFactory.filter())
async def finish(callback: CallbackQuery,
                 callback_data: RehearsalCallbackFactory,
                 state: FSMContext):
    # Запись в БД
    table = callback_data.day + "day"
    weekday_key = [key for key, value in lists.list_days.items() if value == table]
    date_rep = date.today() - timedelta(date.today().weekday() - weekday_key[0])
    list_of_hour = return_list_of_hour(callback_data.hourStart, callback_data.hourEnd)
    client_id = callback.from_user.id
    type_rep = callback_data.type
    for item in list_of_hour:
        pg_master.apply_repetition(table, (True, client_id, type_rep, date_rep, item))
    # Удаляем из списка
    hours.update({table: tuple(x for x in hours[table] if x not in list_of_hour)})

    await state.clear()
    await callback.message.answer(f'Спасибо, что выбрали нас!\n'
                                  f'Записали Вас на {lists.list_of_days[callback_data.day + "day"]},'
                                  f' {callback_data.hourStart}:00-{callback_data.hourEnd}:00\n'
                                  f'Репетиция {lists.list_of_types[callback_data.type]}',
                                  reply_markup=get_request_button())
    await callback.answer()
