"""
SMC INTEGRATION LAYER
Connects Smart Money Engine with Telegram Bot
"""

import pandas as pd
from smc_formatter import get_smc_summary


# =========================
# MAIN FUNCTION
# =========================

def build_smc_report(df):
    """
    Takes OHLC dataframe and returns structured SMC report dict
    """

    smc = get_smc_summary(df)

    report = {}

    # =========================
    # SWING STRUCTURE
    # =========================
    swing = smc.get("swing_structure", {})
    report["Swing Structure"] = {
        "Last Swing High": swing.get("last_swing_high"),
        "Last Swing Low": swing.get("last_swing_low"),
        "Previous Swing High": swing.get("previous_swing_high"),
        "Previous Swing Low": swing.get("previous_swing_low"),
        "Swing High Count": swing.get("swing_high_count"),
        "Swing Low Count": swing.get("swing_low_count"),
        "Highest Swing": swing.get("highest_swing"),
        "Lowest Swing": swing.get("lowest_swing"),
    }

    # =========================
    # BOS
    # =========================
    bos = smc.get("bos", {})
    report["BOS"] = {
        "Last BOS Level": bos.get("last_bos_level"),
        "Previous BOS Level": bos.get("previous_bos_level"),
        "Last BOS Time": bos.get("last_bos_time"),
        "Previous BOS Time": bos.get("previous_bos_time"),
    }

    # =========================
    # CHOCH
    # =========================
    choch = smc.get("choch", {})
    report["CHOCH"] = {
        "Last CHOCH Level": choch.get("last_choch_level"),
        "Previous CHOCH Level": choch.get("previous_choch_level"),
        "Last CHOCH Time": choch.get("last_choch_time"),
        "Previous CHOCH Time": choch.get("previous_choch_time"),
    }

    # =========================
    # LIQUIDITY
    # =========================
    liquidity = smc.get("liquidity", {})
    report["Liquidity"] = {
        "Buy Side Liquidity": liquidity.get("nearest_buy_liquidity"),
        "Sell Side Liquidity": liquidity.get("nearest_sell_liquidity"),
        "Equal High Count": liquidity.get("equal_high_count"),
        "Equal Low Count": liquidity.get("equal_low_count"),
    }

    # =========================
    # SWEEPS
    # =========================
    sweeps = smc.get("sweeps", {})
    report["Liquidity Sweeps"] = {
        "Last Sweep Type": sweeps.get("last_sweep_type"),
        "Last Sweep Level": sweeps.get("last_sweep_level"),
        "Last Sweep Time": sweeps.get("last_sweep_time"),
    }

    # =========================
    # FVG
    # =========================
    fvg = smc.get("fvg", {})
    report["FVG"] = {
        "Bullish FVG Count": fvg.get("bullish_fvg_count"),
        "Bearish FVG Count": fvg.get("bearish_fvg_count"),
        "Nearest Bullish FVG": fvg.get("nearest_bullish_fvg"),
        "Nearest Bearish FVG": fvg.get("nearest_bearish_fvg"),
    }

    # =========================
    # ORDER BLOCKS
    # =========================
    ob = smc.get("order_blocks", {})
    report["Order Blocks"] = {
        "Bullish OB Count": ob.get("bullish_ob_count"),
        "Bearish OB Count": ob.get("bearish_ob_count"),
        "Nearest Bullish OB": ob.get("nearest_bullish_ob"),
        "Nearest Bearish OB": ob.get("nearest_bearish_ob"),
    }

    # =========================
    # IMBALANCE
    # =========================
    imb = smc.get("imbalance", {})
    report["Imbalance"] = {
        "Gap Up Count": imb.get("gap_up_count"),
        "Gap Down Count": imb.get("gap_down_count"),
        "Last Gap Up": imb.get("last_gap_up"),
        "Last Gap Down": imb.get("last_gap_down"),
    }

    return report


# =========================
# TELEGRAM FORMAT HELP
# =========================

def format_smc_text(report):
    """
    Converts structured dict into Telegram readable text
    """

    text = "🏛 Institutional Market Data\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for section, values in report.items():
        text += f"{section}\n"

        for k, v in values.items():
            text += f"{k}: {v}\n"

        text += "\n━━━━━━━━━━━━━━━━━━━━━━\n\n"

    return text
