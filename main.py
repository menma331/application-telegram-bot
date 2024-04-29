import asyncio
import logging

from handlers.admin import admin_router
from handlers.balance import balance_router
from handlers.base import base_router
from handlers.buy import buy_router
from loader import disp, bot
from handlers.fill_an_application import fill_an_application_router


async def start():
    """Запуск."""
    logging.basicConfig(level=logging.INFO)
    print('Bot has been started')

    # Регистрация маршрутизаторов
    disp.include_router(router=fill_an_application_router)
    disp.include_router(router=balance_router)
    disp.include_router(router=buy_router)
    disp.include_router(router=admin_router)
    disp.include_router(router=base_router)

    await disp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Bot has been stopped')
