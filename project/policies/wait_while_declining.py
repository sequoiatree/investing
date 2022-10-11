'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd
import scipy.stats

from project.accounts import brokerage_account, transaction
from project.policies import buy_immediately, policy
from project.utils import cache


class WaitWhileDeclining(policy.Policy):
    '''TODO'''

    def __init__(
        self,
        ticker: str,
        window: int,  # the shortest period (in days) that we want to see a decline
        slope_threshold: float,  # how steep we want the market to be declining.
        r2_threshold: float,  # r**2, aka the coefficient of determination. 0 <= r**2 <= 1. roughly corresponds to quality of fit.
    ) -> None:
        '''TODO'''

        self._ticker = ticker
        self._window = window
        self._slope_threshold = slope_threshold
        self._r2_threshold = r2_threshold

        self._subpolicy_buy_immediately = buy_immediately.BuyImmediately(self._ticker)

    def __call__(
        self,
        date: pd.Timestamp,
        account: brokerage_account.BrokerageAccount,
    ) -> transaction.Transaction:
        '''TODO'''

        ticker_history = cache.ticker_history(self._ticker)
        recent_history = ticker_history.loc[:date].tail(self._window)

        if len(recent_history) < self._window:
            return self._subpolicy_buy_immediately(date, account)

        regression = scipy.stats.linregress(
            x=range(self._window),
            y=[recent_history.loc[date, 'Close'] for date in recent_history.index],
        )
        is_good_fit = (regression.rvalue ** 2) < self._r2_threshold
        is_declining = regression.slope < self._slope_threshold

        if is_good_fit and is_declining:
            # Wait for the market to decline some more.
            return transaction.Transaction(
                to_open={},
                to_cancel=account.open_orders,
            )

        return self._subpolicy_buy_immediately(date, account)
