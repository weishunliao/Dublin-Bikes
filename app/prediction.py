import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression


df = pd.read_csv("app/static/cache/training_2.csv")
cont_features = ['Hour', 'Weekday', 'Total_Available_Bikes', 'Temp', 'Weather(Rain)', 'Visibility', 'Wind_Speed']
X = df[cont_features]
y = df.Available_bike
multiple_linreg = LinearRegression().fit(X[cont_features], y)

pickleFile = open('app/static/cache/model.pickle', 'wb')
pickle.dump(multiple_linreg,pickleFile)
pickleFile.close()

# loaded_model = pickle.load(open(app/static/cache/model.pickle, 'rb'))
# multiple_linreg_predictions = multiple_linreg.predict(X[cont_features])
