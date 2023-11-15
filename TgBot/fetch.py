async def fetch(session, url, token=None):
    """
    Асинхронная функция для выполнения GET-запроса с использованием aiohttp.

    Параметры:
    - session (aiohttp.ClientSession): Экземпляр сессии для асинхронных HTTP-запросов.
    - url (str): URL для GET-запроса.
    - token (str, optional): Токен авторизации. Если None, запрос выполняется без авторизации.

    Возвращает:
    - str: Текстовый ответ от сервера.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    async with session.get(url, headers=headers) as response:
        return await response.text()
