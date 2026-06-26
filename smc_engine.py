"""
SMC ENGINE (PART 3)
Raw Institutional / Smart Money Calculations
NO SIGNALS - ONLY VALUES
"""

import pandas as pd
import numpy as np

# -----------------------------
# 1. SWING STRUCTURE
# -----------------------------

def get_swings(df, lookback=3):
    highs = df['high']
    lows = df['low']

    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(df) - lookback):
        if highs[i] == max(highs[i-lookback:i+lookback]):
            swing_highs.append((i, highs[i]))

        if lows[i] == min(lows[i-lookback:i+lookback]):
            swing_lows.append((i, lows[i]))

    return swing_highs, swing_lows


# -----------------------------
# 2. BOS (Break of Structure)
# -----------------------------

def get_bos(df):
    swing_highs, swing_lows = get_swings(df)

    bos_levels = []

    for i in range(1, len(df)):
        close = df['close'].iloc[i]

        for idx, level in swing_highs:
            if i > idx and close > level:
                bos_levels.append({
                    "type": "bullish",
                    "level": level,
                    "time": df.index[i]
                })

        for idx, level in swing_lows:
            if i > idx and close < level:
                bos_levels.append({
                    "type": "bearish",
                    "level": level,
                    "time": df.index[i]
                })

    return bos_levels


# -----------------------------
# 3. CHOCH (Change of Character)
# -----------------------------

def get_choch(df):
    bos = get_bos(df)
    choch = []

    for i in range(1, len(bos)):
        if bos[i]['type'] != bos[i-1]['type']:
            choch.append({
                "level": bos[i]['level'],
                "time": bos[i]['time'],
                "type": bos[i]['type']
            })

    return choch


# -----------------------------
# 4. LIQUIDITY LEVELS
# -----------------------------

def get_liquidity(df):
    highs = df['high']
    lows = df['low']

    equal_highs = []
    equal_lows = []

    tolerance = 0.002  # 0.2%

    for i in range(1, len(df)):
        for j in range(i-5, i):
            if j < 0:
                continue

            if abs(highs[i] - highs[j]) / highs[j] < tolerance:
                equal_highs.append(highs[i])

            if abs(lows[i] - lows[j]) / lows[j] < tolerance:
                equal_lows.append(lows[i])

    return equal_highs, equal_lows


# -----------------------------
# 5. LIQUIDITY SWEEPS
# -----------------------------

def get_liquidity_sweeps(df):
    eq_highs, eq_lows = get_liquidity(df)

    sweeps = []

    for i in range(1, len(df)):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]

        for h in eq_highs:
            if high > h:
                sweeps.append({
                    "type": "high_sweep",
                    "level": h,
                    "time": df.index[i]
                })

        for l in eq_lows:
            if low < l:
                sweeps.append({
                    "type": "low_sweep",
                    "level": l,
                    "time": df.index[i]
                })

    return sweeps


# -----------------------------
# 6. FVG (Fair Value Gaps)
# -----------------------------

def get_fvg(df):
    fvg = []

    for i in range(2, len(df)):
        # Bullish FVG
        if df['low'].iloc[i] > df['high'].iloc[i-2]:
            fvg.append({
                "type": "bullish",
                "high": df['low'].iloc[i],
                "low": df['high'].iloc[i-2],
                "time": df.index[i]
            })

        # Bearish FVG
        if df['high'].iloc[i] < df['low'].iloc[i-2]:
            fvg.append({
                "type": "bearish",
                "high": df['low'].iloc[i-2],
                "low": df['high'].iloc[i],
                "time": df.index[i]
            })

    return fvg


# -----------------------------
# 7. ORDER BLOCKS (simple version)
# -----------------------------

def get_order_blocks(df):
    ob = []

    for i in range(2, len(df)):
        if df['close'].iloc[i] > df['open'].iloc[i] and df['close'].iloc[i-1] < df['open'].iloc[i-1]:
            ob.append({
                "type": "bullish",
                "high": df['high'].iloc[i-1],
                "low": df['low'].iloc[i-1],
                "time": df.index[i-1]
            })

        if df['close'].iloc[i] < df['open'].iloc[i] and df['close'].iloc[i-1] > df['open'].iloc[i-1]:
            ob.append({
                "type": "bearish",
                "high": df['high'].iloc[i-1],
                "low": df['low'].iloc[i-1],
                "time": df.index[i-1]
            })

    return ob


# -----------------------------
# 8. IMBALANCE
# -----------------------------

def get_imbalance(df):
    imbalances = []

    for i in range(1, len(df)):
        if df['high'].iloc[i-1] < df['low'].iloc[i]:
            imbalances.append({
                "type": "gap_up",
                "size": df['low'].iloc[i] - df['high'].iloc[i-1],
                "time": df.index[i]
            })

        if df['low'].iloc[i-1] > df['high'].iloc[i]:
            imbalances.append({
                "type": "gap_down",
                "size": df['low'].iloc[i-1] - df['high'].iloc[i]
            })

    return imbalances
