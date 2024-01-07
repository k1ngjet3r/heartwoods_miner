import sys
import time
import logging
import colorlog

from pprint import pprint
from pathlib import Path
from PIL import Image

from utils.recon import load_items, Searching
from utils.ctrl import Character_Ctrl
from utils.screenshot import take_screenshot
from utils.utils import Coordinate, load_dimension_params

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(stream_handler)

CTRL = Character_Ctrl()

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get("character").x / 2), 0)

REF_IMG_PATH = str(Path("../images/benchmarks/origin_ref.png"))


class Miner:
    def __init__(self):
        time.sleep(2)
        window = take_screenshot()
        self.ref_coord = None
        self.center = window.absolute_center
        self.position = window.relative_center
        self.boundary = window.boundary
        self.displacement = Coordinate(0, 0)
        CTRL.click_window(window.top_left_corner)

    @staticmethod
    def _calculate_coal_offset(_type):
        if _type == "coal_big":
            return Coordinate(int(ITEM_DIMENSION.get("coal_big").x) / 2, 0)
        else:
            return Coordinate(int(ITEM_DIMENSION.get("coal_small").x) / 2, 0)

    def start_mining_coal(self, ore_root: str):
        """
        Args:
            ore_root (list): path to ore images
        """
        ore_list = load_items(ore_root)
        self.set_reference_point()

        if not self.ref_coord:
            sys.exit()

        if len(ore_list) == 0:
            LOGGER.info(f"Cannot find any coal image from following folder: {ore_root}")
            sys.exit()

        while True:
            current_window = take_screenshot()
            search_rlt = Searching(screenshot=current_window.name)
            possible_ore = search_rlt.find_multiple_items(items=ore_list)
            if len(possible_ore) > 0:
                LOGGER.info(
                    f"possible ore location: {[(coor.x, coor.y) for coor in possible_ore]}"
                )
                move_vector = Coordinate.valid_move(
                    possible_ore, self.position, self.center, self.boundary
                )

                if move_vector:
                    coal_type = move_vector._type
                    coal_offset = self._calculate_coal_offset(_type=coal_type)
                    location_offset = CHARACTER_OFFSET + coal_offset

                    if move_vector.x > 0:
                        move_vector -= location_offset
                        click_position = self.center + coal_offset
                    else:
                        move_vector += location_offset
                        click_position = self.center - coal_offset

                    self._move(move_vector)
                    CTRL.mine(self.center)
                    if "big" in coal_type:
                        time.sleep(8)
                    else:
                        time.sleep(6)
                else:
                    LOGGER.debug("No availible coal was in the boundary")
                    self.return_to_origin()

            else:
                LOGGER.debug("No coal was found")
                self.return_to_origin()

    def _move(self, vector):
        LOGGER.debug(f"Move: {vector}")
        CTRL.move_to(vector)
        self.displacement += vector

    def return_to_origin(self):
        if self.displacement.x == 0 and self.displacement.y == 0:
            LOGGER.debug("Current location is at origin, wait for coal respawn...")
            time.sleep(5)
        else:
            LOGGER.debug(
                "Current location is not at original, moving character back to origin"
            )
            self._move(-self.displacement)

    def calibrate_origin(self):
        if ref_found_coord := self._get_ref_coordinate():
            LOGGER.debug(f"Ref found: {ref_found_coord}")
            vector = ref_found_coord - self.ref_coord
            LOGGER.debug(f"which is off by: {vector}")
            self._move(vector)
        else:
            raise NotImplementedError("origin calibration is not finish")

    def set_reference_point(self):
        if ref_coord := self._get_ref_coordinate():
            self.ref_coord = ref_coord
        else:
            raise NotImplementedError("origin calibration is not finish")

    def _get_ref_coordinate(self):
        window = take_screenshot()
        search = Searching(window.name, match_rate=0.95)
        ref_coord = search.find_one_item(REF_IMG_PATH)
        if len(ref_coord) > 0:
            ref_found_coord = ref_coord[0]
            LOGGER.debug(f"Ref found: {ref_found_coord}")
            return ref_found_coord
        else:
            LOGGER.error("Cannot find the reference, please relocate the character!")
            return None

    def check_inventory(self):
        """open inventory and check if the inventory is full

        Return:
            bool: return True if inventory is full
        """
        raise NotImplementedError()
        CTRL.inventory()

    def deposite_item_to_bank(self):
        """1. Teleport back to town
        2. go to bank
        3. deposite the item
        """
        raise NotImplementedError()

    def go_to_bank_from_teleport(self):
        """1. teleport back to town
        2. go to bank
        """
        raise NotImplementedError()
        CTRL.go_to_town

    def go_to_coal_spot_from_bank():
        raise NotImplementedError()

    def go_to_coal_spot_from_teleport():
        raise NotImplementedError()
        CTRL.go_to_town


if __name__ == "__main__":
    coal_root = str(Path("../images/coal/*.png"))
    miner = Miner()
    # miner.set_reference_point()
    # LOGGER.info("move to (20, 20)")
    # miner._move(Coordinate(20, 20))
    # time.sleep(5)
    # LOGGER.info("return to origin...")
    # miner.return_to_origin()
    # miner._move(Coordinate(20, 0))

    # LOGGER.info("calibrating the origin")
    # miner.calibrate_origin()
    miner.start_mining_coal(coal_root)

    # ref_coordinate = Coordinate(516, 105)
    # ref_path = Path('../images/benchmarks/origin_ref.png')

    # img_name = '/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/benchmark_3.png'
    # test_img_name = '/Users/jeterlin/Dev/github/heartwoods_miner/images/test.png'

    # img = Image.open(img_name)
    # w, h = img.size
    # _center = Coordinate(int(w/2), int(h/2))
    # search = Searching(screenshot=img_name)
    # ref_found = search.find_one_item(str(ref_path))
    # print(f'screenshot dimension: {(w, h)}')
    # print(f'center: {_center}')
    # print(f'center type: {type(_center)}')
    # print(f'ref coord: {ref_found}')
    # print(f'ref type: {type(ref_found)}')
    # print(f'delta: {str(ref_found[0]-_center)}')

    # ref_found.append(_center)
    # print(f'ref coord: {ref_found}')

    # search.mark_item_on_screenshot(ref_found)
