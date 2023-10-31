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
