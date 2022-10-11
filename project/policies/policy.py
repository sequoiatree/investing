'''TODO'''

import abc
from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.accounts import brokerage_account, transaction


class Policy(abc.ABC):
    '''TODO'''

    @abc.abstractmethod
    def __call__(
        self,
        date: pd.Timestamp,
        account: brokerage_account.BrokerageAccount,
    ) -> transaction.Transaction:
        '''TODO'''

        raise NotImplementedError()
