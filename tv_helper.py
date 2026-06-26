# tv_helper.py

from tv_data import get_tv_data
from config import DEFAULT_BARS

def fetch_data(symbol, exchange, interval):
    """
    Unified TV data fetcher
    """
    try:
        df = get_tv_data(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=DEFAULT_BARS
        )

        if df is None or df.empty:
            return None

        return df

    except Exception as e:
        print("TV Fetch Error:", e)
        return None
