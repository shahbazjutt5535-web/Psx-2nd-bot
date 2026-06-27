import pandas as pd
import numpy as np

# ==========================================================
# SMC INSTITUTIONAL ENGINE
# VERSION 3.0 PROFESSIONAL - PRODUCTION READY
# PART 1: IMPORTS + HELPER FUNCTIONS
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
        if value is None or np.isnan(value) or np.isinf(value):
            return 0.0
        if isinstance(value, (int, float, np.integer, np.floating)):
            return round(float(value), 2)
        return value
    except Exception:
        return 0.0


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
# PART 2: PROFESSIONAL SWING STRUCTURE (ICT FRACTAL)
# ==========================================================

def find_swings(df, lookback=3):
    highs = df["high"].reset_index(drop=True)
    lows = df["low"].reset_index(drop=True)

    swing_highs = []
    swing_lows = []

    # Vector lookback to avoid infinite runtime
    for i in range(lookback, len(df) - lookback):
        high = highs.iloc[i]
        if (
            all(high > highs.iloc[i - j] for j in range(1, lookback + 1))
            and all(high >= highs.iloc[i + j] for j in range(1, lookback + 1))
        ):
            swing_highs.append((i, float(high)))

        low = lows.iloc[i]
        if (
            all(low < lows.iloc[i - j] for j in range(1, lookback + 1))
            and all(low <= lows.iloc[i + j] for j in range(1, lookback + 1))
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

    prev_high = swing_highs[-2][1] if len(swing_highs) >= 2 else last_high

    if len(swing_lows):
        last_low = swing_lows[-1][1]
        low_index = swing_lows[-1][0]
    else:
        last_low = lowest(df["low"])
        low_index = 0

    prev_low = swing_lows[-2][1] if len(swing_lows) >= 2 else last_low

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
# PART 3: BREAK OF STRUCTURE (BOS)
# ==========================================================

def break_of_structure(df):
    swings = swing_levels(df)
    last_close = last(df["close"])

    last_high = swings["last_high"]
    last_low = swings["last_low"]
    prev_high = swings["prev_high"]
    prev_low = swings["prev_low"]

    bos_type = "NONE"
    bos_level = 0.0
    previous_level = 0.0

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
# PART 4: CHANGE OF CHARACTER (CHOCH)
# ==========================================================

def change_of_character(df):
    swings = swing_levels(df)
    bos = break_of_structure(df)
    close = last(df["close"])

    choch_type = "NONE"
    choch_level = 0.0
    previous_level = 0.0

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
# PART 5: PROFESSIONAL LIQUIDITY (ICT)
# ==========================================================

def liquidity(df, tolerance_ratio=0.15):
    swings = swing_levels(df)
    atr_series = atr(df)
    atr_value = atr_series.iloc[-1] if not atr_series.empty else 0.0
    tolerance = atr_value * tolerance_ratio

    swing_highs = swings["all_highs"][-20:] # Optimized Lookback tail limit to stop freezing
    swing_lows = swings["all_lows"][-20:]

    equal_highs = []
    equal_lows = []

    for i in range(len(swing_highs)):
        for j in range(i + 1, len(swing_highs)):
            if abs(swing_highs[i][1] - swing_highs[j][1]) <= tolerance:
                equal_highs.append((swing_highs[i][1] + swing_highs[j][1]) / 2)

    for i in range(len(swing_lows)):
        for j in range(i + 1, len(swing_lows)):
            if abs(swing_lows[i][1] - swing_lows[j][1]) <= tolerance:
                equal_lows.append((swing_lows[i][1] + swing_lows[j][1]) / 2)

    buy_side = max(equal_highs) if len(equal_highs) else swings["last_high"]
    sell_side = min(equal_lows) if len(equal_lows) else swings["last_low"]

    highest_eq = max(equal_highs) if len(equal_highs) else 0.0
    lowest_eq = min(equal_lows) if len(equal_lows) else 0.0

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
# PART 6: LIQUIDITY SWEEP
# ==========================================================

def liquidity_sweep(df):
    liq = liquidity(df)

    current_high = last(df["high"])
    current_low = last(df["low"])
    current_close = last(df["close"])

    buy_liq = liq["buy"]
    sell_liq = liq["sell"]

    sweep_type = "NONE"
    sweep_high = 0.0
    sweep_low = 0.0

    if current_high > buy_liq and current_close < buy_liq:
        sweep_type = "BUY_SIDE"
        sweep_high = current_high
        sweep_low = buy_liq
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
        "distance": safe_round(current_close - midpoint(sweep_high, sweep_low))
    }


