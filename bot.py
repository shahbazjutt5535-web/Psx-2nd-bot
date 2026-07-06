"""
SMC Institutional PSX Telegram Bot
Version 2.0
Render Ready
"""

import os
import re
import time
import asyncio
import logging
import threading
from datetime import datetime

import nest_asyncio
import pandas as pd
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN

from tv_data import get_data
from indicators import calculate_all

nest_asyncio.apply()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# Flask (Render Port)
# ----------------------------------------------------

web = Flask(__name__)

@web.route("/")
def home():
    return "SMC Institutional PSX Bot Running"


def run_flask():
    web.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


# ----------------------------------------------------
# Ping
# ----------------------------------------------------

BOT_START = time.time()


# ----------------------------------------------------
# Supported Timeframes
# ----------------------------------------------------

TIMEFRAMES = {
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "1w": "1w",
    "1m": "1m",
}


# ----------------------------------------------------
# Supported Symbols
# ----------------------------------------------------

SYMBOLS = {

    "FFC": ("FFC", "PSX"),
    "ENGRO": ("ENGRO", "PSX"),
    "OGDC": ("OGDC", "PSX"),
    "PPL": ("PPL", "PSX"),
    "PSO": ("PSO", "PSX"),
    "SYS": ("SYS", "PSX"),
    "LUCK": ("LUCK", "PSX"),
    "HUBC": ("HUBC", "PSX"),
    "NBP": ("NBP", "PSX"),
    "UBL": ("UBL", "PSX"),
    "KEL": ("KEL", "PSX"),
    "BOP": ("BOP", "PSX"),

    "MARI": ("MARI", "PSX"),
    "EFERT": ("EFERT", "PSX"),
    "TRG": ("TRG", "PSX"),
    "FCCL": ("FCCL", "PSX"),
    "HBL": ("HBL", "PSX"),
    "MCB": ("MCB", "PSX"),
    "BAHL": ("BAHL", "PSX"),
    "DGKC": ("DGKC", "PSX"),
    "PIOC": ("PIOC", "PSX"),
    "POL": ("POL", "PSX"),
    "APL": ("APL", "PSX"),
    "SNGP": ("SNGP", "PSX"),
    "SSGC": ("SSGC", "PSX"),
    "UNITY": ("UNITY", "PSX"),
    "AIRLINK": ("AIRLINK", "PSX"),
    "ILP": ("ILP", "PSX"),
    "SEARL": ("SEARL", "PSX"),
    "GGL": ("GGL", "PSX"),
    "NML": ("NML", "PSX"),
    "FABL": ("FABL", "PSX"),
    "MEBL": ("MEBL", "PSX"),
    "FFBL": ("FFBL", "PSX"),
    "CHCC": ("CHCC", "PSX"),
    "GHGL": ("GHGL", "PSX"),
    "KOHC": ("KOHC", "PSX"),
    "MLCF": ("MLCF", "PSX"),
    "KTML": ("KTML", "PSX"),
    "INDU": ("INDU", "PSX"),
    "THALL": ("THALL", "PSX"),
    "PAEL": ("PAEL", "PSX"),
    "AVN": ("AVN", "PSX"),
    "TPLP": ("TPLP", "PSX"),
    "GATM": ("GATM", "PSX"),
    "ANL": ("ANL", "PSX"),
    "HCAR": ("HCAR", "PSX"),
    "AGP": ("AGP", "PSX"),
    "ISL": ("ISL", "PSX"),
    "ASTL": ("ASTL", "PSX"),
    "MUGHAL": ("MUGHAL", "PSX"),

    "MZNPETF": ("MZNPETF", "PSX"),
    "NBPGETF": ("NBPGETF", "PSX"),

    # ================= FOREX =================

    "USDPKR": ("USDPKR", "FX_IDC"),

    # ================= INDICES =================

    "DXY": ("DXY", "TVC"),
    "UKOIL": ("UKOIL", "TVC"),

    # ================= CRYPTO =================

    "LINK": ("LINKUSDT", "BINANCE"),
    "ETH": ("ETHUSDT", "BINANCE"),
    "TRX": ("TRXUSDT", "BINANCE")

}

# ----------------------------------------------------
# Command Parser
# ----------------------------------------------------

def parse_command(command: str):

    command = command.replace("/", "").upper()

    if "_" not in command:
        raise Exception("Invalid command")

    symbol, tf = command.split("_", 1)

    if symbol not in SYMBOLS:
        raise Exception("Unsupported Symbol")

    if tf.lower() not in TIMEFRAMES:
        raise Exception("Unsupported Timeframe")

    tv_symbol, exchange = SYMBOLS[symbol]

    return tv_symbol, exchange, tf.lower()
    
