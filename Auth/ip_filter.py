from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def filter_ip(request: Request, call_next):
    ALLOWED_IPS = ["127.0.0.1"]
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Access denied")
    return await call_next(request)
