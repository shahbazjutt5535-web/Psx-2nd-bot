import numpy as np


class VolumeProfile:

    def __init__(self, df, bins=24):

        self.df = df.copy()

        self.bins = bins


    def calculate(self):

        high = self.df["high"].max()

        low = self.df["low"].min()

        step = (high-low)/self.bins

        prices = np.arange(low, high+step, step)

        volumes = np.zeros(len(prices)-1)

        for _, row in self.df.iterrows():

            price = (row["high"]+row["low"])/2

            idx = np.digitize(price, prices)-1

            idx = max(0, min(idx, len(volumes)-1))

            volumes[idx] += row["volume"]

        poc_index = np.argmax(volumes)

        poc = (prices[poc_index]+prices[poc_index+1])/2

        total = volumes.sum()

        target = total*0.70

        order = np.argsort(volumes)[::-1]

        selected = []

        running = 0

        for i in order:

            selected.append(i)

            running += volumes[i]

            if running >= target:

                break

        vah = prices[max(selected)+1]

        val = prices[min(selected)]

        hvn = []

        lvn = []

        average = volumes.mean()

        for i, v in enumerate(volumes):

            level = (prices[i]+prices[i+1])/2

            if v > average*1.5:

                hvn.append(level)

            elif v < average*0.5:

                lvn.append(level)

        return {

            "POC": round(float(poc),2),

            "VAH": round(float(vah),2),

            "VAL": round(float(val),2),

            "HVN": hvn,

            "LVN": lvn,

            "ProfileRange": round(float(high-low),2)

        }


    def poc(self):

        return self.calculate()["POC"]


    def vah(self):

        return self.calculate()["VAH"]


    def val(self):

        return self.calculate()["VAL"]


    def hvn(self):

        return self.calculate()["HVN"]


    def lvn(self):

        return self.calculate()["LVN"]
