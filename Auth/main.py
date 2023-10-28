from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEYS = os.getenv("API_KEYS").split(",") if os.getenv("API_KEYS") else []  # Эмуляция хранения API ключей
INFO_PASSWORD = os.getenv("INFO_PASSWORD")  # Пароль для доступа к эндпоинту /info

@app.get("/")
def read_root(api_key: str = Query(...)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"message": "Hello, you have access!"}

@app.get("/info")
def get_info(password: str = Query(...)):
    if password != INFO_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    project_name = "My Awesome Project"
    return {"current_time": current_time, "project_name": project_name}
