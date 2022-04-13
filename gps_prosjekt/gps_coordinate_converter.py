"""
Copyright Dammen GeoServices
"""

import pandas as pd
import numpy as np


# This class holds a position ground truth which can be used to interpolate accurate positions based on measurement times
class PositionGT:
    def __init__(self, filename):
        self.df = pd.read_csv(filename, sep="\t")
            
    # Gets rid of irrelevant data columns
    def clean_up_df(self):
        self.df = self.df.iloc[:, [2, 3, 5]]
        self.df.columns = ["Time", "Latitude", "Longitude"]

    # Helper function
    def convert_to_ms(self, time_string):
        (t, m, s, ms) = time_string.split(":")
        return (int(t)*3600 + int(m)*60 + int(s))*100 + int(ms)

    # This function creates a millisecond column from the raw tt:mm:ss:msms format
    def sort_on_ms(self):
        ms_col = self.df['Time'].apply(lambda s: self.convert_to_ms(s))
        self.df.insert (1, "Time_ms", ms_col)
        self.df.sort_values("Time_ms")

    # This function takes a time in milliseconds and returns the interpolated latitude and longitude
    def interpolate_coordinates(self, time):
        # Find the two closest points to the time inserted
        high_idx = self.df[self.df["Time_ms"] > time].iloc[0, :].name
        closest_points = self.df.iloc[[high_idx-1, high_idx], :]
        
        # Define interpolation variables
        x_vals = closest_points["Time_ms"].to_numpy()
        lat_vals = closest_points["Latitude"].to_numpy()
        long_vals = closest_points["Longitude"].to_numpy()

        # Find interpolation
        int_lat = np.interp(time, x_vals, lat_vals)
        int_long = np.interp(time, x_vals, long_vals)

        return int_lat, int_long
        


class DataHandler:
    def __init__(self, filename, gt):
        self.df = pd.read_csv(filename, sep="\t")
        self.gt = gt

    def convert_to_ms(self, time_string):
        (t, m, s) = time_string.split(":")
        return (3600*int(t) + 60*int(m) + float(s))*100


    def overwrite_position_estimates(self):
        print(self.df.head(5))
        for index, row in self.df.iterrows():
            ms = self.convert_to_ms(row['UTC Time'])
            lat, long = self.gt.interpolate_coordinates(ms)
            self.df.loc[index, "Latitude"] = lat
            self.df.loc[index, "Longitude"] = long
        print(self.df.head(5))


    def save_data_file(self, out_file):
        self.df.to_csv(out_file, sep="\t", index=False)


if __name__ == "__main__":
    gps_file = "p_r_0001.txt"
    data_file = "ob_20220412141513.txt"
    data_out_file = "fixed_ob_20220412141513.txt"
    # Create position ground truth object pGT
    pGT = PositionGT(gps_file)    # Change input to suit the data needs
    pGT.clean_up_df()
    pGT.sort_on_ms()
    
    # Overwrite the bad position measurements from the data file
    dH = DataHandler(data_file, pGT)
    dH.overwrite_position_estimates()
    dH.save_data_file(data_out_file)
    