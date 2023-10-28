# Examples of implementing the following measures to protect Swagger UI endpoints from unauthorized access:

1. Use authentication and authorization: Implement authentication and authorization mechanisms to ensure that only authorized users can access your Swagger UI endpoints. You can use popular libraries like `fastapi-auth` or `fastapi-jwt` to handle authentication and authorization.
2. Use rate limiting: Implement rate limiting to prevent excessive requests to your Swagger UI endpoints, which could be a sign of an attack. You can use libraries like `fastapi-limiter` to implement rate limiting.
3. Use CORS policies: Implement Cross-Origin Resource Sharing (CORS) policies to allow or deny requests from different origins. This will help protect your endpoints from being accessed by unauthorized users. You can use libraries like `fastapi-cors` to implement CORS policies.
4. Use SSL/TLS encryption: Encrypt your Swagger UI endpoints using SSL/TLS certificates to protect data in transit. This will help prevent eavesdropping and man-in-the-middle attacks.
5. Implement password hashing: Store user passwords securely by hashing them using a suitable hashing algorithm, such as bcrypt or Argon2. This will help prevent unauthorized access to user accounts.
6. Use secure cookies: Use secure cookies to store user sessions, and ensure that the cookie prefix is not predictable to prevent attacks like session hijacking.
7. Implement input validation: Validate user inputs to prevent malicious attacks like SQL injection or cross-site scripting (XSS).
8. Use a web application firewall (WAF): Use a WAF to protect your Swagger UI endpoints from known and unknown attacks. You can use libraries like `fastapi-waf` to implement WAF rules.
9. Regularly update and patch your dependencies: Regularly update and patch your dependencies, including FastAPI and its dependencies, to ensure that you have the latest security fixes.
10. Use a vulnerability scanner: Use a vulnerability scanner to identify potential vulnerabilities in your Swagger UI endpoints and address them before they can be exploited by attackers.

By implementing these measures, you can significantly improve the security of your FastAPI application and protect it from unauthorized access and attacks.

---

## Для защиты Swagger UI в приложениях FastAPI от несанкционированного доступа можно использовать несколько методов:

### Использование переменных окружения

Вы можете использовать переменные окружения для активации/деактивации Swagger UI. Это не является методом защиты в строгом смысле, но позволяет вам быстро включать и выключать Swagger UI в зависимости от окружения (например, разработка, тестирование, продакшн).

### HTTP Basic Auth

Вы можете использовать базовую аутентификацию HTTP для доступа к Swagger UI. Примерно так:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_documentation():
    return FileResponse("path/to/docs")
```

### Использование API-ключа

Еще одним способом защиты является требование API-ключа для доступа к Swagger. Это может быть реализовано с помощью зависимостей.

```python
from fastapi import FastAPI, HTTPException, Depends, Request

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "mysecretkey":
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_documentation():
    return FileResponse("path/to/docs")
```

### Middleware для IP-фильтрации

Вы можете добавить middleware, который проверяет IP-адрес клиента. Это может быть полезным, если Swagger должен быть доступен только с определенных IP-адресов.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def filter_ip(request: Request, call_next):
    ALLOWED_IPS = ["127.0.0.1"]
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Access denied")
    return await call_next(request)
```

Обратите внимание, что эти методы можно комбинировать для дополнительной безопасности.

---

## Интеграция Telegram бота с FastAPI:

### Шаг 1: Настройка Telegram бота на базе AIOGram
```python
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor

bot = Bot(token="YOUR_BOT_TOKEN_HERE")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ALLOWED_USER_ID = 123456789  # Замените на ваш Telegram User ID

async def send_message_to_admin(*args, **kwargs):
    await bot.send_message(chat_id=ALLOWED_USER_ID, text="Bot started")

@dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=["add_ip"])
async def add_ip(message: types.Message):
    ip_address = message.get_args()
    if not ip_address:
        await message.reply("Please provide an IP address.")
        return

    # Добавляем IP-адрес в .env или другой конфигурационный файл
    with open(".env", "a") as f:
        f.write(f"\nALLOWED_IP={ip_address}")

    await message.reply(f"IP address {ip_address} added.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=send_message_to_admin)
```

### Шаг 2: Чтение разрешенных IP из .env в FastAPI
Вы можете использовать библиотеку `python-dotenv` для чтения переменных из `.env` файла.

```python
from fastapi import FastAPI, Request, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ALLOWED_IPS = os.getenv("ALLOWED_IPS").split(",")

@app.middleware("http")
async def filter_ip(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Access denied")
    return await call_next(request)
```

### Шаг 3: Обновление списка разрешенных IP во время выполнения
Если вы хотите обновлять список IP без перезапуска FastAPI приложения, вы можете хранить их в глобальной переменной или другом хранилище, которое можно изменить во время выполнения. В этом случае Telegram-бот может просто модифицировать эту глобальную переменную.

