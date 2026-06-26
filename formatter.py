# smc_formatter.py

def format_output(data, symbol, timeframe):
    """
    ONLY formatting — no logic
    """

    return f"""
🏛 Institutional Market Data ({symbol.upper()} | {timeframe})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Swing Structure
Last Swing High: {data.get('last_swing_high')}
Last Swing Low: {data.get('last_swing_low')}
Previous Swing High: {data.get('prev_swing_high')}
Previous Swing Low: {data.get('prev_swing_low')}
Swing Distance: {data.get('swing_distance')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ Break Of Structure (BOS)
Last BOS Level: {data.get('bos_last')}
Previous BOS Level: {data.get('bos_prev')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ Change Of Character (CHOCH)
Last CHOCH Level: {data.get('choch_last')}
Previous CHOCH Level: {data.get('choch_prev')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ Liquidity
Buy Side: {data.get('buy_liq')}
Sell Side: {data.get('sell_liq')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(remaining sections will auto-fill from same pattern)
"""
