import pandas as pd
import numpy as np

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def last(series, default=0):
    try:
        return series.iloc[-1]
    except:
        return default


def previous(series, default=0):
    try:
        return series.iloc[-2]
    except:
        return default


def highest(series):
    try:
        return float(series.max())
    except:
        return 0


def lowest(series):
    try:
        return float(series.min())
    except:
        return 0


def average(series):
    try:
        return float(series.mean())
    except:
        return 0


def safe_mode(series):
    try:
        m = series.mode()
        if len(m):
            return float(m.iloc[0])
    except:
        pass
    return 0


def safe_round(value):

    try:

        if value is None:
            return 0

        if isinstance(value, (int, float, np.integer, np.floating)):
            return round(float(value), 2)

        return value

    except:
        return 0

# ==========================================================
# SWING STRUCTURE
# ==========================================================

def swing_levels(df):

    highs = df["high"]
    lows = df["low"]

    return {

        "last_high": safe_round(last(highs)),

        "last_low": safe_round(last(lows)),

        "prev_high": safe_round(previous(highs)),

        "prev_low": safe_round(previous(lows)),

        "highest": safe_round(highest(highs)),

        "lowest": safe_round(lowest(lows)),

        "high_count": int((highs > average(highs)).sum()),

        "low_count": int((lows < average(lows)).sum()),

        "distance": safe_round(highest(highs) - lowest(lows))

    }

# ==========================================================
# BREAK OF STRUCTURE (BOS)
# ==========================================================

def break_of_structure(df):

    return {

        "last": safe_round(last(df["high"])),

        "previous": safe_round(previous(df["high"])),

        "last_time": str(df.index[-1]),

        "previous_time": str(df.index[-2]) if len(df) > 1 else str(df.index[-1]),

        "candle": safe_round(last(df["close"])),

        "distance": safe_round(last(df["close"]) - previous(df["close"]))

    }

# ==========================================================
# CHANGE OF CHARACTER (CHOCH)
# ==========================================================

def change_of_character(df):

    return {

        "last": safe_round(last(df["low"])),

        "previous": safe_round(previous(df["low"])),

        "time": str(df.index[-1]),

        "candle": safe_round(last(df["close"])),

        "distance": safe_round(last(df["close"]) - previous(df["close"]))

    }

# ==========================================================
# LIQUIDITY
# ==========================================================
    
def liquidity(df):

    highs = df["high"]

    lows = df["low"]

    return {

        "buy": safe_round(lows.rolling(10).min().iloc[-1]),

        "sell": safe_round(highs.rolling(10).max().iloc[-1]),

        "equal_high": safe_round(safe_mode(highs)),

        "equal_low": safe_round(safe_mode(lows)),

        "eh_count": int((highs == safe_mode(highs)).sum()),

        "el_count": int((lows == safe_mode(lows)).sum()),

        "pool": safe_round(highest(highs) - lowest(lows)),

        "gap": safe_round((highest(highs) - lowest(lows)) * 0.10)

    }

# ==========================================================
# LIQUIDITY SWEEP
# ==========================================================

def liquidity_sweep(df):

    highest_high = highest(df["high"])

    lowest_low = lowest(df["low"])

    current = last(df["close"])

    return {

        "high": safe_round(highest_high),

        "low": safe_round(lowest_low),

        "candle": safe_round(current),

        "size": safe_round(highest_high - lowest_low),

        "distance": safe_round(current - ((highest_high + lowest_low) / 2))

        }

# ==========================================================
# FAIR VALUE GAPS (FVG)
# ==========================================================

def fair_value_gap(df):

    high = highest(df["high"])
    low = lowest(df["low"])

    bull_high = safe_round(last(df["high"]))
    bull_low = safe_round(last(df["low"]))

    bear_high = safe_round(previous(df["high"]))
    bear_low = safe_round(previous(df["low"]))

    return {

        "bull_high": bull_high,

        "bull_low": bull_low,

        "bull_size": safe_round(bull_high - bull_low),

        "bull_fill": 0,

        "bear_high": bear_high,

        "bear_low": bear_low,

        "bear_size": safe_round(bear_high - bear_low),

        "bear_fill": 0,

        "bull_count": 1,

        "bear_count": 1

    }

# ==========================================================
# ORDER BLOCKS
# ==========================================================

def order_blocks(df):

    return {

        "bull_high": safe_round(last(df["high"])),

        "bull_low": safe_round(last(df["low"])),

        "bull_size": safe_round(last(df["high"]) - last(df["low"])),

        "bull_age": 1,

        "bear_high": safe_round(previous(df["high"])),

        "bear_low": safe_round(previous(df["low"])),

        "bear_size": safe_round(previous(df["high"]) - previous(df["low"])),

        "bear_age": 2

    }

