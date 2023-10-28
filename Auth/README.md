Для защиты Swagger UI в приложениях FastAPI от несанкционированного доступа можно использовать несколько методов:

### Использование переменных окружения

Вы можете использовать переменные окружения для активации/деактивации Swagger UI. Это не является методом защиты в строгом смысле, но позволяет вам быстро включать и выключать Swagger UI в зависимости от окружения (например, разработка, тестирование, продакшн).

### HTTP Basic Auth

Вы можете использовать базовую аутентификацию HTTP для доступа к Swagger UI. Примерно так:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(get_current_username)])
async def get_documentation():
    return FileResponse("path/to/docs")
```

### Использование API-ключа

Еще одним способом защиты является требование API-ключа для доступа к Swagger. Это может быть реализовано с помощью зависимостей.

```python
from fastapi import FastAPI, HTTPException, Depends, Request

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "mysecretkey":
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI()

@app.get("/openapi.json", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_openapi_json():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(...)

@app.get("/docs", tags=["documentation"], dependencies=[Depends(verify_api_key)])
async def get_documentation():
    return FileResponse("path/to/docs")
```

### Middleware для IP-фильтрации

Вы можете добавить middleware, который проверяет IP-адрес клиента. Это может быть полезным, если Swagger должен быть доступен только с определенных IP-адресов.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def filter_ip(request: Request, call_next):
    ALLOWED_IPS = ["127.0.0.1"]
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Access denied")
    return await call_next(request)
```

Обратите внимание, что эти методы можно комбинировать для дополнительной безопасности.
