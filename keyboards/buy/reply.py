from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_buy_menu_markup() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardBuilder()

    buttons.button(text='Купить 1 раз')
    buttons.button(text='Купить 2 раза')
    buttons.button(text='Обратно в меню')

    return buttons.as_markup(
        resize_keyboard=True, input_field_placeholder='Выберите '
                                                      'пункт меню.',
        one_time_keyboard=True,
    )