from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from models.models import User, Proposal

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession
)


class DBConnection:
    """
    Класс подключения к базе данных (PostgreSQL).
    """

    def __init__(self):
        self.__async_session = async_session()

    async def __user_exists(self, telegram_id) -> bool:
        """Метод проверки существования пользователя."""
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.__async_session.execute(query)
        return result.scalar() is not None

    async def add_user(self, user: User) -> None:
        """Метод добавления пользователя в базу данных.

            Аргументы:
            • user (User) - объект пользователя.
        """
        user_exists = await self.__user_exists(user.telegram_id)
        if not user_exists:
            self.__async_session.add(user)
            await self.__async_session.commit()

    async def add_proposal(self, proposal: Proposal) -> None:
        """Метод добавления заявки в базу данных.

            Аргументы:
            • proposal (Proposal) - объект заявки.
        """
        self.__async_session.add(proposal)
        await self.__async_session.commit()

    async def top_up_balance(self, top_up_sum: int, telegram_id: int):
        """Метод пополнения баланса по telegram_id пользователя."""
        # Получаем пользователя по telegram_id
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.__async_session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            # Обновляем баланс пользователя
            user.balance += top_up_sum
            await self.__async_session.commit()

    async def get_user_id(self, telegram_id: int):
        """Метод получения primary_key id пользователя через telegram id."""
        query = select(User.id).where(User.telegram_id == telegram_id)
        result = await self.__async_session.execute(query)
        user_id = result.scalar()
        return user_id

    async def get_chat_id(self, telegram_id: int):
        """Получение id чата через telegram_id."""
        query = select(User.chat_id).where(User.telegram_id == telegram_id)
        result = await self.__async_session.execute(query)
        chat_id = result.scalar()
        return chat_id

    async def get_balance(self, telegram_id: int):
        """Получение баланса пользователя через telegram_id."""
        query = select(User.balance).where(User.telegram_id == telegram_id)
        result = await self.__async_session.execute(query)
        chat_id = result.scalar()
        return chat_id

    async def get_all_users_chat_id(self) -> list[int]:
        query = select(User.chat_id)
        result = await self.__async_session.execute(query)
        user_chat_ids = list(result.all())

        return user_chat_ids
