# Relative Strength Index Programe: Using the data on stock prices from Yahoo Finance to calculate the RSI
# RSI: A technical oscillator that uses clsong price data for identifying overbought and oversold signals
# Also used to spot divergences warning of a trend change in price

# Formula:
# RSI_stepone = 100 - [100/{1+(avg. gain / avg. loss)}]
# Typically we use the average gain and average loss over 14 periods

#1: Importing the necessary libraries
from cProfile import label
from tracemalloc import start
from matplotlib.lines import lineStyles
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as MSE
import yfinance as yf

#2: Defining the data retrieval function
stock_ticker = input("Please enter the stock ticker to generate Closing price and RSI graphs: ")

def stocks (stock, start_date, end_date):
    # The ticker
    ticker = stock
    tickerdata = yf.Ticker (ticker)
    tickerdf = tickerdata.history(period = '1d', start = start_date, end = end_date)
    return tickerdf
stock2 = stocks (stock_ticker, "2017-10-17", "2022-10-17")
stock2.drop (columns = ["Dividends", "Stock Splits", 'Open', 'High', 'Low', 'Volume'], inplace = True)
print (stock2.head())

# stock2 is the main data source we will use for the RSI Calculation
def RSI_fn(data, period):
    N = len(stock2['Close'])
    U = [0] * N
    D = [0] * N
    pos_fl = []
    neg_fl = []

    for i in range (1, len(typ_pr)):
        if typ_pr[i]> typ_pr[i-1]:
            pos_fl.append (typ_pr[i-1])
            neg_fl.append(0)
        elif typ_pr[i-1]>typ_pr[i]:
            pos_fl.append(0)
            neg_fl.append(typ_pr[i-1])
        else:
            pos_fl.append(0)
            neg_fl.append(0)
    pos_mf = []
    neg_mf = []
    for i in range (period-1, len(pos_fl)):
        pos_mf.append(sum(pos_fl[i+1-period: i +1]))
    for i in range (period-1, len(neg_fl)):
        neg_mf.append(sum(neg_fl[i+1-period : i + 1]))
    MFI = 100 * (np.array(pos_mf) / (np.array (pos_mf) + np.array(neg_mf)))
    new_df = pd.DataFrame()
    new_df = stock2 [period:]
    new_df ['MFI'] = MFI
    return MFI, new_df
RSI_main, new_df = MFI (stock2, 14)
print (new_df.head(5))

df1 = new_df.drop(columns = ['Open', 'High', 'Low', 'Volume'])
print (df1.head(5))
# Plotting MFI and the candlestick graph of stock prices in one graph

figure, axis = plt.subplots(2)
figure.suptitle('Stock Close Price and RSI Chart')
axis[0].plot(df1['Close'])
axis[0].set_title('Closing Price Chart')

axis[1].plot(df1['MFI'])
axis[1].set_title('RSI Chart')

os_one = axis[1].axhline(0, linestyle = '--', color = 'green', label = "Oversold 1")
os_two = axis[1].axhline (20, linestyle = '--', color = 'blue', label = "Oversold 2")
os_three = axis[1].axhline(30, linestyle = '--', label = "Oversold 3")

# Significant level: Overbought
ob_one = axis[1].axhline (70, linestyle = '--', label = "Overbought 1")
ob_two = axis[1].axhline(80, linestyle = '--', color = 'red', label = "Overbought 2")
ob_three = axis[1].axhline(100, linestyle = '--', color = 'yellow', label = "Overbought 3")
legend = axis[1].legend(handles = [ob_one, ob_two, ob_three, os_one, os_two, os_three], loc = "center left",
                        bbox_to_anchor = (1,0.5) ,ncol = 1, fontsize = "small")
figure.tight_layout(pad = 1.0)
plt.show()

