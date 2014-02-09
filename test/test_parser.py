"Test Parser module"

import pytest
import subprocess

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"

def expected_matches_parsed_path(expected, parser_path, input_path):
    "confirm expected results found when parsing an input file"
    expected = str(expected) + '\n'
    with open(input_path) as input_file:
        found = subprocess.check_output(parser_path, stdin=input_file)
    return expected == found

basic_results = ('000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                 '444444444 ERR', '555555555 ERR', '666666666 ERR', '777777777 ERR',
                 '888888888 ERR', '999999999 ERR', '123456789',)
advanced_results = ('000000051', '49006771? ILL', '1234?678? ILL', '200000000 ERR',
                    '490067715 ERR', '?23456789 ILL', '0?0000051 ILL', '49086771? ILL')
@pytest.mark.parametrize('input_path, expected_results',(
        (path_to_basic_input, basic_results),
        (path_to_advanced_input, advanced_results),
        ))
def test_parser(input_path, expected_results):
    "confirm Results from basic input file"
    assert expected_matches_parsed_path(expected='\n'.join(expected_results),
                                        parser_path='parser/parser.py',
                                        input_path=input_path)
