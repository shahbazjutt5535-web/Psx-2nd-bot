from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# ==========================================================
# LOGIN
# ==========================================================

tv = TvDatafeed()


# ==========================================================
# TIMEFRAME MAPPING
# ==========================================================

TIMEFRAME_MAP = {

    "5m": Interval.in_5_minute,

    "15m": Interval.in_15_minute,

    "30m": Interval.in_30_minute,

    "1h": Interval.in_1_hour,

    "4h": Interval.in_4_hour,

    "1d": Interval.in_daily,

    "1w": Interval.in_weekly,

    "1m": Interval.in_monthly

}


# ==========================================================
# EXCHANGE
# ==========================================================

DEFAULT_EXCHANGE = "PSX"
# ==========================================================
# GET DATA
# ==========================================================

def get_data(symbol, timeframe, bars=500):

    if timeframe not in TIMEFRAME_MAP:
        raise Exception(f"Unsupported timeframe: {timeframe}")

    interval = TIMEFRAME_MAP[timeframe]

    try:

        df = tv.get_hist(
            symbol=symbol,
            exchange=DEFAULT_EXCHANGE,
            interval=interval,
            n_bars=bars
        )

    except Exception as e:

        logger.exception(e)
        raise Exception("TradingView connection failed.")

    if df is None or len(df) == 0:
        raise Exception(f"No data received for {symbol}.")

    df = df.copy()
