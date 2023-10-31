import requests

# Здесь замените на актуальный URL и порт вашего FastAPI сервера
url = 'http://localhost:8000/'

# Имя пользователя и пароль для авторизации
username = 'example'
password = 'example_password'

response = requests.get(url, params={'username': username, 'password': password})

# Проверка ответа
if response.status_code == 200:
    print(f"Success: {response.json()}")
else:
    print(f"Failed: {response.json()}")
