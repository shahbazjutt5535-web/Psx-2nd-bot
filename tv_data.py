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
# ==========================================================
# DATA CLEANING + FINAL OUTPUT
# ==========================================================

    # Ensure datetime index is clean
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            pass

    # Standardize column names (just in case)
    df.columns = [str(c).lower() for c in df.columns]

    # Remove duplicates if any
    df = df[~df.index.duplicated(keep="last")]

    # Sort by time (important for indicators)
    df = df.sort_index()

    # Handle missing values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    # Final safety check
    if len(df) < 20:
        raise Exception(f"Not enough clean data for {symbol}.")

    return df
