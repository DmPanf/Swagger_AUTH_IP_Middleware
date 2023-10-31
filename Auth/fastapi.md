Для реализации авторизации по паролю в FastAPI с использованием файла `.env` для хранения хеша пароля и заданных имен, вы можете использовать библиотеку `python-dotenv` для чтения `.env` файла и библиотеку `passlib` для хеширования и проверки паролей.

### Подготовка

1. Установите FastAPI и Uvicorn, если еще не установлены:
    ```bash
    pip install fastapi uvicorn
    ```
  
2. Установите `python-dotenv` и `passlib`:
    ```bash
    pip install python-dotenv passlib
    ```

### Пример кода

#### .env
```
USERNAME=example
PASSWORD_HASH=hashed_password_here
```

#### main.py
```python
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

# Загрузка .env файла
load_dotenv()

# Инициализация FastAPI приложения
app = FastAPI()

# Инициализация CryptContext для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получение переменных окружения
USERNAME = os.getenv("USERNAME")
PASSWORD_HASH = os.getenv("PASSWORD_HASH")

# Зависимость для авторизации
def verify_password(username: str, password: str):
    if username != USERNAME:
        raise HTTPException(status_code=401, detail="Incorrect username")
    
    if not pwd_context.verify(password, PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return username

# Тестовый эндпоинт
@app.get("/", tags=["root"])
async def read_root(username = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}
```

Теперь, когда вы отправляете запрос к корневому эндпоинту (`/`), FastAPI будет использовать функцию `verify_password` для проверки имени пользователя и пароля.

Вы можете запустить приложение, используя следующую команду:

```bash
uvicorn main:app --reload
```

Этот код является простым примером и предназначен для демонстрационных целей. В реальном проекте рекомендуется использовать более продвинутые методы авторизации и аутентификации.
