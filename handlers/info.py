from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.basic_kb import get_menu_button


router = Router()


@router.callback_query(F.data == 'price')
async def price(callback: CallbackQuery):
    await callback.message.answer(text='Здесь прайс-лист', reply_markup=get_menu_button())
    await callback.answer()
