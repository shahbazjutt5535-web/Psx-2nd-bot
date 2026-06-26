from tvDatafeed import TvDatafeed, Interval
import pandas as pd


class TVData:

    def __init__(self):
        self.tv = TvDatafeed(auto_login=False)

        self.interval_map = {
            "5m": Interval.in_5_minute,
            "15m": Interval.in_15_minute,
            "30m": Interval.in_30_minute,
            "1h": Interval.in_1_hour,
            "4h": Interval.in_4_hour,
            "1d": Interval.in_daily,
            "1w": Interval.in_weekly,
            "1M": Interval.in_monthly,
        }

    def get_data(self, symbol, exchange="PSX", timeframe="4h", bars=500):

        interval = self.interval_map.get(timeframe)

        df = self.tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=bars
        )

        if df is None:
            return None

        if len(df) == 0:
            return None

        df.reset_index(inplace=True)

        return df

    def get_close(self, df):
        return float(df.iloc[-1]["close"])

    def get_high(self, df):
        return float(df.iloc[-1]["high"])

    def get_low(self, df):
        return float(df.iloc[-1]["low"])

    def get_open(self, df):
        return float(df.iloc[-1]["open"])

    def get_volume(self, df):
        return float(df.iloc[-1]["volume"])

    def latest_candle(self, df):
        return df.iloc[-1]

    def previous_candle(self, df):
        return df.iloc[-2]

    def last_100(self, df):
        return df.tail(100)

    def last_200(self, df):
        return df.tail(200)

    def last_300(self, df):
        return df.tail(300)

    def last_500(self, df):
        return df.tail(500)
