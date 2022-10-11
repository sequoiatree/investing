'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd
import yfinance as yf

from project.orders import order


class LimitOrder(order.Order):
    '''TODO'''

    def __init__(
        self,
        *,
        date_placed: pd.Timestamp,
        ticker: yf.Ticker,
        shares: Optional[int] = None,
        available_principal: Optional[float] = None,
        limit_price: float,
    ) -> None:

        self._limit_price = limit_price

        # Order.__init__ requires the share price, which is determined by the limit price.
        super().__init__(
            date_placed=date_placed,
            ticker=ticker,
            shares=shares,
            available_principal=available_principal,
        )

    @property
    def limit_price(
        self,
    ) -> float:
        '''TODO'''

        return self._limit_price

    @property
    def share_price(
        self,
    ) -> float:
        '''TODO'''

        return self.limit_price

    @property
    def duration(
        self,
    ) -> pd.Timedelta:
        '''TODO'''

        return pd.Timedelta(60, 'd')

    def _should_execute(
        self,
        date: pd.Timestamp,
    ) -> bool:
        '''TODO'''

        return self.ticker_history.loc[date, 'Low'] <= self.limit_price