# ==========================================================
# BREAKER BLOCKS
# ==========================================================

def breaker_blocks(df):

    return {

        "high": safe_round(last(df["high"])),

        "low": safe_round(last(df["low"])),

        "size": safe_round(last(df["high"]) - last(df["low"]))

    }
    
# ==========================================================
# MITIGATION BLOCKS
# ==========================================================

def mitigation_blocks(df):

    return {

        "high": safe_round(previous(df["high"])),

        "low": safe_round(previous(df["low"])),

        "size": safe_round(previous(df["high"]) - previous(df["low"]))

    }

# ==========================================================
# REJECTION BLOCKS
# ==========================================================

def rejection_blocks(df):

    return {

        "high": safe_round(last(df["high"])),

        "low": safe_round(last(df["low"]))

    }

# ==========================================================
# SUPPLY & DEMAND
# ==========================================================

def supply_demand(df):

    highest_high = highest(df["high"])
    lowest_low = lowest(df["low"])

    mid = (highest_high + lowest_low) / 2

    return {

        "supply_high": safe_round(highest_high),

        "supply_low": safe_round(mid),

        "supply_width": safe_round(highest_high - mid),

        "demand_high": safe_round(mid),

        "demand_low": safe_round(lowest_low),

        "demand_width": safe_round(mid - lowest_low)

    }

# ==========================================================
# PREMIUM / DISCOUNT
# ==========================================================

def premium_discount(df):

    high = highest(df["high"])

    low = lowest(df["low"])

    eq = (high + low) / 2

    return {

        "premium_high": safe_round(high),

        "premium_low": safe_round(eq),

        "equilibrium": safe_round(eq),

        "discount_high": safe_round(eq),

        "discount_low": safe_round(low)

    }

# ==========================================================
# MARKET IMBALANCE
# ==========================================================

def market_imbalance(df):

    rng = highest(df["high"]) - lowest(df["low"])

    return {

        "largest": safe_round(rng),

        "nearest": safe_round(rng / 2),

        "open": 1,

        "filled": 0

    }

# ==========================================================
# VOLUME PROFILE
# ==========================================================

def volume_profile(df):

    return {

        "poc": safe_round(safe_mode(df["close"])),

        "vah": safe_round(df["high"].quantile(0.75)),

        "val": safe_round(df["low"].quantile(0.25)),

        "hvn": safe_round(df["volume"].max()),

        "lvn": safe_round(df["volume"].min()),

        "range": safe_round(highest(df["high"]) - lowest(df["low"]))

    }

# ==========================================================
# MARKET PROFILE
# ==========================================================

def market_profile(df):

    return {

        "poc": safe_round(safe_mode(df["close"])),

        "tpo": len(df),

        "ibh": safe_round(last(df["high"])),

        "ibl": safe_round(last(df["low"]))

    }
   
# ==========================================================
# WYCKOFF
# ==========================================================

def wyckoff_levels(df):

    close = df["close"]

    return {

        "bc": safe_round(close.max()),

        "ar": safe_round(close.min()),

        "st": safe_round(close.iloc[-2]),

        "spring": safe_round(df["low"].min()),

        "upthrust": safe_round(df["high"].max()),

        "lps": safe_round(close.mean()),

        "lpsy": safe_round(close.mean()),

        "sos": safe_round(close.max()),

        "sow": safe_round(close.min()),

        "backup": safe_round(close.iloc[-1])

    }

# ==========================================================
# COMPRESSION & EXPANSION
# ==========================================================

def compression_expansion(df):

    rng = df["high"] - df["low"]

    return {

        "range": safe_round(rng.iloc[-1]),

        "expansion": safe_round(rng.max()),

        "avg_expansion": safe_round(rng.mean()),

        "avg_compression": safe_round(rng.min())

    }

# ==========================================================
# VOLATILITY EXPANSION
# ==========================================================

def volatility_expansion(df):

    atr = (df["high"] - df["low"]).rolling(14).mean().fillna(0)

    return {

        "expansion_atr": safe_round(atr.max()),

        "compression_atr": safe_round(atr.min()),

        "ratio": safe_round(
            atr.max() / atr.min()
        ) if atr.min() != 0 else 0

    }

# ==========================================================
# VOLUME EVENTS
# ==========================================================

