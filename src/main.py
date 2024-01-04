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

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get("character")[0] / 2), 0)

class Miner:
    def __init__(self):
        time.sleep(2)
        window = ScreenGrabber()
        self.center = window.center
        self.position = window.center
        self.boundary = window.boundary
        CTRL.click_window(window.top_left_corner)

    def _calculate_coal_offset(_type):
        if _type == 'coal_big':
            return Coordinate(int(ITEM_DIMENSION.get("coal_big")) / 2, 0)
        else:
            return Coordinate(int(ITEM_DIMENSION.get("coal_small")) / 2, 0)

    def start_mining_coal(self, ore_root: str):
        """
        Args:
            ore_root (list): path to ore images
        """
        ore_list = load_items(ore_root)
        if len(ore_list) == 0:
            LOGGER.info(f"Cannot find any coal image from following folder: {ore_root}")
            sys.exit()
        while True:
            current_window = ScreenGrabber()
            search_rlt = Searching(screenshot=current_window.name)
            possible_ore = search_rlt.find_multiple_items(items=ore_list)
            if len(possible_ore) > 0:
                LOGGER.info(
                    f"possible ore location: {[(coor.x, coor.y) for coor in possible_ore]}"
                )
                move_vecter = Coordinate.valid_move(
                    possible_ore, self.position, self.center, self.boundary)

                if move_vecter:
                    coal_offset = self._calculate_coal_offset(
                                                    _type= move_vecter._type)
                    location_offset = CHARACTER_OFFSET + coal_offset

                    if move_vecter.x > 0:
                        move_vecter -= location_offset
                        click_position = self.center + coal_offset
                    else:
                        move_vecter += location_offset
                        click_position = self.center - coal_offset

                    LOGGER.debug(f"Move to {move_vecter}...")
                    CTRL.move_to(move_vecter)
                    self.position += move_vecter
                    CTRL.mine(click_position)
                else:
                    LOGGER.debug('No availible coal was in the boundary')
                    CTRL.move_to(-self.current_position)

            else:
                LOGGER.debug("No coal was found")
                if self.current_position.x == 0 and self.current_position.y == 0:
                    LOGGER.debug(
                        "Current location is at origin, wait for coal respawn..."
                    )
                    time.sleep(5)
                else:
                    LOGGER.debug(
                        "Current location is not at original, moving character back to origin"
                    )
                    CTRL.move_to(-self.current_position)

    def calibrate_origin(self):
        ref_coordinate = Coordinate(516, 136)
        ref_path = Path('../images/benchmarks/origin_ref.png')
        window = ScreenGrabber()
        
        search = Searching(screenshot=window.name)
        ref_found = search.find_one_item(ref_path)
        if len(ref_found) == 0:
            LOGGER.error('cannot find the reference rock during the origin calibration')
        else:
            ref_found_coord = ref_found[0]
            vecter = ref_found_coord - ref_coordinate
            CTRL.move_to(vecter)


if __name__ == "__main__":
    coal_root = str(Path("../images/coal/*.png"))
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
