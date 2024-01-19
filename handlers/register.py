import re
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import html

from keyboards.basic_kb import get_name_kb, get_menu_button
from classes import NameUserCallback
from master_db import pg_master


def name_rename_bd(client_id, username, name):
    pattern_1 = r"[<code>]|[</code>]"
    name = re.sub(pattern_1, "", name)
    if pg_master.check_id(client_id=client_id) is None:
        pg_master.reg(data=(client_id, username, name))
    else:
        pg_master.rename(client_id=client_id, username=username, name=name)


router = Router()


# Хэндлер на комманду /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    # print(f"message.from_user.id: {message.from_user.id}\n"
    #       f"message.from_user.username: {message.from_user.username}")
    await message.answer("Добро пожаловать!\nЗдесь вы сможете быстро и удобно забронировать репетицию в "
                         "{Здесь могло быть ваше название}\nДля начала давай познакомимся!\nКак тебя зовут?"
                         " (напиши /name и укажи своё имя)")


@router.message(Command("name"))
async def cmd_name(message: Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.code(html.quote(command.args))}!\n"
                             f"Обращаю твоё внимание, что именно под таким именем тебя запишут на мероприятие,"
                             f" поэтому прошу подтвердить, что всё указано верно"
                             , parse_mode="HTML", reply_markup=get_name_kb(command=command))
    else:
        await message.answer(f"Пожалуйста, укажи своё имя после команды /name!")


@router.callback_query(NameUserCallback.filter())
async def register_client(callback: CallbackQuery,
                          callback_data: NameUserCallback):
    # Записываем в БД
    name_rename_bd(callback.from_user.id, callback.from_user.username, callback_data.name)
    await callback.message.answer('Отлично! Ты зарегестрирован!\n',
                                  reply_markup=get_menu_button())

    await callback.answer()


@router.callback_query(F.data == 'rename')
async def rename_client(callback: CallbackQuery):
    await callback.message.answer('Напиши /name и введи корректное имя')
    await callback.answer()
