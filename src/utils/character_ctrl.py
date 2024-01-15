import math
import time
import pyautogui
from loguru import logger

from utils.utils import load_mvmt_params, Coordinate

PACE = load_mvmt_params()


def round_half_up(n, decimals=3):
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5) / multiplier


class Character_Ctrl:
    @staticmethod
    def _hold_and_release(key, duration):
        logger.debug(f"holding {key} for duration: {duration}s")
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def click_window(self, p: Coordinate):
        logger.debug(f"Clicking window at {(p.x, p.y)}")
        pyautogui.click(p.x, p.y)

    def _calculate_mvmt(self, distance):
        return abs(0.003326 * distance - 0.113757)

    def _move_horizonal(self, x, debug=False):
        if x != 0:
            if x > 0:
                key = "d"
            elif x < 0:
                key = "a"
            if not debug:
                duration = self._calculate_mvmt(x)
                self._hold_and_release(key, duration)
            else:
                self._hold_and_release(key, duration=0.5)

    def _move_vertical(self, y, debug=False):
        if y != 0:
            if y > 0:
                key = "s"
            elif y < 0:
                key = "w"
            if not debug:
                duration = self._calculate_mvmt(y)
                self._hold_and_release(key, duration)
            else:
                self._hold_and_release(key, duration=0.5)

    def inventory(self):
        logger.debug("Open/close inventory")
        pyautogui.press("b")

    def go_to_town(self):
        logger.debug("Teleport back to the town")
        pyautogui.press("t")

    def mine(self, p: Coordinate):
        logger.debug("Mining...")
        pyautogui.click(p.x, p.y)

    def move(self, p: Coordinate):
        self._move_vertical(p.y)
        self._move_horizonal(p.x)

    def press(self, key, presses):
        pyautogui.press(key, presses=presses)


if __name__ == "__main__":
    Ctrl = Character_Ctrl()
    # Ctrl.click_window(7, 19)
    # Ctrl.inventory()
    # time.sleep(3)
    # Ctrl.inventory()
    # time.sleep(1)
    Ctrl.mine(Coordinate(645, 396))
