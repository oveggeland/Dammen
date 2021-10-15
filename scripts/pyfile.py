import struct
import numpy as np
import os
from PIL import Image

"""
Her er scriptet for å konvertere en .rd7 fil til en .csv fil (som kan åpnes og leses i feks excel)

For at scriptet skal fungere er det viktig at dataen ligger slik du har definert i FILE_DIR. 
Du må også ha en mappe "results" og hvor scriptet lagrer resultatene.
"""

# Retningen til datafilen du vil lese
# Sørg for at python scriptet blir kjørt fra mappen scripts
FILE_DIR = "data/p_r_0010.rd7"
N_SAMPLES = 765

if __name__ == "__main__":
    # f er fil-leser objektet
    f = open(FILE_DIR, "rb")

    # Find antall verdier i filen og alloker dataminne til å hente ut verdiene
    n_values = os.stat(FILE_DIR).st_size/4
    assert n_values%1 == 0, "File is not 32bit binary"
    n_rows = N_SAMPLES
    n_cols = int(n_values//n_rows + 1)
    values = np.zeros((n_rows, n_cols))

    # Loop over alle verdiene og lagre dem i values
    counter = 0
    while counter < n_values:
        val = struct.unpack('i', f.read(4))[0]
        values[counter%n_rows, counter//n_rows] = val

        counter += 1


    # Lagre lesbar data som .csv
    np.savetxt(f"results/data_{n_rows}_rows.csv", values, delimiter=",")

    # Lagre svart/hvitt bilde
    values -= values.min()
    values /= values.max()
    values *= 255
    im = Image.fromarray(values)
    im = im.convert('L')
    im.save(f"results/figs/values_fromrow_{slice_row}:.jpeg")

    print("finish reading")
