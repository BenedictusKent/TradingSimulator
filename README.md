# Trading Simulator

The goal of this project is to do auto trading using the data of certain provided stock and to maximize the profit gained using our own algorithms.

## Data

Stock used in this project is the data of ```NASDAQ:IBM```.  
Data contains 4 columns: ```open, high, low, close```  
![Table sample](/img/table.png)

The chart below shows the graph of the training data (*close* data):  
![Chart sample](/img/chart.png)  

The data used in this training is only the *close* data.  
The input data for training is to append 60-day window data to the present data.  
By this approach, we can feed the model with 60 days of past data and have it predict the next day data.

## Training with Long Short-Term Memory (LSTM)
Since we are mainly focusing on the time series problem. 
- LSTM contains feedback connections which make them different to traditional feedforward neural networks.
- which allows useful information about preious data in sequence to help with the processing of new data points.

### How does LSTM works?
3 main dependencies:
- cell state (current long-term memory of network)
- previous hidden state (output of previous data)
- input data 

LSTM uses series of gates to control information flow
which acts as filters to generate information for training:
- forget gate
- input gate
- output gates  

For more detailed explanation, please refer here [LSTM](https://towardsdatascience.com/lstm-networks-a-detailed-explanation-8fae6aefc7f9)

### Model Architecture
Below is the summary of the model architecture used:  
![Model summary](/img/model.png)

## Testing
To test the data, ```testing.csv``` is loaded and only take *close* data.  
1. Use the last row of training data and have it predict the price.  
2. The price predicted will be stored in an array.  
3. Append actual stock price data to training data and drop the first element in training data.
4. Predict next day data.
5. Repeat no. 3 until there is no more data.  

We used 2 different methods of testing:  
1. Split training data to test data [First 800 data are training, the rest are test].
![Prediction chart: Split](/img/predict.png)  
2. Use all training data to train, test data use ```testing.csv```  
![Prediction chart: Separated](/img/test.png)  

The model should be fed with actual test data, otherwise the result will be terrible.  
![Bad test](/img/badtest.png)  

## Trading Algorithm
Our approach to maximize revenue is to introduce **stop loss** method.  
Our algorithm can be simply explained by bullet points:
- When no stock is held:
  - If the stock price is predicted to go up, then **buy**.
  - If the stock price is predicted to go down, then **hold**.
- When stock is held:
  - Keep track stock price of the current with the day before.
  - If the current price is higher and next day stock is projected to go up, then **hold**.
  - If the current price is higher and next day stock is projected to go down by 5%, then **sell**.
