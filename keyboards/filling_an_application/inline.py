from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_confirm_budget_markup(exclude: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения бюджета."""
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Верно✅', callback_data='confirm')
    if not exclude:
        buttons.button(text='Изменить🖊', callback_data='rewrite')
    buttons.button(text='Вернуться в меню🔙', callback_data='menu')
    buttons.adjust(2)
    return buttons.as_markup()


def get_phone_number_markup() -> InlineKeyboardMarkup:
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Дать номер телефона📞', )
    buttons.button(text='Вернуться в меню🔙', callback_data='menu')
    buttons.adjust(2)
