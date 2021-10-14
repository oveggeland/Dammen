import struct
import numpy as np
import os
from PIL import Image

file_dir = "./data/p_r_0010.rd7"


if __name__ == "__main__":
    os.chdir("/home/oveggeland/Desktop/Dammen")

    f = open(file_dir, "rb")

    n_values = os.stat(file_dir).st_size/4
    assert n_values%1 == 0, "File is not 32bit binary"
    n_rows = 765
    n_cols = int(n_values//n_rows + 1)

    values = np.zeros((n_rows, n_cols))

    val = 1
    counter = 0
    while counter < n_values:
        val = struct.unpack('i', f.read(4))[0]
        values[counter%n_rows, counter//n_rows] = val
        print(counter)
        print(val)

        counter += 1


    # Save raw data
    np.savetxt(f"./data/data_{n_rows}_rows.csv", values, delimiter=",")

    # Create image
    slice_row = 0
    values = values[slice_row:, :]
    values -= values.min()
    values /= values.max()
    values *= 255
    im = Image.fromarray(values)
    im = im.convert('L')
    im.save(f"./results/figs/values_fromrow_{slice_row}:.jpeg")


    print("finish reading")
