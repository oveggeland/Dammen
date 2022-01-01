import numpy as np
import pandas as pd
import sys
import os

from matplotlib import pyplot as plt


"""
Denne koden interpolerer dataen fra et dybdekart og lager et oversiktsbilde
"""
def main():
    filename = "../data/filter17.dat"
    threshold = 50000000
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    

    # Read data with pandas
    print("Reading data")
    df = pd.read_csv(filename)
    df.drop(df.columns[len(df.columns)-2:], axis=1, inplace=True)
    columns = ["N", "E", "Val"]
    df.columns = columns

    # Rotate and align coordinates with the southermost point in the origin
    print("Rotating coordinates")
    df, nx, ny = align_coordinates(df)

    # Transform into numpy array by interpolation
    print("Interpolating")
    map = np.zeros((ny, nx))

    indices = np.arange(ny)
    for x in range(nx):
        points = df[df["X"] == x].sort_values("Y")
        xp = points["Y"]
        fp = points["Val"]

        col = np.interp(indices, xp, fp)
        map[:, x] = col
    

    bin_map = map > threshold


    # Plot both maps
    print("Saving maps")
    dir = "../results/interpolation/"
    name = filename.split("/")[-1][:-4]

    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(map, cmap='gray', origin='lower')
    ax[0].set_title("Grayscale")
    ax[1].imshow(bin_map, cmap='gray', origin='lower')
    ax[1].set_title(f"Binary with threshold at {threshold}")
    plt.savefig(os.path.join(dir, name))

    # Plot grayscale alone
    plt.imshow(map, cmap='gray', origin='lower')
    plt.savefig(os.path.join(dir, name+"_grayscale"))

    # Plot binary alone 
    plt.imshow(bin_map, cmap='gray', origin='lower')
    plt.savefig(os.path.join(dir, name+"_binary"))

    print("Finished")

def align_coordinates(df):
    # Find notrtermost and easternmost points
    south_point = df.loc[df["N"].idxmin()]
    east_point = df.loc[df["E"].idxmax()]
    angle = find_angle(south_point, east_point)

    # Transform array into relative coordinates
    df["N"] = df["N"].transform(lambda n: (n - south_point.N)*10).astype(int)
    df["E"] = df["E"].transform(lambda e: (south_point.E - e)*10).astype(int)

    # Rotate coordinates
    rot = rotation_matrix(angle)
    print("Rotating with an angle of ", angle*180/np.pi)
    df = df.apply(lambda row : rotate(rot, row), axis=1)

    # Adjust for offsets (can occur if map is not completely square)
    east_offset = df["E"].min()
    north_offset = df["N"].min()
    df["N"] = df["N"].transform(lambda n: (n - north_offset)).astype(int)
    df["E"] = df["E"].transform(lambda e: (e - east_offset)).astype(int)

    columns = ["X", "Y", "Val"]
    df.columns = columns
    return df, df["X"].max(), df["Y"].max()



def find_angle(n_point, e_point):
    dx = e_point["E"] - n_point["E"]
    dy = e_point["N"] - n_point["N"]

    return np.arctan(dx/dy)

def rotation_matrix(angle):
    return np.array(
        [[np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]]
    )

def rotate(rot, point):
    vec = np.array([point.N, point.E])
    vec = rot @ vec
    point.N = vec[0]
    point.E = vec[1]
    return point

if __name__ == '__main__':
    main()
