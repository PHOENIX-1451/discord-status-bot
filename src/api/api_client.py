import httpx

from src.api.api_mappings import APIMappings
from src.singleton import SingletonMeta


class APIClient(metaclass = SingletonMeta):

    def __init__(self, base_url = None, timeout = 10.0):
        if base_url is not None:
            # Create async client to make requests
            self.async_session = httpx.AsyncClient(base_url = base_url, timeout = timeout, headers = APIMappings.DEFAULT_HEADERS)

    async def post(self, data):
        # Merge headers (default + auth token)
        headers = {**self.async_session.headers, **data.get("headers")}
        # Send request
        response = await self.async_session.post(data["url"], headers = headers, json = data.get("payload"), params = data.get("params"), follow_redirects = False)
        # Return response
        return response

    async def get(self, data: dict):
        # Merge headers (default + auth token)
        headers = {**self.async_session.headers, **data.get("headers")}
        # Send request
        response = await self.async_session.get(data["url"], headers = headers, params = data.get("params"), follow_redirects = False)
        # Return response
        return response

    async def close_async_session(self):
        # Close session
        await self.async_session.aclose()
