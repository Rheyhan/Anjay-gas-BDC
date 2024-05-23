import os
import pandas as pd

def create_submission(predicted, path = "submission.csv"):
    folder_loc = '/'.join([i for i in path.split("/")][:-1])
    if os.path.exists(folder_loc):
        os.makedirs(folder_loc)
    df = pd.read_excel("Data/Submission_Format.xlsx")
    df["Kelas"] = predicted
    df.to_csv(path, index=False)