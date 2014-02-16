"Fixtures used by test modules"

import pytest
import random

from parse import settings

def pytest_report_header(config):
    return "Bank OCR Kata Tests"
