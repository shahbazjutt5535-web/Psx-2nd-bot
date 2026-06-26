# bot.py

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from symbol_map import SYMBOLS
from config import TIMEFRAMES
from tv_helper import fetch_data
from smc_engine_wrapper import run_smc
from smc_formatter import format_output


BOT_TOKEN = "YOUR_TOKEN"


def parse_command(text):
    # /ffc_5m
    text = text.replace("/", "")
    parts = text.split("_")

    symbol = parts[0].lower()
    tf = parts[1] if len(parts) > 1 else "5m"

    return symbol, tf


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text

    symbol_key, tf = parse_command(cmd)

    if symbol_key not in SYMBOLS:
        await update.message.reply_text("Invalid symbol")
        return

    meta = SYMBOLS[symbol_key]

    df = fetch_data(meta["symbol"], meta["exchange"], tf)

    if df is None:
        await update.message.reply_text("No data found")
        return

    smc_data = run_smc(df, symbol_key, tf)

    output = format_output(smc_data, symbol_key, tf)

    await update.message.reply_text(output)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("ffc_5m", handle))
app.add_handler(CommandHandler("ffc_15m", handle))
app.add_handler(CommandHandler("ffc_1h", handle))
app.add_handler(CommandHandler("ffc_1d", handle))

app.run_polling()
