import sys
import time

from loguru import logger
from pathlib import Path
from PIL import Image

from utils.recon import load_items, Searching, search_for_coal, find_ref_rock
from utils.character_ctrl import Character_Ctrl
from utils.screenshot import (
    take_screenshot,
    mark_coordinates_on_screenshot,
    game_resolution,
)
from utils.utils import Coordinate, load_dimension_params, Boundary

CTRL = Character_Ctrl()

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get("character").x / 2), 0)

REF_IMG_PATH = str(Path("../images/benchmarks/refs/ref_rock_left_top.png"))


class Miner:
    boundary = Boundary(
        x_min=-game_resolution.x / 2,
        y_min=-game_resolution.y / 2,
        x_max=game_resolution.x / 2,
        y_max=game_resolution.y / 2,
    )
    displacement = Coordinate(0, 0)
    ref_coord = None

    def __init__(self):
        time.sleep(2)
        window = take_screenshot()
        self.character_center = window.character_center
        CTRL.click_window(window.top_left_coordinate)

    @staticmethod
    def _calculate_coal_offset(_type):
        with Image.open(_type) as img:
            w, _ = img.size
        return Coordinate(w / 2, 0)

    def start_mining_coal(self):
        """
        Args:
            ore_root (list): path to ore images
        """
        self.set_reference_point()

        if not self.ref_coord:
            logger.error("Fail to find the ref rock!")
            sys.exit()

        while True:
            screenshot = take_screenshot()
            possible_ore = search_for_coal(screenshot.filepath, show=True)
            if possible_ore:
                logger.info(
                    f"possible ore location: {[(coor.x, coor.y) for coor in possible_ore]}"
                )
                move_vector = Coordinate.valid_move(
                    possible_ore,
                    self.displacement,
                    self.character_center,
                    self.boundary,
                )

                if move_vector:
                    coal_type = move_vector._type
                    coal_offset = self._calculate_coal_offset(_type=coal_type)
                    location_offset = CHARACTER_OFFSET + coal_offset

                    if move_vector.x > 0:
                        move_vector -= location_offset
                    else:
                        move_vector += location_offset

                    self._move(move_vector)
                    CTRL.mine(self.character_center)
                    if "big" in coal_type:
                        time.sleep(8)
                    else:
                        time.sleep(6)
                    self.return_to_origin()
            else:
                logger.debug("No coal was found")
                self.return_to_origin()

    def _move(self, vector):
        logger.debug(f"Move: {vector}")
        CTRL.move(vector)
        self.displacement += vector

    def return_to_origin(self):
        if self.displacement.x == 0 and self.displacement.y == 0:
            if not self._get_ref_coordinate():
                logger.debug("Resetting the character...")
                CTRL.go_to_coal_spot_from_town()
            else:
                logger.debug("Current location is at origin, wait for coal respawn...")
                time.sleep(5)
        else:
            logger.debug(
                "Current location is not at original, moving character back to origin"
            )
            CTRL.move_reverse(-self.displacement)
            self.displacement = Coordinate(0, 0)

    def calibrate_origin(self):
        if ref_found_coord := self._get_ref_coordinate():
            logger.debug(f"Ref found: {ref_found_coord}")
            vector = ref_found_coord - self.ref_coord
            logger.debug(f"which is off by: {vector}")
            self._move(vector)
        else:
            raise NotImplementedError("origin calibration is not finish")

    def set_reference_point(self):
        if ref_coord := self._get_ref_coordinate():
            self.ref_coord = ref_coord
        else:
            logger.debug("Cannot find the ref rock, resetting the position...")
            CTRL.go_to_coal_spot_from_town()
            ref_coord = self._get_ref_coordinate()
            self.ref_coord = ref_coord

    def _get_ref_coordinate(self, retry=5):
        while retry > 0:
            window = take_screenshot()
            if ref_found := find_ref_rock(window.filepath, show=True):
                return ref_found
            else:
                retry -= 1
                logger.debug("Cannot find the reference, retry in 2 sec")
                time.sleep(2)
        else:
            logger.debug("Cannot find the reference!")

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
        CTRL.go_to_town()


if __name__ == "__main__":
    import csv
    csv_file_name = "example.csv"
    # coal_root = str(Path("../images/coal/*.png"))
    miner = Miner()
    # CTRL._hold_and_release("w", 1)
    # rlt = {}
    # print("Start")

    # with open(csv_file_name, mode="w", newline="") as file:
    #     writer = csv.writer(file)
    #     for i in range(200):
    #         duration = (i + 1) * 0.005
    #         p1 = miner._get_ref_coordinate()[0]
    #         CTRL._hold_and_release("w", duration)
    #         p2 = miner._get_ref_coordinate()[0]
    #         CTRL._hold_and_release("s", duration)

    #         writer.writerow([str(duration), p2.y-p1.y])

    # p1 = miner._get_ref_coordinate()
    # CTRL._hold_and_release("d", 0.001)
    # CTRL.press("right", presses=10)
    # CTRL.press("d")
    # CTRL.press("d")
    # p2 = miner._get_ref_coordinate()
    # print(p2.x - p1.x)
    # miner = Miner()
    miner.start_mining_coal()
    # miner.heal()

    # displacement = Coordinate(100, 0)
    # with open(csv_file_name, mode="w", newline="") as file:
    #     writer = csv.writer(file)
    #     for i in range(30):
    #         p1 = miner._get_ref_coordinate()[0]
    #         CTRL.move(displacement)

    #         CTRL.move_reverse(-displacement)
    #         p2 = miner._get_ref_coordinate()[0]
    #         print(f"p1: {p1}, p2: {p2}")

    #         writer.writerow([str(i), str(p1.x - p2.x)])
