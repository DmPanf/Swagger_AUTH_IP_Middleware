async def fetch(session, url, token):
    headers = {'Authorization': f'Bearer {token}'}
    async with session.get(url, headers=headers) as response:
        return await response.text()
