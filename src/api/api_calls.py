import os
from datetime import datetime

import httpx

from src.api import APIClient
from src.api.api_mappings import APIMappings
from src.authorisation import Authorisation


class APICalls:

    # Cache responses
    CACHE = {}

    @classmethod
    def access_cache(cls, key):
        return cls.CACHE.get(key)

    @classmethod
    async def get_server_data(cls):
        try:
            data = {
                "url": APIMappings.BASE_URL + APIMappings.ENDPOINTS["getServerData"],
                "headers": {"x-token": Authorisation.generate_authcode(3)},
                "params": {
                    "usid": os.getenv("USID")
                }
            }
            # Send request
            api_client = APIClient()
            response =  await api_client.get(data)
            # Check if an error occurred
            response.raise_for_status()
            server_data = response.json()
            # Store in cache
            cls.CACHE[cls.get_server_data] = server_data
            # Return data
            return server_data
        except httpx.HTTPStatusError as hse:
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: API Call HTTPError - {hse}")
            if hse.response.status_code == 404:
                cls.CACHE[cls.get_server_data] = "Server not found :("
            else:
                cls.CACHE[cls.get_server_data] = "Error"
        except Exception as e:
            cls.CACHE[cls.get_server_data] = "[Error]"
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: API Call - {e}")

