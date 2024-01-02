import time
import logging
import pyautogui

from utils.utils import load_mvmt_params, Coordinate

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

PACE = load_mvmt_params()

class Character_Ctrl:
    @staticmethod
    def _hold_and_release(key, duration):
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def click_window(self, p:Coordinate):
        pyautogui.click(p.x, p.y)

    def _move_horizonal(self, x, debug=False):
        if x != 0:
            if x > 0:
                key = "d"
                pace = PACE.get("right")
            elif x < 0:
                key = "a"
                pace = PACE.get("left")
            if not debug:
                duration = abs(x / pace)
                self._hold_and_release(key, duration)
            else:
                self._hold_and_release(key, duration=0.5)

    def _move_vertical(self, y, debug=False):
        if y != 0:
            if y > 0:
                key = "s"
                pace = PACE.get("down")
            elif y < 0:
                key = "w"
                pace = PACE.get("up")
            if not debug:
                duration = abs(y / pace)
                self._hold_and_release(key, duration)
            else:
                self._hold_and_release(key, duration=0.5)

    def inventory(self):
        pyautogui.press("b")

    def go_to_town(self):
        pyautogui.press("t")

    def mine(self, p:Coordinate):
        LOGGER.debug("Mining...")
        pyautogui.click(p.x, p.y)

    def move_to(self, p:Coordinate):
        self._move_vertical(p.y)
        self._move_horizonal(p.x)


if __name__ == "__main__":
    Ctrl = Character_Ctrl()
    Ctrl.click_window(7, 19)
    # Ctrl.inventory()
    # time.sleep(3)
    # Ctrl.inventory()
    # time.sleep(1)
    Ctrl._move_horizonal(-2)
    time.sleep(1)
