import matplotlib.pyplot as plt
import numpy as np
import cv2, sys, os


def convert_to_grayscale(input_image):
    grayscale_image = 0.299 * input_image[:, :, 0:1] + 0.587 * input_image[:, :, 1:2] + 0.114 * input_image[:, :,
                                                                                                    2:3]
    return grayscale_image


if __name__ == '__main__':
    img_file = "/home/avraham/Downloads/soda.bmp"#sys.argv[1]
    if not os.path.exists(img_file):
        sys.stderr.write("Given image file does not exist")
        sys.exit(1)
    img = cv2.imread(img_file)
    titles = ['Black and White', 'Red', 'Green', 'Blue']
    yaxes = 'Number of Pixels'
    xaxes = ['BW Pixel values', 'Red pixel values', 'Green pixel values', 'Blue pixel values']
    imgs = [convert_to_grayscale(img),img[:,:,0], img[:,:,1],img[:,:,2]]
    f, a = plt.subplots(2, 2)
    a = a.ravel()
    for idx, ax in enumerate(a):
        ax.hist(imgs[idx].ravel(), bins=list(range(255)))
        ax.set_title(titles[idx])
        ax.set_xlabel(xaxes[idx])
        ax.set_ylabel(yaxes)
    f.tight_layout()
    f.savefig("tmp.png")
    # plt.tight_layout()
    # plt.savefig("tmp.png")
