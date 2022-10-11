'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.accounts import brokerage_account, transaction
from project.orders import market_order
from project.policies import policy


class BuyImmediately(policy.Policy):
    '''TODO'''

    def __init__(
        self,
        ticker: str,
    ) -> None:
        '''TODO'''

        self._ticker = ticker

    def __call__(
        self,
        date: pd.Timestamp,
        account: brokerage_account.BrokerageAccount,
    ) -> transaction.Transaction:
        '''TODO'''

        order = market_order.MarketOrder(
            date_placed=date,
            ticker=self._ticker,
            available_principal=account.settlement_fund,
        )

        return transaction.Transaction(
            to_open={order},
            to_cancel=account.open_orders,
        )
