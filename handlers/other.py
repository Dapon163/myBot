from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.text)
async def answer(callback: CallbackQuery):
    await callback.message.answer(text='Ой, опять кто-то балуется!\n'
                                       'Классного тебе денёчка!')
    await callback.answer()
