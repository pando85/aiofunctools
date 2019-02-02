[![Build Status](https://travis-ci.org/pando85/aiofunctools.svg?branch=master)](https://travis-ci.org/pando85/aiofunctools) [![License](https://img.shields.io/github/license/pando85/aiofunctools.svg)](https://github.com/pando85/aiofunctools/blob/master/LICENSE) [![Documentation Status](https://readthedocs.org/projects/aiofunctools/badge/?version=latest)](https://aiofunctools.readthedocs.io/en/latest/?badge=latest)
# aiofunctools

Library to help in Python functional programing. It’s asyncio compatible.

Basic idea behind it is [Railway Oriented Programing](https://fsharpforfunandprofit.com/rop/).

This allows us to:
- simplify our code.
- improve error management.
- be cool! be functional!

Examples:

Old code example:

```python
async def create_user_handler(request) -> Response:
    try:
        user = check_valid_user(request)
        create_user(user)
    except InvalidBody:
        return_422('Invalid body')
    except UserAlreadyExists:
        return_409('User already exists')
    return_201(user)
```


ROP example:

```python
async def create_user_handler(request) -> Response:
    return await compose(
        check_valid_user,
        create_user,
        return_201
    )(request)


```
