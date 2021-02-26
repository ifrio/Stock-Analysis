import yfinance as yf
import numpy as np
from datetime import date
import pandas as pd
import pickle
import os

class StockAnalysis:
    watchList = set()
    budget = 0

    def __init__(self):
        filesize = os.path.getsize("stockList.txt")
        if filesize != 0:
            with open('stockList.txt',"rb") as f:
                self.watchList = pickle.load(f)

    def save(self):
        with open("stockList.txt", "wb" ) as f:
            pickle.dump(self.watchList, f)

    def getWatchList(self):
        return self.watchList
    
    def addToList(self,ticker):
        if ticker in self.watchList:
            print(ticker, 'is already in watchlist!')
        else:
            self.watchList.add(ticker)
            self.save()
            print(ticker, 'has been added to watchlist!')
    
    def removeFromList(self, ticker):
        if ticker in self.watchList:
            self.watchList.remove(ticker)
            print(ticker, 'has been removed from watchlist!')
            self.save()
        else:
            print(ticker, 'is not in watchlist!')

    def backTestSMA(self,ticker, budget=1000):
        today = date.today()
        today = today.strftime("%Y-%m-%d")
        ticker = ticker
        start = "2020-10-01"
        end = today
        interval = "1d"
        data = self.stock_data(ticker, start, end, interval)

        data['mu_20'] = self.rolling_average(data,'Close',20)
        data['std_20'] = self.rolling_std(data,'Close',20)
        zScores = [(data["Close"][day] - data["mu_20"][day]) / data["std_20"][day] for day in range(len(data))]
        shares = 0
        hasPosition = False

        for day in range(len(data)):
            # Sell short if the z-score is > 1
            if zScores[day] > 1 and hasPosition:
                budget = shares * data["Close"][day]
                shares = 0
                hasPosition = False
            # Buy long if the z-score is < 1
            elif zScores[day] < -1 and hasPosition == False:
                shares = budget / data["Close"][day]
                hasPosition = True
            # Clear positions if the z-score less than .5
            elif abs(zScores[day]) < 0.5 and hasPosition:
                budget = shares * data["Close"][day]
                shares = 0
                hasPosition = False
            # Hold if z-score greater than .5
            else:
                continue

        return budget

    def stock_data(self,ticker, start, end, interval):
        df= yf.Ticker(ticker)
        df = df.history(start=start, end=end, interval=interval)
        df.reset_index(level=0, inplace=True)
        return df

    def rolling_average(self,df,columns, window):
        return df[columns].rolling(window).mean()

    def rolling_std(self,df,columns, window):
        return df[columns].rolling(window).std()