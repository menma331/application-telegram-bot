from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from database import DBConnection

bot = Bot(token=TOKEN)
disp = Dispatcher()
db_connection = DBConnection()
storage = MemoryStorage()