# ==========================================================
# PART 7: FAIR VALUE GAP (ICT)
# ==========================================================

def fair_value_gap(df):
    bullish_fvgs = []
    bearish_fvgs = []
    
    # Process only last 50 candles to prevent heavy trace loops
    start_idx = max(2, len(df) - 50)

    for i in range(start_idx, len(df)):
        c1_high = df["high"].iloc[i - 2]
        c1_low = df["low"].iloc[i - 2]
        c3_high = df["high"].iloc[i]
        c3_low = df["low"].iloc[i]

        current_close = df["close"].iloc[-1]

        if c1_high < c3_low:
            gap_low = c1_high
            gap_high = c3_low
            size = gap_high - gap_low
            fill = 0.0
            if current_close > gap_low:
                fill = min(100.0, ((current_close - gap_low) / size) * 100)
            bullish_fvgs.append({"high": gap_high, "low": gap_low, "size": size, "fill": fill})

        if c1_low > c3_high:
            gap_high = c1_low
            gap_low = c3_high
            size = gap_high - gap_low
            fill = 0.0
            if current_close < gap_high:
                fill = min(100.0, ((gap_high - current_close) / size) * 100)
            bearish_fvgs.append({"high": gap_high, "low": gap_low, "size": size, "fill": fill})

    nearest_bull = bullish_fvgs[-1] if bullish_fvgs else None
    nearest_bear = bearish_fvgs[-1] if bearish_fvgs else None

    return {
        "bull_high": safe_round(nearest_bull["high"]) if nearest_bull else 0.0,
        "bull_low": safe_round(nearest_bull["low"]) if nearest_bull else 0.0,
        "bull_size": safe_round(nearest_bull["size"]) if nearest_bull else 0.0,
        "bull_fill": safe_round(nearest_bull["fill"]) if nearest_bull else 0.0,
        "bear_high": safe_round(nearest_bear["high"]) if nearest_bear else 0.0,
        "bear_low": safe_round(nearest_bear["low"]) if nearest_bear else 0.0,
        "bear_size": safe_round(nearest_bear["size"]) if nearest_bear else 0.0,
        "bear_fill": safe_round(nearest_bear["fill"]) if nearest_bear else 0.0,
        "bull_count": len(bullish_fvgs),
        "bear_count": len(bearish_fvgs)
    }


# ==========================================================
# PART 8: ORDER BLOCKS (ICT)
# ==========================================================

def order_blocks(df):
    bos = break_of_structure(df)
    bull_ob = None
    bear_ob = None

    if bos["type"] == "BULLISH":
        for i in range(len(df) - 2, max(1, len(df) - 50), -1):
            if df["close"].iloc[i] < df["open"].iloc[i]:
                bull_ob = {"high": df["high"].iloc[i], "low": df["low"].iloc[i], "age": len(df) - i}
                break

    elif bos["type"] == "BEARISH":
        for i in range(len(df) - 2, max(1, len(df) - 50), -1):
            if df["close"].iloc[i] > df["open"].iloc[i]:
                bear_ob = {"high": df["high"].iloc[i], "low": df["low"].iloc[i], "age": len(df) - i}
                break

    return {
        "bull_high": safe_round(bull_ob["high"]) if bull_ob else 0.0,
        "bull_low": safe_round(bull_ob["low"]) if bull_ob else 0.0,
        "bull_size": safe_round(bull_ob["high"] - bull_ob["low"]) if bull_ob else 0.0,
        "bull_age": bull_ob["age"] if bull_ob else 0,
        "bear_high": safe_round(bear_ob["high"]) if bear_ob else 0.0,
        "bear_low": safe_round(bear_ob["low"]) if bear_ob else 0.0,
        "bear_size": safe_round(bear_ob["high"] - bear_ob["low"]) if bear_ob else 0.0,
        "bear_age": bear_ob["age"] if bear_ob else 0
    }


# ==========================================================
# PART 9: BREAKER / MITIGATION / REJECTION BLOCKS
# ==========================================================

