Для запроса списка моделей с вашего FastAPI сервера из телеграм-бота, вам нужно написать функцию, которая будет выполнять HTTP GET запрос к вашему API. Вот пример кода телеграм-бота, который осуществляет такой запрос с использованием библиотеки `aiohttp` для асинхронного выполнения HTTP запросов:

```python
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
```

В этом коде пропущено обновление `.env` файла и вывод отладочной информации для упрощения примера. Обратите внимание, что нужно будет задать переменную `API_URL` в вашем файле `.env` или передать напрямую в код.

Если вам нужно использовать токен для доступа к API, то его можно добавить в заголовки запроса следующим образом:

```python
async def fetch(session, url, token):
    headers = {'Authorization': f'Bearer {token}'}
    async with session.get(url, headers=headers) as response:
        return await response.text()
```

Вам также потребуется передать этот токен при вызове функции `fetch`:

```python
response = await fetch(session, f"{API_URL}/models", "your_token_here")
``` 

Не забудьте подставить фактический токен авторизации в место `"your_token_here"` при реальном использовании кода.
