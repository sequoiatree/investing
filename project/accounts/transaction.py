'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

from project.orders import order
from project.utils import templating


class Transaction:
    '''TODO'''

    def __init__(
        self,
        *,
        to_open: Optional[Set[order.Order]] = None,
        to_cancel: Optional[Set[order.Order]] = None,
    ) -> None:

        self._to_open = to_open or set()
        self._to_cancel = to_cancel or set()

    def __repr__(
        self,
    ) -> str:
        '''TODO'''

        orders = []
        orders.extend(f'+{order:@}' for order in self.to_open)
        orders.extend(f'-{order:@}' for order in self.to_cancel)

        return templating.template(
            'Transaction({orders})',
            orders=', '.join(orders),
        )

    @property
    def to_open(
        self,
    ) -> Set[order.Order]:
        '''TODO'''

        return self._to_open.copy()

    @property
    def to_cancel(
        self,
    ) -> Set[order.Order]:
        '''TODO'''

        return self._to_cancel.copy()
