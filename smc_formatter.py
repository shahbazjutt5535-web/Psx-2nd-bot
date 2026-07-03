"""
SMC FORMATTER (PART 4 - FINAL)
Converts Smart Money raw engine data into structured output
NO SIGNALS - ONLY RAW STRUCTURED VALUES
"""

from smc_engine import *


# =========================
# 1. SWING STRUCTURE
# =========================

def format_swings(df):
    highs, lows = get_swings(df)

    return {
        "last_swing_high": highs[-1] if len(highs) > 0 else None,
        "last_swing_low": lows[-1] if len(lows) > 0 else None,

        "previous_swing_high": highs[-2] if len(highs) > 1 else None,
        "previous_swing_low": lows[-2] if len(lows) > 1 else None,

        "swing_high_count": len(highs),
        "swing_low_count": len(lows),

        "highest_swing": max([h[1] for h in highs]) if highs else None,
        "lowest_swing": min([l[1] for l in lows]) if lows else None,
    }


# =========================
# 2. BOS (Break of Structure)
# =========================

def format_bos(df):
    bos = get_bos(df)

    if not bos:
        return {}

    last = bos[-1]
    prev = bos[-2] if len(bos) > 1 else None

    return {
        "last_bos_level": last.get("level"),
        "last_bos_time": last.get("time"),

        "previous_bos_level": prev.get("level") if prev else None,
        "previous_bos_time": prev.get("time") if prev else None,
    }


# =========================
# 3. CHOCH
# =========================

def format_choch(df):
    choch = get_choch(df)

    if not choch:
        return {}

    last = choch[-1]
    prev = choch[-2] if len(choch) > 1 else None

    return {
        "last_choch_level": last.get("level"),
        "last_choch_time": last.get("time"),

        "previous_choch_level": prev.get("level") if prev else None,
        "previous_choch_time": prev.get("time") if prev else None,
    }


# =========================
# 4. LIQUIDITY
# =========================

def format_liquidity(df):
    eq_highs, eq_lows = get_liquidity(df)

    return {
        "nearest_buy_liquidity": eq_lows[-1] if eq_lows else None,
        "nearest_sell_liquidity": eq_highs[-1] if eq_highs else None,

        "equal_high_count": len(eq_highs),
        "equal_low_count": len(eq_lows),
    }


# =========================
# 5. LIQUIDITY SWEEPS
# =========================

def format_sweeps(df):
    sweeps = get_liquidity_sweeps(df)

    if not sweeps:
        return {}

    last = sweeps[-1]

    return {
        "last_sweep_type": last.get("type"),
        "last_sweep_level": last.get("level"),
        "last_sweep_time": last.get("time"),
    }


# =========================
# 6. FAIR VALUE GAPS (FVG)
# =========================

def format_fvg(df):
    fvg = get_fvg(df)

    bullish = [f for f in fvg if f["type"] == "bullish"]
    bearish = [f for f in fvg if f["type"] == "bearish"]

    return {
        "nearest_bullish_fvg": bullish[-1] if bullish else None,
        "nearest_bearish_fvg": bearish[-1] if bearish else None,

        "bullish_fvg_count": len(bullish),
        "bearish_fvg_count": len(bearish),
    }


# =========================
# 7. ORDER BLOCKS
# =========================

def format_order_blocks(df):
    ob = get_order_blocks(df)

    bullish = [x for x in ob if x["type"] == "bullish"]
    bearish = [x for x in ob if x["type"] == "bearish"]

    return {
        "nearest_bullish_ob": bullish[-1] if bullish else None,
        "nearest_bearish_ob": bearish[-1] if bearish else None,

        "bullish_ob_count": len(bullish),
        "bearish_ob_count": len(bearish),
    }


# =========================
# 8. IMBALANCE
# =========================

def format_imbalance(df):
    imbalance = get_imbalance(df)

    gap_up = [g for g in imbalance if g["type"] == "gap_up"]
    gap_down = [g for g in imbalance if g["type"] == "gap_down"]

    return {
        "gap_up_count": len(gap_up),
        "gap_down_count": len(gap_down),

        "last_gap_up": gap_up[-1] if gap_up else None,
        "last_gap_down": gap_down[-1] if gap_down else None,
    }

# =========================
# 8.5. VWAP SYSTEM (YEH BLOCK NAYA ADD HUA HAI)
# =========================
def format_vwap(df):
    from indicators import calculate_vwap_metrics
    try:
        return calculate_vwap_metrics(df)
    except Exception:
        return {}

# =========================
# 9. MASTER OUTPUT FUNCTION
# =========================
def get_smc_summary(df):
    return {
        "swing_structure": format_swings(df),
        "bos": format_bos(df),
        "choch": format_choch(df),
        "liquidity": format_liquidity(df),
        "sweeps": format_sweeps(df),
        "fvg": format_fvg(df),
        "order_blocks": format_order_blocks(df),
        "imbalance": format_imbalance(df),
        "vwap_system": format_vwap(df),  # <-- YEH LINE YAHAN LGA DI HAI
    }