# ----------------------------------------------------
# START COMMAND
# ----------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ping = round((time.time() - BOT_START) * 1000)

    msg = f"""
✅ Your PSX Bot is working!

Status : Online

Ping Response Time : {ping} ms

━━━━━━━━━━━━━━━━━━━━

Supported Timeframes

5m
15m
30m
1h
4h
1d
1w
1m

━━━━━━━━━━━━━━━━━━━━

Example Commands

/ffc_5m
/ffc_15m
/ffc_30m
/ffc_1h
/ffc_4h
/ffc_1d
/ffc_1w
/ffc_1m

/ogdc_1h
/engro_4h
/ppl_1d
/sys_5m

━━━━━━━━━━━━━━━━━━━━

Institutional Market Data Ready
"""

    await update.message.reply_text(msg)


# ----------------------------------------------------
# HELP COMMAND
# ----------------------------------------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
"""
Command Format

/symbol_timeframe

Examples

/ffc_5m
/ffc_15m
/ffc_30m
/ffc_1h
/ffc_4h
/ffc_1d
/ffc_1w
/ffc_1m

/ogdc_1h
/ppl_4h
/sys_1d
/luck_5m
"""
)


# ----------------------------------------------------
# MAIN COMMAND HANDLER
# ----------------------------------------------------

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        symbol, exchange, timeframe = parse_command(update.message.text)

    except Exception as e:

        await update.message.reply_text(
            "❌ Invalid command.\n\nExample:\n/ffc_1h"
        )
        return

    await update.message.reply_text(
        f"""⏳ {symbol} {timeframe} data is processing...

Please wait...
"""
    )

    try:

     df = await asyncio.to_thread(
    get_data,
    symbol,
    exchange,
    timeframe
)

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            f"❌ Error fetching {symbol} {timeframe} data from TradingView."
        )

        return

    if df is None:

        await update.message.reply_text(
            f"❌ Error fetching {symbol} {timeframe} data from TradingView."
        )

        return

    if len(df) == 0:

        await update.message.reply_text(
            f"❌ No candles received for {symbol} {timeframe}."
        )

        return

    try:

        smc_data = calculate_all(df)

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            "❌ Error calculating Smart Money indicators."
        )

        return

    try:

        report = build_report(
            smc_data,
            symbol,
            timeframe
        )

    except Exception as e:

        logger.exception(e)

        await update.message.reply_text(
            "❌ Error building report."
        )

        return

    if len(report) > 4096:

        for i in range(0, len(report), 4000):
            await update.message.reply_text(
                report[i:i+4000]
            )

    else:

        await update.message.reply_text(report)

# ----------------------------------------------------
# REPORT BUILDER
# PART 4 (SECTION 1 → SECTION 8)
# ----------------------------------------------------

def v(x):
    if x is None:
        return "-"
    try:
        return round(float(x), 2)
    except:
        return x


