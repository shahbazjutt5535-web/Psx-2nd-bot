"""
==========================================================
SMART MONEY CONCEPTS MODULE
Institutional Market Structure Engine
Part 1A
==========================================================
"""

import pandas as pd
import numpy as np


# ==========================================================
# Helper
# ==========================================================

def _price(v):
    try:
        return float(v)
    except:
        return np.nan


# ==========================================================
# Swing High Detection
# ==========================================================

def find_swing_highs(df, left=2, right=2):

    swings = []

    highs = df["high"].values

    for i in range(left, len(df)-right):

        current = highs[i]

        previous = highs[i-left:i]

        future = highs[i+1:i+right+1]

        if current > previous.max() and current > future.max():

            swings.append({
                "index": i,
                "price": float(current),
                "time": df.index[i]
            })

    return swings


# ==========================================================
# Swing Low Detection
# ==========================================================

def find_swing_lows(df, left=2, right=2):

    swings = []

    lows = df["low"].values

    for i in range(left, len(df)-right):

        current = lows[i]

        previous = lows[i-left:i]

        future = lows[i+1:i+right+1]

        if current < previous.min() and current < future.min():

            swings.append({
                "index": i,
                "price": float(current),
                "time": df.index[i]
            })

    return swings


# ==========================================================
# Last Swing High
# ==========================================================

def get_last_swing_high(df):

    highs = find_swing_highs(df)

    if len(highs) == 0:
        return None

    return highs[-1]


# ==========================================================
# Last Swing Low
# ==========================================================

def get_last_swing_low(df):

    lows = find_swing_lows(df)

    if len(lows) == 0:
        return None

    return lows[-1]


# ==========================================================
# Previous Swing High
# ==========================================================

def get_previous_swing_high(df):

    highs = find_swing_highs(df)

    if len(highs) < 2:
        return None

    return highs[-2]


# ==========================================================
# Previous Swing Low
# ==========================================================

def get_previous_swing_low(df):

    lows = find_swing_lows(df)

    if len(lows) < 2:
        return None

    return lows[-2]
    # ==========================================================
# Highest Confirmed Swing High
# ==========================================================

def highest_swing(df, lookback=300):

    data = df.tail(lookback)

    highs = find_swing_highs(data)

    if len(highs) == 0:
        return None

    return max(highs, key=lambda x: x["price"])


# ==========================================================
# Lowest Confirmed Swing Low
# ==========================================================

def lowest_swing(df, lookback=300):

    data = df.tail(lookback)

    lows = find_swing_lows(data)

    if len(lows) == 0:
        return None

    return min(lows, key=lambda x: x["price"])


# ==========================================================
# Swing High Count
# ==========================================================

def count_swing_highs(df, lookback=300):

    data = df.tail(lookback)

    return len(find_swing_highs(data))


# ==========================================================
# Swing Low Count
# ==========================================================

def count_swing_lows(df, lookback=300):

    data = df.tail(lookback)

    return len(find_swing_lows(data))


# ==========================================================
# Swing Distance
# ==========================================================

def swing_distance(df, lookback=300):

    high = highest_swing(df, lookback)

    low = lowest_swing(df, lookback)

    if high is None or low is None:
        return None

    return abs(high["price"] - low["price"])


# ==========================================================
# Current Price Distance From Last Swing High
# ==========================================================

def distance_from_last_high(df):

    swing = get_last_swing_high(df)

    if swing is None:
        return None

    price = float(df["close"].iloc[-1])

    return price - swing["price"]


# ==========================================================
# Current Price Distance From Last Swing Low
# ==========================================================

def distance_from_last_low(df):

    swing = get_last_swing_low(df)

    if swing is None:
        return None

    price = float(df["close"].iloc[-1])

    return price - swing["price"]
