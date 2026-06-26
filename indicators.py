import pandas as pd
import numpy as np

# ---------------- CORE ----------------
def swing_levels(df):
    return {
        "last_high": df['high'].iloc[-1],
        "last_low": df['low'].iloc[-1],
        "prev_high": df['high'].iloc[-2],
        "prev_low": df['low'].iloc[-2],
        "highest": df['high'].max(),
        "lowest": df['low'].min(),
        "high_count": len(df[df['high'] > df['high'].mean()]),
        "low_count": len(df[df['low'] < df['low'].mean()]),
        "distance": df['high'].max() - df['low'].min()
    }

# ---------------- BOS / CHOCH ----------------
def break_of_structure(df):
    return {
        "last_level": df['high'].iloc[-1],
        "prev_level": df['high'].iloc[-2],
        "last_time": str(df.index[-1]),
        "prev_time": str(df.index[-2]),
        "last_candle": df['close'].iloc[-1],
        "distance": df['close'].iloc[-1] - df['close'].iloc[-2]
    }

def change_of_character(df):
    return {
        "last_level": df['low'].iloc[-1],
        "prev_level": df['low'].iloc[-2],
        "last_time": str(df.index[-1]),
        "last_candle": df['close'].iloc[-1],
        "distance": df['close'].iloc[-1] - df['close'].iloc[-2]
    }

# ---------------- LIQUIDITY ----------------
def liquidity(df):
    return {
        "buy": df['low'].rolling(10).min().iloc[-1],
        "sell": df['high'].rolling(10).max().iloc[-1],
        "eq_high": df['high'].mode()[0],
        "eq_low": df['low'].mode()[0],
        "eq_high_count": 2,
        "eq_low_count": 3,
        "pool": df['high'].max() - df['low'].min(),
        "gap": (df['high'].max() - df['low'].min()) * 0.1
    }

# ---------------- MAIN ENGINE ----------------
def smc_engine(df):

    return {
        "swing": swing_levels(df),
        "bos": break_of_structure(df),
        "choch": change_of_character(df),
        "liq": liquidity(df),

        "sweep": {"high": df['high'].max(), "low": df['low'].min(), "candle": df['close'].iloc[-1], "size": 0, "distance": 0},

        "fvg": {"bull_high": 0, "bull_low": 0, "bull_size": 0, "bull_fill": 0,
                "bear_high": 0, "bear_low": 0, "bear_size": 0, "bear_fill": 0,
                "bull_count": 0, "bear_count": 0},

        "ob": {"bull_high": 0, "bull_low": 0, "bull_size": 0, "bull_age": 0,
               "bear_high": 0, "bear_low": 0, "bear_size": 0, "bear_age": 0},

        "breaker": {"high": 0, "low": 0, "size": 0},
        "mitigation": {"high": 0, "low": 0, "size": 0},
        "reject": {"high": 0, "low": 0},

        "sd": {"supply_high": 0, "supply_low": 0, "supply_width": 0,
               "demand_high": 0, "demand_low": 0, "demand_width": 0},

        "pd": {"premium_high": 0, "premium_low": 0, "eq": 0,
               "discount_high": 0, "discount_low": 0},

        "imb": {"largest": 0, "nearest": 0, "open": 0, "filled": 0},

        "vp": {"poc": df['close'].mode()[0], "vah": df['high'].quantile(0.75),
               "val": df['low'].quantile(0.25), "hvn": 0, "lvn": 0, "range": df['high'].max()-df['low'].min()},

        "mp": {"poc": df['close'].mode()[0], "tpo": 0, "ibh": df['high'].iloc[-1], "ibl": df['low'].iloc[-1]},

        "wyckoff": {"bc": 0, "ar": 0, "st": 0, "spring": 0, "ut": 0,
                    "lps": 0, "lpsu": 0, "sos": 0, "sow": 0, "bu": 0},

        "vol": {"compression": 0, "expansion": 0, "avg_exp": 0, "avg_comp": 0},

        "vola": {"exp": 0, "comp": 0, "ratio": 0},

        "vole": {"high": 0, "low": 0, "spike": 0, "dry": 0, "avg": 0, "rel": 0},

        "gap": {"up": 0, "down": 0, "size": 0, "fill": 0},

        "fib": {"0.618": 0, "1.0": 0, "1.272": 0, "1.618": 0, "2.0": 0, "2.618": 0},

        "pivot": {"classic": 0, "r1": 0, "r2": 0, "r3": 0, "s1": 0, "s2": 0, "s3": 0},

        "candle": {"bull_engulf": 0, "bear_engulf": 0, "hammer": 0,
                   "doji": 0, "inside": 0, "outside": 0},

        "risk": {"invalid": 0, "breakout": 0, "breakdown": 0,
                 "stop": 0, "target": 0}
    }
