В FastAPI, вы можете ограничить доступ к документации Swagger UI (или другой документации, такой как ReDoc), используя зависимости. Один из самых простых способов сделать это — это использование HTTP Basic Auth или токена для авторизации.

### Пример с HTTP Basic Auth:

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "password"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return credentials.username

@app.get("/docs", tags=["documentation"], include_in_schema=False)
async def custom_swagger_ui_html(req: Request, username: str = Depends(verify_password)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url=req.url_for("openapi_schema"))

@app.get("/openapi.json", tags=["documentation"], include_in_schema=False)
async def openapi_schema(username: str = Depends(verify_password)):
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Custom schema", version=1, routes=app.routes)
```

### Пример с токеном:

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyQuery

app = FastAPI()

api_key = APIKeyQuery(name="api_key", auto_error=False)

def verify_token(api_key: str = Depends(api_key)):
    correct_api_key = "mysecretpassword"
    if api_key != correct_api_key:
        raise HTTPException(status_code=401, detail="Incorrect API Key")
    return api_key

@app.get("/docs", tags=["documentation"], include_in_schema=False)
async def custom_swagger_ui_html(req: Request, api_key: str = Depends(verify_token)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url=req.url_for("openapi_schema"))

@app.get("/openapi.json", tags=["documentation"], include_in_schema=False)
async def openapi_schema(api_key: str = Depends(verify_token)):
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Custom schema", version=1, routes=app.routes)
```

В этих примерах, если пользователь пытается зайти на `/docs` (Swagger UI) или `/openapi.json`, ему потребуется либо правильный Basic Auth (первый пример), либо корректный API ключ в параметре запроса (второй пример).

Теперь доступ к Swagger UI и OpenAPI схеме ограничен и требует аутентификации.
