#!/usr/bin/env python

" Decorators to assist with testing "

import pytest

@pytest.fixture
def repeats(count):
    " decorator that runs a function repeatedly "
    def decorator(function):
        def decorated_function(*args, **kwargs):
            for i in range(count):
                function(*args, **kwargs)
        return decorated_function
    return decorator
