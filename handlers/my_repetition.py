from aiogram import Router, F
from master_db import pg_master
from aiogram.types import Message, CallbackQuery
from keyboards.basic_kb import get_menu_button
from lib import lists

router = Router()


def get_time_table(dict_hour: tuple):
    str_time = str(dict_hour[0]) + ':00 - '
    for i in range(1, len(dict_hour), 1):
        if dict_hour[i] - dict_hour[i - 1] == 1:
            continue
        else:
            str_time += str(dict_hour[i - 1] + 1) + ':00\n' + str(dict_hour[i]) + ':00 - '
    str_time += str(dict_hour[-1] + 1) + ':00'
    return str_time


@router.callback_query(F.data == "my_repetition")
async def my_repetition(callback: CallbackQuery):
    rep_list = {}
    answer_str = ""
    for i in range(7):
        table = lists.list_days[i]
        rep_list.update({table: pg_master.search_repetition(table=table, client_id=callback.from_user.id)})
        if rep_list[table]:
            answer_str += "В " + lists.list_of_days[table] + ":\n" + get_time_table(rep_list[table]) + "\n"
    await callback.message.answer(text=f"Список ваших забронированных репетиций:\n"
                                       f"{answer_str}",
                                  reply_markup=get_menu_button())
    await callback.answer()
