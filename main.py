import os, sys, cv2, shutil
import matplotlib.pyplot as plt
import numpy as np

from CumulativeData import CumulativeData
from References import References
from Sample import Sample


def split_into_samples():
    filenames = list(sorted(os.listdir("data")))
    filenames = [file for file in filenames if file.upper().startswith("SAMP")]
    samps = []
    for i in range(len(filenames) // 6):
        samps.append(Sample(filenames[i * 6:(i + 1) * 6]))
    return samps


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
    f.tight_layout()
    f.savefig(save_path)
    plt.close(f)


def histo_name(original_name: str) -> str:
    return original_name[5:-4]+"_histogram"+".png"


def write_histos(sample: Sample, base_dir: str):
    histo_filenames = [histo_name(name) for name in sample.all_filenames()]
    imgs = sample.all_imgs()
    for i in range(len(imgs)):
        write_single_histo_chart(imgs[i], os.path.join(base_dir, histo_filenames[i]))


def write_minus_images(sample: Sample, base_dir: str):
    filter_sizes = ["470", "505", "545"]
    sample_imgs_lit = [sample.ET470_lit, sample.ET505_lit, sample.ET545_lit]
    sample_imgs_unlit = [sample.ET470_unlit, sample.ET505_unlit, sample.ET545_unlit]
    for i in range(3):
        minus_img = np.clip(sample_imgs_lit[i] - sample_imgs_unlit[i], 0, 255)
        minus_img_histo_path = os.path.join(base_dir, sample.name + f"_{filter_sizes[i]}_subtracted_histo.png")
        write_single_histo_chart(minus_img, minus_img_histo_path)
        cv2.imwrite(os.path.join(base_dir, sample.name + f"_{filter_sizes[i]}_subtracted.png"), minus_img)


def write_minus_reference_images(sample: Sample, references: References, base_dir: str):
    filter_sizes = ["470", "505", "545"]
    sample_imgs = [sample.ET470_lit, sample.ET505_lit, sample.ET545_lit]
    for reference in [references.reference_one, references.reference_two]:
        reference_imgs = [reference.ET470_lit, reference.ET505_lit, reference.ET545_lit]
        for i in range(3):
            minus_img = np.clip(sample_imgs[i] - reference_imgs[i], 0, 255)
            minus_img_histo_path = os.path.join(base_dir, sample.name + f"_{reference.name}_{filter_sizes[i]}_subtracted_histo.png")
            write_single_histo_chart(minus_img, minus_img_histo_path)
            cv2.imwrite(os.path.join(base_dir, sample.name + f"_{reference.name}_{filter_sizes[i]}_subtracted.png"), minus_img)


def write_scatter_plot(sample: Sample, references: References, base_dir: str):
    fig, ax = plt.subplots()
    x = sample.brightest_pixels.all_bw_brightest()+references.yeast_reference.brightest_pixels.all_bw_brightest()
    y = sample.brightest_pixels.all_green_brightest()+references.yeast_reference.brightest_pixels.all_green_brightest()
    labels = [sample.name + " " + bright_name for bright_name in sample.brightest_pixels.all_brightest_names()]\
             + ["yeast " + name for name in references.yeast_reference.brightest_pixels.all_brightest_names()]
    ax.scatter(x, y)
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i], y[i]))
    plt.savefig(os.path.join(base_dir, "scatter.png"))
    plt.close(fig)


def analyze_sample(sample: Sample, references: References, cumulative_data: CumulativeData):
    sample.load() # loads image files into memory
    base_dir = f"results/{sample.name}"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    [shutil.copyfile(os.path.join("data", img_name), os.path.join(base_dir, img_name)) for img_name in sample.all_filenames()] # copies files
    write_histos(sample, base_dir) # writes histos
    write_minus_images(sample, base_dir)
    write_minus_reference_images(sample, references, base_dir)
    write_scatter_plot(sample, references, base_dir)
    cumulative_data.add_sample(sample.brightest_pixels)
    sample.unload()  # frees memory


def main():
    samples = split_into_samples()
    references = References()
    cumulative_data = CumulativeData()
    for i in range(len(samples)):
        sample = samples[i]
        analyze_sample(sample, references, cumulative_data)
        print(f"Finished Sample {sample.name}")
    cumulative_data.write_csv("results")


if __name__ == '__main__':
    main()
