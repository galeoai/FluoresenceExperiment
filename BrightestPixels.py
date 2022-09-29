

class BrightestPixels:
    def __init__(self, green_lit_470, BW_lit_470, green_unlit_470, BW_unlit_470,
                 green_lit_505, BW_lit_505, green_unlit_505, BW_unlit_505,
                 green_lit_545, BW_lit_545, green_unlit_545, BW_unlit_545):
        self.green_lit_470 = green_lit_470
        self.BW_lit_470 = BW_lit_470
        self.green_unlit_470 = green_unlit_470
        self.BW_unlit_470 = BW_unlit_470
        self.green_lit_505 = green_lit_505
        self.BW_lit_505 = BW_lit_505
        self.green_unlit_505 = green_unlit_505
        self.BW_unlit_505 = BW_unlit_505
        self.green_lit_545 = green_lit_545
        self.BW_lit_545 = BW_lit_545
        self.green_unlit_545 = green_unlit_545
        self.BW_unlit_545 = BW_unlit_545

    def all_green_brightest(self):
        return [self.green_lit_470, self.green_lit_505, self.green_lit_545, self.green_unlit_470, self.green_unlit_505,
                self.green_unlit_545]

    def green_brightest_to_str(self):
        return [str(it) for it in self.all_green_brightest()]

    def all_bw_brightest(self):
        return [self.BW_lit_470, self.BW_lit_505, self.BW_lit_545, self.BW_unlit_470, self.BW_unlit_505, self.BW_unlit_545]

    def bw_brightest_to_str(self):
        return [str(it) for it in self.all_bw_brightest()]

    @staticmethod
    def all_brightest_names():
        return ["470 lit", "505 lit", "545 lit", "470 dark", "505 dark", "545 dark"]