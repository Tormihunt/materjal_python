from sklearn.model_selection import train_test_split
import pandas as pd
df = pd.read_csv("data/standardised_data.csv")
print(df.shape)
print(df.head())