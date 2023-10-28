### Запуск FastAPI
- **`uvicorn main:app --host 0.0.0.0 --port 8000`**

### Примеры с использованием `curl`

Для проверки работы API с помощью `curl`, вы можете выполнить следующие команды:

1. Для доступа к корневому эндпоинту с API-ключом "123abc":

    ```bash
    curl -G "http://127.0.0.1:8000/" --data-urlencode "api_key=123abc"
    ```

2. Для доступа к эндпоинту `/info` с паролем "mysecretpassword":

    ```bash
    curl -G "http://127.0.0.1:8000/info" --data-urlencode "password=mysecretpassword"
    ```

### Примеры с использованием Google Colab и Python

Для выполнения запросов из Google Colab, вы можете использовать библиотеку `requests`. Пример кода:

```python
import requests

# Запрос к корневому эндпоинту с API-ключом "123abc"
response = requests.get("http://127.0.0.1:8000/", params={"api_key": "123abc"})
print(f"Response from /: {response.json()}")

# Запрос к эндпоинту /info с паролем "mysecretpassword"
response = requests.get("http://127.0.0.1:8000/info", params={"password": "mysecretpassword"})
print(f"Response from /info: {response.json()}")
```

Важно, что IP-адрес и порт (`127.0.0.1:8000`) должны соответствовать тем, на которых запущен ваш FastAPI сервер. Если сервер запущен на другой машине или в контейнере, надо заменить адрес и порт на соответствующие.
