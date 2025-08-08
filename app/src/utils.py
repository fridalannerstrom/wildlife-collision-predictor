import pandas as pd

def read_csv_latin1(path):
    return pd.read_csv(path, encoding="latin1")