import sys
import time
import logging

from pprint import pprint
from pathlib import Path
from PIL import Image

from utils.recon import load_items, Searching
from utils.ctrl import Character_Ctrl
from utils.screenshot import ScreenGrabber
from utils.utils import Coordinate, load_dimension_params

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CTRL = Character_Ctrl()

ITEM_DIMENSION = load_dimension_params()
CHARACTER_OFFSET = Coordinate(int(ITEM_DIMENSION.get("character")[0] / 2), 0)

REF_IMG_PATH = str(Path('../images/benchmarks/origin_ref.png'))

class Miner:
    def __init__(self):
        time.sleep(2)
        window = ScreenGrabber()
        self.ref_coord = None
        self.center = window.absolute_center
        self.position = window.relative_center
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
        self.setting_reference_point()

        if not self.ref_coord:
            sys.exit()

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
                move_vector = Coordinate.valid_move(
                    possible_ore, self.position, self.center, self.boundary)

                if move_vector:
                    coal_offset = self._calculate_coal_offset(
                                                    _type= move_vector._type)
                    location_offset = CHARACTER_OFFSET + coal_offset

                    if move_vector.x > 0:
                        move_vector -= location_offset
                        click_position = self.center + coal_offset
                    else:
                        move_vector += location_offset
                        click_position = self.center - coal_offset

                    LOGGER.debug(f"Move to {move_vector}...")
                    CTRL.move_to(move_vector)
                    self.position += move_vector
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
        window = ScreenGrabber()
        search = Searching(screenshot=window.name)
        ref_found = search.find_one_item(REF_IMG_PATH)
        if len(ref_found) == 0:
            LOGGER.error('cannot find the reference rock during the origin calibration')
        else:
            ref_found_coord = ref_found[0]
            vector =  self.ref_coord - ref_found_coord
            CTRL.move_to(vector)
            self.position += vector

    def setting_reference_point(self):
        window = ScreenGrabber()
        search = Searching(window.name)
        ref_coord = search.find_one_item(REF_IMG_PATH)
        if ref_coord and len(ref_coord) > 0:
            self.ref_coord = ref_coord
        else:
            LOGGER.error('Cannot find the reference, please relocate the character!')

    def check_inventory(self):
        """ open inventory and check if the inventory is full

        Return:
            bool: return True if inventory is full
        """        
        raise NotImplementedError()
        CTRL.inventory()

    def deposite_item_to_bank(self):
        """ 1. Teleport back to town
            2. go to bank
            3. deposite the item
        """
        raise NotImplementedError()

    def go_to_bank_from_teleport(self):
        """ 1. teleport back to town
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
    # coal_root = str(Path("../images/coal/*.png"))
    # Miner().start_mining_coal(coal_root)

    ref_coordinate = Coordinate(516, 105)
    ref_path = Path('../images/benchmarks/origin_ref.png')

    img_name = '/Users/jeterlin/Dev/github/heartwoods_miner/images/benchmarks/benchmark_3.png'
    test_img_name = '/Users/jeterlin/Dev/github/heartwoods_miner/images/test.png'
    
    img = Image.open(img_name)
    w, h = img.size
    _center = Coordinate(int(w/2), int(h/2))
    search = Searching(screenshot=img_name)
    ref_found = search.find_one_item(str(ref_path))
    print(f'screenshot dimension: {(w, h)}')
    print(f'center: {_center}')
    print(f'center type: {type(_center)}')
    print(f'ref coord: {ref_found}')
    print(f'ref type: {type(ref_found)}')
    print(f'delta: {str(ref_found[0]-_center)}')


    ref_found.append(_center)
    print(f'ref coord: {ref_found}')

    search.mark_item_on_screenshot(ref_found)

    

    