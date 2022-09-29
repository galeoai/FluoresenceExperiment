from References import matching_image_names
from Sample import Sample
import glob

yeast_reference = Sample(matching_image_names("data/*yeast*"))
yeast_reference.load()
brightest_pixels = yeast_reference.brightest_pixels
print(brightest_pixels.green_brightest_to_str())
print(brightest_pixels.bw_brightest_to_str())
