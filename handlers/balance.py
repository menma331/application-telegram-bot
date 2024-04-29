from aiogram import Router, F
from aiogram.types import Message

from config import admins_id
from keyboards.menu_reply import get_menu_markup
from loader import db_connection

balance_router = Router()


@balance_router.message(F.text == 'Мой баланс💰')
async def handle_get_balance(message: Message):
    """Обработчик проверки баланса."""
    balance = await db_connection.get_balance(message.from_user.id)
    is_admin = message.from_user.id in admins_id

    text = f'Ваш баланс: <b>{balance}</b> у.е'
    await message.answer(
        text=text,
        reply_markup=get_menu_markup(is_admin=is_admin),
        parse_mode='HTML'
    )
