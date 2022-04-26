# Trading Simulator

The goal of this project is to do auto trading using the data of certain provided stock and to maximize the profit gained using our own algorithms.

## Data

Stock used in this project is the data of ```NASDAQ:IBM```.  
Data contains 4 columns: ```open, high, low, close```  
![Table sample](/img/table.png)

The chart below shows the graph of the training data:  
![Chart sample](/img/chart.png)

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
[something shall be written here...]

## Trading Algorithm
Our approach to maximize revenue is to introduce **stop loss** method.  
Our algorithm can be simply explained by bullet points:
- When no stock is held:
  - If the stock price is predicted to go up, then **buy**.
  - If the stock price is predicted to go down, then **hold**.
- When stock is held:
  - Keep track stock price of the current with the day before.
  - If the current price is higher and next day stock is projected to go up, then **hold**.
  - If the current price is higher and next day stock is projected to go down by x percent, then **sell**.
