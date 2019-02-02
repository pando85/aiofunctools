Welcome to aiofunctools's documentation!
========================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    bind
    compose

Aiofunctools
------------

Library to help in Python functional programing. It's asyncio compatible.

Basic idea behind it is `Railway Oriented Programing`_.

This allows us to:
  - simplify our code.
  - improve error management.
  - be cool! be functional!

Examples:

Old code example:

.. code-block:: python

    async def create_user_handler(request) -> Response:
        try:
            user = check_valid_user(request)
        except InvalidBody:
            return_422('Invalid body')
        try:
            create_user(user)
        except UserAlreadyExists:
            return_409('User already exists')
        return_201(user)


ROP example:

.. code-block:: python

    async def create_user_handler(request) -> Response:
        return await compose(
            check_valid_user,
            create_user,
            return_201
        )(request)




Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _railway oriented programing: https://fsharpforfunandprofit.com/rop/
