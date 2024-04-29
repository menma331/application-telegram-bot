from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def get_menu_markup(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Метод получения кнопок меню."""
    buttons = ReplyKeyboardBuilder()

    buttons.button(text='Оставить заявку📋')
    buttons.button(text='Купить товар📦')
    buttons.button(text='Мой баланс💰')

    if is_admin:
        # Если пользователь администратор, ему предложит еще одну кнопку
        buttons.row(KeyboardButton(text='Отправить сообщение пользователям📤'))

    return buttons.as_markup(
        resize_keyboard=True, input_field_placeholder='Выберите '
                                                      'пункт меню.',
        one_time_keyboard=True,
    )
