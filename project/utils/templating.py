'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import

import pandas as pd


def template(
    *template: str,  # pylint: disable=redefined-outer-name
    separator: str = ' ',
    **macros: Any,
) -> str:
    '''TODO'''

    return (
        separator
        .join(template)
        .format(**macros)
    )

def stringify_date(
    date: pd.Timestamp,
) -> str:
    '''TODO'''

    return str(date.date())
