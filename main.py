import os, sys, cv2, shutil
import matplotlib.pyplot as plt
import numpy as np

from Sample import Sample


def split_into_samples():
    filenames = list(sorted(os.listdir("data")))
    filenames = [file for file in filenames if file.upper().startswith("SAMP")]
    samps = []
    for i in range(len(filenames) // 6):
        samps.append(Sample(filenames[i * 6:(i + 1) * 6]))
    return samps


def sample_name(sample: Sample) -> str:
    return sample.ET545_unlit_name[5:sample.ET545_unlit_name.index("_W.O")]


def convert_to_grayscale(input_image):
    grayscale_image = 0.299 * input_image[:, :, 0:1] + 0.587 * input_image[:, :, 1:2] + 0.114 * input_image[:, :,
                                                                                                    2:3]
    return grayscale_image


def write_single_histo_chart(img: np.ndarray, save_path: str):
    titles = ['Black and White', 'Red', 'Green', 'Blue']
    yaxes = 'Number of Pixels'
    xaxes = ['BW Pixel values', 'Red pixel values', 'Green pixel values', 'Blue pixel values']
    imgs = [convert_to_grayscale(img), img[:, :, 0], img[:, :, 1], img[:, :, 2]]
    f, a = plt.subplots(2, 2)
    a = a.ravel()
    for idx, ax in enumerate(a):
        ax.hist(imgs[idx].ravel(), bins=list(range(255)))
        ax.set_title(titles[idx])
        ax.set_xlabel(xaxes[idx])
        ax.set_ylabel(yaxes)
    plt.tight_layout()
    plt.savefig(save_path)


def histo_name(original_name: str) -> str:
    return original_name[5:-3]+"png"


def write_histos(sample: Sample, base_dir: str):
    histo_filenames = [histo_name(name) for name in sample.all_filenames()]
    imgs = sample.all_imgs()
    for i in range(len(imgs)):
        write_single_histo_chart(imgs[i], os.path.join(base_dir, histo_filenames[i]))


def write_minus_images(sample: Sample, base_dir: str):
    minus_470 = np.clip(sample.ET470_lit - sample.ET470_unlit, 0, 255)
    minus_470_path = os.path.join(base_dir, sample_name(sample)+"_470_subtracted_histo.png")
    write_single_histo_chart(minus_470, minus_470_path)
    cv2.imwrite(os.path.join(base_dir, sample_name(sample)+"_470_subtracted.png"), minus_470)
    minus_505 = np.clip(sample.ET505_lit - sample.ET505_unlit, 0, 255)
    minus_505_path = os.path.join(base_dir, sample_name(sample)+"_505_subtracted.png")
    write_single_histo_chart(minus_505, minus_505_path)
    cv2.imwrite(os.path.join(base_dir, sample_name(sample) + "_505_subtracted.png"), minus_505)
    minus_545 = np.clip(sample.ET545_lit - sample.ET545_unlit, 0, 255)
    minus_545_path = os.path.join(base_dir, sample_name(sample)+"_545_subtracted.png")
    write_single_histo_chart(minus_545, minus_545_path)
    cv2.imwrite(os.path.join(base_dir, sample_name(sample) + "_545_subtracted.png"), minus_545)


def analyze_sample(sample: Sample):
    sample.load() # loads image files into memory
    base_dir = f"results/{sample_name(sample)}"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    [shutil.copyfile(os.path.join("data", img_name), os.path.join(base_dir, img_name)) for img_name in sample.all_filenames()] # copies files
    write_histos(sample, base_dir) # writes histos
    write_minus_images(sample, base_dir)
    sample.unload() # frees memory


def main():
    samples = split_into_samples()
    for sample in samples:
        analyze_sample(sample)
        sys.exit(0)


if __name__ == '__main__':
    main()
