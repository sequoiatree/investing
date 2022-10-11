'''TODO'''

import enum
from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import


class OrderFormat(enum.Enum):
    '''TODO'''

    DEFAULT = ''
    SHARES = '@'


class Status(enum.Enum):
    '''TODO'''

    CANCELED = 'canceled'
    EXECUTED = 'executed'
    EXPIRED = 'expired'
    OPEN = 'open'
    PROSPECTIVE = 'prospective'
