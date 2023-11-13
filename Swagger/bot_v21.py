from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiohttp import ClientSession, ClientTimeout
import json
import os
from datetime import datetime

# Загрузка переменных окружения
API_URL = os.getenv("API_URL")  # Например, "http://87.236.81.236:33021"

# Инициализация бота
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

@dp.message_handler(commands=['models'])
async def send_models(message: types.Message):
    timeout = ClientTimeout(total=10)  # Устанавливаем общий таймаут в 10 секунд

    async with ClientSession(timeout=timeout) as session:  # Инициализация асинхронной сессии HTTP
        try:
            response = await fetch(session, f"{API_URL}/models")  # Отправка GET запроса на API для получения списка моделей
            models_data = json.loads(response)  # Десериализация полученного JSON ответа
            models_list = models_data.get('Models', [])

            markup = InlineKeyboardMarkup()  # Создание разметки для inline-кнопок

            for model in models_list:  # Добавление inline-кнопок с моделями в разметку
                markup.add(InlineKeyboardButton(model, callback_data=model))

            current_time = datetime.now().strftime("%H:%M:%S")
            msg = f"🪩 Список доступных моделей (время: {current_time}):"
            await message.answer(msg, reply_markup=markup)  # Отправка сообщения с inline-кнопками

        except Exception as e:
            await message.answer(f"⛔ Невозможно загрузить список моделей. Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
