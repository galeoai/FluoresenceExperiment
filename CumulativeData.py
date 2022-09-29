import os
from typing import List
from BrightestPixels import BrightestPixels
from Sample import Sample


class CumulativeData:
    def __init__(self):
        self.brightest_pixels: List[BrightestPixels] = []

    def add_sample(self, brightest_pixel_datum: BrightestPixels):
        self.brightest_pixels.append(brightest_pixel_datum)

    def write_csv(self, base_dir):
        with open(os.path.join(base_dir, "master_spreadsheet.csv"), 'w+') as master_spreadsheet:
            master_spreadsheet.write("green_lit_470,green_lit_505,green_lit_545,green_unlit_470,green_unlit_505,green_unlit_545,BW_lit_470,BW_lit_505,BW_lit_545,BW_unlit_470,BW_unlit_505,BW_unlit_545\n")
            for br in self.brightest_pixels:
                master_spreadsheet.write(",".join(br.green_brightest_to_str())+","+",".join(br.bw_brightest_to_str())+"\n")

