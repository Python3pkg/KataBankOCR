#!/usr/bin/env python

" This file first tests the settings module, then everything "

import pytest


def main():
    exit_status = pytest.main(['-k', 'settings.py'])
    exited_cleanly = 0
    if exit_status == exited_cleanly:
        pytest.main(['-k', 'test'])
    else:
        print 'Testing halted after test failures in settings.py'

if __name__ == "__main__":
    main()

    


