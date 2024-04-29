from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from config import admins_id, YOUKASSA
from keyboards.buy.reply import get_buy_menu_markup
from keyboards.menu_reply import get_menu_markup
from loader import db_connection
from states import TopUpBalanceStates

buy_router = Router()
top_up_balance_states = TopUpBalanceStates()


@buy_router.message(F.text == 'Купить товар📦')
async def handle_buy(message: Message, bot: Bot, state: FSMContext):
    """Обработчик пункта меню 'Купить товар📦'."""
    await state.set_state(top_up_balance_states.BUY_PRODUCT)
    await message.answer(
        text='Выберите один из предложенных товаров или вернитесь в '
             'меню📋', reply_markup=get_buy_menu_markup()
    )


@buy_router.message(F.text == 'Купить 1 раз', top_up_balance_states.BUY_PRODUCT)
async def handle_buy_one_time(message: Message, state: FSMContext, bot: Bot):
    """Отправка счета на одну покупку."""
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка товара',
        description='Купить 1 раз - купить 500 у.е.',
        payload='Payment through a bot',
        provider_token=YOUKASSA,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Купить 1 раз',
                amount=50000
            ),
        ]
    )


@buy_router.message(F.text == 'Купить 2 раза', top_up_balance_states.BUY_PRODUCT)
async def handle_buy_one_time(message: Message, state: FSMContext, bot: Bot):
    """Отправка счета на две покупки."""
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка товара',
        description='Купить 2 раза - купить 1000 у.е.',
        payload='Payment through a bot',
        provider_token=YOUKASSA,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Купить 2 раза',
                amount=100000
            ),
        ]
    )


@buy_router.pre_checkout_query()
async def handle_pre_checkout_query(
        pre_checkout_query: PreCheckoutQuery,
        bot: Bot
):
    """Обработка платежа и изменение баланса пользователя на пополненную сумму."""
    total_amount = pre_checkout_query.total_amount // 100
    await db_connection.top_up_balance(
        top_up_sum=total_amount,
        telegram_id=pre_checkout_query.from_user.id
    )
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True
    )


@buy_router.message(F.successful_payment)
async def process_confirm(message: Message, state: FSMContext):
    """Подтверждение успешной покупки товара и очищение состояния."""
    is_admin = message.from_user.id in admins_id
    await state.clear()
    text = 'Вы успешно купили товар✅'
    await message.answer(text=text, reply_markup=get_menu_markup(is_admin=is_admin))


@buy_router.message(F.text == 'Обратно в меню🔙', top_up_balance_states.BUY_PRODUCT)
async def handle_back_to_menu(message: Message, state: FSMContext):
    """Обработка попытки вернуться назад к меню."""
    is_admin = message.from_user.id in admins_id
    await state.clear()

    text = 'Вы вернулись обратно в меню📋'
    await message.answer(text=text, reply_markup=get_menu_markup(is_admin=is_admin))
