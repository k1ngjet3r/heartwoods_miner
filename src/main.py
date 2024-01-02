import sys
import time
import logging

from pprint import pprint

from utils.recon import matching, load_templete
from utils.ctrl import Character_Ctrl
from utils.screenshot import ScreenGrabber
from utils.utils import load_mvmt_params, load_dimension_params

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CTRL = Character_Ctrl()
PACE = 390
CENTER_OFFSET = (0, 20)
# BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\benchmarks\river_rock.png"

BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\coal\coal_3.png"
TEMPLETE = load_templete(r"images\coal")

def calculate_vector(p1: tuple, p2: tuple) -> tuple[float]:
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    return (delta_x, delta_y)

class Miner:
    delta = (0, 0)
    def __init__(self):
        time.sleep(2)
        _, center, top_left_corner = ScreenGrabber()
        self.center = center
        CTRL.click_window(top_left_corner)

    def start_mining(self):
        while True:
            pass

    def _displacement(self, vecter_1, vecter_2):
        return (vecter_1[0]+ vecter_2[0], vecter_1[1]+vecter_2[1])

if __name__ == "__main__":
    # boundry = (500, 500)
    # time.sleep(2)
    # _, center, top_left_corner = ScreenGrabber()
    # CTRL.click_window(top_left_corner[0], top_left_corner[1])
    # current_position = (center[0] + CENTER_OFFSET[0], center[1] + CENTER_OFFSET[1])

    # while True:
    #     try:
    #         screenshot_1, _, _ = ScreenGrabber()
    #         target_position = matching(screenshot_1, TEMPLETE)[0]

    #         vector = calculate_vector(current_position, target_position)
    #         print(f"distance from character: {vector}")
    #         CTRL.move_to(vector)

    #         if vector[0] > 0:
    #             click_coordinate = (center[0] + 50, center[1])
    #         else:
    #             click_coordinate = (center[0] - 50, center[1])
    #         CTRL.mine(click_coordinate[0], click_coordinate[1])
    #         time.sleep(8)

    #         # return to center
    #         CTRL.move_to((-vector[0], -vector[1]))
    #     except IndexError:
    #         logging.debug("No coal was found")
    #         time.sleep(1)
    # CTRL.mine(center[0], center[1])
