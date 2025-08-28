import os
import httpx

from src.api.api_mappings import APIMappings
from src.authorisation import Authorisation


class APICalls:

    @staticmethod
    async def get_server_data(self):
        try:
            data = {
                "url": APIMappings.BASE_URL + APIMappings.ENDPOINTS["getServerData"],
                "headers": {"x-token": Authorisation.generate_authcode(3)},
                "params": {
                    "usid": os.getenv("USID")
                }
            }
        except httpx.HTTPStatusError as hse:
            print(hse)
        except Exception as e:
            print(e)

