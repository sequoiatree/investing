'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.orders import order


class MarketOrder(order.Order):
    '''TODO'''

    @property
    def share_price(
        self,
    ) -> float:
        '''TODO'''

        return self.ticker_history.loc[self.date_placed, 'High']

    @property
    def duration(
        self,
    ) -> pd.Timedelta:
        '''TODO'''

        return pd.Timedelta(1, 'd')

    def _should_execute(
        self,
        date: pd.Timestamp,
    ) -> bool:
        '''TODO'''

        return True
