import joblib
import pandas as pd

regressor = joblib.load("./data/band_gap_rf.joblib")
user_var = pd.read_csv("user_variables.csv")
standard_deviation = pd.read_csv("./data/standardised_deviation_data.csv").iloc[7, 0]
mean = pd.read_csv("./data/mean_data.csv").iloc[7, 0]
prediction = regressor.predict(user_var)
prediction = prediction*standard_deviation+mean
print(f'Band_gapi väärtus on {prediction[0]:.2f} eV')
