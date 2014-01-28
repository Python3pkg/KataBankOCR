" Collect pytest fixtures "

import pytest
import random

import settings

def pytest_report_header(config):
    return "Bank OCR Kata Tests"

@pytest.fixture
def get_account_string():
    " return function that returns valid length string of account characters "
    def account_string():
        length = settings.figures_per_entry
        get_char = lambda x: random.choice(settings.figures.values())
        return ''.join(map(get_char, range(length)))
    return account_string

