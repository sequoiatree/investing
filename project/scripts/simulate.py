'''TODO'''  # python -i project/scripts/simulate.py to inspect simulation.account after.

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd

from project.accounts import brokerage_account
from project.policies import buy_immediately, policy
from project.scripts import simulation


def deposit_daily(
    amount: float,
) -> Generator[float, None, None]:
    '''TODO'''

    while True:
        yield amount


def simulate_vti_since_epoch(
    policy: policy.Policy,  # pylint: disable=redefined-outer-name
    deposit_schedule=Optional[Union[Generator[float, None, None], pd.Series]],
) -> brokerage_account.BrokerageAccount:
    '''TODO'''

    sim = simulation.Simulation(policy, 'NASDAQ')
    sim.run(
        start_date=pd.Timestamp('2001-06-15'),
        end_date=pd.Timestamp.today(),
        deposit_schedule=deposit_schedule,
    )

    return sim.account


if __name__ == '__main__':

    bi_acct = simulate_vti_since_epoch(
        buy_immediately.BuyImmediately('VTI'),
        deposit_daily(500),
    )

    # cbm_acct = simulate_vti_since_epoch(
    #     constant_below_market.ConstantBelowMarket('VTI', 5.0),
    #     deposit_daily(500),
    # )

    # wwd_acct = simulate_vti_since_epoch(
    #     wait_while_declining.WaitWhileDeclining('VTI', 30, -0.15, 0.75),
    #     deposit_daily(500),
    # )

    today = pd.Timestamp.today()
