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
    def __init__(self, screenshot:str, match_rate=0.8) -> None:
        self.screenshot = screenshot
        self.img_rgb = cv2.imread(self.screenshot)
        self.img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)
        self.match_rate = match_rate

    def find_one_item(self, item:str) -> list[Coordinate]:
        """ find item in the screen

        Args:
            item (str): path to the image to find in the screenshot

        Return:
            list: list containing possible coordinates
        """
        if not os.path.exists(item):
            logger.critical(f'Item: {item} cannot found')
            raise FileNotFoundError(f'Cannot find the item un   der: {item}')

        possible_coordinate = []
        # item_name = str(item).split('/')[-1].replace('.png', '')
        item_name = item
        logger.debug(f'finding item: {item_name} in screenshot: {self.screenshot}')
        pattern = cv2.imread(str(item), 0)
        w, h = pattern.shape[::-1]
        match_res = cv2.matchTemplate(
                                self.img_gray, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(match_res >= self.match_rate)
        for p in zip(*loc[::-1]):
            coordinate = Coordinate(
                                x = int(p[0] + w / 2),
                                y = int(p[1] + h / 2),
                                _type = item_name
                            )
            Coordinate.append_if_not_close(coordinate, possible_coordinate)

        if len(possible_coordinate) > 0:
            logger.info(
                f'Item found in following coordinates: {[str(c) for c in possible_coordinate]}'
            )
            return possible_coordinate
        else:
            logger.debug('item not found')

    def find_multiple_items(self, items:list[str]) -> list[Coordinate]:
        possible_coordinate = []
        for item in items:
            if search_rlt := self.find_one_item(item):
                possible_coordinate += search_rlt

        return possible_coordinate

def _search_and_return_coordinate(screenshot, img_root, threshold=0.8):
    img_root_path = str(Path(img_root))
    items = load_items(img_root_path)
    s = Searching(screenshot, match_rate=threshold)
    possible_location = s.find_multiple_items(items)
    if len(possible_location) > 0:
        return possible_location

def search_for_coal(screenshot, threshold=0.8, show=False):
    coal_images_path = Path('../images/coal/*.png')
    items = load_items(str(coal_images_path))
    logger.info(f'images: {items}')
    s = Searching(screenshot, match_rate=threshold)
    possible_location = s.find_multiple_items(items)
    if show:
        dimension_params = load_dimension_params()
        Mark_Coordinates(screenshot, possible_location).box(dimension_params)

    return possible_location

def find_ref_rock(screenshot, threshold=0.8):
    ref_image_root = '../images/benchmarks/refs/*.png'
    possible_location = _search_and_return_coordinate(screenshot, ref_image_root)
    return possible_location

if __name__ == "__main__":
    screenshot='/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/benchmark_2.png'
    possible_coordinates = find_ref_rock(screenshot)
    Mark_Coordinates(screenshot, possible_coordinates).box()