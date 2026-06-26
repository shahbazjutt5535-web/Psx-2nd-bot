import math
import pandas as pd
import numpy as np


def f(value, digits=2):
    if value is None:
        return "N/A"

    if isinstance(value, float):
        if math.isnan(value):
            return "N/A"

    try:
        return round(float(value), digits)
    except:
        return value


def last(series):
    try:
        return series.iloc[-1]
    except:
        return None


def previous(series):
    try:
        return series.iloc[-2]
    except:
        return None


def percent(a, b):
    if b == 0:
        return 0

    return ((a-b)/b)*100


def distance(price, level):
    if level is None:
        return None

    return abs(price-level)


def candle_body(row):
    return abs(row["close"]-row["open"])


def candle_range(row):
    return row["high"]-row["low"]


def upper_wick(row):

    return row["high"]-max(row["open"],row["close"])


def lower_wick(row):

    return min(row["open"],row["close"])-row["low"]


def is_bull(row):

    return row["close"]>row["open"]


def is_bear(row):

    return row["close"]<row["open"]


def rolling_high(df,length):

    return df["high"].rolling(length).max()


def rolling_low(df,length):

    return df["low"].rolling(length).min()


def atr(df,length=14):

    high=df["high"]

    low=df["low"]

    close=df["close"]

    tr1=high-low

    tr2=(high-close.shift()).abs()

    tr3=(low-close.shift()).abs()

    tr=pd.concat([tr1,tr2,tr3],axis=1).max(axis=1)

    return tr.rolling(length).mean()


def ema(df,length):

    return df["close"].ewm(span=length,adjust=False).mean()


def sma(df,length):

    return df["close"].rolling(length).mean()
