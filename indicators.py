import pandas as pd
import numpy as np

# ==========================================================
# SMC INSTITUTIONAL ENGINE
# VERSION 3.0 PROFESSIONAL
# PART 1
# IMPORTS + HELPER FUNCTIONS
# ==========================================================


def last(series, default=0):
    try:
        return series.iloc[-1]
    except Exception:
        return default


def previous(series, default=0):
    try:
        return series.iloc[-2]
    except Exception:
        return default


def highest(series):
    try:
        return float(series.max())
    except Exception:
        return 0.0


def lowest(series):
    try:
        return float(series.min())
    except Exception:
        return 0.0


def average(series):
    try:
        return float(series.mean())
    except Exception:
        return 0.0


def safe_mode(series):
    try:
        m = series.mode()

        if len(m) > 0:
            return float(m.iloc[0])

    except Exception:
        pass

    return 0.0


def safe_round(value):

    try:

        if value is None:
            return 0

        if isinstance(
            value,
            (
                int,
                float,
                np.integer,
                np.floating
            )
        ):
            return round(float(value), 2)

        return value

    except Exception:
        return 0


def atr(df, period=14):

    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - df["close"].shift()).abs(),
            (df["low"] - df["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr.rolling(period).mean().fillna(0)


def body_size(df):

    return (df["close"] - df["open"]).abs()


def candle_range(df):

    return df["high"] - df["low"]


def upper_wick(df):

    return df["high"] - df[["open", "close"]].max(axis=1)


def lower_wick(df):

    return df[["open", "close"]].min(axis=1) - df["low"]


def midpoint(high, low):

    return (high + low) / 2
    
# ==========================================================
# PART 2
# PROFESSIONAL SWING STRUCTURE
# ICT FRACTAL ALGORITHM
# ==========================================================

def find_swings(df, lookback=3):

    highs = df["high"].reset_index(drop=True)
    lows = df["low"].reset_index(drop=True)

    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(df) - lookback):

        high = highs.iloc[i]

        if (
            all(high > highs.iloc[i - j] for j in range(1, lookback + 1))
            and
            all(high >= highs.iloc[i + j] for j in range(1, lookback + 1))
        ):
            swing_highs.append((i, float(high)))

        low = lows.iloc[i]

        if (
            all(low < lows.iloc[i - j] for j in range(1, lookback + 1))
            and
            all(low <= lows.iloc[i + j] for j in range(1, lookback + 1))
        ):
            swing_lows.append((i, float(low)))

    return swing_highs, swing_lows


def swing_levels(df):

    swing_highs, swing_lows = find_swings(df)

    if len(swing_highs):

        last_high = swing_highs[-1][1]
        high_index = swing_highs[-1][0]

    else:

        last_high = highest(df["high"])
        high_index = 0

    if len(swing_highs) >= 2:
        prev_high = swing_highs[-2][1]
    else:
        prev_high = last_high

    if len(swing_lows):

        last_low = swing_lows[-1][1]
        low_index = swing_lows[-1][0]

    else:

        last_low = lowest(df["low"])
        low_index = 0

    if len(swing_lows) >= 2:
        prev_low = swing_lows[-2][1]
    else:
        prev_low = last_low

    return {

        "last_high": safe_round(last_high),

        "last_low": safe_round(last_low),

        "prev_high": safe_round(prev_high),

        "prev_low": safe_round(prev_low),

        "highest": safe_round(highest(df["high"])),

        "lowest": safe_round(lowest(df["low"])),

        "high_count": len(swing_highs),

        "low_count": len(swing_lows),

        "distance": safe_round(last_high - last_low),

        "high_index": high_index,

        "low_index": low_index,

        "all_highs": swing_highs,

        "all_lows": swing_lows

    }
# ==========================================================
# PART 3
# PROFESSIONAL BREAK OF STRUCTURE (BOS)
# ==========================================================

def break_of_structure(df):

    swings = swing_levels(df)

    last_close = last(df["close"])

    last_high = swings["last_high"]
    last_low = swings["last_low"]

    prev_high = swings["prev_high"]
    prev_low = swings["prev_low"]

    bos_type = "NONE"
    bos_level = 0
    previous_level = 0

    if last_close > last_high:

        bos_type = "BULLISH"

        bos_level = last_high

        previous_level = prev_high

    elif last_close < last_low:

        bos_type = "BEARISH"

        bos_level = last_low

        previous_level = prev_low

    else:

        if abs(last_close - last_high) < abs(last_close - last_low):

            bos_type = "NEUTRAL"

            bos_level = last_high

            previous_level = prev_high

        else:

            bos_type = "NEUTRAL"

            bos_level = last_low

            previous_level = prev_low

    return {

        "type": bos_type,

        "last": safe_round(bos_level),

        "previous": safe_round(previous_level),

        "last_time": str(df.index[-1]),

        "previous_time": str(df.index[-2]) if len(df) > 1 else str(df.index[-1]),

        "candle": safe_round(last_close),

        "distance": safe_round(last_close - bos_level)

        }
# ==========================================================
# PART 4
# PROFESSIONAL CHANGE OF CHARACTER (CHOCH)
# ==========================================================

def change_of_character(df):

    swings = swing_levels(df)

    bos = break_of_structure(df)

    close = last(df["close"])

    choch_type = "NONE"

    choch_level = 0

    previous_level = 0

    if bos["type"] == "BULLISH":

        if close < swings["last_low"]:

            choch_type = "BEARISH"

            choch_level = swings["last_low"]

            previous_level = swings["prev_low"]

        else:

            choch_type = "NONE"

            choch_level = swings["last_high"]

            previous_level = swings["prev_high"]

    elif bos["type"] == "BEARISH":

        if close > swings["last_high"]:

            choch_type = "BULLISH"

            choch_level = swings["last_high"]

            previous_level = swings["prev_high"]

        else:

            choch_type = "NONE"

            choch_level = swings["last_low"]

            previous_level = swings["prev_low"]

    else:

        if abs(close - swings["last_high"]) < abs(close - swings["last_low"]):

            choch_level = swings["last_high"]

            previous_level = swings["prev_high"]

        else:

            choch_level = swings["last_low"]

            previous_level = swings["prev_low"]

    return {

        "type": choch_type,

        "last": safe_round(choch_level),

        "previous": safe_round(previous_level),

        "time": str(df.index[-1]),

        "candle": safe_round(close),

        "distance": safe_round(close - choch_level)

}
# ==========================================================
# PART 5
# PROFESSIONAL LIQUIDITY (ICT)
# ==========================================================

def liquidity(df, tolerance_ratio=0.15):

    swings = swing_levels(df)

    atr_value = atr(df).iloc[-1]

    tolerance = atr_value * tolerance_ratio

    swing_highs = swings["all_highs"]
    swing_lows = swings["all_lows"]

    equal_highs = []
    equal_lows = []

    # -------- Equal Highs --------

    for i in range(len(swing_highs)):

        for j in range(i + 1, len(swing_highs)):

            if abs(swing_highs[i][1] - swing_highs[j][1]) <= tolerance:

                equal_highs.append(

                    (swing_highs[i][1] + swing_highs[j][1]) / 2

                )

    # -------- Equal Lows --------

    for i in range(len(swing_lows)):

        for j in range(i + 1, len(swing_lows)):

            if abs(swing_lows[i][1] - swing_lows[j][1]) <= tolerance:

                equal_lows.append(

                    (swing_lows[i][1] + swing_lows[j][1]) / 2

                )

    buy_side = max(equal_highs) if len(equal_highs) else swings["last_high"]

    sell_side = min(equal_lows) if len(equal_lows) else swings["last_low"]

    highest_eq = max(equal_highs) if len(equal_highs) else 0

    lowest_eq = min(equal_lows) if len(equal_lows) else 0

    pool = abs(buy_side - sell_side)

    gap = abs(swings["last_high"] - swings["last_low"])

    return {

        "buy": safe_round(buy_side),

        "sell": safe_round(sell_side),

        "equal_high": safe_round(highest_eq),

        "equal_low": safe_round(lowest_eq),

        "eh_count": len(equal_highs),

        "el_count": len(equal_lows),

        "pool": safe_round(pool),

        "gap": safe_round(gap)

            }
# ==========================================================
# PART 6
# PROFESSIONAL LIQUIDITY SWEEP
# ICT LIQUIDITY GRAB
# ==========================================================

def liquidity_sweep(df):

    liq = liquidity(df)

    current_high = last(df["high"])
    current_low = last(df["low"])
    current_close = last(df["close"])

    buy_liq = liq["buy"]
    sell_liq = liq["sell"]

    sweep_type = "NONE"

    sweep_high = 0
    sweep_low = 0

    # ------------------------------
    # Buy Side Sweep
    # Wick above liquidity
    # Close back below liquidity
    # ------------------------------

    if current_high > buy_liq and current_close < buy_liq:

        sweep_type = "BUY_SIDE"

        sweep_high = current_high
        sweep_low = buy_liq

    # ------------------------------
    # Sell Side Sweep
    # Wick below liquidity
    # Close back above liquidity
    # ------------------------------

    elif current_low < sell_liq and current_close > sell_liq:

        sweep_type = "SELL_SIDE"

        sweep_high = sell_liq
        sweep_low = current_low

    else:

        sweep_high = current_high
        sweep_low = current_low

    return {

        "type": sweep_type,

        "high": safe_round(sweep_high),

        "low": safe_round(sweep_low),

        "candle": safe_round(current_close),

        "size": safe_round(abs(sweep_high - sweep_low)),

        "distance": safe_round(
            current_close -
            midpoint(sweep_high, sweep_low)
        )

    }
# ==========================================================
# PART 7
# PROFESSIONAL FAIR VALUE GAP (ICT)
# ==========================================================

def fair_value_gap(df):

    bullish_fvgs = []
    bearish_fvgs = []

    for i in range(2, len(df)):

        c1_high = df["high"].iloc[i - 2]
        c1_low = df["low"].iloc[i - 2]

        c3_high = df["high"].iloc[i]
        c3_low = df["low"].iloc[i]

        current_close = df["close"].iloc[-1]

        # ----------------------------
        # Bullish FVG
        # Candle1 High < Candle3 Low
        # ----------------------------

        if c1_high < c3_low:

            gap_low = c1_high
            gap_high = c3_low

            size = gap_high - gap_low

            fill = 0

            if current_close > gap_low:

                fill = min(
                    100,
                    ((current_close - gap_low) / size) * 100
                )

            bullish_fvgs.append({

                "high": gap_high,

                "low": gap_low,

                "size": size,

                "fill": fill

            })

        # ----------------------------
        # Bearish FVG
        # Candle1 Low > Candle3 High
        # ----------------------------

        if c1_low > c3_high:

            gap_high = c1_low
            gap_low = c3_high

            size = gap_high - gap_low

            fill = 0

            if current_close < gap_high:

                fill = min(
                    100,
                    ((gap_high - current_close) / size) * 100
                )

            bearish_fvgs.append({

                "high": gap_high,

                "low": gap_low,

                "size": size,

                "fill": fill

            })

    nearest_bull = bullish_fvgs[-1] if bullish_fvgs else None
    nearest_bear = bearish_fvgs[-1] if bearish_fvgs else None

    return {

        "bull_high": safe_round(nearest_bull["high"]) if nearest_bull else 0,

        "bull_low": safe_round(nearest_bull["low"]) if nearest_bull else 0,

        "bull_size": safe_round(nearest_bull["size"]) if nearest_bull else 0,

        "bull_fill": safe_round(nearest_bull["fill"]) if nearest_bull else 0,

        "bear_high": safe_round(nearest_bear["high"]) if nearest_bear else 0,

        "bear_low": safe_round(nearest_bear["low"]) if nearest_bear else 0,

        "bear_size": safe_round(nearest_bear["size"]) if nearest_bear else 0,

        "bear_fill": safe_round(nearest_bear["fill"]) if nearest_bear else 0,

        "bull_count": len(bullish_fvgs),

        "bear_count": len(bearish_fvgs)

        }
# ==========================================================
# PART 8
# PROFESSIONAL ORDER BLOCKS (ICT)
# ==========================================================

def order_blocks(df):

    bos = break_of_structure(df)

    bull_ob = None
    bear_ob = None

    # ----------------------------------------------------
    # Bullish Order Block
    # Last bearish candle before bullish BOS
    # ----------------------------------------------------

    if bos["type"] == "BULLISH":

        for i in range(len(df) - 2, 1, -1):

            if df["close"].iloc[i] < df["open"].iloc[i]:

                bull_ob = {

                    "high": df["high"].iloc[i],

                    "low": df["low"].iloc[i],

                    "age": len(df) - i

                }

                break

    # ----------------------------------------------------
    # Bearish Order Block
    # Last bullish candle before bearish BOS
    # ----------------------------------------------------

    elif bos["type"] == "BEARISH":

        for i in range(len(df) - 2, 1, -1):

            if df["close"].iloc[i] > df["open"].iloc[i]:

                bear_ob = {

                    "high": df["high"].iloc[i],

                    "low": df["low"].iloc[i],

                    "age": len(df) - i

                }

                break

    return {

        "bull_high": safe_round(
            bull_ob["high"]
        ) if bull_ob else 0,

        "bull_low": safe_round(
            bull_ob["low"]
        ) if bull_ob else 0,

        "bull_size": safe_round(
            bull_ob["high"] - bull_ob["low"]
        ) if bull_ob else 0,

        "bull_age": bull_ob["age"] if bull_ob else 0,

        "bear_high": safe_round(
            bear_ob["high"]
        ) if bear_ob else 0,

        "bear_low": safe_round(
            bear_ob["low"]
        ) if bear_ob else 0,

        "bear_size": safe_round(
            bear_ob["high"] - bear_ob["low"]
        ) if bear_ob else 0,

        "bear_age": bear_ob["age"] if bear_ob else 0

                   }
# ==========================================================
# PART 9
# PROFESSIONAL BREAKER / MITIGATION / REJECTION BLOCKS
# ==========================================================

def breaker_blocks(df):

    bos = break_of_structure(df)

    ob = order_blocks(df)

    close = last(df["close"])

    breaker = {

        "high": 0,

        "low": 0,

        "size": 0,

        "type": "NONE"

    }

    # Bullish Order Block broken to downside
    if (
        ob["bull_high"] > 0 and
        close < ob["bull_low"]
    ):

        breaker = {

            "high": ob["bull_high"],

            "low": ob["bull_low"],

            "size": ob["bull_size"],

            "type": "BEARISH"

        }

    # Bearish Order Block broken to upside
    elif (
        ob["bear_high"] > 0 and
        close > ob["bear_high"]
    ):

        breaker = {

            "high": ob["bear_high"],

            "low": ob["bear_low"],

            "size": ob["bear_size"],

            "type": "BULLISH"

        }

    return {

        "high": safe_round(breaker["high"]),

        "low": safe_round(breaker["low"]),

        "size": safe_round(breaker["size"]),

        "type": breaker["type"]

    }


# ==========================================================
# MITIGATION BLOCK
# ==========================================================

def mitigation_blocks(df):

    ob = order_blocks(df)

    close = last(df["close"])

    result = {

        "high": 0,

        "low": 0,

        "size": 0,

        "type": "NONE"

    }

    # Bullish mitigation

    if (
        ob["bull_low"] > 0 and
        ob["bull_low"] <= close <= ob["bull_high"]
    ):

        result = {

            "high": ob["bull_high"],

            "low": ob["bull_low"],

            "size": ob["bull_size"],

            "type": "BULLISH"

        }

    # Bearish mitigation

    elif (
        ob["bear_low"] > 0 and
        ob["bear_low"] <= close <= ob["bear_high"]
    ):

        result = {

            "high": ob["bear_high"],

            "low": ob["bear_low"],

            "size": ob["bear_size"],

            "type": "BEARISH"

        }

    return {

        "high": safe_round(result["high"]),

        "low": safe_round(result["low"]),

        "size": safe_round(result["size"]),

        "type": result["type"]

    }


# ==========================================================
# REJECTION BLOCK
# ==========================================================

def rejection_blocks(df):

    wick_up = upper_wick(df).iloc[-1]

    wick_down = lower_wick(df).iloc[-1]

    body = body_size(df).iloc[-1]

    rejection = {

        "high": 0,

        "low": 0,

        "type": "NONE"

    }

    # Strong bearish rejection

    if wick_up > body * 2:

        rejection = {

            "high": last(df["high"]),

            "low": last(df["low"]),

            "type": "BEARISH"

        }

    # Strong bullish rejection

    elif wick_down > body * 2:

        rejection = {

            "high": last(df["high"]),

            "low": last(df["low"]),

            "type": "BULLISH"

        }

    return {

        "high": safe_round(rejection["high"]),

        "low": safe_round(rejection["low"]),

        "type": rejection["type"]

    }
