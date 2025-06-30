#!/usr/local/bin/python3

# Adapted from: Zebing Lin (https://github.com/linzebing)

from datetime import datetime, date
import math
import numpy as np
import time
import sys
import yfinance as yf

if len(sys.argv) == 1:
    symbols = ['UPRO', 'TMF']
else:
    symbols = sys.argv[1].split(',')
    for i in range(len(symbols)):
        symbols[i] = symbols[i].strip().upper()

num_trading_days_per_year = 252
window_size = 20
date_format = "%Y-%m-%d"
reference_date = datetime.today()
end_timestamp = int(reference_date.timestamp())
start_timestamp = int(end_timestamp - (1.4 * (window_size + 1) + 4) * 86400)

def get_volatility_and_performance(symbol, reference_date=reference_date):
    # Get data using yfinance
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=datetime.fromtimestamp(start_timestamp), end=datetime.fromtimestamp(end_timestamp))
    
    if len(hist) < window_size + 1:
        raise Exception(f"Not enough data points for {symbol}")
    
    # Get closing prices
    prices = hist['Close'].values.tolist()
    prices.reverse()
    
    volatilities_in_window = []
    for i in range(window_size):
        volatilities_in_window.append(math.log(prices[i] / prices[i+1]))
    
    most_recent_date = hist.index[-1].date()
    assert (reference_date.date() - most_recent_date).days <= 4, f"reference date is {reference_date.date()}, most recent trading day is {most_recent_date}"

    return np.std(volatilities_in_window, ddof=1) * np.sqrt(num_trading_days_per_year), prices[0] / prices[window_size] - 1.0

def main():
    volatilities = []
    performances = []
    sum_inverse_volatility = 0.0
    for symbol in symbols:
        volatility, performance = get_volatility_and_performance(symbol, reference_date)
        sum_inverse_volatility += 1 / volatility
        volatilities.append(volatility)
        performances.append(performance)

    print("Portfolio: {}, as of {} (window size is {} days)".format(str(symbols), reference_date.strftime('%Y-%m-%d'), window_size))
    for i in range(len(symbols)):
        print('{} allocation ratio: {:.2f}% (anualized volatility: {:.2f}%, performance: {:.2f}%)'.format(
            symbols[i], 
            float(100 / (volatilities[i] * sum_inverse_volatility)), 
            float(volatilities[i] * 100), 
            float(performances[i] * 100)
        ))

if __name__ == "__main__":
    main()