def breaker_blocks(df):
    ob = order_blocks(df)
    close = last(df["close"])

    result = {"type": "NONE", "high": 0.0, "low": 0.0, "size": 0.0}

    if ob["bull_high"] > 0 and close < ob["bull_low"]:
        result = {"type": "BEARISH", "high": ob["bull_high"], "low": ob["bull_low"], "size": ob["bull_size"]}
    elif ob["bear_high"] > 0 and close > ob["bear_high"]:
        result = {"type": "BULLISH", "high": ob["bear_high"], "low": ob["bear_low"], "size": ob["bear_size"]}

    return {
        "type": result["type"],
        "high": safe_round(result["high"]),
        "low": safe_round(result["low"]),
        "size": safe_round(result["size"])
    }


def mitigation_blocks(df):
    ob = order_blocks(df)
    close = last(df["close"])

    result = {"type": "NONE", "high": 0.0, "low": 0.0, "size": 0.0}

    if ob["bull_high"] > 0 and ob["bull_low"] <= close <= ob["bull_high"]:
        result = {"type": "BULLISH", "high": ob["bull_high"], "low": ob["bull_low"], "size": ob["bull_size"]}
    elif ob["bear_high"] > 0 and ob["bear_low"] <= close <= ob["bear_high"]:
        result = {"type": "BEARISH", "high": ob["bear_high"], "low": ob["bear_low"], "size": ob["bear_size"]}

    return {
        "type": result["type"],
        "high": safe_round(result["high"]),
        "low": safe_round(result["low"]),
        "size": safe_round(result["size"])
    }


def rejection_blocks(df):
    body = body_size(df).iloc[-1]
    upper = upper_wick(df).iloc[-1]
    lower = lower_wick(df).iloc[-1]
    high = last(df["high"])
    low = last(df["low"])

    rtype = "NONE"
    if upper >= body * 2 and upper > lower:
        rtype = "BEARISH"
    elif lower >= body * 2 and lower > upper:
        rtype = "BULLISH"

    return {
        "type": rtype,
        "high": safe_round(high),
        "low": safe_round(low),
        "size": safe_round(high - low)
    }
    

# ==========================================================
# PART 10: SUPPLY / DEMAND & IMBALANCE
# ==========================================================

def supply_demand(df):
    swings = swing_levels(df)
    supply_high = swings["last_high"]
    supply_low = previous(df["high"])
    demand_high = previous(df["low"])
    demand_low = swings["last_low"]

    return {
        "supply_high": safe_round(max(supply_high, supply_low)),
        "supply_low": safe_round(min(supply_high, supply_low)),
        "supply_width": safe_round(abs(supply_high - supply_low)),
        "demand_high": safe_round(max(demand_high, demand_low)),
        "demand_low": safe_round(min(demand_high, demand_low)),
        "demand_width": safe_round(abs(demand_high - demand_low))
    }


def premium_discount(df):
    high = highest(df["high"])
    low = lowest(df["low"])
    eq = midpoint(high, low)

    return {
        "premium_high": safe_round(high),
        "premium_low": safe_round(eq),
        "equilibrium": safe_round(eq),
        "discount_high": safe_round(eq),
        "discount_low": safe_round(low)
    }


def market_imbalance(df):
    gaps = []
    atr_series = atr(df)
    
    # Safe rolling range lookback
    for i in range(max(1, len(df) - 50), len(df)):
        gap = abs(df["open"].iloc[i] - df["close"].iloc[i - 1])
        if gap > atr_series.iloc[i] * 0.25:
            gaps.append(gap)

    largest = max(gaps) if gaps else 0.0
    nearest = gaps[-1] if gaps else 0.0

    return {
        "largest": safe_round(largest),
        "nearest": safe_round(nearest),
        "open_count": len(gaps),
        "filled_count": 0
    }


# ==========================================================
# PART 11: VOLUME & MARKET PROFILE
# ==========================================================

