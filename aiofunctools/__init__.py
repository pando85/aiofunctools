import functools

from inspect import iscoroutinefunction
from toolz import curry
from typing import Callable, TypeVar


__version__ = '0.0.1'

T = TypeVar('T')


def _iscoroutinefunction_or_partial(object):
    if (isinstance(object, functools.partial) or
            isinstance(object, curry) or isinstance(object, bind)):
        return iscoroutinefunction(object.func)
    return iscoroutinefunction(object)


def compose(*funcs: Callable) -> Callable:
    first, second, *rest = funcs
    if rest:
        second = compose(second, *rest)
    if _iscoroutinefunction_or_partial(first) and _iscoroutinefunction_or_partial(second):
        async def _async(*args, **kwargs):
            return await second(await first(*args, **kwargs))
        return _async
    if _iscoroutinefunction_or_partial(second):
        async def _async(*args, **kwargs):
            return await second(first(*args, **kwargs))
        return _async
    if _iscoroutinefunction_or_partial(first):
        async def _async(*args, **kwargs):
            return second(await first(*args, **kwargs))
        return _async

    def _func(*args, **kwargs):
        return second(first(*args, **kwargs))
    return _func


class bind(curry):
    def __call__(self, *args, **kwargs):
        error = self._get_check_error(args)
        if error:
            return self._get_error(error)
        return curry.__call__(self, *args, **kwargs)

    def _get_check_error(self, _list):
        for x in _list:
            if isinstance(x, Exception):
                return x
        return None

    def _async_error(self, error):
        async def _async():
            return error
        return _async()

    def _get_error(self, error):
        if iscoroutinefunction(self.func):
            return self._async_error(error)
        return error
