'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.accounts import transaction
from project.orders import order, enums
from project.utils import cache, errors, math, templating


class BrokerageAccount:
    '''TODO'''

    def __init__(
        self,
        settlement_fund: float = 0.0,
    ) -> None:

        self._settlement_fund = settlement_fund
        self._open_orders = set()
        self._holdings = {}

    def __repr__(
        self,
    ) -> str:
        '''TODO'''

        return templating.template(
            'Present value:'
            '  ${value:,.2f}',
            'Settlement fund:',
            '  ${settlement_fund:,.2f} (total)',
            '  ${available_balance:,.2f} (available)',
            'Holdings:',
            *[
                f'  {ticker}: {shares:,}'
                for ticker, shares in self.holdings.items()
            ],
            'Open orders: {open_orders:,}',
            separator='\n',
            value=self.value(pd.Timestamp.today()),
            settlement_fund=self.settlement_fund,
            available_balance=self.available_balance,
            open_orders=len(self.open_orders),
        )

    @property
    def settlement_fund(
        self,
    ) -> float:
        '''TODO'''

        return self._settlement_fund

    @property
    def available_balance(
        self,
    ) -> float:
        '''TODO'''

        return self.settlement_fund - self.principal

    @property
    def principal(
        self,
    ) -> float:
        '''TODO'''

        return sum(order.principal for order in self.open_orders)

    @property
    def open_orders(
        self,
    ) -> Set[order.Order]:
        '''TODO'''

        return self._open_orders.copy()

    @property
    def holdings(
        self,
    ) -> Dict[str, int]:
        '''TODO'''

        return self._holdings.copy()

    def deposit(
        self,
        amount: float,
    ) -> None:
        '''TODO'''

        self._settlement_fund += amount

    def update(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        executed = set()
        expired = set()

        for order in self.open_orders:  # pylint: disable=redefined-outer-name

            order.update(date)

            if order.status is enums.Status.EXECUTED:
                executed.add(order)

            if order.status is enums.Status.EXPIRED:
                expired.add(order)

        for order in executed:
            self._settlement_fund -= order.principal
            self._open_orders.remove(order)
            self._holdings[order.ticker.ticker] = self.holdings.get(order.ticker.ticker, 0) + order.shares

        for order in expired:
            self._open_orders.remove(order)

        if self.available_balance < 0:
            raise errors.IllegalStateError(templating.template(
                'Account overdrawn executing {executing}, expiring {expiring}.',
                executing=executed,
                expiring=expired,
            ))

    def transact(
        self,
        date: pd.Timestamp,
        transaction: transaction.Transaction,  # pylint: disable=redefined-outer-name
    ) -> None:
        '''TODO'''

        prospective_orders = self.open_orders
        prospective_orders = prospective_orders.difference(transaction.to_cancel)
        prospective_orders = prospective_orders.union(transaction.to_open)

        prospective_principal = sum(order.principal for order in prospective_orders)

        if prospective_principal > self.settlement_fund:
            raise errors.InvalidOperationError(templating.template(
                'Insufficient funds (${balance:,.2f}) for {transaction}.',
                balance=self.settlement_fund,
                transaction=transaction,
            ))

        for order in transaction.to_cancel:  # pylint: disable=redefined-outer-name
            order.cancel(date)
            self._open_orders.remove(order)

        for order in transaction.to_open:
            order.open(date)
            self._open_orders.add(order)

    @math.rounded
    def value(
        self,
        date: pd.Timestamp,
    ) -> float:
        '''TODO'''

        date = date.normalize()

        return self.settlement_fund + self.portfolio_value(date)

    @math.rounded
    def portfolio_value(
        self,
        date: pd.Timestamp,
    ) -> float:
        '''TODO'''

        date = date.normalize()

        return sum(
            cache.ticker_history(ticker).loc[date, 'Open'] * quantity
            for ticker, quantity in self.holdings.items()
        )
