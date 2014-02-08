" Fixtures used by test modules "

import pytest
import random

import settings

def pytest_report_header(config):
    return "Bank OCR Kata Tests"

@pytest.fixture(params =(0, 1, -10, False, True, [], (), {}, set(), 3.14159))
def non_string(request):
    " Return an arbitrary non-string value "
    return request.param

@pytest.fixture(params=(0, 1, -10, False, True, 3.14159))
def non_iterable(request):
    " return an arbitrary non-iterable value "
    return request.param

@pytest.fixture
def get_figure():
    " return function that returns a random valid Figure "
    return lambda: random.choice(settings.figures.keys())

@pytest.fixture
def get_figures(get_figure):
    " return function that returns an Entry's worth of valid Figures "
    count = settings.figures_per_entry
    return lambda: [get_figure() for _ in range(count)]

@pytest.fixture
def get_numeral():
    " return function that returns a valid Numeral "
    list_of_valid_numerals = list(settings.valid_numerals)
    return lambda: random.choice(list_of_valid_numerals)

@pytest.fixture
def get_numerals(get_numeral):
    " return function that returns an Entry's worth of random Numerals "
    count = settings.figures_per_entry
    return lambda: [get_numeral() for _ in range(count)]

@pytest.fixture
def get_account(get_numerals):
    " return function that returns a random Account "
    return lambda: ''.join(get_numerals())

@pytest.fixture
def get_accounts(get_account):
    " return function that returns a File's worth of random Accounts "
    count = settings.approximate_entries_per_file
    return lambda: [get_account() for _ in range(count)]

