from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_message_confirm_markup():
    """Метод получения inline кнопок для подтверждения текста для рассылки."""
    buttons = InlineKeyboardBuilder()

    buttons.button(text='Подтверждаю✅', callback_data='confirm')
    buttons.button(text='Переписать🖊', callback_data='rewrite')
    buttons.button(text='Отмена❌', callback_data='cancel')

    buttons.adjust(1)

    return buttons.as_markup()
