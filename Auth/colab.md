Для обращения к FastAPI эндпоинту из Google Colab, вы можете использовать библиотеку `requests`. Предположим, у нас есть FastAPI приложение, работающее на `http://localhost:8000/`, и мы хотим авторизоваться, передав имя пользователя и пароль.

### Пример FastAPI приложения (main.py)

```python
from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Хранение хешированных паролей и имен пользователей (в реальной жизни, это должно быть в БД)
users = {
    "example": pwd_context.hash("example_password"),
}

def verify_password(username: str, password: str):
    password_hash = users.get(username)
    if not password_hash or not pwd_context.verify(password, password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return username

@app.get("/", tags=["root"])
async def read_root(username = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}
```

Запустите это приложение с помощью `uvicorn main:app --reload`.

### Пример кода в Google Colab

```python
import requests

# Здесь замените на актуальный URL и порт вашего FastAPI сервера
url = 'http://localhost:8000/'

# Имя пользователя и пароль для авторизации
username = 'example'
password = 'example_password'

response = requests.get(url, params={'username': username, 'password': password})

# Проверка ответа
if response.status_code == 200:
    print(f"Success: {response.json()}")
else:
    print(f"Failed: {response.json()}")
```

Этот код выполняет HTTP GET запрос к FastAPI серверу с параметрами `username` и `password`. После выполнения запроса, ответ проверяется на статус код 200, который означает успешное выполнение запроса.

Обратите внимание, что передача параметров авторизации через URL-параметры является небезопасной практикой и представлена здесь только для демонстрационных целей. В реальном приложении лучше использовать более безопасные методы, такие как HTTP Basic Auth или OAuth2.
