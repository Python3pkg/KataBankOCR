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
        get_char = lambda x: random.choice(settings.figures.values())
        return ''.join(map(get_char, range(length)))
    return account

@pytest.fixture(params =(0, 1, -10, False, True, [], (), {}, set(), 3.14159))
def non_string(request):
    " Return an arbitrary non-string value "
    return request.param

