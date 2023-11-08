# Использование тела запроса:

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    type: str
    features: dict

@app.post("/predict")
async def create_item(item: Item):
    # Здесь будет логика вашего предсказания
    # Вы можете использовать данные из item
    return item
