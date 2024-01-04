import os
import cv2
import math
import logging
import numpy as np

from glob import glob
from pathlib import Path

from utils.utils import Coordinate

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def load_items(path) -> list[str]:
    return [f for f in glob(path)]

class Searching:
    def __init__(self, screenshot:str, match_rate=0.8) -> None:
        self.screenshot = screenshot
        self.img_rgb = cv2.imread(screenshot)
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
            raise FileNotFoundError(f'Cannot find the item under: {item}')

        possible_coordinate = []
        item_name = item.split('/')[-1].replace('.png', '')
        pattern = cv2.imread(item, 0)
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

        return possible_coordinate

    def find_multiple_items(self, items:list[str]) -> list[Coordinate]:
        possible_coordinate = []
        for item in items:
            if len(search_rlt := self.find_one_item(item)) != 0:
                possible_coordinate += search_rlt

        return possible_coordinate

    def mark_item_on_screenshot(self, possible_coordinate, name=None):
        if len(possible_coordinate) == 0:
            LOGGER.error('Possible coordinate passed into the method is empty')
        for coor in possible_coordinate:
            cv2.circle(
                        img=self.img_rgb, center=(coor.x, coor.y), 
                        radius=5, color=(0, 0, 255), thickness=-1)
        if not name:
            name = self.screenshot.replace('.png', '_rlt.png')
        
        cv2.imwrite(name, self.img_rgb)

def search_for_coal(screenshot, threshold=0.8, show=False):
    coal_images_path = Path('../images/coal/*.png')
    items = load_items(str(coal_images_path))
    LOGGER.info(f'images: {items}')
    s = Searching(screenshot, match_rate=threshold)
    possible_location = s.find_multiple_items(items)
    if show:
        s.mark_item_on_screenshot(possible_location)

    return possible_location

if __name__ == "__main__":
    search = Searching(
        screenshot='/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/benchmark_3.png',
    )
    center = Coordinate(698, 380)
    rlt = search.find_one_item('/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/origin_ref.png')
    search.mark_item_on_screenshot(rlt)

    print("reference offset")
    for r in rlt:
        distance = r - center
        print(str(distance))

    # print(b)
