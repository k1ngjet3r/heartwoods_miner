import os
import cv2
import logging
import numpy as np

from glob import glob

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
TEMPLETE = r"images\coal"

def load_templete(path) -> list[str]:
    return [f for f in glob(path + r"\*.png")]


def matching(screenshot, templetes, threshold=0.8):
    img_rgb = cv2.imread(screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    for t in templetes:
        LOGGER.debug(f'Seraching templete: {t}')
        pattern = cv2.imread(t, 0)
        w, h = pattern.shape[::-1]
        res = cv2.matchTemplate(img_gray, pattern, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        LOGGER.info(f'loc result: {loc}')
        for pt in zip(*loc[::-1]):
            LOGGER.info(f'coordinate: {pt}')
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # cv2.circle(img_rgb, pt, radius=1, color=(0, 0, 255), thickness=-1)

    cv2.imwrite(screenshot.replace(".png", "_rlt.png"), img_rgb)


if __name__ == "__main__":
    # matching(
    #     screenshot=r'images\benchmarks\benchmark_1.png',
    #     templete=r'images/coal/coal_2.png'
    # )
    for b in glob(r"images\benchmarks\*.png"):
        matching(b, load_templete(TEMPLETE))
        break
        # print(b)
