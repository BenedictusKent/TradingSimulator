# Trading Simulator

The goal of this project is to do auto trading using the data of certain provided stock and to maximize the profit gained using our own algorithms.

## Data

Stock used in this project is the data of ```NASDAQ:IBM```.  
Data contains 4 columns: ```open, high, low, close```
![Table sample](/img/table.png)

The chart below shows the graph of the training data:
![Chart sample](/img/chart.png)

## Training
[something shall be written here...]

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
