" Fixtures used by multiple test modules "

import pytest
import random

import settings

def pytest_report_header(config):
    return "Bank OCR Kata Tests"

@pytest.fixture
def get_account():
    " return function that returns a valid-length string of Numerals "
    def account():
        length = settings.figures_per_entry
        valid_numerals = settings.figures.values()
        get_numeral = lambda x: random.choice(valid_numerals)
        return ''.join(map(get_numeral, range(length)))
    return account

@pytest.fixture(params =(0, 1, -10, False, True, [], (), {}, set(), 3.14159))
def non_string(request):
    " Return an arbitrary non-string value "
    return request.param