def build_report(data, symbol, timeframe):

    msg = f"""
🏛 Institutional Market Data

Symbol : {symbol}
TimeFrame : {timeframe.upper()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Swing Structure

Last Swing High: {v(data['swing']['last_high'])}
Last Swing Low: {v(data['swing']['last_low'])}

Previous Swing High: {v(data['swing']['prev_high'])}
Previous Swing Low: {v(data['swing']['prev_low'])}

Swing High Count: {v(data['swing']['high_count'])}
Swing Low Count: {v(data['swing']['low_count'])}

Highest Swing: {v(data['swing']['highest'])}
Lowest Swing: {v(data['swing']['lowest'])}

Swing Distance: {v(data['swing']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ Break Of Structure (BOS)

Last BOS Level: {v(data['bos']['last'])}
Previous BOS Level: {v(data['bos']['previous'])}

Last BOS Time: {data['bos']['last_time']}
Previous BOS Time: {data['bos']['previous_time']}

Last BOS Candle: {data['bos']['candle']}

Distance From Current Price: {v(data['bos']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ Change Of Character (CHOCH)

Last CHOCH Level: {v(data['choch']['last'])}
Previous CHOCH Level: {v(data['choch']['previous'])}

Last CHOCH Time: {data['choch']['time']}
Last CHOCH Candle: {data['choch']['candle']}

Distance From Current Price: {v(data['choch']['distance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ Liquidity

Nearest Buy Side Liquidity: {v(data['liquidity']['buy'])}

Nearest Sell Side Liquidity: {v(data['liquidity']['sell'])}

Highest Equal High: {v(data['liquidity']['equal_high'])}

Lowest Equal Low: {v(data['liquidity']['equal_low'])}

Equal High Count: {v(data['liquidity']['eh_count'])}

Equal Low Count: {v(data['liquidity']['el_count'])}

Liquidity Pool Size: {v(data['liquidity']['pool'])}

Liquidity Gap: {v(data['liquidity']['gap'])}

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

Open Bullish FVG Count: {v(data['fvg']['bull_count'])}

Open Bearish FVG Count: {v(data['fvg']['bear_count'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7️⃣ Order Blocks

Nearest Bullish OB High: {v(data['ob']['bull_high'])}

Nearest Bullish OB Low: {v(data['ob']['bull_low'])}

Bullish OB Size: {v(data['ob']['bull_size'])}

Bullish OB Age: {v(data['ob']['bull_age'])}

Nearest Bearish OB High: {v(data['ob']['bear_high'])}

Nearest Bearish OB Low: {v(data['ob']['bear_low'])}

Bearish OB Size: {v(data['ob']['bear_size'])}

Bearish OB Age: {v(data['ob']['bear_age'])}

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

Rejection High: {v(data['rejection']['high'])}

Rejection Low: {v(data['rejection']['low'])}

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

Equilibrium: {v(data['pd']['equilibrium'])}

Discount Zone High: {v(data['pd']['discount_high'])}

Discount Zone Low: {v(data['pd']['discount_low'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣3️⃣ Market Imbalance

Largest Imbalance: {v(data['imbalance']['largest'])}

Nearest Imbalance: {v(data['imbalance']['nearest'])}

Open Imbalance Count: {v(data['imbalance']['open'])}

Filled Imbalance Count: {v(data['imbalance']['filled'])}

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

TPO Count: {v(data['mp']['tpo'])}

Initial Balance High: {v(data['mp']['ibh'])}

Initial Balance Low: {v(data['mp']['ibl'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣6️⃣ Wyckoff Raw Levels

Buying Climax: {v(data['wyckoff']['bc'])}

Automatic Rally: {v(data['wyckoff']['ar'])}

Secondary Test: {v(data['wyckoff']['st'])}

Spring: {v(data['wyckoff']['spring'])}

Upthrust: {v(data['wyckoff']['upthrust'])}

Last Point Of Support: {v(data['wyckoff']['lps'])}

Last Point Of Supply: {v(data['wyckoff']['lpsy'])}

Sign Of Strength: {v(data['wyckoff']['sos'])}

Sign Of Weakness: {v(data['wyckoff']['sow'])}

Backing Up: {v(data['wyckoff']['backup'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣7️⃣ Compression & Expansion

Compression Range: {v(data['compression']['range'])}

Expansion Range: {v(data['compression']['expansion'])}

Average Expansion: {v(data['compression']['avg_expansion'])}

Average Compression: {v(data['compression']['avg_compression'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣8️⃣ Volatility Expansion

Expansion ATR: {v(data['volatility']['expansion_atr'])}

Compression ATR: {v(data['volatility']['compression_atr'])}

Range Ratio: {v(data['volatility']['ratio'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣9️⃣ Volume Events

Highest Volume Price: {v(data['volume']['highest_price'])}

Lowest Volume Price: {v(data['volume']['lowest_price'])}

Volume Spike: {v(data['volume']['spike'])}

Volume Dry-up: {v(data['volume']['dryup'])}

Average Volume 50: {v(data['volume']['avg50'])}

Relative Volume: {v(data['volume']['relative'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣0️⃣ Gaps

Gap Up: {v(data['gap']['up'])}

Gap Down: {v(data['gap']['down'])}

Gap Size: {v(data['gap']['size'])}

Gap Fill %: {v(data['gap']['fill'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣1️⃣ Fibonacci Extension

0.618: {v(data['fib']['0.618'])}

1.000: {v(data['fib']['1.000'])}

1.272: {v(data['fib']['1.272'])}

1.618: {v(data['fib']['1.618'])}

2.000: {v(data['fib']['2.000'])}

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

Woodie Pivot: {v(data['pivot']['woodie'])}

Camarilla H3: {v(data['pivot']['h3'])}

Camarilla H4: {v(data['pivot']['h4'])}

Camarilla L3: {v(data['pivot']['l3'])}

Camarilla L4: {v(data['pivot']['l4'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣3️⃣ Candle Pattern Values

Bullish Engulfing: {data['candle']['bull_engulf']}

Bearish Engulfing: {data['candle']['bear_engulf']}

Hammer: {data['candle']['hammer']}

Shooting Star: {data['candle']['shooting_star']}

Doji: {data['candle']['doji']}

Morning Star: {data['candle']['morning_star']}

Evening Star: {data['candle']['evening_star']}

Inside Bar: {data['candle']['inside']}

Outside Bar: {data['candle']['outside']}

Harami: {data['candle']['harami']}

Dark Cloud Cover: {data['candle']['dark_cloud']}

Piercing Line: {data['candle']['piercing']}

Tweezer Top: {data['candle']['tweezer_top']}

Tweezer Bottom: {data['candle']['tweezer_bottom']}

Three White Soldiers: {data['candle']['three_white']}

Three Black Crows: {data['candle']['three_black']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣4️⃣ Risk Levels

Nearest Invalid Level: {v(data['risk']['invalid'])}

Nearest Breakout Level: {v(data['risk']['breakout'])}

Nearest Breakdown Level: {v(data['risk']['breakdown'])}

ATR Stop Distance: {v(data['risk']['stop'])}

ATR Target Distance: {v(data['risk']['target'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣5️⃣ VWAP System ({timeframe.upper()})

Requested Timeframe VWAP:
↳ {timeframe.upper()} VWAP: {v(data['vwap_system'][timeframe]['val']) if timeframe in data['vwap_system'] else v(data['vwap_system']['session']['val'])} | Dist: {v(data['vwap_system'][timeframe]['dist']) if timeframe in data['vwap_system'] else v(data['vwap_system']['session']['dist'])} | {data['vwap_system'][timeframe]['pos'] if timeframe in data['vwap_system'] else data['vwap_system']['session']['pos']} | {data['vwap_system'][timeframe]['dir'] if timeframe in data['vwap_system'] else data['vwap_system']['session']['dir']} | Cross: {data['vwap_system'][timeframe]['cross'] if timeframe in data['vwap_system'] else data['vwap_system']['session']['cross']}

Anchored VWAP Levels:
• Anchored VWAP Swing High: {v(data['vwap_system']['avwap_sh']['val'])} | Dist: {v(data['vwap_system']['avwap_sh']['dist'])} | {data['vwap_system']['avwap_sh']['pos']}
• Anchored VWAP Swing Low: {v(data['vwap_system']['avwap_sl']['val'])} | Dist: {v(data['vwap_system']['avwap_sl']['dist'])} | {data['vwap_system']['avwap_sl']['pos']}
• Anchored VWAP Latest BOS: {v(data['vwap_system']['avwap_bos']['val'])} | Dist: {v(data['vwap_system']['avwap_bos']['dist'])} | {data['vwap_system']['avwap_bos']['pos']}
• Anchored VWAP Latest CHOCH: {v(data['vwap_system']['avwap_choch']['val'])} | Dist: {v(data['vwap_system']['avwap_choch']['dist'])} | {data['vwap_system']['avwap_choch']['pos']}
• Anchored VWAP Latest Breakout: {v(data['vwap_system']['avwap_breakout']['val'])} | Dist: {v(data['vwap_system']['avwap_breakout']['dist'])} | {data['vwap_system']['avwap_breakout']['pos']}

VWAP Analytics:
• Confluence: {data['vwap_system']['confluence']}
• Strongest Support: {v(data['vwap_system']['strongest_support'])}
• Strongest Resistance: {v(data['vwap_system']['strongest_resistance'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return msg
    
# ----------------------------------------------------
# DYNAMIC COMMAND REGISTRATION
# ----------------------------------------------------

def register_symbol_commands(app):

    logger.info("Registering Commands...")

    total = 0

    for symbol in SYMBOLS:

        for tf in TIMEFRAMES:

            command = f"{symbol.lower()}_{tf}"

            app.add_handler(
                CommandHandler(
                    command,
                    handle
                )
            )

            total += 1

    logger.info(f"{total} Commands Registered.")


# ----------------------------------------------------
# MAIN
# ----------------------------------------------------

def main():

    logger.info("Starting Institutional PSX Bot...")

    flask_thread = threading.Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    register_symbol_commands(application)

    logger.info("Bot Started Successfully.")

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )


# ----------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.info("Bot Stopped.")

    except Exception as e:

        logger.exception(e)
