import asyncio
import os
import random
import discord
from datetime import datetime
from pathlib import Path
from discord.errors import HTTPException
from discord.ext import tasks

from src.api import APIClient, APICalls
from src.api.api_mappings import APIMappings
from src.utilities import Mappings
from src.utilities.image_editor import ImageEditor


class StatusBot(discord.Client):

    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DEFAULT = False
    PREVIOUS_SERVER_INFO = {
        "name": "",
        "region": "",
        "country": "",
        "map": ""
    }

    async def on_ready(self):
        # Initialise API client singleton
        APIClient(base_url = APIMappings.BASE_URL)
        ie = ImageEditor()
        ie.add_font("futura_large", f"{self.PROJECT_ROOT}/assets/fonts/Futura.ttf", 130)
        ie.add_font("dejavu_sans_small", f"{self.PROJECT_ROOT}/assets/fonts/DejaVu Sans.ttf", 45)
        await APICalls.get_server_data()
        print("Bot Ready")
        # Start update loop
        self.refresh_cache.start(int(os.environ.get("BASE_REFRESH_INTERVAL")))
        self.update_profile.start()
        self.update_rich_presence.start()

    async def close(self):
        # Close API client session
        api_client = APIClient()
        await api_client.close_async_session()
        # Close connection to discord
        await super().close()
        print("Bot Terminated")


    @tasks.loop()
    async def refresh_cache(self, base_refresh_interval):
        # Call api
        await APICalls.get_server_data()
        # Jitter to prevent API calls from syncing (Base refresh interval + random int)
        await asyncio.sleep(base_refresh_interval + random.randint(0, 5))

    @tasks.loop(seconds = 12)
    async def update_rich_presence(self):
        # Access data
        server_data = APICalls.access_cache(APICalls.get_server_data)

        # Check if there was an error
        if isinstance(server_data, str):
            if not self.DEFAULT:
                # Reset everything to default
                await self.default(server_data)
                return
        else:
            # Update rich presence
            player_count = server_data["info"]["serverInfo"]
            # Check if there is a queue
            if server_data["info"]["inQue"] > 0:
                # Include players in Queue
                player_count += f" [{server_data["info"]["inQue"]}]"
            player_count += f" - {server_data["info"]["map"]} ({server_data["info"]["mode"]})"

            # Update rich presence
            activity = discord.Game(name = player_count)
            await self.change_presence(activity = activity)
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: Updated Rich Presence ({player_count})")

    @tasks.loop(seconds = 60)
    async def update_profile(self):
        try:
            # Access data
            server_data = APICalls.access_cache(APICalls.get_server_data)

            # Check if there was an error
            if not isinstance(server_data, str) :
                if server_data["info"]["map"] != self.PREVIOUS_SERVER_INFO["map"]:
                    self.PREVIOUS_SERVER_INFO["map"] = server_data["info"]["map"]
                    # Get map image (Banner)
                    path = f"{self.PROJECT_ROOT}/assets/images/maps/{Mappings.MAP_FILE_MAPPINGS[server_data["info"]["map"]]}"
                    with open(path, "rb") as f:
                        banner_bytes = f.read()
                    # Get Profile picture (as bytes)
                    image_editor = ImageEditor()
                    profile_picture_bytes = image_editor.create_map_pfp(path, server_data["info"]["smallmode"], str(server_data["info"]["favourites"]))
                    # Change profile picture and banner
                    await self.user.edit(avatar = profile_picture_bytes, banner = banner_bytes)
                    self.DEFAULT = False
                    print(f"[{datetime.now().strftime("%H:%M:%S")}]: Updated profile picture and banner ({server_data["info"]["map"]})")

        except HTTPException as he:
            # Get error details
            error = await he.response.json()
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: {error}")

            # Check if profile update got rate limited
            avatar_error = error["errors"].get("avatar")
            banner_error = error["errors"].get("banner")

            # Retry if profile update got rate limited
            if avatar_error:
                if avatar_error["_errors"][0]["code"] == "AVATAR_RATE_LIMIT":
                    self.PREVIOUS_SERVER_INFO["map"] = ""
            elif banner_error:
                if banner_error["_errors"][0]["code"] == "BANNER_RATE_LIMIT":
                    self.PREVIOUS_SERVER_INFO["map"] = ""

        except Exception as e:
            print(type(e))
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: PB - {e}")

    async def default(self, message):
        try:
            # Change rich presence to the provided message
            activity = discord.Game(name = message)
            # Apply changes
            await self.change_presence(activity = activity)

            # Change profile picture & banner to defaults
            with open(f"{self.PROJECT_ROOT}/assets/images/default/BoB Profile Picture.png", "rb") as f:
                profile_picture = f.read()

            with open(f"{self.PROJECT_ROOT}/assets/images/default/BoB GIF Banner.gif", "rb") as f:
                banner = f.read()

            # Apply changes
            await self.user.edit(avatar = profile_picture, banner = banner)
            self.PREVIOUS_SERVER_INFO["map"] = ""
            self.DEFAULT = True
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: Reset to default")
        except HTTPException as he:
            # Get error details
            error = await he.response.json()
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: {error}")
            # Check if profile update got rate limited
            avatar_error = error["errors"].get("avatar")
            banner_error = error["errors"].get("banner")
            # Retry if profile update got rate limited
            if avatar_error:
                if avatar_error["_errors"][0]["code"] == "AVATAR_RATE_LIMIT":
                    self.DEFAULT = False
            elif banner_error:
                if banner_error["_errors"][0]["code"] == "BANNER_RATE_LIMIT":
                    self.DEFAULT = False
        except Exception as e:
            print(f"[{datetime.now().strftime("%H:%M:%S")}]: D - {e}")