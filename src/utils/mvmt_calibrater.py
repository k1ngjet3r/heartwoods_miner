import sys
import time
import logging

from pprint import pprint

from utils.recon import Searching
from utils.ctrl import Character_Ctrl
from utils.screenshot import take_screenshot
from utils.utils import Coordinate

BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\benchmarks\river_rock.png"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
CTRL = Character_Ctrl()


def movement_calibration(direction):
    def _rock_coordinate():
        screenshot = take_screenshot()
        if rock_found := Searching(screenshot.name).find_one_item(BENCHMARK_ROCK):
            return rock_found[0]

    if p1 := _rock_coordinate():
        if direction == "up":
            CTRL._move_vertical(-1, debug=True)
        elif direction == "down":
            CTRL._move_vertical(1, debug=True)
        elif direction == "right":
            CTRL._move_horizonal(1, debug=True)
        elif direction == "left":
            CTRL._move_horizonal(-1, debug=True)
        else:
            logging.error("Invalid direction!")
    time.sleep(0.5)
    p2 = _rock_coordinate()

    delta = p2 - p1
    return delta


if __name__ == "__main__":
    order = {"right": [], "up": [], "left": [], "down": []}

    ctrl = Character_Ctrl()
    ctrl.click_window(Coordinate(7, 19))

    for i in range(50):
        LOGGER.debug(f"round: {i}")
        for direction in order.keys():
            delta = movement_calibration(direction)
            if direction in ["right", "left"]:
                delta = delta.x
            else:
                delta = delta.y
            LOGGER.info(f"direction: {direction}, delta: {delta}")
            order[direction].append(delta * 2)

    for direction in order:
        rlt = order[direction]
        avg = sum(rlt) / len(rlt)
        print(f"{direction}- avg {avg} pixel/sec")
