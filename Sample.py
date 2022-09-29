import re, cv2, os
from typing import List, Tuple

import numpy as np

from BrightestPixels import BrightestPixels


def convert_to_grayscale(input_image):
    grayscale_image = 0.299 * input_image[:, :, 0:1] + 0.587 * input_image[:, :, 1:2] + 0.114 * input_image[:, :,
                                                                                                    2:3]
    return grayscale_image


class Sample:
    def __init__(self, filenames: List[str], unlit_token="W.O.LIGHT"):
        self.unlit_token = unlit_token
        self.ET470_unlit_name, filenames = self.filter(filenames, ["470", unlit_token])
        self.ET505_unlit_name, filenames = self.filter(filenames, ["505", unlit_token])
        self.ET545_unlit_name, filenames = self.filter(filenames, ["545", unlit_token])
        self.ET470_lit_name, filenames = self.filter(filenames, ["470"])
        self.ET505_lit_name, filenames = self.filter(filenames, ["505"])
        self.ET545_lit_name, filenames = self.filter(filenames, ["545"])
        self._name = None
        self._brightest_pixels = None

    def load(self):
        self.ET470_unlit = cv2.imread(os.path.join("data", self.ET470_unlit_name))
        self.ET505_unlit = cv2.imread(os.path.join("data", self.ET505_unlit_name))
        self.ET545_unlit = cv2.imread(os.path.join("data", self.ET545_unlit_name))
        self.ET470_lit = cv2.imread(os.path.join("data", self.ET470_lit_name))
        self.ET505_lit = cv2.imread(os.path.join("data", self.ET505_lit_name))
        self.ET545_lit = cv2.imread(os.path.join("data", self.ET545_lit_name))

    def unload(self):
        del self.ET470_unlit
        del self.ET505_unlit
        del self.ET545_unlit
        del self.ET470_lit
        del self.ET505_lit
        del self.ET545_lit

    @property
    def brightest_pixels(self) -> BrightestPixels:
        # returns 99.6th percentile of pixels
        if self._brightest_pixels is None:
            imgs = self.all_imgs()
            brightest_pixel_data = []
            for img in imgs:
                brightest_pixel_data.append(np.percentile(img[:,:,1], 99.6).item())
                brightest_pixel_data.append(np.percentile(convert_to_grayscale(img), 99.6))
            self._brightest_pixels = BrightestPixels(*brightest_pixel_data)
        return self._brightest_pixels

    def filter(self, names: List[str], search_tokens: List[str]) -> Tuple[str, List[str]]:
        patterns = [re.compile(token) for token in search_tokens]
        matches = []
        for i in range(len(names)):
            found = True
            for pat in patterns:
                if not pat.search(names[i]):
                    found = False
                    break
            if found:
                matches.append(i)
        if len(matches) != 1:
            raise RuntimeError(f"Cannot solve Sample names. Found {len(matches)}, ({matches}) samples for phrases {search_tokens} for {names}")
        else:
            ret = names[matches[0]]
            del[names[matches[0]]]
            return ret, names
    
    def all_filenames(self) -> List[str]:
        return       [
                     self.ET470_lit_name,
                     self.ET505_lit_name,
                     self.ET545_lit_name,
                     self.ET470_unlit_name,
                     self.ET505_unlit_name,
                     self.ET545_unlit_name
        ]

    def all_imgs(self):
        return [self.ET470_lit, self.ET505_lit, self.ET545_lit, self.ET470_unlit, self.ET505_unlit, self.ET545_unlit]

    @property
    def name(self):
        if self._name is None:
            if self.ET545_unlit_name.upper().startswith("REF"):
                start = 4 # len(REF_)
            else:
                start = 5 # len(SAMP_)
            self._name = self.ET545_unlit_name[5:self.ET545_unlit_name.index("_"+self.unlit_token)]
        return self._name

