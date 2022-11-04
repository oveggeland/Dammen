"""
Copyright Dammen GeoServices
"""

import pandas as pd
import numpy as np
import os

def merge_files(folder):
    try:
        os.mkdir(os.path.join("target", os.path.basename(folder)))
    except:
        print("Already exists")
        
    # Filename
    gps_file = os.path.join("source", folder, "gps_data.csv")
    data_file = os.path.join("source", folder, "sonar_data.txt")
    data_out_file = os.path.join("target", folder, "merged_gps_sonar_data.csv")

    # Create position ground truth object pGT
    gps_data = pd.read_csv(gps_file)

    gps_times = gps_data['T'].to_numpy()
    gps_x = gps_data['X'].to_numpy()
    gps_y = gps_data['Y'].to_numpy()

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
    merge_files("porsgrunn")
    merge_files("skoklevann")