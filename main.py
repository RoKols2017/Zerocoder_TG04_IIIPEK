import asyncio
import logging
import os



from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from dotenv import load_dotenv

from kbd import more_kbd, options_kbd, url_kbd, start_kbd, build_keyboard
from utils import set_loglevel

load_dotenv()
TOKEN = os.getenv('TOKEN')
set_loglevel(level=os.getenv('LOG_LEVEL', 'INFO'))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['help']))
async def process_help_command(message: types.Message):
    await message.answer('''Я умею выполнять такие команды:
    /start - Запустить бота
    /help - Этот текст
    /links - Список ссылок
    /dynamic - Список опций
    ''')

@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer(text='Привет!', reply_markup= await build_keyboard(start_kbd, is_inline=False))

@dp.message(Command(commands=['links']))
async def process_links_command(message: types.Message):
    await message.answer(text='Список ссылок', reply_markup= await build_keyboard(url_kbd, is_inline=True, url=True))

@dp.message(Command(commands=['dynamic']))
async def process_dynamic_command(message: types.Message):
    await message.answer(text='Динамические опции', reply_markup= await build_keyboard(more_kbd, is_inline=True))

@dp.message(F.text.in_(start_kbd))
async def process_start_callback(message: types.Message):
    await message.answer(f"{message.text}, {message.from_user.full_name}!")

@dp.callback_query(F.data.in_(more_kbd.keys()))
async def process_more_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Обновленные опции", reply_markup= await build_keyboard(options_kbd, is_inline=True))

@dp.callback_query(F.data.in_(options_kbd.keys()))
async def process_options_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text=f"Вы выбрали {options_kbd[callback_query.data]}")


if __name__ == '__main__':
    dp.run_polling(bot)
