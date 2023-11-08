import requests

# Это URL для внутренней связи в Docker
url = 'http://app:8003/items'

# Здесь вы можете добавить необходимые заголовки, данные и прочее
response = requests.get(url)

# Обработка ответа
data = response.json()
