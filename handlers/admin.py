from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, chat

from config import admins_id
from keyboards.admin.inline import get_message_confirm_markup
from keyboards.menu_reply import get_menu_markup
from loader import db_connection
from states import AdminStates

admin_router = Router()
admin_states = AdminStates()


@admin_router.message(F.text == 'Отправить сообщение пользователям📤')
async def handle_make_a_newsletter(message: Message, state: FSMContext):
    """Обработка попытки отправить сообщение пользователям."""
    is_admin = message.from_user.id in admins_id

    if is_admin:
        await state.set_state(admin_states.WAIT_FOR_ADMIN_MESSAGE)
        text = 'Введите сообщение, которое будет выслано <b>всем</b> пользователям'
        await message.answer(text=text, parse_mode='HTML')
    else:
        await message.answer(
            text='Вы не имеете доступа к этой команде❌',
            reply_markup=get_menu_markup()
        )


@admin_router.message(admin_states.WAIT_FOR_ADMIN_MESSAGE)
async def handle_news_letter(message: Message, state: FSMContext):
    """Получение сообщения, которое нужно отправить пользователям."""
    await state.update_data(admin_text=message.text)
    await state.set_state(admin_states.WAIT_FOR_CONFIRM)

    text = f'Ваше сообщение:\n\n' \
           f'{message.text}'
    await message.answer(text=text, reply_markup=get_message_confirm_markup())


@admin_router.callback_query(F.data == 'confirm', admin_states.WAIT_FOR_CONFIRM)
async def handle_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Если админ подтвердил, что сообщение правильное."""
    # Получение чата id пользователей
    data = await state.get_data()
    admin_message = data['admin_text']
    all_users_chat_id = await db_connection.get_all_users_chat_id()

    for chat_id in all_users_chat_id:
        try:
            await bot.send_message(text=admin_message, chat_id=chat_id[0])
        except TelegramForbiddenError:
            pass

    await callback.message.answer(
        text='Сообщения успешно отправлены✅',
        reply_markup=get_menu_markup(is_admin=True)
    )
    await state.clear()
    await callback.answer()


@admin_router.callback_query(
    F.data == 'rewrite', admin_states.WAIT_FOR_CONFIRM
)
async def handle_rewrite(callback: CallbackQuery):
    """Обработчик написанного бюджета."""
    text = 'Введите сообщение, которое будет выслано <b>всем</b> пользователям"'
    await callback.message.answer(text=text, parse_mode='HTML')
    await callback.answer()


@admin_router.callback_query(
    F.data == 'cancel', admin_states.WAIT_FOR_CONFIRM
)
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """Обработка отмены рассылки сообщения."""
    text = 'Вы вернулись в меню'
    await callback.message.answer(
        text=text,
        reply_markup=get_menu_markup(is_admin=True)
    )
    await callback.answer()
    await state.clear()
