import os
from typing import List
import matplotlib.pyplot as plt


def write_scatter_plot(x: List[float], y: List[float], names: List[str], name: str, cutofff: float):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, txt in enumerate(names):
        if y[i] > cutofff:
            ax.annotate(txt, (x[i], y[i]))
    plt.savefig(f"{name}")
    plt.close(fig)


def main():

    green_lit_470 =[]
    green_lit_505 =[]
    green_lit_545 =[]
    green_unlit_470 =[]
    green_unlit_505 =[]
    green_unlit_545 =[]
    BW_lit_470 =[]
    BW_lit_505 =[]
    BW_lit_545 =[]
    BW_unlit_470 =[]
    BW_unlit_505 = []
    BW_unlit_545 = []
    cols = [green_lit_470, green_lit_505, green_lit_545, green_unlit_470, green_unlit_505, green_unlit_545, BW_lit_470,BW_lit_505,BW_lit_545,BW_unlit_470,BW_unlit_505,BW_unlit_545]
    names = []
    with open("master_spreadsheet.csv", 'r') as spreadsheet:
        lines = spreadsheet.readlines()
    for line in lines[1:]:
        split_line = line.split(",")
        names.append(split_line[0])
        for i in range(len(cols)):
            cols[i].append(float(split_line[i+1]))

    xs_order = [green_lit_470, green_lit_505, green_lit_545, green_unlit_470, green_unlit_505, green_unlit_545]
    ys_order = [BW_lit_470, BW_lit_505, BW_lit_545, BW_unlit_470, BW_unlit_505, BW_unlit_545]
    filter_names = ["470_LIT", "505_LIT", "545_LIT", "470_UNLIT", "505_UNLIT", "545_UNLIT"]
    cutoffs = [35, 13, 4, 13, 8, 4.1]
    for i in range(len(xs_order)):
        write_scatter_plot(xs_order[i], ys_order[i], names, filter_names[i]+".png", cutoffs[i])


if __name__ == '__main__':
    main()
