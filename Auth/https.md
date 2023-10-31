Для безопасной передачи учетных данных, вы можете использовать несколько подходов:

### 1. HTTPS

Используйте HTTPS для шифрования трафика между клиентом и сервером. Это основной шаг для обеспечения безопасности передаваемых данных.

### 2. HTTP Basic Authentication

Вы можете использовать HTTP Basic Authentication, где имя пользователя и пароль кодируются с использованием base64 и передаются в заголовке HTTP. FastAPI упрощает этот процесс.

#### FastAPI код:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "example": pwd_context.hash("example_password"),
}

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    
    if username not in users or not pwd_context.verify(password, users[username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return username

@app.get("/", tags=["root"])
def read_root(username: str = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}
```

#### Код в Google Colab:

```python
import requests
from requests.auth import HTTPBasicAuth

url = 'https://localhost:8000/'  # Используйте HTTPS
username = 'example'
password = 'example_password'

response = requests.get(url, auth=HTTPBasicAuth(username, password))

if response.status_code == 200:
    print(f"Success: {response.json()}")
else:
    print(f"Failed: {response.json()}")
```

### 3. OAuth2

Для еще большей безопасности, вы можете использовать OAuth2 с токенами. Этот метод является стандартом для современных веб-приложений и API.

### 4. Custom Headers

Вы также можете передать учетные данные в пользовательских заголовках HTTP, хотя это и не является стандартным методом.

#### FastAPI код:

```python
from fastapi import FastAPI, Request, HTTPException
from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "example": pwd_context.hash("example_password"),
}

def verify_password(request: Request):
    username = request.headers.get("X-Username")
    password = request.headers.get("X-Password")

    if username not in users or not pwd_context.verify(password, users[username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return username

@app.get("/", tags=["root"])
def read_root(username: str = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}
```

#### Код в Google Colab:

```python
import requests

url = 'https://localhost:8000/'  # Используйте HTTPS
headers = {'X-Username': 'example', 'X-Password': 'example_password'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"Success: {response.json()}")
else:
    print(f"Failed: {response.json()}")
```

Выберите подход, который наиболее подходит для вашего случая. На практике часто используют комбинацию этих методов.
