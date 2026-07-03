# formatter.py

def format_output(data, symbol, timeframe):
    """
    ONLY formatting — no logic
    """
    # Main object se vwap_system data nikalna
    vwap = data.get('vwap_system', {})
    tf_lower = str(timeframe).lower()
    
    # Fallback checking agar data nested framework (jaise imbalance/smc_summary) se aa raha ho
    if not vwap and isinstance(data.get('imbalance'), dict):
        vwap = data.get('imbalance', {}).get('vwap_system', {})

    def fmt_row(m):
        """Helper to print VWAP metrics cleanly"""
        if not m or not isinstance(m, dict): 
            return "Data Unavailable"
        return f"{m.get('val', 0.0)} | Dist: {m.get('dist', 0.0)} | {m.get('pos', 'N/A')} | {m.get('dir', 'Flat')} | Cross: {m.get('cross', 'No')}"

    # Requested timeframe ka data nikalna (agar na mile toh session vwap fallback)
    target_vwap = vwap.get(tf_lower) if tf_lower in vwap else vwap.get('session')

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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ VWAP System ({timeframe.upper()})
Requested Timeframe VWAP:
↳ {timeframe.upper()} VWAP: {fmt_row(target_vwap)}

Anchored VWAP Levels:
• Anchored VWAP Swing High: {vwap.get('avwap_sh', {}).get('val', '-')} | Dist: {vwap.get('avwap_sh', {}).get('dist', '-')} | {vwap.get('avwap_sh', {}).get('pos', '-')}
• Anchored VWAP Swing Low: {vwap.get('avwap_sl', {}).get('val', '-')} | Dist: {vwap.get('avwap_sl', {}).get('dist', '-')} | {vwap.get('avwap_sl', {}).get('pos', '-')}
• Anchored VWAP Latest BOS: {vwap.get('avwap_bos', {}).get('val', '-')} | Dist: {vwap.get('avwap_bos', {}).get('dist', '-')} | {vwap.get('avwap_bos', {}).get('pos', '-')}
• Anchored VWAP Latest CHOCH: {vwap.get('avwap_choch', {}).get('val', '-')} | Dist: {vwap.get('avwap_choch', {}).get('dist', '-')} | {vwap.get('avwap_choch', {}).get('pos', '-')}
• Anchored VWAP Latest Breakout: {vwap.get('avwap_breakout', {}).get('val', '-')} | Dist: {vwap.get('avwap_breakout', {}).get('dist', '-')} | {vwap.get('avwap_breakout', {}).get('pos', '-')}

VWAP Analytics:
• VWAP Confluence: {vwap.get('confluence', 'N/A')}
• Strongest Support VWAP: {vwap.get('strongest_support', 'N/A')}
• Strongest Resistance VWAP: {vwap.get('strongest_resistance', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
