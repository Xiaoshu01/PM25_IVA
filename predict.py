# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:41:48 2019

@author: 73921
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Activation,LSTM
import matplotlib.pyplot as plt
from sklearn import metrics
import os


 
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
	Frame a time series as a supervised learning dataset.
	Arguments:
		data: Sequence of observations as a list or NumPy array.
		n_in: Number of lag observations as input (X).
		n_out: Number of observations as output (y).
		dropnan: Boolean whether or not to drop rows with NaN values.
	Returns:
		Pandas DataFrame of series framed for supervised learning.
	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg


###清洗数据
def parse(x):
    return datetime.strptime(x, '%Y %m %d %H')
dataset = pd.read_csv("BeijingPM20100101_20151231.csv", parse_dates = [['year', 'month', 'day', 'hour']], index_col = 0, date_parser = parse)
dataset.drop('No', axis=1, inplace=True)
dataset.columns = [c.replace(' ', '_') for c in dataset.columns]
dataset.index.name = 'date'
dataset.drop(['PM_Dongsi','PM_Dongsihuan','PM_Nongzhanguan'], axis=1, inplace=True)
dataset = dataset[24:]
dataset['PM_US_Post'].fillna(0, inplace=True)
dataset.fillna(0, inplace=True)

###使用labelencoder对风向进行编码
values = dataset.values
encoder = LabelEncoder()
values[:,6] = encoder.fit_transform(values[:,6].astype(str))

###将所有变量转变成float
values = values.astype('float32')

###直接调用函数进行MIN-MAX标准化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

###作为监督学习的框架
reframed = series_to_supervised(scaled, 1, 1)

###去掉不进行预测的列
reframed.drop(reframed.columns[[10,12,13,14,15,16,17,18,19]], axis=1, inplace=True)
reframed.columns = ['season(t-1)','PM_US_POST(t-1)','DEWP(t-1)','HUMI(t-1)','PRES(t-1)','TEMP(t-1)','cbwd(t-1)','lws(t-1)','pre(t-1)','Iprec(t-1)','PM_US_POST(t)']
#print(reframed.head())

###拆分训练数据和测试数据
values = reframed.values
n_train_hours = 4*365 * 24  ###四年的数据做训练
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

###################################################################
#搭建LSTM模型
##确定网络结构
model = Sequential()
model.add(LSTM(32, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')


##训练网络
history = model.fit(train_X, train_y, epochs=32, batch_size=36, validation_data=(test_X, test_y), verbose=2, shuffle=False)

##画出历史数据
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

###模型评估
### 预测
### make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

### invert scaling for forecast
inv_yhat = np.concatenate((yhat, test_X[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

### invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = np.concatenate((test_y, test_X[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
### calculate RMSE
rmse = np.sqrt(metrics.mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

plt.plot(train_y,label='train')
plt.plot(inv_yhat[1:],label='inhat')
plt.show()
plt.plot(test_y,label='test')
plt.plot(yhat[1:],label='yhat')
plt.show()

###未来数据预测








