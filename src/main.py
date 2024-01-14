import sys
import time
import logging

from pathlib import Path
from PIL import Image

from utils.recon import load_items, Searching
from utils.character_ctrl import Character_Ctrl
from utils.screenshot import take_screenshot, mark_coordinates_on_screenshot
from utils.utils import Coordinate, load_dimension_params

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

CTRL = Character_Ctrl()

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get("character").x / 2), 0)

REF_IMG_PATH = str(Path("../images/benchmarks/origin_ref.png"))


class Miner:
    def __init__(self):
        time.sleep(2)
        window = take_screenshot()
        self.ref_coord = None
        # TODO: added position and boundary back to class
        self.character_center = window.character_center
        self.position = None
        self.boundary = None
        self.displacement = Coordinate(0, 0)
        CTRL.click_window(window.top_left_coordinate)

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
            search_rlt = Searching(screenshot=current_window.filepath)
            possible_ore = search_rlt.find_multiple_items(items=ore_list)
            if len(possible_ore) > 0:
                LOGGER.info(
                    f"possible ore location: {[(coor.x, coor.y) for coor in possible_ore]}"
                )
                move_vector = Coordinate.valid_move(
                    possible_ore, self.position, self.character_center, self.boundary
                )

                if move_vector:
                    coal_type = move_vector._type
                    coal_offset = self._calculate_coal_offset(_type=coal_type)
                    location_offset = CHARACTER_OFFSET + coal_offset

                    if move_vector.x > 0:
                        move_vector -= location_offset
                        click_position = self.character_center + coal_offset
                    else:
                        move_vector += location_offset
                        click_position = self.character_center - coal_offset

                    self._move(move_vector)
                    CTRL.mine(self.character_center)
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

    def _take_screenshot_and_find_items(self, item_list):
        window = take_screenshot()
        search = Searching(screenshot=window.filepath)
        possible_location = search.find_multiple_items(items=item_list)
        if len(possible_location) > 0:
            return possible_location

    def _move(self, vector):
        LOGGER.debug(f"Move: {vector}")
        CTRL.move(vector)
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

    def _get_ref_coordinate(self, retry=5):
        while retry > 0:
            window = take_screenshot()
            search = Searching(window.filepath, match_rate=0.95)
            ref_coord = search.find_one_item(REF_IMG_PATH)
            if ref_coord:
                ref_found_coord = ref_coord[0]
                mark_coordinates_on_screenshot(window.filepath, [ref_found_coord])
                LOGGER.debug(f"Ref found: {ref_found_coord}")
                return ref_found_coord
            else:
                retry -= 1
                LOGGER.debug("Cannot find the reference, retry in 2 sec")
                time.sleep(2)
        else:
            LOGGER.error("Cannot find the reference, please relocate the character!")

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
    import csv

    csv_file_name = "example.csv"
    coal_root = str(Path("../images/coal/*.png"))
    miner = Miner()
    rlt = {}
    print("Start")

    # with open(csv_file_name, mode="w", newline="") as file:
    #     writer = csv.writer(file)
    #     for i in range(200):
    #         duration = (i + 1) * 0.005
    #         p1 = miner._get_ref_coordinate()
    #         CTRL._hold_and_release("d", duration)
    #         p2 = miner._get_ref_coordinate()
    #         CTRL._hold_and_release("a", duration)

    #         writer.writerow([str(duration), p2.x-p1.x])

    p1 = miner._get_ref_coordinate()
    # CTRL._hold_and_release("d", 0.001)
    CTRL.press("right", presses=10)
    # CTRL.press("d")
    # CTRL.press("d")
    p2 = miner._get_ref_coordinate()
    print(p2.x - p1.x)
