import os
import csv
import numpy as np
import pandas as pd

"""
Cleans the exported tracking data output of the OptiTrack
"""
class CameraPoseCleaner():
    def __init__(self):
        pass

    @staticmethod
    def load_from_file(cleaned_poses_path):
        df = pd.read_csv(cleaned_poses_path)
        return df

    @staticmethod
    def clean_camera_pose_file(pose_path, write_cleaned_to_file=False):
        cleaned_pose_path = pose_path[:pose_path.rfind(".csv")] + "_cleaned.csv"

        header_rows = []
        rows = []

        with open(pose_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row_id, row in enumerate(reader):

                if row_id == 3 or row_id == 5 or row_id == 6:
                    header_rows.append(row)

                elif row_id > 6:
                    rows.append(row)
                else:
                    continue

        headers = ['_'.join([x[i] for x in header_rows if len(x[i]) > 0]) for i in range(len(header_rows[0]))]
        headers = [h.replace(" ", "_").replace("(", "").replace(")", "") for h in headers]

        first_marker_column = min([i for (i, h) in enumerate(headers) if "Marker" in h])

        headers = headers[:first_marker_column]
        rows = [row[:first_marker_column] for row in rows]

        df = pd.DataFrame(rows, columns=headers)

        if write_cleaned_to_file:
            df.to_csv(cleaned_pose_path)

        return df
            
