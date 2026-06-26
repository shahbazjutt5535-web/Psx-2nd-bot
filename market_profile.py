import numpy as np


class MarketProfile:

    def __init__(self, df, tick_size=0.5):

        self.df = df.copy()
        self.tick = tick_size

    def calculate(self):

        price_count = {}

        for _, row in self.df.iterrows():

            low = row["low"]
            high = row["high"]

            p = low

            while p <= high:

                key = round(p, 2)

                price_count[key] = price_count.get(key, 0) + 1

                p += self.tick

        if len(price_count) == 0:

            return None

        poc = max(price_count, key=price_count.get)

        ib = self.df.iloc[:min(2, len(self.df))]

        ib_high = ib["high"].max()

        ib_low = ib["low"].min()

        return {

            "POC": round(float(poc), 2),

            "TPO Count": len(price_count),

            "Initial Balance High": round(float(ib_high), 2),

            "Initial Balance Low": round(float(ib_low), 2)

        }

    def poc(self):

        return self.calculate()["POC"]

    def tpo(self):

        return self.calculate()["TPO Count"]

    def ib_high(self):

        return self.calculate()["Initial Balance High"]

    def ib_low(self):

        return self.calculate()["Initial Balance Low"]
