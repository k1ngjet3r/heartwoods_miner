import os
import logging
import pyautogui
import pygetwindow as pgw

from PIL import Image

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

IMAGE_ROOT = "images"


def ScreenGrabber():
    image_name = os.path.join(IMAGE_ROOT, "test.png")
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
    im.save(image_name)


if __name__ == "__main__":
    image_name = os.path.join(IMAGE_ROOT, "test.png")
    ScreenGrabber()
    im = Image.open(image_name)
    im.show()
