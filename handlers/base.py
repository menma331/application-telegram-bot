from aiogram import Router, F
from aiogram.types import Message

from config import admins_id
from keyboards.menu_reply import get_menu_markup
from loader import db_connection
from models.models import User

base_router = Router()


@base_router.message(F.text == '/start')
async def handle_start(message: Message):
    """Обработчик команды /start.

        Действия:
        • Добавление нового пользователя в базу;
        • Присылает приветственное сообщение;
        • Присылает кнопки меню.
    """
    is_admin = message.from_user.id in admins_id
    user = User(
        username=message.from_user.username,
        telegram_id=message.from_user.id,
        is_superuser=is_admin,
        chat_id=message.chat.id
    )
    await db_connection.add_user(user=user)
    text = 'Добро пожаловать в бота разработанного' \
           ' <a href="https://rabota.by/resume/fd60bec0ff0ccc24760039ed1f6c76586c347600">' \
           'Сыса Романом Алексеевичем</a> в качестве тестового задания.' \
           '\nДля продолжения работы выберите пункт из меню.'

    await message.answer(
        text=text,
        reply_markup=get_menu_markup(is_admin=is_admin),
        parse_mode='HTML'
    )


@base_router.message(F.text == '/menu')
async def handle_menu(message: Message):
    """Обработчик команды /menu."""
    is_admin = message.from_user.id in admins_id
    text = 'Оставить заявку📋 - оставить заявку на разработку бота.' \
           '\n\nКупить товар📦 - купить один из предложенных товаров.' \
           '\n\nМой баланс💰 - проверка текущего баланса с возможностью пополнения.'
    await message.answer(text=text, reply_markup=get_menu_markup(is_admin=is_admin))


@base_router.message()
async def handle_unknown_message(message: Message):
    """Обработчик неизвестного сообщения."""
    is_admin = message.from_user.id in admins_id
    await message.answer(
        text='Я не понимаю о чем вы говорите. Давайте работать в рамках '
             'меню', reply_markup=get_menu_markup(is_admin=is_admin)
    )
