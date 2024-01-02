import os
import cv2
import math
import logging
import numpy as np

from glob import glob
from pathlib import Path

from utils.utils import Coordinate
from utils.screenshot import ScreenGrabber

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
TEMPLETE = r"images\coal"


def load_templete(path) -> list[str]:
    return [f for f in glob(path + r"\*.png")]


def matching(screenshot, templetes: list[str], threshold=0.8):
    rlt: dict = dict.fromkeys(templetes)
    img_rgb = cv2.imread(screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    for t in templetes:
        LOGGER.debug(f"Seraching templete: {t}")
        pattern = cv2.imread(t, 0)
        w, h = pattern.shape[::-1]
        res = cv2.matchTemplate(img_gray, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        possible_coordinate = [
            (int(c[0] + w / 2), int(c[1] + h / 2)) \
                                                for c in zip(*loc[::-1])]
        _append_only_diff_coordinates(t, possible_coordinate, rlt)

    LOGGER.info(f'Possible Location for {screenshot.split("/")[-1]}: {rlt}')

    for pt in rlt:
        cv2.circle(
            img=img_rgb, center=pt, radius=5, color=(0, 0, 255), thickness=-1)

    cv2.imwrite(screenshot, img_rgb)
    return rlt

def _append_only_diff_coordinates(templete, incomming_coor, rlt_coor):
    for c in incomming_coor:
        if not rlt_coor.get(templete, None):
            rlt_coor[templete] = [c]
        else:
            for r in rlt_coor[templete]:
                if _calculate_distance(c, r) < 5:
                    break
            else:
                rlt_coor[templete].append(c)

def _calculate_distance(x: list[int], y: list[int]) -> float:
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def search_for_coal(screenshot, threshold=0.8):
    templetes = load_templete(Path('images/coal'))
    possible_location = matching(screenshot, templetes, threshold)
    locations = []
    for key, value in possible_location.items():
        for coor in value:
            locations.append({
                'coordinate': coor,
                'type': key
            })
    return locations

if __name__ == "__main__":
    # matching(
    #     screenshot=r'images\benchmarks\benchmark_1.png',
    #     templete=r'images/coal/coal_2.png'
    # )
    screenshot, center, _ = ScreenGrabber()
    coal_location = matching(screenshot, load_templete(TEMPLETE))
    relative_location = [
        (center[0] - coal[0], center[1] - coal[1]) for coal in coal_location
    ]

    print(f"Relative location: {relative_location}")

    # print(b)
