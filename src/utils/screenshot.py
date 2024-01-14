import os
import cv2
import pyautogui
import pygetwindow as pgw

from pathlib import Path
from loguru import logger
from datetime import datetime
from dataclasses import dataclass

from PIL import Image

from utils.utils import Coordinate, Boundary


IMAGE_ROOT = str(Path("../images"))

TITLE_BAR_OFFSET = 31

@dataclass
class game_resolution:
    x = 1280
    y = 720
    x_offset = 8
    y_offset = 31

@dataclass
class Screenshot:
    """ Storing the detail of a screen shot

    Args:
        filepath (str): name of the saved screenshot filepath
        screen_center (Coordinate): the screen center of the game window (including the title bar)
        character_coordinate (Coordinate): the center of the game screen (exclude the title bar)

    """
    filepath: str
    window_center: Coordinate
    character_center: Coordinate
    top_left_coordinate: Coordinate

def take_screenshot(new_file=False):
    if new_file:
        filename = datetime.now().strftime("%H_%M_%S") + ".png"
    else:
        filename = 'screenshot.png'
    image_name = os.path.join(IMAGE_ROOT, filename)
    titles = pgw.getAllTitles()
    if "Heartwood Online" not in titles:
        logger.critical("Heartwood Online window cannot be found!")
    else:
        window = pgw.getWindowsWithTitle("Heartwood Online")[0]

        left, top = window.topleft
        right, bottom = window.bottomright

        corrected_left = left + game_resolution.x_offset
        corrected_top = top + game_resolution.y_offset
        corrected_right = corrected_left + game_resolution.x
        corrected_bottom = corrected_top + game_resolution.y

        logger.debug('Taking screenshot...')
        pyautogui.screenshot(image_name)
        im = Image.open(image_name)
        im = im.crop((
            corrected_left , corrected_top, corrected_right, corrected_bottom))
        im.save(image_name)

        window_center = Coordinate(
            int((left + right) / 2),
            int((top + bottom) / 2)
        )
        character_center = Coordinate(
            int(game_resolution.x_offset + game_resolution.x / 2 + left),
            int(game_resolution.y_offset + game_resolution.y / 2 + top)
        )
        top_left_coordinate = Coordinate(left + 10, top + 10)
        return Screenshot(
            image_name,
            window_center,
            character_center,
            top_left_coordinate
        )

def mark_coordinates_on_screenshot(screenshot:str, coordinates:list[Coordinate]):
    output_img_name = screenshot.replace('.png', '_rlt.png')
    image = cv2.imread(screenshot)

    for coord in coordinates:
        cv2.circle(
            img=image,
            center=(coord.x, coord.y),
            radius=2,
            thickness=-1,
            color=(0, 0, 255)
        )
    cv2.imwrite(output_img_name, image)

class Mark_Coordinates:
    def __init__(self, screenshot, coordinates) -> None:
        self.output_name = screenshot.replace(
                                    '.png', '_marked.png')
        self.image = cv2.imread(screenshot)
        self.coordinates = coordinates

    def point(self):
        for coord in self.coordinates:
            cv2.circle(
                img=self.image,
                center=(coord.x, coord.y),
                radius=2,
                thickness=-1,
                color=(0, 0, 255)
        )
        cv2.imwrite(self.output_name, self.image)

    def box(self, dimension_params:dict):
        for coord in self.coordinates:
            if coord._type == 'coal_big':
                dimension = dimension_params.get('coal_big')
            elif 'coal_small' in coord._type:
                dimension = dimension_params.get('coal_small')
            else:
                raise NotImplementedError(
                    'Entered value did not implemented yet')

            start_point = coord - dimension/2
            end_point = start_point + dimension

            cv2.rectangle(
                img=self.image,
                pt1=(start_point.x, start_point.y),
                pt2=(end_point.x, end_point.y),
                thickness=2,
                color=(0, 0, 255)
            )
        cv2.imwrite(self.output_name, self.image)

if __name__ == "__main__":
    screenshot = take_screenshot()
    print(screenshot.character_center)
