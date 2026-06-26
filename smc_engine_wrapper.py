# smc_engine_wrapper.py

from smc_engine import analyze_smc

def run_smc(df, symbol, timeframe):
    """
    Returns raw structured SMC data (NO calculations in bot)
    """

    result = analyze_smc(df)

    return result
