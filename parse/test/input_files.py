"details regarding input files used for testing"

import os

directory =  os.path.join(os.path.dirname(__file__), 'input_files')

class Basic:
    "details regarding the Basic input file"

    path = os.path.join(directory, 'basic.txt')
    line_count = 44
    results = ['000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
               '444444444 ERR', '555555555 AMB', '666666666 AMB', '777777177',
               '888888888 AMB', '999999999 AMB', '123456789']

class Advanced:
    "details regarding the Advanced input file"

    path = os.path.join(directory, 'advanced.txt')
    line_count = 32
    results = ['000000051', '490067715 AMB', '1234?678?', '200000000',
               '490067715 AMB', '123456789', '000000051', '490867715']

