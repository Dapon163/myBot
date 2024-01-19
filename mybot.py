import asyncio
import logging
from config_reader import config
from aiogram import Bot, Dispatcher


from handlers import info, menu, register, repetition, my_repetition, other
from admin import user_request

bot = Bot(token=config.bot_token.get_secret_value())


async def main():
    # Включаем логирование бота
    logging.basicConfig(level=logging.INFO)

    # Создаём объект бота

    # Создаём диспатчер
    dp = Dispatcher()

    # Подключаем все хэндлеры
    dp.include_routers(register.router,
                       menu.router,
                       info.router,
                       repetition.router,
                       user_request.router,
                       my_repetition.router,
                       other.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
