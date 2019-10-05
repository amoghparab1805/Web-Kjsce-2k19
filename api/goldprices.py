# LinearRegression is a machine learning library for linear regression 
from sklearn.linear_model import LinearRegression 
# pandas and numpy are used for data manipulation 
import pandas as pd 
import numpy as np 
# matplotlib and seaborn are used for plotting graphs 
import matplotlib.pyplot as plt 
import seaborn 
# fix_yahoo_finance is used to fetch data 
import yfinance as yf
import datetime
from sklearn.model_selection import train_test_split
from sklearn import preprocessing,svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

total = 0
df = yf.download('GLD','2008-01-01','2019-10-04')
# Only keep close columns 
df=df[['Close']] 
#print(df.head())
# Drop rows with missing values 
predict_days = 30
df['Prediction'] = df[['Close']].shift(-predict_days)
X = np.array(df.drop(['Prediction'],1))
X = X[:-predict_days]
y = np.array(df['Prediction'])
y = y[:-predict_days]
x_train, x_test, y_train, y_test =  train_test_split(X,y,test_size=0.2, random_state=0)
lr = LinearRegression()
lr.fit(x_train,y_train)
lr_confidence =  lr.score(x_test,y_test)
x_predict = np.array(df.drop(['Prediction'],1))[-predict_days:]
lr_prediction = lr.predict(x_predict)
lr_prediction = lr.predict(x_predict)

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in lr_prediction:
	next_date =  datetime.datetime.fromtimestamp(next_unix)
	next_unix += 86400
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]
	total+=i

avgpredict = total/len(lr_prediction)


df['Close'].plot()
df['Prediction'].plot()
plt.legend(loc = 4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
#print(lr_confidence)