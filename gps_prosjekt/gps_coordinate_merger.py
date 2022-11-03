"""
Copyright Dammen GeoServices
"""

import pandas as pd
import numpy as np
import glob
import os

def merge_files(folder, gps_delimiter=";", gps_col=3):
    try:
        os.mkdir(os.path.join("target", os.path.basename(folder)))
    except:
        print("Already exists")
        
    # Filenames
    gps_file = glob.glob(os.path.join("source", folder, "*.csv"))[0]
    data_file = glob.glob(os.path.join("source", folder, "*.txt"))[0]
    data_out_file = os.path.join("target", folder, "merged_"+os.path.basename(data_file))

    # Create position ground truth object pGT
    gps_data = pd.read_csv(gps_file, sep=gps_delimiter)

    gps_times = gps_data.iloc[:, gps_col].to_numpy()
    gps_x = gps_data.iloc[:, 0].to_numpy()
    gps_y = gps_data.iloc[:, 1].to_numpy()

    h = gps_times // 10000
    m = (gps_times % 10000) // 100
    s = gps_times % 100
    gps_total_seconds = s + 60*m + 3600*h

    print("GPS time interval:", gps_total_seconds.min(), gps_total_seconds.max())

    # Read datafile and interpolate gps coordinates
    sonar_data = pd.read_csv(data_file, delim_whitespace=True)

    sonar_total_seconds = sonar_data["HOUR"].to_numpy()*3600 + sonar_data["MINUTE"].to_numpy()*60 + sonar_data["SECOND"].to_numpy()
    print("Data time interval:", sonar_total_seconds.min(), sonar_total_seconds.max())

    sonar_data['CDP_X'] = np.interp(sonar_total_seconds, gps_total_seconds, gps_x)
    sonar_data['CDP_Y'] = np.interp(sonar_total_seconds, gps_total_seconds, gps_y)

    sonar_data.to_csv(data_out_file, index=False)


if __name__ == "__main__":
    merge_files("porsgrunn", gps_delimiter=";", gps_col=2)
    merge_files("skoklevann", gps_delimiter=",", gps_col=3)