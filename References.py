import glob, os
from typing import List

from Sample import Sample


def matching_image_names(search: str) -> List[str]:
    return [filename[filename.find("/") + 1:] for filename in glob.glob(search)]


class References:
    def __init__(self):
        self.reference_one = Sample(matching_image_names("data/REF_1*"), "OFF")
        self.reference_one.load()
        self.reference_two = Sample(matching_image_names("data/REF_Sample_Dish*"))
        self.reference_two.load()
        self.yeast_reference = Sample(matching_image_names("data/*yeast*"))
        self.yeast_reference.load()
