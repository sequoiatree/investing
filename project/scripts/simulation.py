'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd
import pandas_market_calendars as mcal

from project.accounts import brokerage_account
from project.policies import policy
from project.utils import templating


class Simulation:
    '''TODO'''

    def __init__(
        self,
        policy: policy.Policy,  # pylint: disable=redefined-outer-name
        stock_exchange: str,
    ) -> None:

        self._account = brokerage_account.BrokerageAccount()
        self._policy = policy
        self._calendar = mcal.get_calendar(stock_exchange)
        self._date = None

    @property
    def account(
        self,
    ) -> brokerage_account.BrokerageAccount:
        '''TODO'''

        return self._account

    @property
    def policy(
        self,
    ) -> policy.Policy:
        '''TODO'''

        return self._policy

    @property
    def calendar(
        self,
    ) -> mcal.MarketCalendar:
        '''TODO'''

        return self._calendar

    @property
    def date(
        self,
    ) -> pd.Timestamp:
        '''TODO'''

        if not self._date:
            raise AttributeError(templating.template(
                'This simulation has no date as it has not been run.',
            ))

        return self._date

    def run(
        self,
        *,
        start_date: pd.Timestamp,
        end_date: Optional[pd.Timestamp] = None,
        duration: Optional[pd.Timedelta] = None,
        deposit_schedule: Optional[Union[pd.Series, Generator[float, None, None]]] = None,
    ) -> None:
        '''TODO'''

        if bool(end_date) == bool(duration):
            raise ValueError(templating.template(
                'Cannot run simulation.',
                'Please either provide the end date or the duration.',
            ))

        print(templating.template('Running simulation ...'))

        end_date = end_date if end_date else (start_date + duration)

        for date in self.calendar.schedule(start_date, end_date).index:

            if not self._date or (date.year != self.date.year):
                print(templating.template('Year: {year}', year=date.year))

            self._date = date

            self.account.update(date)

            if deposit_schedule:
                deposit_amount = (
                    deposit_schedule.loc[date]
                    if isinstance(deposit_schedule, pd.Series)
                    else next(deposit_schedule)
                )
                self.account.deposit(deposit_amount)

            transaction = self.policy(date, self.account)
            self.account.transact(date, transaction)

            self.account.update(date)

        print(templating.template('Simulation complete.'))
