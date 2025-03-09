import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = 'http://127.0.0.1:8000/api/'
MEDIA_URL = 'http://127.0.0.1:8000/media/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выбери букву для изучения:", reply_markup=get_main_menu())

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Буквы", callback_data="letters")],
    ])
    return keyboard

@dp.callback_query(lambda c: c.data == 'letters')
async def process_callback(callback_query: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}letters/") as response:
            data = await response.json()

    if isinstance(data, list) and len(data) > 0:
        item = data[0]
        await send_item(callback_query.message, item)
    else:
        await bot.answer_callback_query(callback_query.id, "Данные не найдены.")

async def send_item(message: types.Message, item):
    text = f"**{item['text']}**"
    await bot.send_message(message.chat.id, text, parse_mode="Markdown")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Произнести", callback_data=f"pronounce_{item['id']}")],
    ])
    await bot.send_message(message.chat.id, "Нажми, чтобы услышать:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('pronounce_'))
async def process_pronounce(callback_query: types.CallbackQuery):
    _, item_id = callback_query.data.split('_')

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}letters/{item_id}/") as response:
            data = await response.json()

    if data and data.get('audio'):
        audio_url = data['audio']  # Используем полный URL из API
        print(f"Аудио URL: {audio_url}")  # Отладочное сообщение

        try:
            # Отправляем аудио
            await bot.send_audio(callback_query.message.chat.id, audio_url)
            print("Аудио успешно отправлено.")  # Отладочное сообщение
        except Exception as e:
            print(f"Ошибка при отправке аудио: {e}")  # Отладочное сообщение
            await bot.answer_callback_query(callback_query.id, "Ошибка при отправке аудио.")
    else:
        await bot.answer_callback_query(callback_query.id, "Аудио не найдено.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())