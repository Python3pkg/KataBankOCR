#!/usr/bin/env python

" This file first tests the settings module, then everything "

import pytest

def main():
    print 'Testing settings...'
    exit_status = pytest.main(['-k', 'parser/settings.py'])
    exited_cleanly = 0
    if exit_status == exited_cleanly:
        print 'Settings look fine. Will now test everything.'
        pytest.main(['-k', 'test'])
    else:
        print 'Settings failed. Testing halted.'

if __name__ == "__main__":
    main()
