import sys
import time
import logging

from pprint import pprint

from src.utils.recon import matching
from src.utils.ctrl import Character_Ctrl
from src.utils.screenshot import ScreenGrabber

BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\benchmarks\river_rock.png"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
CTRL = Character_Ctrl()


def movement_calibration(direction):
    def _rock_coordinate():
        screenshot_1, _, _ = ScreenGrabber()
        return matching(screenshot_1, [BENCHMARK_ROCK])[0]

    p1 = _rock_coordinate()

    if direction == "up":
        CTRL.move_vertical(-1, debug=True)
    elif direction == "down":
        CTRL.move_vertical(1, debug=True)
    elif direction == "right":
        CTRL.move_horizonal(1, debug=True)
    elif direction == "left":
        CTRL.move_horizonal(-1, debug=True)
    else:
        logging.error("Invalid direction!")
    time.sleep(2)

    p2 = _rock_coordinate()

    delta = (p1[0] - p2[0], p1[1] - p2[1])
    return delta


if __name__ == "__main__":
    order = {"right": [], "up": [], "left": [], "down": []}

    ctrl = Character_Ctrl()
    ctrl.click_window(7, 19)

    for i in range(20):
        LOGGER.debug(f"round: {i}")
        for direction in order.keys():
            delta = movement_calibration(direction)
            if direction in ["right", "left"]:
                delta = delta[0]
            else:
                delta = delta[1]
            LOGGER.info(f"direction: {direction}, delta: {delta}")
            order[direction].append(delta * 2)

    for direction in order:
        rlt = order[direction]
        avg = sum(rlt) / len(rlt)
        print(f"{direction}- avg {avg} pixel/sec")
