import os
from datetime import datetime
import logging
import pyautogui
import pygetwindow as pgw

from PIL import Image

from utils.utils import Coordinate

LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

IMAGE_ROOT = "images"

class Window:
    def __inti__(self, name, center:Coordinate, top_left_corner):
        self.name = name
        self.center = center
        self.top_left_corner = top_left_corner

def ScreenGrabber(new_file=False):
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

    pyautogui.screenshot(image_name)
    im = Image.open(image_name)
    im = im.crop((left, top, right, bottom))
    # LOGGER.info(f"Screen Center: {left+10, top+10}")
    im.save(image_name)
    center = ((left + right) / 2, (top + bottom) / 2)
    window_top_left_corner = (left + 10, top + 10)
    return Window(image_name, center, window_top_left_corner)


if __name__ == "__main__":
    ScreenGrabber()
    # im = Image.open(image_name)
    # im.show()
