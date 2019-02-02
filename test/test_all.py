import pytest

from functools import partial

from aiofunctools import _iscoroutinefunction_or_partial, compose, bind


async def async_sum(x: int, y: int) -> int:
    return x + y


def _sum(x: int, y: int) -> int:
    return x + y


def test_iscoroutinefunction_or_partial():
    async def foo(boo, woo):
        return (boo, woo)
    partial_foo = partial(foo, None)
    assert _iscoroutinefunction_or_partial(partial_foo) is True


def test_iscoroutinefunction_or_partial_or_bind():
    async def foo(boo, woo):
        return (boo, woo)
    partial_foo = bind(foo)
    assert _iscoroutinefunction_or_partial(partial_foo(None)) is True


def test_iscoroutinefunction_or_partial_false():
    def foo(boo, woo):
        return (boo, woo)
    partial_foo = partial(foo, None)
    assert _iscoroutinefunction_or_partial(partial_foo) is False


def test_compose():
    def x2(x: int) -> int:
        return x * 2

    def plus5(x: int) -> int:
        return x + 5
    assert compose(x2, plus5)(1) == 7
    assert compose(x2, plus5, x2)(1) == 14


@pytest.mark.asyncio
async def test_compose_async():
    async def x2(x: int) -> int:
        return x * 2

    async def plus5(x: int) -> int:
        return x + 5
    assert await compose(x2, plus5)(1) == 7
    assert await compose(x2, plus5, x2)(1) == 14


@pytest.mark.asyncio
async def test_compose_async_first():
    async def x2(x: int) -> int:
        return x * 2

    def plus5(x: int) -> int:
        return x + 5
    assert await compose(x2, plus5)(1) == 7
    assert await compose(x2, plus5, x2)(1) == 14


def test_bind():
    def x5(x: int) -> int:
        return x * 5

    maybe_x5 = bind(x5)
    assert maybe_x5(1) == 5

    error = maybe_x5(Exception())
    assert isinstance(error, Exception)
    assert not isinstance(error, int)


def test_bind_curry():
    maybe_sum = bind(_sum)
    maybe_sum1 = maybe_sum(1)
    assert maybe_sum1(4) == 5

    error = maybe_sum1(Exception())
    assert isinstance(error, Exception)
    assert not isinstance(error, int)


@pytest.mark.asyncio
async def test_bind_async():
    maybe_sum = bind(async_sum)
    maybe_sum1 = maybe_sum(1)
    assert await maybe_sum1(5) == 6

    error = await maybe_sum(Exception())
    assert isinstance(error, Exception)
    assert not isinstance(error, int)


@pytest.mark.asyncio
async def test_compose_with_bind_error():
    maybe_sum = bind(async_sum)

    async def return_error(x: int):
        return Exception()

    assert await compose(maybe_sum(1), maybe_sum(2))(3) == 6
    assert isinstance(await compose(maybe_sum(1), maybe_sum(2))(Exception()), Exception)
    assert isinstance(await compose(return_error, maybe_sum(1))(3), Exception)
