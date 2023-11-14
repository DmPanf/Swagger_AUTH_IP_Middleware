from fastapi import FastAPI, Request, Depends

app = FastAPI()

def get_client_ip(request: Request):
    if "x-forwarded-for" in request.headers:
        # В случае использования прокси, таких как Nginx
        ip = request.headers["x-forwarded-for"]
        ip = ip.split(",")[0]
    else:
        ip = request.client.host
    return ip

@app.get("/")
async def read_root(request: Request):
    client_ip = get_client_ip(request)
    return {"client_ip": client_ip}
