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
    # ==========================================================
# Market Structure Builder
# ==========================================================

def build_market_structure(df, lookback=300):

    last_high = get_last_swing_high(df)
    last_low = get_last_swing_low(df)

    previous_high = get_previous_swing_high(df)
    previous_low = get_previous_swing_low(df)

    highest = highest_swing(df, lookback)
    lowest = lowest_swing(df, lookback)

    return {

        "last_swing_high": None if last_high is None else last_high["price"],
        "last_swing_high_time": None if last_high is None else str(last_high["time"]),

        "last_swing_low": None if last_low is None else last_low["price"],
        "last_swing_low_time": None if last_low is None else str(last_low["time"]),

        "previous_swing_high": None if previous_high is None else previous_high["price"],
        "previous_swing_high_time": None if previous_high is None else str(previous_high["time"]),

        "previous_swing_low": None if previous_low is None else previous_low["price"],
        "previous_swing_low_time": None if previous_low is None else str(previous_low["time"]),

        "highest_swing": None if highest is None else highest["price"],
        "highest_swing_time": None if highest is None else str(highest["time"]),

        "lowest_swing": None if lowest is None else lowest["price"],
        "lowest_swing_time": None if lowest is None else str(lowest["time"]),

        "swing_high_count": count_swing_highs(df, lookback),
        "swing_low_count": count_swing_lows(df, lookback),

        "swing_distance": swing_distance(df, lookback),

        "distance_from_last_high": distance_from_last_high(df),
        "distance_from_last_low": distance_from_last_low(df)

    }
    # ==========================================================
# Smart Money - Part 1D
# Public Functions & Helpers
# ==========================================================


def safe_round(value, digits=2):
    """
    Safely round numeric values.
    """
    try:
        if value is None:
            return None
        return round(float(value), digits)
    except:
        return None


def format_structure(structure):

    if structure is None:
        return {}

    result = {}

    for key, value in structure.items():

        if isinstance(value, float):
            result[key] = safe_round(value)

        else:
            result[key] = value

    return result


def get_swing_structure(df):

    """
    Returns complete Swing Structure dictionary.

    Used by main.py

    """

    structure = build_market_structure(df)

    return format_structure(structure)


# ==========================================================
# Simple Validation
# ==========================================================

def validate_structure(df):

    try:

        data = get_swing_structure(df)

        return len(data) > 0

    except:

        return False


# ==========================================================
# Module Test
# ==========================================================

if __name__ == "__main__":

    print("Smart Money Part 1 Loaded Successfully.")
    # ==========================================================
# SMART MONEY - PART 2
# BOS (Break of Structure) & CHOCH (Change of Character)
# ICT-based Logic (Swing-based)
# ==========================================================


def _get_last_confirmed_swing_highs(df, lookback=200):
    data = df.tail(lookback)
    return find_swing_highs(data)


def _get_last_confirmed_swing_lows(df, lookback=200):
    data = df.tail(lookback)
    return find_swing_lows(data)


# ==========================================================
# BOS DETECTION (Bullish & Bearish)
# ==========================================================

def detect_bos(df, lookback=200):

    swings_high = _get_last_confirmed_swing_highs(df, lookback)
    swings_low = _get_last_confirmed_swing_lows(df, lookback)

    close = df["close"].iloc[-1]
    time = df.index[-1]

    bos = {
        "last_bullish_bos_level": None,
        "last_bearish_bos_level": None,
        "last_bullish_bos_time": None,
        "last_bearish_bos_time": None,
        "last_bos_candle": None,
        "distance_from_price": None
    }

    # --------------------------
    # Bullish BOS (break above swing high)
    # --------------------------
    for s in reversed(swings_high):

        if close > s["price"]:

            bos["last_bullish_bos_level"] = s["price"]
            bos["last_bullish_bos_time"] = str(s["time"])
            bos["last_bos_candle"] = str(time)
            bos["distance_from_price"] = close - s["price"]
            break

    # --------------------------
    # Bearish BOS (break below swing low)
    # --------------------------
    for s in reversed(swings_low):

        if close < s["price"]:

            bos["last_bearish_bos_level"] = s["price"]
            bos["last_bearish_bos_time"] = str(s["time"])
            bos["last_bos_candle"] = str(time)
            bos["distance_from_price"] = close - s["price"]
            break

    return bos


# ==========================================================
# CHOCH DETECTION (Trend Shift)
# ==========================================================

