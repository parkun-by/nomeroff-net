from typing import List
from NomeroffNet import textPostprocessing
from NomeroffNet import TextDetector
from NomeroffNet import OptionsDetector
from NomeroffNet import RectDetector
from NomeroffNet import Detector
import matplotlib.image as mpimg
import sys
import os


class Nomeroff:
    """
    Recognize car plates numbers
    """

    def __init__(self, country_code: str):
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

        # NomeroffNet path
        self.NOMEROFF_NET_DIR = os.path.abspath('./')
        self.FILES_PATH = '/tmp/temp_files_parkun'
        sys.path.append(self.NOMEROFF_NET_DIR)

        # Import license plate recognition tools.

        # load models
        self.rectDetector = RectDetector()

        self.optionsDetector = OptionsDetector()
        self.optionsDetector.load("latest")

        self.textDetector = TextDetector.get_static_module(country_code)()
        self.textDetector.load("latest")

        self.nnet = Detector()
        self.nnet.loadModel(self.NOMEROFF_NET_DIR)

    def recognize(self, path: str) -> List[str]:
        # Detect numberplate
        img_path = os.path.join(self.FILES_PATH, path)
        img = mpimg.imread(img_path)

        # Generate image mask.
        cv_imgs_masks = self.nnet.detect_mask([img])

        recognized_plates = list()

        for cv_img_masks in cv_imgs_masks:
            # Detect points.
            arr_points = self.rectDetector.detect(cv_img_masks)

            # cut zones
            zones = self.rectDetector.get_cv_zonesBGR(img, arr_points, 64, 295)

            # find standart
            region_ids, state_ids, count_lines = \
                self.optionsDetector.predict(zones)

            region_names = self.optionsDetector.getRegionLabels(region_ids)

            # find text with postprocessing by standart
            text_arr = self.textDetector.predict(zones)
            text_arr = textPostprocessing(text_arr, region_names)
            recognized_plates += text_arr

        return recognized_plates


if __name__ == "__main__":
    nomeroff = Nomeroff('by')
    plates = nomeroff.recognize(os.path.join("images", "123.jpg"))
    print(plates)