def volume_profile(df, bins=24):
    low = lowest(df["low"])
    high = highest(df["high"])

    if high <= low:
        return {"poc": 0.0, "vah": 0.0, "val": 0.0, "hvn": 0.0, "lvn": 0.0, "range": 0.0}

    prices = np.linspace(low, high, bins + 1)
    volume_bins = np.zeros(bins)
    typical = (df["high"] + df["low"] + df["close"]) / 3

    for price, volume in zip(typical, df["volume"]):
        idx = np.searchsorted(prices, price) - 1
        idx = max(0, min(idx, bins - 1))
        volume_bins[idx] += volume

    poc_index = int(np.argmax(volume_bins))
    lvn_index = int(np.argmin(volume_bins))
    poc = (prices[poc_index] + prices[poc_index + 1]) / 2

    total_volume = volume_bins.sum()
    if total_volume == 0:
        return {"poc": safe_round(poc), "vah": high, "val": low, "hvn": safe_round(poc), "lvn": low, "range": safe_round(high - low)}

    sorted_index = np.argsort(volume_bins)[::-1]
    used = []
    cumulative = 0

    for i in sorted_index:
        cumulative += volume_bins[i]
        used.append(i)
        if cumulative >= total_volume * 0.70:
            break

    vah = prices[max(used) + 1] if used else high
    val = prices[min(used)] if used else low

    return {
        "poc": safe_round(poc),
        "vah": safe_round(vah),
        "val": safe_round(val),
        "hvn": safe_round((prices[poc_index] + prices[poc_index + 1]) / 2),
        "lvn": safe_round((prices[lvn_index] + prices[lvn_index + 1]) / 2),
        "range": safe_round(high - low)
    }


def market_profile(df):
    vp = volume_profile(df)
    first = df.iloc[:30] if len(df) >= 30 else df
    ib_high = highest(first["high"])
    ib_low = lowest(first["low"])

    return {
        "poc": vp["poc"],
        "tpo": len(df),
        "ibh": safe_round(ib_high),
        "ibl": safe_round(ib_low)
    }


# ==========================================================
# PART 12: WYCKOFF & COMPRESSION ENGINE
# ==========================================================

def wyckoff_levels(df):
    high = highest(df["high"])
    low = lowest(df["low"])
    close = last(df["close"])
    volume = last(df["volume"])
    avg_volume = average(df["volume"].tail(20))

    buying_climax = high
    automatic_rally = low + (high - low) * 0.25
    secondary_test = low + (high - low) * 0.50
    spring = low
    upthrust = high
    lps = low + (high - low) * 0.35
    lpsy = high - (high - low) * 0.35
    sos = high if volume > avg_volume else close
    sow = low if volume > avg_volume else close

    return {
        "buying_climax": safe_round(buying_climax),
        "automatic_rally": safe_round(automatic_rally),
        "secondary_test": safe_round(secondary_test),
        "spring": safe_round(spring),
        "upthrust": safe_round(upthrust),
        "lps": safe_round(lps),
        "lpsy": safe_round(lpsy),
        "sos": safe_round(sos),
        "sow": safe_round(sow),
        "backup": safe_round(close)
    }


def compression_expansion(df):
    ranges = candle_range(df)
    avg = average(ranges.tail(20))
    current = last(ranges)

    compression = current < avg * 0.70
    expansion = current > avg * 1.50

    return {
        "compression": safe_round(current if compression else 0.0),
        "expansion": safe_round(current if expansion else 0.0),
        "avg_expansion": safe_round(avg),
        "avg_compression": safe_round(avg * 0.70)
    }


def volatility_expansion(df):
    atr_series = atr(df)
    current = last(atr_series)
    previous_atr = previous(atr_series)
    ratio = current / previous_atr if previous_atr > 0 else 0.0

    return {
        "expansion_atr": safe_round(current),
        "compression_atr": safe_round(previous_atr),
        "ratio": safe_round(ratio)
    }
    

# ==========================================================
# PART 13: VOLUME EVENTS, GAPS & FIBONACCI
# ==========================================================

def volume_events(df):
    current_volume = last(df["volume"])
    avg50 = average(df["volume"].tail(50))

    highest_volume_price = df.loc[df["volume"].idxmax(), "close"] if not df["volume"].empty else 0.0
    lowest_volume_price = df.loc[df["volume"].idxmin(), "close"] if not df["volume"].empty else 0.0

    relative = current_volume / avg50 if avg50 > 0 else 0.0
    spike = bool(current_volume > avg50 * 2)
    dryup = bool(current_volume < avg50 * 0.5)

    return {
        "highest_price": safe_round(highest_volume_price),
        "lowest_price": safe_round(lowest_volume_price),
        "spike": spike,
        "dryup": dryup,
        "average50": safe_round(avg50),
        "relative": safe_round(relative)
    }


