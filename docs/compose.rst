Compose
=======

Description
-----------

Function used to compose other functions.

Allow async functions.

First input function is first executed.

Example
-------

Compose:

.. code-block:: python

    from aiofunctools import compose

    async def test(_input):

    return await compose(
        first,
        awaitable_second,
        third)(_input)


It is same code than:

.. code-block:: python

    from aiofunctools import compose

    async def test(_input):
    return third(
        await awaitable_second(
            first(_input)))