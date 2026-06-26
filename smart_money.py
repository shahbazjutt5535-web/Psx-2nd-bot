import pandas as pd
import numpy as np

from helpers import *


class SmartMoney:

    def __init__(self, df):

        self.df = df.copy()

        self.swing_highs = []
        self.swing_lows = []

        self.bos = []

        self.choch = []

        self.equal_highs = []

        self.equal_lows = []

        self.buy_liquidity = []

        self.sell_liquidity = []

        self.sweeps = []

        self.fvg = []

        self.order_blocks = []

        self.breaker_blocks = []

        self.mitigation_blocks = []

        self.supply = []

        self.demand = []

        self.imbalances = []



    ##################################################

    # SWING HIGH LOW

    ##################################################

    def detect_swings(self, left=3, right=3):

        high = self.df["high"].values

        low = self.df["low"].values

        for i in range(left, len(self.df)-right):

            if high[i] == max(high[i-left:i+right+1]):

                self.swing_highs.append({

                    "index": i,

                    "price": high[i]

                })

            if low[i] == min(low[i-left:i+right+1]):

                self.swing_lows.append({

                    "index": i,

                    "price": low[i]

                })

        return self.swing_highs, self.swing_lows



    ##################################################

    # BREAK OF STRUCTURE

    ##################################################

    def detect_bos(self):

        self.detect_swings()

        close = self.df["close"].values

        for swing in self.swing_highs:

            i = swing["index"]

            if i >= len(close)-1:

                continue

            for j in range(i+1, len(close)):

                if close[j] > swing["price"]:

                    self.bos.append({

                        "type": "Bullish",

                        "level": swing["price"],

                        "index": j

                    })

                    break

        for swing in self.swing_lows:

            i = swing["index"]

            if i >= len(close)-1:

                continue

            for j in range(i+1, len(close)):

                if close[j] < swing["price"]:

                    self.bos.append({

                        "type": "Bearish",

                        "level": swing["price"],

                        "index": j

                    })

                    break

        return self.bos



    ##################################################

    # CHOCH

    ##################################################

    def detect_choch(self):

        if len(self.bos) == 0:

            self.detect_bos()

        previous = None

        for b in self.bos:

            if previous is None:

                previous = b

                continue

            if b["type"] != previous["type"]:

                self.choch.append({

                    "index": b["index"],

                    "level": b["level"],

                    "type": b["type"]

                })

            previous = b

        return self.choch
