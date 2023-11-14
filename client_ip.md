## Client IP

Для определения IP-адреса пользователя при использовании Swagger UI в FastAPI, вы можете получить IP из объекта запроса Request, который предоставляется FastAPI. IP-адрес можно извлечь из заголовков запроса.

Вот пример функции, которая извлекает IP-адрес из запроса:

```python
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

```

Этот код сначала проверяет наличие заголовка X-Forwarded-For, который часто используется прокси-серверами (такими как Nginx или load balancers), для передачи реального IP-адреса клиента.
Если заголовка нет, используется request.client.host.
