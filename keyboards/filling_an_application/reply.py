from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_line_of_business_markup() -> ReplyKeyboardMarkup:
    """Метод получения кнопок выбора направления бизнеса."""
    buttons = ReplyKeyboardBuilder()

    buttons.button(text='Продажа')
    buttons.button(text='Производство')
    buttons.button(text='Оказание услуг')

    return buttons.as_markup(
        resize_keyboard=True, input_field_placeholder='Выберите '
                                                      'пункт меню.',
        one_time_keyboard=True,
    )


def get_platform_keyboard_markup() -> ReplyKeyboardMarkup:
    """Метод получения платформы для бота."""
    buttons = ReplyKeyboardBuilder()

    buttons.button(text='Телеграмм')
    buttons.button(text='Ватсап')
    buttons.button(text='Вайбер')

    return buttons.as_markup(
        resize_keyboard=True, input_field_placeholder='Выберите '
                                                      'пункт меню.',
        one_time_keyboard=True,
    )


def get_phone_number_markup() -> ReplyKeyboardMarkup:
    """Клавиатура запроса номера телефона."""
    buttons = ReplyKeyboardBuilder()
    buttons.button(text='Дать номер телефона📞', request_contact=True)
    buttons.button(text='Вернуться в меню🔙')
    buttons.adjust(1)
    return buttons.as_markup(
        resize_keyboard=True, input_field_placeholder='Введите номер телефона📞',
        one_time_keyboard=True,
    )
