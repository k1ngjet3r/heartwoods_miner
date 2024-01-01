import time
import logging
import pyautogui

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

PACE = 371.35

class Character_Ctrl:
    @staticmethod
    def _hold_and_release(key, duration):
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def click_window(self, x, y):
        pyautogui.click(x, y)

    def move_horizonal(self, x, debug=False):
        if x != 0:
            if x > 0:
                key = "d"
            elif x < 0:
                key = "a"
            if not debug:
                duration = abs(x / PACE)
                self._hold_and_release(key, duration)

            else:
                self._hold_and_release(key, duration=0.5)

    def move_vertical(self, y, debug=False):
        if y != 0:
            if y > 0:
                key = "s"
            elif y < 0:
                key = "w"
            if not debug:
                duration = abs(y / PACE)
                self._hold_and_release(key, duration)
            else:
                self._hold_and_release(key, duration=0.5)

    def inventory(self):
        pyautogui.press("b")

    def go_to_town(self):
        pyautogui.press("t")

    def mine(self, x, y):
        LOGGER.debug("Mining...")
        pyautogui.click(x, y)

    def move_to(self, vector):
        self.move_vertical(vector[1])
        self.move_horizonal(vector[0])

if __name__ == "__main__":
    Ctrl = Character_Ctrl()
    Ctrl.click_window(7, 19)
    # Ctrl.inventory()
    # time.sleep(3)
    # Ctrl.inventory()
    # time.sleep(1)
    Ctrl.move_horizonal(-2)
    time.sleep(1)
