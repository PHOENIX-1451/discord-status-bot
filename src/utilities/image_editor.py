from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from src.singleton import SingletonMeta


class ImageEditor(metaclass = SingletonMeta):

    def __init__(self, copy_path = f"{Path(__file__).resolve()}/temp/"):
        # Assign values
        self.fonts = {}
        self.copy_path = copy_path

    def add_font(self, key, font_path, size = 16):
        self.fonts[key] = ImageFont.truetype(font_path, size = size)

    def create_map_pfp(self, map_path, mode, favourites):
        # Open image file
        original = Image.open(map_path)
        # Create a copy (prevents the original from being edited)
        copy = original.copy()
        original.close()
        # Get width & height
        W, H = copy.size

        draw = ImageDraw.Draw(copy)
        # Add game mode
        mode_bounds = draw.textbbox((0, 0), mode, font = self.fonts.get("futura_large"))
        draw.text(
            ((W - mode_bounds[2]) / 2, (H - mode_bounds[3]) / 2 - 20), mode, font = self.fonts.get("futura_large")
        )

        # Add favourites
        star_bounds = draw.textbbox((0, 0), "\u2605" + favourites, font = self.fonts.get("dejavu_sans_small"))
        draw.text(
            ((W - star_bounds[2]) / 2, (H - star_bounds[3]) / 2 + 70), "\u2605" + favourites, font = self.fonts.get("dejavu_sans_small")
        )

        # Save in memory as bytes and return
        bytes_io = BytesIO()
        copy.save(bytes_io, format = "JPEG")
        return bytes_io.getvalue()




