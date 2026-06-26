"""
SMC Institutional PSX Bot (STRICT FORMAT LOCK)
Commands:
/ffc_5m
/ffc_1h
/ogdc_4h
"""

import os
import asyncio
import logging
import nest_asyncio
import pandas as pd
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tvDatafeed import TvDatafeed, Interval

from indicators import *

nest_asyncio.apply()

BOT_TOKEN = os.environ.get("7809164972:AAEr1day076eHhJIOKZvUjCRnF29EZUOOXs")

logging.basicConfig(level=logging.INFO)

# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "SMC Bot Active"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# ---------------- TV ----------------
tv = TvDatafeed()

interval_map = {
    "5m": Interval.in_5_minute,
    "15m": Interval.in_15_minute,
    "30m": Interval.in_30_minute,
    "1h": Interval.in_1_hour,
    "4h": Interval.in_4_hour,
    "1d": Interval.in_daily,
    "1w": Interval.in_weekly,
    "1M": Interval.in_monthly
}

def parse_cmd(text):
    text = text.replace("/", "")
    parts = text.split("_")

    symbol = parts[0].upper()
    tf = parts[1] if len(parts) > 1 else "4h"

    if tf not in interval_map:
        tf = "4h"

    return symbol, tf

def get_data(symbol, tf):
    return tv.get_hist(
        symbol=symbol,
        exchange="PSX",
        interval=interval_map[tf],
        n_bars=500
    )

def v(x):
    if pd.isna(x):
        return "N/A"
    try:
        return round(float(x), 2)
    except:
        return "N/A"

