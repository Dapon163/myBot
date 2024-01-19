from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from keyboards.basic_kb import get_menu_kb
from master_db import pg_master

router = Router()


@router.message(Command("menu"))
async def menu(message: Message):
    name = pg_master.get_name(message.from_user.id)
    print(message)
    if message is not None:
        await message.answer(f'Привет, {name}!\n'
                             f'Что тебя интересует?',
                             reply_markup=get_menu_kb())


@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery):
    name = pg_master.get_name(callback.from_user.id)
    if callback.message is not None:
        await callback.message.answer(f'Привет, {name}!\n'
                                      f'Что тебя интересует?',
                                      reply_markup=get_menu_kb())
    await callback.answer()
