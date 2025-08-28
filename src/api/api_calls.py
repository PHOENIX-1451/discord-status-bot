import os
import httpx

from src.api import APIClient
from src.api.api_mappings import APIMappings
from src.authorisation import Authorisation


class APICalls:

    @staticmethod
    async def get_server_data():
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
            server_data =  await api_client.get(data)
            # Return request
            return server_data.json()
        except httpx.HTTPStatusError as hse:
            print(hse)
        except Exception as e:
            print(e)

