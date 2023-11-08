# Использование Path параметров:

from fastapi import FastAPI

app = FastAPI()

@app.get("/predict/{item_id}")
async def read_item(item_id: int):
    # Здесь будет логика вашего предсказания
    return {"item_id": item_id}
