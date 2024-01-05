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
class Screenshot:
    name: str
    relative_center: Coordinate
    size: tuple
    top_left_corner: Coordinate = None
    boundary: Boundary = None
    absolute_center: Coordinate = None

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
    im = im.crop((left, top+TITLE_BAR_OFFSET, right, bottom))
    # LOGGER.info(f"Screen Center: {left+10, top+10}")
    im.save(image_name)
    w, h = im.size

    absolute_center = Coordinate((left + right) / 2, (top + TITLE_BAR_OFFSET + bottom) / 2)
    relative_center = Coordinate(int(w/2), int(h/2))
    window_top_left_corner = Coordinate(left + 10, top + 10)
    boundary = Boundary(0, 0, right, bottom-TITLE_BAR_OFFSET)
    return Screenshot(
        name = image_name, 
        relative_center = relative_center, 
        size = (w, h),
        top_left_corner = window_top_left_corner,
        boundary=boundary, 
        absolute_center=absolute_center
    )

def get_screenshot_info(screenshot):
    im = Image.open(screenshot)
    size = im.size
    return Screenshot(
        name = screenshot,
        relative_center = Coordinate(int(size[0]/2), int(size[1]/2)),
        size = size,
    )

def trim_title_bar(screenshot):
    im = Image.open(screenshot)
    w, h = im.size
    im = im.crop((0, TITLE_BAR_OFFSET, w, h))
    im.save(screenshot)


if __name__ == "__main__":
    # ScreenGrabber()
    img = '/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/benchmark_3.png'
    trim_title_bar(img)
    ss = get_screenshot_info(img)
    print(f'name: {ss.name}')
    print(f'relative_center: {ss.relative_center}')
    print(f'size: {ss.size}')
    # im = Image.open(image_name)
    # im.show()