def gaps(df):
    if len(df) < 2:
        return {"gap_up": 0.0, "gap_down": 0.0, "size": 0.0, "fill": 0.0}

    prev_close = previous(df["close"])
    today_open = last(df["open"])
    gap = today_open - prev_close

    gap_up = gap if gap > 0 else 0.0
    gap_down = abs(gap) if gap < 0 else 0.0
    fill = 0.0

    if gap_up > 0:
        fill = min(100.0, max(0.0, (today_open - last(df["low"])) / gap_up * 100))
    elif gap_down > 0:
        fill = min(100.0, max(0.0, (last(df["high"]) - today_open) / gap_down * 100))

    return {
        "gap_up": safe_round(gap_up),
        "gap_down": safe_round(gap_down),
        "size": safe_round(abs(gap)),
        "fill": safe_round(fill)
    }


def fibonacci(df):
    high = highest(df["high"])
    low = lowest(df["low"])
    diff = high - low

    return {
        "0.236": safe_round(high - diff * 0.236),
        "0.382": safe_round(high - diff * 0.382),
        "0.500": safe_round(high - diff * 0.500),
        "0.618": safe_round(high - diff * 0.618),
        "0.786": safe_round(high - diff * 0.786),
        "1.000": safe_round(high),
        "1.272": safe_round(high + diff * 0.272),
        "1.618": safe_round(high + diff * 0.618),
        "2.000": safe_round(high + diff)
    }


def pivots(df):
    high = previous(df["high"])
    low = previous(df["low"])
    close = previous(df["close"])

    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2 * (pivot - low)
    s3 = low - 2 * (high - pivot)

    return {
        "pivot": safe_round(pivot),
        "r1": safe_round(r1),
        "r2": safe_round(r2),
        "r3": safe_round(r3),
        "s1": safe_round(s1),
        "s2": safe_round(s2),
        "s3": safe_round(s3)
    }


# ==========================================================
# PART 14: CANDLE PATTERNS & RISK ENGINE
# ==========================================================

def candle_patterns(df):
    if len(df) < 2:
        return {"bull_engulf": False, "bear_engulf": False, "hammer": False, "shooting_star": False, "doji": False, "inside": False, "outside": False}

    o = df["open"]
    h = df["high"]
    l = df["low"]
    c = df["close"]

    body = abs(c.iloc[-1] - o.iloc[-1])
    rng = h.iloc[-1] - l.iloc[-1]

    bull_engulf = bool(c.iloc[-2] < o.iloc[-2] and c.iloc[-1] > o.iloc[-1] and c.iloc[-1] >= o.iloc[-2] and o.iloc[-1] <= c.iloc[-2])
    bear_engulf = bool(c.iloc[-2] > o.iloc[-2] and c.iloc[-1] < o.iloc[-1] and o.iloc[-1] >= c.iloc[-2] and c.iloc[-1] <= o.iloc[-2])
    hammer = bool(lower_wick(df).iloc[-1] > body * 2 and upper_wick(df).iloc[-1] < body)
    shooting = bool(upper_wick(df).iloc[-1] > body * 2 and lower_wick(df).iloc[-1] < body)
    doji = bool(body <= rng * 0.10 if rng > 0 else True)
    inside = bool(h.iloc[-1] < h.iloc[-2] and l.iloc[-1] > l.iloc[-2])
    outside = bool(h.iloc[-1] > h.iloc[-2] and l.iloc[-1] < l.iloc[-2])

    return {
        "bull_engulf": bull_engulf,
        "bear_engulf": bear_engulf,
        "hammer": hammer,
        "shooting_star": shooting,
        "doji": doji,
        "inside": inside,
        "outside": outside
    }


def risk_levels(df):
    atr_val = atr(df)
    atr_value = last(atr_val) if not atr_val.empty else 0.0
    close = last(df["close"])
    swing = swing_levels(df)

    stop_buy = swing["last_low"] - atr_value
    stop_sell = swing["last_high"] + atr_value
    target_buy = close + atr_value * 2
    target_sell = close - atr_value * 2

    return {
        "atr": safe_round(atr_value),
        "buy_stop": safe_round(stop_buy),
        "sell_stop": safe_round(stop_sell),
        "buy_target": safe_round(target_buy),
        "sell_target": safe_round(target_sell),
        "risk_reward": 2.0
    }


# ==========================================================
# MAIN CALCULATION ENGINE
# ==========================================================

def calculate_all(df):
    if df is None or len(df) < 50:
        raise ValueError("Institutional Engine require at least 50 historical candle vectors.")

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

# BACKWARD COMPATIBILITY
smc_engine = calculate_all