def detect_choch(df, lookback=200):

    swings_high = _get_last_confirmed_swing_highs(df, lookback)
    swings_low = _get_last_confirmed_swing_lows(df, lookback)

    close = df["close"].iloc[-1]
    time = df.index[-1]

    choch = {
        "last_bullish_choch_level": None,
        "last_bearish_choch_level": None,
        "last_bullish_choch_time": None,
        "last_bearish_choch_time": None,
        "last_choch_candle": None,
        "distance_from_price": None
    }

    # --------------------------
    # Bullish CHOCH (break structure after bearish)
    # --------------------------
    if len(swings_high) > 1:

        prev_high = swings_high[-2]["price"]

        if close > prev_high:

            choch["last_bullish_choch_level"] = prev_high
            choch["last_bullish_choch_time"] = str(swings_high[-2]["time"])
            choch["last_choch_candle"] = str(time)
            choch["distance_from_price"] = close - prev_high

    # --------------------------
    # Bearish CHOCH
    # --------------------------
    if len(swings_low) > 1:

        prev_low = swings_low[-2]["price"]

        if close < prev_low:

            choch["last_bearish_choch_level"] = prev_low
            choch["last_bearish_choch_time"] = str(swings_low[-2]["time"])
            choch["last_choch_candle"] = str(time)
            choch["distance_from_price"] = close - prev_low

    return choch


# ==========================================================
# STRUCTURE WRAPPER (MAIN EXPORT)
# ==========================================================

def get_structure_signals(df, lookback=200):

    bos = detect_bos(df, lookback)
    choch = detect_choch(df, lookback)

    return {
        "BOS": bos,
        "CHOCH": choch
        }
# ==========================================================
# SMART MONEY - PART 3
# Liquidity Engine (EQH / EQL / Sweeps / Pools)
# ==========================================================


def _round_price(p, precision=0.5):
    """
    Group prices into liquidity zones
    """
    try:
        return round(float(p) / precision) * precision
    except:
        return None


# ==========================================================
# Equal Highs & Equal Lows
# ==========================================================

def find_equal_highs(df, tolerance=0.2, lookback=200):

    data = df.tail(lookback)

    highs = data["high"].values

    eqh = []

    for i in range(len(highs)):
        for j in range(i+1, len(highs)):

            if abs(highs[i] - highs[j]) <= tolerance:
                eqh.append((float(highs[i]), float(highs[j])))

    return eqh


def find_equal_lows(df, tolerance=0.2, lookback=200):

    data = df.tail(lookback)

    lows = data["low"].values

    eql = []

    for i in range(len(lows)):
        for j in range(i+1, len(lows)):

            if abs(lows[i] - lows[j]) <= tolerance:
                eql.append((float(lows[i]), float(lows[j])))

    return eql


# ==========================================================
# Liquidity Pools
# ==========================================================

def get_liquidity_pools(df, lookback=200):

    eqh = find_equal_highs(df, lookback=lookback)
    eql = find_equal_lows(df, lookback=lookback)

    pools = {
        "buy_side_liquidity": [x[0] for x in eqh],
        "sell_side_liquidity": [x[0] for x in eql],
        "eqh_count": len(eqh),
        "eql_count": len(eql)
    }

    return pools


# ==========================================================
# Liquidity Sweep Detection
# ==========================================================

def detect_liquidity_sweeps(df, lookback=200):

    data = df.tail(lookback)

    sweeps = []

    for i in range(2, len(data)):

        prev_high = data["high"].iloc[i-1]
        prev_low = data["low"].iloc[i-1]

        current_high = data["high"].iloc[i]
        current_low = data["low"].iloc[i]

        close = data["close"].iloc[i]

        time = data.index[i]

        # --------------------------
        # Buy-side sweep (high broken then close below)
        # --------------------------
        if current_high > prev_high and close < prev_high:

            sweeps.append({
                "type": "buy_side_liquidity_sweep",
                "level": float(prev_high),
                "time": str(time),
                "size": float(current_high - prev_high),
                "distance": float(close - prev_high)
            })

        # --------------------------
        # Sell-side sweep (low broken then close above)
        # --------------------------
        if current_low < prev_low and close > prev_low:

            sweeps.append({
                "type": "sell_side_liquidity_sweep",
                "level": float(prev_low),
                "time": str(time),
                "size": float(prev_low - current_low),
                "distance": float(close - prev_low)
            })

    return sweeps


# ==========================================================
# Liquidity Summary (MAIN EXPORT)
# ==========================================================

def get_liquidity_data(df, lookback=200):

    pools = get_liquidity_pools(df, lookback)
    sweeps = detect_liquidity_sweeps(df, lookback)

    return {
        "buy_side_liquidity": pools["buy_side_liquidity"],
        "sell_side_liquidity": pools["sell_side_liquidity"],
        "equal_high_count": pools["eqh_count"],
        "equal_low_count": pools["eql_count"],
        "liquidity_sweeps": sweeps,
        "total_sweeps": len(sweeps)
    }
