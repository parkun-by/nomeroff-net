from typing import List
from NomeroffNet.YoloV5Detector import Detector
from NomeroffNet.BBoxNpPoints import \
    NpPointsCraft, \
    getCvZoneRGB, \
    convertCvZonesRGBtoBGR, \
    reshapePoints

from NomeroffNet.OptionsDetector import OptionsDetector
from NomeroffNet.TextDetector import TextDetector
from NomeroffNet.TextPostprocessing import textPostprocessing

import matplotlib.image as mpimg
import sys
import os
import numpy as np
import cv2


class Nomeroff:
    """
    Recognize car plates numbers
    """

    def __init__(self, country_code: str = "by"):
        # Specify device
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

        # NomeroffNet path
        self.NOMEROFF_NET_DIR = os.path.abspath('./')
        self.FILES_PATH = '/tmp/temp_files_parkun'
        sys.path.append(self.NOMEROFF_NET_DIR)

        # Import license plate recognition tools.

        # load models
        self.detector = Detector()
        self.detector.load()

        self.npPointsCraft = NpPointsCraft()
        self.npPointsCraft.load()

        self.optionsDetector = OptionsDetector()
        self.optionsDetector.load("latest")

        self.textDetector = TextDetector.get_static_module(country_code)()
        self.textDetector.load("latest")

    def recognize(self, img_path: str) -> List[str]:
        # Detect numberplate
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        targetBoxes = self.detector.detect_bbox(img)
        all_points = self.npPointsCraft.detect(img,
                                               targetBoxes,
                                               [5, 2, 0])

        # cut zones
        zones = convertCvZonesRGBtoBGR(
            [getCvZoneRGB(img, reshapePoints(rect, 1)) for rect in all_points]
        )

        # predict zones attributes
        regionIds, countLines = self.optionsDetector.predict(zones)
        regionNames = self.optionsDetector.getRegionLabels(regionIds)

        # find text with postprocessing by standart
        textArr = self.textDetector.predict(zones)
        recognized_plates = textPostprocessing(textArr, regionNames)

        return recognized_plates


if __name__ == "__main__":
    nomeroff = Nomeroff('by')
    plates = nomeroff.recognize(os.path.join("images", "123.jpg"))
    print(plates)
