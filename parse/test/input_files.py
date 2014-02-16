"details regarding input files used for testing"

import os

directory = os.path.join(os.path.dirname(__file__), 'input_files')

class Basic:
    "details regarding the Basic input file"

    path = os.path.join(directory, 'basic.txt')
    line_count = 44
    accounts = [
        '000000000',
        '111111111',
        '222222222',
        '333333333',
        '444444444',
        '555555555',
        '666666666',
        '777777777',
        '888888888',
        '999999999',
        '123456789',
        ]
    results = [
        '000000000',
        '711111111',
        '222222222 AMB',
        '333393333',
        '444444444 AMB',
        '555555555 AMB',
        '666666666 AMB',
        '777777177',
        '888888888 AMB',
        '999999999 AMB',
        '123456789',
        ]

class Advanced:
    "details regarding the Advanced input file"

    path = os.path.join(directory, 'advanced.txt')
    line_count = 32
    results = [
        '000000051',
        '49006771? AMB',
        '123456789',
        '200800000',
        '490067715 AMB',
        '123456789',
        '000000051',
        '490867715',
        ]
