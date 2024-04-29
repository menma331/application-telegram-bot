from datetime import datetime

from aiogram.types import DateTime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Table, Boolean, \
    Double, ForeignKey, ForeignKeyConstraint, Index, Numeric
from sqlalchemy.dialects.postgresql import NUMRANGE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    registration_at: Mapped[DateTime] = mapped_column(
        type_=TIMESTAMP, default=datetime.utcnow
    )


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(type_=Integer, primary_key=True)
    username: Mapped[str] = mapped_column(type_=String(45), nullable=False)
    telegram_id: Mapped[int] = mapped_column(type_=Integer, nullable=False)
    chat_id: Mapped[int] = mapped_column(type_=Integer, nullable=False)
    balance: Mapped[int] = mapped_column(
        nullable=True, type_=Integer,
        default=0.0
    )
    is_superuser: Mapped[bool] = mapped_column(
        type_=Boolean, default=False,
        nullable=False
    )


class Proposal(Base):
    __tablename__ = 'proposal'

    id: Mapped[int] = mapped_column(type_=Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(type_=Integer)
    business_line: Mapped[str] = mapped_column(type_=String(30))
    platform_of_bot: Mapped[str] = mapped_column(type_=String(30))
    range_of_budget: Mapped[NUMRANGE] = mapped_column(type_=NUMRANGE)
    phone_number: Mapped[str] = mapped_column(type_=String(15))

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id']),
    )
