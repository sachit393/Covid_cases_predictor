import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

df = pd.read_csv('Covid 19 Confirmed Cases-Kerala.csv',index_col='Date',parse_dates=True)
# daily data
df.index.freq='D'

#plotting the timeseries
plt.plot(df['Confirmed'])
plt.show()

# removing initial values close to 0

df=df.loc['2020-06-01':]

# MAKING ARIMA MODEL

model = ARIMA(df['Confirmed'],order=(2,1,5))
fitted_model = model.fit()

forecast = fitted_model.predict(len(df),len(df)+5,typ='levels').rename('ARIMA(2,1,5) Future')
print(forecast)

import pickle
pickle.dump(fitted_model,open("model.sav", "wb"))
