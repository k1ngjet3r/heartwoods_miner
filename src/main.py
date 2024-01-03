import sys
import time
import logging

from pprint import pprint
from pathlib import Path

from utils.recon import load_items, Searching
from utils.ctrl import Character_Ctrl
from utils.screenshot import ScreenGrabber
from utils.utils import Coordinate, load_dimension_params

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CTRL = Character_Ctrl()
PACE = 390
CENTER_OFFSET = (0, 20)
# BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\benchmarks\river_rock.png"

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get('character')[0] / 2), 0)

BENCHMARK_ROCK = r"C:\Users\Jeter\dev\heartwoods_miner\images\coal\coal_3.png"
TEMPLETE = load_items(r"images\coal")

class Miner:
    current_position = Coordinate(x=0, y=0)
    def __init__(self):
        time.sleep(2)
        window = ScreenGrabber()
        self.center = window.center
        CTRL.click_window(window.top_left_corner)

    def start_mining_coal(self, ore_root:str):
        """
        Args:
            ore_root (list): path to ore images
        """
        ore_list = load_items(ore_root)
        while True:
            current_window = ScreenGrabber()
            search_rlt = Searching(screenshot=current_window.name)
            possible_ore = search_rlt.find_multiple_items(items=ore_list)
            if len(possible_ore) > 0:
                LOGGER.info(f'possible ore location: {[(coor.x, coor.y) 
                                                    for coor in possible_ore]}')
                closest_ore = Coordinate.find_closest_coordinate(possible_ore)
                ore_offset = Coordinate(int(ITEM_DIMENSION.get('coal_big'))/2, 0) \
                    if closest_ore._type == 'coal_big' \
                        else Coordinate(int(ITEM_DIMENSION.get('coal_small'))/2, 0)
                location_offset = CHARACTER_OFFSET + ore_offset
                vecter = closest_ore - self.center
                if vecter.x > 0:
                    vecter -= location_offset
                    click_position = self.center + ore_offset
                else:
                    vecter += location_offset
                    click_position = self.center - ore_offset

                LOGGER.debug(f'Move to {vecter}...')
                CTRL.move_to(vecter)
                self.current_position += vecter
                CTRL.mine(click_position)

            else:
                LOGGER.debug('No coal was found')
                if self.current_position == Coordinate(0, 0):
                    LOGGER.debug(
                        'Current location is at origin, wait for coal respawn...')
                    time.sleep(5)
                else:
                    LOGGER.debug(
                        'Current location is not at original, moving character back to origin'
                    )
                    CTRL.move_to(-vecter)

if __name__ == "__main__":
    coal_root = str(Path('images/coal'))
    Miner().start_mining_coal(coal_root)
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
