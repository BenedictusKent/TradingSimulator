import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
import math
from sklearn.metrics import mean_squared_error
from keras.models import load_model

# You can write code above the if-main block.
def __create_dataset(timestep,data):
  x_data = []
  y_data = []
  data = data.iloc[:,0:1].values
  sc = MinMaxScaler(feature_range = (0, 1))
  data = sc.fit_transform(data)
  for i in range(timestep, len(data)):
      # print(i-timestep,i)
      x_data.append(data[i-timestep:i,0])
      y_data.append(data[i,0])
  x_train, y_train = np.array(x_data), np.array(y_data)
  # print(y_train[0])
  x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
  return x_train,y_train
def __train(x_train,y_train):
  model = Sequential()
  model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
  model.add(LSTM(50, return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(50, return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(50))
  model.add(Dropout(0.2))
  model.add(Dense(1))

  model.compile(optimizer='adam', loss='mean_squared_error')
  model.fit(x_train, y_train, epochs=100, batch_size=32)
  return model
def __create_test(timestep,train,test):
  train = train.iloc[:,0:1].values
  test = test.iloc[:,0:1].values
  testing = np.concatenate([train[-60:,0],test[:,0]])
  x_data = []
  for i in range(timestep,len(testing)):
      x_data.append(testing[i-timestep:i])
  x_test = np.array(x_data)
  x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
  # print(x_test.shape)
  return x_test
def __action(status,yesterday_price,data,model):
  sc = MinMaxScaler(feature_range = (0, 1))
  data = sc.fit_transform(data)
  data = np.reshape(data,(1,60,1))
  predicted = model.predict(data)
  predicted = sc.inverse_transform(predicted)
  action = 0
  if status == 0:
    if yesterday_price > predicted: # dropped
      status = 0
      action = 0
    elif yesterday_price < predicted: # increase
      status = 1
      action = 1
  elif status == 1:
    sell_ratio = (yesterday_price - predicted)/yesterday_price # stop loss trigger
    profit_ratio = (predicted - yesterday_price)/predicted # take profit trigger
    if sell_ratio > 0.01 or profit_ratio > 0.005 : # 1% change in price or 2% change in price
      status = 0
      action = -1
    else:
      status = 1
      action = 0
  return status, action, predicted
if __name__ == "__main__":
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--training", default="training_data.csv", help="input training data file name")
    parser.add_argument("--testing", default="testing_data.csv", help="input testing data file name")
    parser.add_argument("--output", default="output.csv", help="output file name")
    args = parser.parse_args()
    # The following part is an example.
    # You can modify it at will.
    training = pd.read_csv(args.training,delimiter=',',names=['Open','High','Low','Close'])
    testing = pd.read_csv(args.testing,delimiter=',',names=['Open','High','Low','Close'])
    x_train, y_train = __create_dataset(60,training)
    # model = __train(x_train,y_train)
    model = load_model("model.h5")
    testing_data = __create_test(60,training,testing)
    status = 0 # starting with nothing
    yesterday_price = training.iloc[-1,0]
    ## to check
    y_1 = []
    y_2 = []
    with open(args.output, "w") as output_file:
        for val,row in enumerate(testing_data):
            # We will perform your action as the open price in the next day.
            status, action, predicted = __action(status,yesterday_price,row,model)
            # print("Day:",val,",",status,action)
            output_file.write(str(action)+"\n")
            yesterday_price = testing.iloc[val,0] # keeping track of previous day
            # print(yesterday_price,predicted)

