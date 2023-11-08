from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
async def read_item(item_id: int = None, item_type: str = None):
    # Здесь будет логика вашего предсказания
    # Возвращаемый результат может зависеть от item_id, item_type, обоих или ни одного
    return {"item_id": item_id, "item_type": item_type}
