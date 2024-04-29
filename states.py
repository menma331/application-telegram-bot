from aiogram.fsm.state import State, StatesGroup


class SubmitApplicationStates(StatesGroup):
    """Класс состояний оформления заявки."""
    CHOOSE_LINE_OF_BUSINESS_STATE = State()
    CHOOSE_PLATFORM_STATE = State()
    BUDGET_REQUEST_STATE = State()
    WAIT_FOR_PHONE_STATE = State()
    FINISHED_APPLICATION_STATE = State()


class TopUpBalanceStates(StatesGroup):
    """Класс состояний покупки товара."""
    BUY_PRODUCT = State()


class AdminStates(StatesGroup):
    """Класс состояний для обработчиков администратора."""
    WAIT_FOR_ADMIN_MESSAGE = State()
    WAIT_FOR_CONFIRM = State()
