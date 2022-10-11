'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.accounts import brokerage_account, transaction
from project.orders import limit_order
from project.policies import policy
from project.utils import cache


class ConstantBelowMarket(policy.Policy):
    '''TODO'''

    def __init__(
        self,
        ticker: str,
        discount: float,
    ) -> None:
        '''TODO'''

        self._ticker = ticker
        self._discount = discount

    def __call__(
        self,
        date: pd.Timestamp,
        account: brokerage_account.BrokerageAccount,
    ) -> transaction.Transaction:
        '''TODO'''

        ticker_history = cache.ticker_history(self._ticker)

        order = limit_order.LimitOrder(
            date_placed=date,
            ticker=self._ticker,
            available_principal=account.available_balance,
            limit_price=ticker_history.loc[date, 'Open'] - self._discount,
        )

        return transaction.Transaction(to_open={order})
