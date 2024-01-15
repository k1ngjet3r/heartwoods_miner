import os
import cv2
import numpy as np

from glob import glob
from pathlib import Path
from loguru import logger

from utils.utils import Coordinate, load_dimension_params
from utils.screenshot import Mark_Coordinates


def load_items(path) -> list[str]:
    return [f for f in glob(path)]


class Searching:
    def __init__(self, screenshot: str, match_rate=0.8) -> None:
        self.screenshot = screenshot
        self.img_rgb = cv2.imread(self.screenshot)
        self.img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)
        self.match_rate = match_rate

    def find_one_item(self, item: str) -> list[Coordinate]:
        """find item in the screen

        Args:
            item (str): path to the image to find in the screenshot

        Return:
            list: list containing possible coordinates
        """
        if not os.path.exists(item):
            logger.critical(f"Item: {item} cannot found")
            raise FileNotFoundError(f"Cannot find the item under: {item}")

        possible_coordinate = []
        # item_name = str(item).split('/')[-1].replace('.png', '')
        logger.debug(f"finding item: {item} in screenshot: {self.screenshot}")
        pattern = cv2.imread(str(item), 0)
        w, h = pattern.shape[::-1]
        match_res = cv2.matchTemplate(self.img_gray, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(match_res >= self.match_rate)
        for p in zip(*loc[::-1]):
            coordinate = Coordinate(
                                x = int(p[0] + w / 2),
                                y = int(p[1] + h / 2),
                                _type = item
                            )
            Coordinate.append_if_not_close(coordinate, possible_coordinate)

        if len(possible_coordinate) > 0:
            logger.info(
                f"Item found in following coordinates: {[str(c) for c in possible_coordinate]}"
            )
            return possible_coordinate
        else:
            logger.debug("item not found")

    def find_multiple_items(
        self, items: list[str], mark=False, mark_color=(0, 0, 255)
    ) -> list[Coordinate]:
        possible_coordinate = []
        for item in items:
            if search_rlt := self.find_one_item(item):
                possible_coordinate += search_rlt

        if len(possible_coordinate) > 0 and mark:
            Mark_Coordinates()

        return possible_coordinate


def _search_and_return_coordinate(screenshot, img_root, threshold=0.8):
    img_root_path = str(Path(img_root))
    items = load_items(img_root_path)
    s = Searching(screenshot, match_rate=threshold)
    possible_location = s.find_multiple_items(items)
    if len(possible_location) > 0:
        return possible_location


def search_for_coal(screenshot, threshold=0.8, show=False):
    coal_img_root = "../images/coal/*.png"
    possible_location = _search_and_return_coordinate(
        screenshot, coal_img_root, threshold
    )
    if possible_location:
        if show:
            Mark_Coordinates(screenshot, possible_location).box(color="green")

        return possible_location


def find_ref_rock(screenshot, threshold=0.8, show=False):
    ref_image_root = "../images/benchmarks/refs/ref_rock_left_top.png"
    possible_location = _search_and_return_coordinate(
        screenshot, ref_image_root, threshold
    )
    if possible_location:
        if show:
            Mark_Coordinates(screenshot, possible_location).box(color="red")
        return possible_location


if __name__ == "__main__":
    screenshot = str(Path("../images/benchmarks/benchmark_3.png"))
    search_for_coal(screenshot, show=True)
    find_ref_rock(screenshot, show=True)
