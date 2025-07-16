import asyncio
import logging
import os



from aiogram import Bot, Dispatcher,types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from dotenv import load_dotenv

from kbd import reply_kbd
from utils import set_loglevel

load_dotenv()
TOKEN = os.getenv('TOKEN')
set_loglevel(level=os.getenv('LOG_LEVEL', 'INFO'))

bot = Bot(token=TOKEN)
dp = Dispatcher()
print
@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer(text='Привет!', reply_markup=reply_kbd)



if __name__ == '__main__':
    dp.run_polling(bot)
