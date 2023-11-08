## FastAPI

Чтобы добавить в ваш код авторизацию запросов по токену, можно использовать систему зависимостей FastAPI для создания функции, которая будет проверять токен перед выполнением операций. Для этого потребуется создать зависимость, которую можно использовать в пути операции. 

Вот обновленный код с добавлением простой проверки токена авторизации:

```python
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
# Импортируем остальные необходимые модули...

# Ваши остальные импорты и код...

# Токен авторизации для примера. В реальном приложении это должно быть защищено!
FAKE_TOKEN = "yourtokenhere"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def token_auth(token: str = Depends(oauth2_scheme)):
    if token != FAKE_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Неверный токен авторизации"
        )
    return token

@app.post('/predict')
async def predict(
    file: UploadFile = File(...),
    mdl_name: Optional[str] = Form(None),
    token: str = Depends(token_auth)):  # Добавляем зависимость проверки токена
    # Ваш код обработки предсказаний...
    pass

# Ваш код...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

В этом примере:

- `OAuth2PasswordBearer` используется для определения того, как клиент должен отправить токен.
- `token_auth` функция выполняет проверку полученного токена.
- В путь операции `predict` добавлена зависимость `token: str = Depends(token_auth)`, которая требует, чтобы запрос содержал действительный токен.

Обратите внимание, что это только пример использования статического токена. В реальном приложении вы бы использовали более безопасный механизм для генерации и проверки токенов, например, с использованием JWT (JSON Web Tokens) и соответствующего механизма их обновления.

## CURL

Для выполнения запроса к эндпоинту с использованием авторизации по токену через `curl`, вам нужно будет добавить заголовок `Authorization` с токеном в формате `Bearer <токен>`. Вот пример такого запроса:

```sh
curl -X 'GET' \
  'http://X.X.X.X:port/models' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer mytoken'
```

В этой команде:

- `-X 'GET'` указывает, что это GET запрос.
- `-H` добавляет заголовок к запросу. В данном случае, мы добавляем `accept: application/json`, который говорит серверу, что мы ожидаем ответ в формате JSON, и заголовок `Authorization` с токеном авторизации.
- После `-H 'Authorization: Bearer mytoken'` вы указываете схему авторизации (`Bearer`) и сам токен авторизации (`mytoken`).

Если эндпоинт `/models` настроен на использование токенов для авторизации и токен `vo1da2fon0` действителен, запрос должен быть успешно выполнен. Если эндпоинт не защищен токеном, то второй заголовок с токеном не потребуется.
---

## Telegram-Bot
Чтобы установить значение модели по умолчанию для параметра `mdl_name` в вашем эндпоинте `predict` в FastAPI, вы должны задать это значение по умолчанию в параметрах функции. Вместо того, чтобы устанавливать `None` в качестве значения по умолчанию, установите путь к вашей модели по умолчанию:

```python
async def predict(file: UploadFile = File(...), mdl_name: str = Form('./default/best.pt')):
    # Ваш код далее...
```

Теперь, если параметр `mdl_name` не будет предоставлен при вызове этого эндпоинта, он автоматически примет значение `'./default/best.pt'`.

Вам также может потребоваться убедиться, что значение по умолчанию соответствует тому, как вы хотите обрабатывать путь к модели:

```python
    # Если имя модели предоставлено и это не значение по умолчанию, создаем полный путь к модели
    if mdl_name and mdl_name != './default/best.pt':
        selected_model = os.path.join(default_mdl_path, mdl_name)
    else:
        selected_model = mdl_name  # Это уже полный путь к модели по умолчанию

    # Проверяем, существует ли файл модели
    if not os.path.exists(selected_model):
        return {"error": "Model file does not exist"}

    # Ваш код для использования selected_model далее...
```

Этот подход гарантирует, что если `mdl_name` не указан, будет использоваться значение по умолчанию, а если указано что-то, что отличается от пути по умолчанию, код попытается использовать это значение.

## Bot -> OAUTH

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
API_URL = os.getenv("API_URL")  # Например, "http://X.X.X.X:port"

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

---
## Swagger

Если Swagger UI запрашивает `username` и `password`, а также `client_id` и `client_secret`, это означает, что настроен OAuth2 с потоком пароля (password flow). В вашем предыдущем коде вы использовали `OAuth2PasswordBearer`, который предполагает получение токена через отдельный эндпоинт, который вы не предоставили.

Чтобы это работало с Swagger UI, вам нужно реализовать эндпоинт для получения токена. Вот пример того, как это может быть реализовано в FastAPI:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# Это должно быть безопасно храниться и проверяться
FAKE_USERS_DB = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Неправильное имя пользователя")
    user = UserModel(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Неправильный пароль")

    return {"access_token": user.username, "token_type": "bearer"}

# Ваши остальные эндпоинты и код...
```

После того, как у вас есть эндпоинт `/token`, вы можете использовать Swagger UI следующим образом:

1. Откройте Swagger UI (`/docs`).
2. Кликните `Authorize`.
3. В поля `username` и `password` введите данные, которые будут соответствовать вашей логике аутентификации (в примере выше, это может быть `johndoe` и пароль, который после хеширования будет соответствовать `fakehashedsecret`).
4. Поля `client_id` и `client_secret` могут быть оставлены пустыми, если ваша аутентификация не требует их.
5. Нажмите `Authorize`, чтобы получить токен.
6. Затем вы можете использовать другие эндпоинты, и токен будет автоматически включен в запросы.

Убедитесь, что ваши пути и логика аутентификации соответствуют тому, что поддерживается вашим API и Swagger UI. В реальных приложениях вы бы использовали более безопасный метод хеширования и проверки паролей, а также методы для сохранения и обновления токенов.
