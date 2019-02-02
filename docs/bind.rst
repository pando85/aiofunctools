Bind
====

Description
-----------

Function used to pass-through execution if input is an Exception.

In addition, it currify function.


Example
-------

.. code-block:: python

    def x5(x: int) -> int:
        return x * 5

    maybe_x5 = bind(x5)
    assert maybe_x5(1) == 5

    error = maybe_x5(Exception())


Curry
-----

Curried functions admit less inputs than mandatory ones and return a function with that inputs fixed.

In `this great book`_ is explained better.


.. code-block:: python

    def _sum(x: int, y: int) -> int:
        return x + y

    maybe_sum = bind(_sum)
    maybe_sum1 = maybe_sum(1)
    assert maybe_sum1(4) == 5

    error = maybe_sum1(Exception())


Decorator
---------

.. code-block:: python

    @bind
    def x5(x: int) -> int:
        return x * 5


.. _this great book: http://learnyouahaskell.com/higher-order-functions#curried-functions
