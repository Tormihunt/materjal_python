from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd
df = pd.read_csv("data/standardised_data.csv")

#split training and testing data
X = df.drop('band_gap', axis=1)
y = df["band_gap"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regressor = RandomForestRegressor(n_estimators=100, random_state=42)
#train
regressor.fit(X_train, y_train)
#test
y_pred = regressor.predict(X_test)

#show evaluation
accuracy_absolute = mean_absolute_error(y_test, y_pred)
accuracy_mean = mean_squared_error(y_test, y_pred)
accuracy_r2 = r2_score(y_test, y_pred)
print(f'Accuracy absolute: {100 - accuracy_absolute * 100:.2f}%')
print(f'Accuracy mse: {100 - accuracy_mean * 100:.2f}%')
print(f'Accuracy r2 {accuracy_r2 * 100:.2f}%')

# save
joblib.dump(regressor, "./data/band_gap_rf.joblib")