# ---------------- FULL FORMAT ENGINE ----------------
def build_report(df, symbol, tf):

    data = smc_engine(df)

    last = df.iloc[-1]

    msg = f"""
🏛 Institutional Market Data
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Swing Structure

Last Swing High: {v(data['swing']['last_high'])}
Last Swing Low: {v(data['swing']['last_low'])}

Previous Swing High: {v(data['swing']['prev_high'])}
Previous Swing Low: {v(data['swing']['prev_low'])}

Swing High Count: {data['swing']['high_count']}
Swing Low Count: {data['swing']['low_count']}

Highest Swing: {v(data['swing']['highest'])}
Lowest Swing: {v(data['swing']['lowest'])}

Swing Distance: {v(data['swing']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ Break Of Structure (BOS)

Last BOS Level: {v(data['bos']['last_level'])}
Previous BOS Level: {v(data['bos']['prev_level'])}

Last BOS Time: {data['bos']['last_time']}
Previous BOS Time: {data['bos']['prev_time']}

Last BOS Candle: {data['bos']['last_candle']}

Distance From Current Price: {v(data['bos']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ Change Of Character (CHOCH)

Last CHOCH Level: {v(data['choch']['last_level'])}
Previous CHOCH Level: {v(data['choch']['prev_level'])}

Last CHOCH Time: {data['choch']['last_time']}
Last CHOCH Candle: {data['choch']['last_candle']}

Distance From Current Price: {v(data['choch']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ Liquidity

Nearest Buy Side Liquidity: {v(data['liq']['buy'])}
Nearest Sell Side Liquidity: {v(data['liq']['sell'])}

Highest Equal High: {v(data['liq']['eq_high'])}
Lowest Equal Low: {v(data['liq']['eq_low'])}

Equal High Count: {data['liq']['eq_high_count']}
Equal Low Count: {data['liq']['eq_low_count']}

Liquidity Pool Size: {v(data['liq']['pool'])}
Liquidity Gap: {v(data['liq']['gap'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ Liquidity Sweeps

Last High Sweep: {v(data['sweep']['high'])}
Last Low Sweep: {v(data['sweep']['low'])}

Sweep Candle: {data['sweep']['candle']}
Sweep Size: {v(data['sweep']['size'])}
Sweep Distance: {v(data['sweep']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ Fair Value Gaps (FVG)

Nearest Bullish FVG High: {v(data['fvg']['bull_high'])}
Nearest Bullish FVG Low: {v(data['fvg']['bull_low'])}
Bullish FVG Size: {v(data['fvg']['bull_size'])}
Bullish FVG Fill %: {v(data['fvg']['bull_fill'])}

Nearest Bearish FVG High: {v(data['fvg']['bear_high'])}
Nearest Bearish FVG Low: {v(data['fvg']['bear_low'])}
Bearish FVG Size: {v(data['fvg']['bear_size'])}
Bearish FVG Fill %: {v(data['fvg']['bear_fill'])}

Open Bullish FVG Count: {data['fvg']['bull_count']}
Open Bearish FVG Count: {data['fvg']['bear_count']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7️⃣ Order Blocks

Nearest Bullish OB High: {v(data['ob']['bull_high'])}
Nearest Bullish OB Low: {v(data['ob']['bull_low'])}
Bullish OB Size: {v(data['ob']['bull_size'])}
Bullish OB Age: {data['ob']['bull_age']}

Nearest Bearish OB High: {v(data['ob']['bear_high'])}
Nearest Bearish OB Low: {v(data['ob']['bear_low'])}
Bearish OB Size: {v(data['ob']['bear_size'])}
Bearish OB Age: {data['ob']['bear_age']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

8️⃣ Breaker Blocks
Breaker High: {v(data['breaker']['high'])}
Breaker Low: {v(data['breaker']['low'])}
Breaker Size: {v(data['breaker']['size'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

9️⃣ Mitigation Blocks
Mitigation High: {v(data['mitigation']['high'])}
Mitigation Low: {v(data['mitigation']['low'])}
Mitigation Size: {v(data['mitigation']['size'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔟 Rejection Blocks
Rejection High: {v(data['reject']['high'])}
Rejection Low: {v(data['reject']['low'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣1️⃣ Supply & Demand
Nearest Supply High: {v(data['sd']['supply_high'])}
Nearest Supply Low: {v(data['sd']['supply_low'])}
Supply Width: {v(data['sd']['supply_width'])}

Nearest Demand High: {v(data['sd']['demand_high'])}
Nearest Demand Low: {v(data['sd']['demand_low'])}
Demand Width: {v(data['sd']['demand_width'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣2️⃣ Premium Discount
Premium Zone High: {v(data['pd']['premium_high'])}
Premium Zone Low: {v(data['pd']['premium_low'])}
Equilibrium: {v(data['pd']['eq'])}
Discount Zone High: {v(data['pd']['discount_high'])}
Discount Zone Low: {v(data['pd']['discount_low'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣3️⃣ Market Imbalance
Largest Imbalance: {v(data['imb']['largest'])}
Nearest Imbalance: {v(data['imb']['nearest'])}
Open Imbalance Count: {data['imb']['open']}
Filled Imbalance Count: {data['imb']['filled']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣4️⃣ Volume Profile
POC: {v(data['vp']['poc'])}
VAH: {v(data['vp']['vah'])}
VAL: {v(data['vp']['val'])}
HVN: {v(data['vp']['hvn'])}
LVN: {v(data['vp']['lvn'])}
Profile Range: {v(data['vp']['range'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣5️⃣ Market Profile
POC: {v(data['mp']['poc'])}
TPO Count: {data['mp']['tpo']}
Initial Balance High: {v(data['mp']['ibh'])}
Initial Balance Low: {v(data['mp']['ibl'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣6️⃣ Wyckoff Raw Levels
Buying Climax: {v(data['wyckoff']['bc'])}
Automatic Rally: {v(data['wyckoff']['ar'])}
Secondary Test: {v(data['wyckoff']['st'])}
Spring: {v(data['wyckoff']['spring'])}
Upthrust: {v(data['wyckoff']['ut'])}
Last Point Of Support: {v(data['wyckoff']['lps'])}
Last Point Of Supply: {v(data['wyckoff']['lpsu'])}
Sign Of Strength: {v(data['wyckoff']['sos'])}
Sign Of Weakness: {v(data['wyckoff']['sow'])}
Backing Up: {v(data['wyckoff']['bu'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣7️⃣ Compression & Expansion
Compression Range: {v(data['vol']['compression'])}
Expansion Range: {v(data['vol']['expansion'])}
Average Expansion: {v(data['vol']['avg_exp'])}
Average Compression: {v(data['vol']['avg_comp'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣8️⃣ Volatility Expansion
Expansion ATR: {v(data['vola']['exp'])}
Compression ATR: {v(data['vola']['comp'])}
Range Ratio: {v(data['vola']['ratio'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣9️⃣ Volume Events
Highest Volume Price: {v(data['vole']['high'])}
Lowest Volume Price: {v(data['vole']['low'])}
Volume Spike: {v(data['vole']['spike'])}
Volume Dry-up: {v(data['vole']['dry'])}
Average Volume 50: {v(data['vole']['avg'])}
Relative Volume: {v(data['vole']['rel'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣0️⃣ Gaps
Gap Up: {v(data['gap']['up'])}
Gap Down: {v(data['gap']['down'])}
Gap Size: {v(data['gap']['size'])}
Gap Fill %: {v(data['gap']['fill'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣1️⃣ Fibonacci Extension
0.618: {v(data['fib']['0.618'])}
1.000: {v(data['fib']['1.0'])}
1.272: {v(data['fib']['1.272'])}
1.618: {v(data['fib']['1.618'])}
2.000: {v(data['fib']['2.0'])}
2.618: {v(data['fib']['2.618'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣2️⃣ Advanced Pivot
Classic Pivot: {v(data['pivot']['classic'])}
R1: {v(data['pivot']['r1'])}
R2: {v(data['pivot']['r2'])}
R3: {v(data['pivot']['r3'])}
S1: {v(data['pivot']['s1'])}
S2: {v(data['pivot']['s2'])}
S3: {v(data['pivot']['s3'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣3️⃣ Candle Pattern Values
Bullish Engulfing: {data['candle']['bull_engulf']}
Bearish Engulfing: {data['candle']['bear_engulf']}
Hammer: {data['candle']['hammer']}
Doji: {data['candle']['doji']}
Inside Bar: {data['candle']['inside']}
Outside Bar: {data['candle']['outside']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣4️⃣ Risk Levels
Nearest Invalid Level: {v(data['risk']['invalid'])}
Nearest Breakout Level: {v(data['risk']['breakout'])}
Nearest Breakdown Level: {v(data['risk']['breakdown'])}
ATR Stop Distance: {v(data['risk']['stop'])}
ATR Target Distance: {v(data['risk']['target'])}
"""

    return msg

# ---------------- HANDLER ----------------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol, tf = parse_cmd(update.message.text)

    df = await asyncio.to_thread(get_data, symbol, tf)

    if df is None or df.empty:
        await update.message.reply_text("No data")
        return

    msg = build_report(df, symbol, tf)
    await update.message.reply_text(msg)

# ---------------- MAIN ----------------
def main():
    import threading
    threading.Thread(target=run_flask).start()

    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # dynamic wildcard handler
    bot.add_handler(CommandHandler(None, handle))

    bot.run_polling()

if __name__ == "__main__":
    main()