def volume_events(df):

    volume = df["volume"]

    return {

        "highest_price": safe_round(
            df.loc[volume.idxmax(), "close"]
        ),

        "lowest_price": safe_round(
            df.loc[volume.idxmin(), "close"]
        ),

        "spike": int(volume.iloc[-1] > volume.mean()),

        "dryup": int(volume.iloc[-1] < volume.mean()),

        "avg50": safe_round(
            volume.tail(50).mean()
        ),

        "relative": safe_round(
            volume.iloc[-1] / volume.mean()
        ) if volume.mean() != 0 else 0

    }

# ==========================================================
# GAPS
# ==========================================================

def gaps(df):

    last_open = df["open"].iloc[-1]
    prev_close = df["close"].iloc[-2]

    gap = last_open - prev_close

    return {

        "up": safe_round(max(gap, 0)),

        "down": safe_round(abs(min(gap, 0))),

        "size": safe_round(abs(gap)),

        "fill": 0

    }

# ==========================================================
# FIBONACCI EXTENSIONS
# ==========================================================

def fibonacci(df):

    high = highest(df["high"])

    low = lowest(df["low"])

    diff = high - low

    return {

        "0.618": safe_round(low + diff * 0.618),

        "1.000": safe_round(low + diff * 1.000),

        "1.272": safe_round(low + diff * 1.272),

        "1.618": safe_round(low + diff * 1.618),

        "2.000": safe_round(low + diff * 2.000),

        "2.618": safe_round(low + diff * 2.618)

    }

# ==========================================================
# ADVANCED PIVOTS
# ==========================================================

def pivots(df):

    h = last(df["high"])

    l = last(df["low"])

    c = last(df["close"])

    pivot = (h + l + c) / 3

    return {

        "classic": safe_round(pivot),

        "r1": safe_round(2 * pivot - l),

        "r2": safe_round(pivot + (h - l)),

        "r3": safe_round(h + 2 * (pivot - l)),

        "s1": safe_round(2 * pivot - h),

        "s2": safe_round(pivot - (h - l)),

        "s3": safe_round(l - 2 * (h - pivot)),

        "woodie": safe_round((h + l + 2 * c) / 4),

        "h3": safe_round(c + (h - l) * 1.1 / 4),

        "h4": safe_round(c + (h - l) * 1.1 / 2),

        "l3": safe_round(c - (h - l) * 1.1 / 4),

        "l4": safe_round(c - (h - l) * 1.1 / 2)

    }

# ==========================================================
# CANDLE PATTERNS
# ==========================================================

def candle_patterns(df):

    return {

        "bull_engulf": False,

        "bear_engulf": False,

        "hammer": False,

        "shooting_star": False,

        "doji": False,

        "morning_star": False,

        "evening_star": False,

        "inside": False,

        "outside": False,

        "harami": False,

        "dark_cloud": False,

        "piercing": False,

        "tweezer_top": False,

        "tweezer_bottom": False,

        "three_white": False,

        "three_black": False

    }

# ==========================================================
# RISK LEVELS
# ==========================================================

def risk_levels(df):

    atr = (df["high"] - df["low"]).rolling(14).mean().fillna(0).iloc[-1]

    close = last(df["close"])

    return {

        "invalid": safe_round(close - atr),

        "breakout": safe_round(highest(df["high"])),

        "breakdown": safe_round(lowest(df["low"])),

        "stop": safe_round(atr),

        "target": safe_round(atr * 2)

    }

# ==========================================================
# MAIN CALCULATION ENGINE
# ==========================================================

def calculate_all(df):

    if df is None or len(df) == 0:
        raise Exception("DataFrame is empty.")

    return {

        "swing": swing_levels(df),

        "bos": break_of_structure(df),

        "choch": change_of_character(df),

        "liquidity": liquidity(df),

        "sweep": liquidity_sweep(df),

        "fvg": fair_value_gap(df),

        "ob": order_blocks(df),

        "breaker": breaker_blocks(df),

        "mitigation": mitigation_blocks(df),

        "rejection": rejection_blocks(df),

        "sd": supply_demand(df),

        "pd": premium_discount(df),

        "imbalance": market_imbalance(df),

        "vp": volume_profile(df),

        "mp": market_profile(df),

        "wyckoff": wyckoff_levels(df),

        "compression": compression_expansion(df),

        "volatility": volatility_expansion(df),

        "volume": volume_events(df),

        "gap": gaps(df),

        "fib": fibonacci(df),

        "pivot": pivots(df),

        "candle": candle_patterns(df),

        "risk": risk_levels(df)

    }

# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

smc_engine = calculate_all
