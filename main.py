import pandas as pd
import numpy as np
import math
import datetime


def log_return(start, end):
    return np.log(end['pv'] / start['pv']) / (end['Date'] - start['Date']).total_seconds() * 365 * 86400


def main():
    df = pd.read_csv('data/btcusd_5y_1d.csv')
    risk_free_rate = 0.05
    reference_date = datetime.datetime(2022, 11, 15)
    # parse dates
    df['Date'] = pd.to_datetime(df['Date'])
    # calcualte present value
    df['pv'] = df['Close'] / np.power(1 + risk_free_rate, (df['Date'] - reference_date).dt.total_seconds() / 365 / 86400)
    # calculate log returns
    df['log_returns'] = np.log(df['pv'] / df['pv'].shift(1))
    # calculate volatility
    df['volatility'] = df['log_returns'].rolling(7).std() * math.sqrt(365)
    # print(df['log_returns'].std() * math.sqrt(365))
    # print(log_return(df.iloc[-1], df.iloc[0]))
    print(df[['Date', 'volatility']].tail(20))


if __name__ == "__main__":
    main()
