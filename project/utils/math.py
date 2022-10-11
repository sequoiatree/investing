'''TODO'''

from typing import *  # pylint: disable=unused-wildcard-import, wildcard-import


def rounded(
    function: Callable[..., float],
) -> Callable[..., float]:
    '''TODO'''

    return lambda *args, **kwargs: round(function(*args, **kwargs), 2)
