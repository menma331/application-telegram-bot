import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import admins_id
from keyboards.filling_an_application.inline import get_confirm_budget_markup
from keyboards.filling_an_application.reply import get_line_of_business_markup, \
    get_platform_keyboard_markup, get_phone_number_markup
from keyboards.menu_reply import get_menu_markup
from loader import bot, db_connection
from models.models import Proposal
from states import SubmitApplicationStates

fill_an_application_router = Router()

submit_application_states = SubmitApplicationStates()


@fill_an_application_router.message(F.text == 'Оставить заявку📋')
async def handler_submit_application(message: Message, state: FSMContext):
    """Обработчик начала заполнения заявки."""
    await message.answer(
        text='Какое направление вашего бизнеса?',
        reply_markup=get_line_of_business_markup()
    )
    await state.set_state(submit_application_states.CHOOSE_LINE_OF_BUSINESS_STATE)

    await set_timeout_timer(message.from_user.id, state)


async def set_timeout_timer(user_id, state: FSMContext):
    await asyncio.sleep(600)  # 10 минут
    async with state.get_data() as data:
        if not data['is_application_filling']:
            await bot.send_message(user_id, "Вы забыли заполнить заявку!")


@fill_an_application_router.message(
    submit_application_states.CHOOSE_LINE_OF_BUSINESS_STATE
)
async def handle_choose_line_of_business(message: Message, state: FSMContext):
    """Обработчик выбора направления бизнеса."""
    if message.text not in ['Продажа', 'Производство', 'Оказание услуг']:
        # Если заказчик прислал не поддерживаемое направление бизнеса
        await message.answer(
            text='Мы не работаем с таким направлением бизнеса',
            reply_markup=get_line_of_business_markup()
        )
        return

    await state.update_data(business_line=message.text)
    await message.answer(
        text='Хорошо, записал. А теперь выберите платформу, на которой будет бот.',
        reply_markup=get_platform_keyboard_markup()
    )
    await state.set_state(submit_application_states.CHOOSE_PLATFORM_STATE)


@fill_an_application_router.message(submit_application_states.CHOOSE_PLATFORM_STATE)
async def handle_choose_platform_of_bot(message: Message, state: FSMContext):
    """Обработчик выбора платформы бота."""
    if message.text not in ['Телеграмм', 'Ватсап', 'Вайбер']:
        # Если заказчик прислал не поддерживаемую платформу для бота
        await message.answer(
            text='Мы разрабатываем ботов только на предложенных платформах',
            reply_markup=get_platform_keyboard_markup()
        )
        return

    await state.update_data(platform_of_bot=message.text)

    text = 'Хорошо, записал.' \
           '\nПодскажите, какой у вас бюджет ?' \
           '\nВведите в формате "<b>5000 до 10000</b>". Валютой считается условная ' \
           'единица.'
    await message.answer(
        text=text,
        parse_mode='HTML'
    )
    await state.set_state(submit_application_states.BUDGET_REQUEST_STATE)


@fill_an_application_router.message(submit_application_states.BUDGET_REQUEST_STATE)
async def handle_budget_request(message: Message, state: FSMContext):
    """Обработчик выбора бюджета."""
    try:
        # Из сообщения получаем диапазон бюджета
        budget_range = message.text.split(" до ")
        budget_from = abs(float(budget_range[0]))
        budget_to = abs(float(budget_range[1]))
        text = f'Ваш бюджет от {budget_from} до {budget_to} у.е.'
        await message.answer(text=text, reply_markup=get_confirm_budget_markup())
        await state.update_data(budget_from=budget_from)
        await state.update_data(budget_to=budget_to)

    except Exception as e:
        print(e)
        text = 'Введите диапазон бюджета в формате "<b>5000 до 10000</b>"'
        await message.answer(text=text, parse_mode='HTML')


@fill_an_application_router.callback_query(
    F.data == 'confirm', submit_application_states.BUDGET_REQUEST_STATE
)
async def handle_confirm(callback: CallbackQuery, state: FSMContext):
    """После подтверждения бюджета, у пользователя запросит номер телефона."""
    text = 'Отлично !' \
           ' Ваша заявка почти заполнена. Осталось только получить телефон для связи'
    await callback.message.answer(
        text=text, reply_markup=get_phone_number_markup(), parse_mode='HTML'
    )
    await callback.answer()

    await state.set_state(submit_application_states.FINISHED_APPLICATION_STATE)


@fill_an_application_router.callback_query(
    F.data == 'rewrite', submit_application_states.BUDGET_REQUEST_STATE
)
async def handle_rewrite(callback: CallbackQuery):
    """Переписать уже написанный бюджет на стадии заполнения заявки."""
    text = 'Введите диапазон бюджета в формате "<b>5000 до 10000</b>"'
    await callback.message.answer(text=text, parse_mode='HTML')
    await callback.answer()


@fill_an_application_router.message(
    F.contact,
    submit_application_states.FINISHED_APPLICATION_STATE
)
async def handle_finish_filling_application(message: Message, state: FSMContext):
    """Обработка заполненной заявки.

        Действия:
        • Закидывает новую заявку в базу;
        • Скидывает администраторам новую заявку.
    """
    await state.update_data(phone_number=message.contact.phone_number)

    data = await state.get_data()
    business_line = data['business_line']
    platform_of_bot = data['platform_of_bot']
    unhandled_budget_from = data['budget_from']
    unhandled_budget_to = data['budget_to']
    phone_number = data['phone_number']

    # Подтачивание данных под стандарты
    budget_from = min(unhandled_budget_from, unhandled_budget_to)
    budget_to = max(unhandled_budget_from, unhandled_budget_to)
    user_id = await db_connection.get_user_id(message.from_user.id)
    budget = (budget_from, budget_to)

    proposal = Proposal(
        user_id=user_id,
        business_line=business_line,
        platform_of_bot=platform_of_bot,
        range_of_budget=(budget_from, budget_to),
        phone_number=phone_number
    )
    await db_connection.add_proposal(proposal=proposal)

    # Отправка сообщения пользователю об успешно сформированной заявке
    is_admin = message.from_user.id in admins_id
    successfully_proposal_text = "Заявка успешно принята✅"
    await message.answer(
        text=successfully_proposal_text, reply_markup=get_menu_markup(
            is_admin=is_admin
        )
    )

    # Получение id чатов с администраторами
    admins_chat_id = []
    for admin_id in admins_id:
        chat_id = await db_connection.get_chat_id(admin_id)
        admins_chat_id.append(chat_id)

    # Отправка заявки администраторам
    proposal_text = f'Была сформирована заявка.' \
                    f'\n\nПлатформа бота: {platform_of_bot}' \
                    f'\nНаправление бизнеса: {business_line}' \
                    f'\nБюджет от {budget[0]} до {budget[1]} у.е' \
                    f'\nНомер телефона: `{phone_number}`'
    for chat_id in admins_chat_id:
        await bot.send_message(chat_id=chat_id, text=proposal_text, parse_mode='MARKDOWN')


@fill_an_application_router.callback_query(F.data == "menu")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """Возврат к меню."""
    is_admin = callback.message.from_user.id in admins_id
    await state.clear()

    await callback.message.answer(
        text='Вы вернулись в меню📋',
        reply_markup=get_menu_markup(is_admin=is_admin)
    )
    await callback.answer()
