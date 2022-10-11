'''TODO'''

import abc
from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd
import yfinance as yf

from project.orders import enums
from project.utils import cache, errors, templating


class Order(abc.ABC):
    '''TODO'''

    def __init__(
        self,
        *,
        date_placed: pd.Timestamp,
        ticker: Union[yf.Ticker, str],
        shares: Optional[int] = None,
        available_principal: Optional[float] = None,
    ) -> None:

        if bool(shares) == bool(available_principal):
            raise ValueError(templating.template(
                'Cannot instantiate order.',
                'Please either provide the number of shares or the available principal.',
            ))

        self._cache = cache
        self._status = enums.Status.PROSPECTIVE
        self._date_placed = date_placed
        self._date_executed = None
        self._ticker = ticker if isinstance(ticker, yf.Ticker) else yf.Ticker(ticker)
        self._shares = shares if shares else int(available_principal // self.share_price)

        self._validate_operation(self.date_placed)

    def __repr__(
        self,
    ) -> str:
        '''TODO'''

        return f'{self}'

    def __format__(
        self,
        spec: str,
    ) -> str:
        '''TODO'''

        quantity = templating.template(
            '{ticker}@{shares:,}',
            ticker=self.ticker.ticker,
            shares=self.shares,
        )

        if spec == enums.OrderFormat.DEFAULT.value:
            return templating.template(
                '{order_type}({quantity} placed {date_placed}, {status}{date_executed})',
                order_type=type(self).__name__,
                quantity=quantity,
                date_placed=templating.stringify_date(self.date_placed),
                status=self.status.value,
                date_executed=(
                    f' {templating.stringify_date(self.date_executed)}'
                    if self.status is enums.Status.EXECUTED
                    else ''
                ),
            )

        if spec == enums.OrderFormat.SHARES.value:
            return quantity

        raise ValueError(templating.template(
            'Invalid spec: {spec}.',
            spec=spec,
        ))

    @property
    def status(
        self,
    ) -> enums.Status:
        '''TODO'''

        return self._status

    @property
    def date_placed(
        self,
    ) -> pd.Timestamp:
        '''TODO'''

        return self._date_placed

    @property
    def date_executed(
        self,
    ) -> pd.Timestamp:
        '''TODO'''

        if self.status is not enums.Status.EXECUTED:
            raise AttributeError(templating.template(
                '{order} has no execution date as it has not been executed.',
                order=self,
            ))

        return self._date_executed

    @property
    def ticker(
        self,
    ) -> yf.Ticker:
        '''TODO'''

        return self._ticker

    @property
    def ticker_history(
        self,
    ) -> pd.DataFrame:
        '''TODO'''

        return cache.ticker_history(self.ticker.ticker)

    @property
    def shares(
        self,
    ) -> int:
        '''TODO'''

        return self._shares

    @property
    def principal(
        self,
    ) -> float:
        '''TODO'''

        return self.shares * self.share_price

    @property
    @abc.abstractmethod
    def share_price(
        self,
    ) -> float:
        '''TODO'''

        raise NotImplementedError()

    @property
    def expiry_date(
        self,
    ) -> pd.Timestamp:
        '''TODO'''

        return self.date_placed + self.duration

    @property
    @abc.abstractmethod
    def duration(
        self,
    ) -> pd.Timedelta:
        '''TODO'''

        raise NotImplementedError()

    def open(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        self._validate_operation(date)

        if self.status is not enums.Status.PROSPECTIVE:
            raise errors.InvalidOperationError(templating.template(
                'Cannot open {order} as it is {status}.',
                order=self,
                status=self.status.value,
            ))

        self._status = enums.Status.OPEN

    def cancel(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        self._validate_operation(date)

        if self.status is not enums.Status.OPEN:
            raise errors.InvalidOperationError(templating.template(
                'Cannot cancel {order} as it is {status}.',
                order=self,
                status=self.status.value,
            ))

        self._status = enums.Status.CANCELED

    def update(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        self._validate_operation(date)

        if self.status is not enums.Status.OPEN:
            raise errors.InvalidOperationError(templating.template(
                'Cannot update {order} as it is {status}.',
                order=self,
                status=self.status.value,
            ))

        if date < self.date_placed:
            raise errors.InvalidOperationError(templating.template(
                'Cannot update {order} as update date {date} precedes order placement.',
                order=self,
                date=templating.stringify_date(date),
            ))

        if date > self.expiry_date:
            self._expire()
            return

        if self._should_execute(date):
            self._execute(date)
            return

    @abc.abstractmethod
    def _should_execute(
        self,
        date: pd.Timestamp,
    ) -> bool:
        '''TODO'''  # We can assume the date is on or after date_placed & within the expiry period.

        raise NotImplementedError()

    def _execute(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        if self.status is not enums.Status.OPEN:
            raise errors.InvalidOperationError(templating.template(
                'Cannot execute {order} as it is {status}.',
                order=self,
                status=self.status.value,
            ))

        self._status = enums.Status.EXECUTED
        self._date_executed = date

    def _expire(
        self,
    ) -> None:
        '''TODO'''

        if self.status is not enums.Status.OPEN:
            raise errors.InvalidOperationError(templating.template(
                'Cannot expire {order} as it is {status}.',
                order=self,
                status=self.status.value,
            ))

        self._status = enums.Status.EXPIRED

    def _validate_operation(
        self,
        date: pd.Timestamp,
    ) -> None:
        '''TODO'''

        if date not in self.ticker_history.index:
            raise errors.InvalidOperationError(templating.template(
                'Cannot operate on {order} as ticker history is undefined on {date}.',
                order=self,
                date=templating.stringify_date(date),
            ))
