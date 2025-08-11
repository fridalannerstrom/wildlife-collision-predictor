import pandas as pd

url = "https://github.com/fridalannerstrom/wildlife-collision-predictor/releases/download/data/cleaned_data.csv"
df = pd.read_csv(url, encoding="latin1")
print(df.head())