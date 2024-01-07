import os
import logging
import pyautogui
import pygetwindow as pgw

from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from PIL import Image

from utils.utils import Coordinate, Boundary

LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

IMAGE_ROOT = str(Path("../images"))

TITLE_BAR_OFFSET = 31

@dataclass
class game_resolution:
    x = 1280
    y = 720
    x_offset = 8
    y_offset = 31

@dataclass
class Screenshot:
    """ Storing the detail of a screen shot

    Args:
        filepath (str): name of the saved screenshot filepath
        screen_center (Coordinate): the screen center of the game window (including the title bar)
        character_coordinate (Coordinate): the center of the game screen (exclude the title bar)

    """
    filepath: str
    window_center: Coordinate
    character_center: Coordinate
    top_left_coordinate: Coordinate = None

def take_screenshot(new_file=False):
    if new_file:
        filename = datetime.now().strftime("%H_%M_%S") + ".png"
    else:
        filename = 'screenshot.png'
    image_name = os.path.join(IMAGE_ROOT, filename)
    titles = pgw.getAllTitles()
    if "Heartwood Online" not in titles:
        LOGGER.error("Heartwood Online window cannot be found!")
    else:
        window = pgw.getWindowsWithTitle("Heartwood Online")[0]

        left, top = window.topleft
        right, bottom = window.bottomright

        corrected_left = left + game_resolution.x_offset
        corrected_top = top + game_resolution.y_offset
        corrected_right = corrected_left + game_resolution.x
        corrected_bottom = corrected_top + game_resolution.y

        pyautogui.screenshot(image_name)
        im = Image.open(image_name)
        im = im.crop((
            corrected_left , corrected_top, corrected_right, corrected_bottom))
        im.save(image_name)

        window_center = Coordinate(
            int((left + right) / 2),
            int((top + bottom) / 2)
        )
        character_center = Coordinate(
            int(game_resolution.x_offset + game_resolution.x / 2 + left),
            int(game_resolution.y_offset + game_resolution.y / 2 + top)
        )
        top_left_coordinate = Coordinate(left + 10, top + 10)
        return Screenshot(
            image_name,
            window_center,
            character_center,
            top_left_coordinate
        )

if __name__ == "__main__":
    take_screenshot()
