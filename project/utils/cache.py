'''TODO'''

import functools
from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd
import yfinance as yf


@functools.cache
def ticker_history(
    ticker: str,
) -> pd.DataFrame:
    '''TODO'''  # Cache this query across orders since it's so expensive for each order to do it separately.

    ticker = yf.Ticker(ticker)

    historical_data = ticker.history(period='max')
    today_data = ticker.history('1d')

    return (
        historical_data
        if today_data.index[0] in historical_data.index
        else pd.concat([historical_data, today_data])
    )
