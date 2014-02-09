"Test Parser module"

import pytest
import subprocess

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"
basic_results = ('000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                 '444444444 ERR', '555555555 ERR', '666666666 ERR', '777777777 ERR',
                 '888888888 ERR', '999999999 ERR', '123456789',)
advanced_results = ('000000051', '49006771? ILL', '1234?678? ILL', '200000000 ERR',
                    '490067715 ERR', '?23456789 ILL', '0?0000051 ILL', '49086771? ILL')
@pytest.fixture(params=((basic_results, path_to_basic_input),
                        (advanced_results, path_to_advanced_input),))
def expectations_and_source(request):
    "return expected results and input path from which to find them"
    expected, path = request.param
    expected = '\n'.join(expected) + '\n'
    return expected, path

def test_stdin_and_stdout(expectations_and_source):
    "confirm Results parsed correctly from StdIn to StdOut"
    expected_results, input_path = expectations_and_source
    with open(input_path) as input_file:
        found_results = subprocess.check_output('parser/parser.py', stdin=input_file)
    assert expected_results == found_results

def test_in_path_and_stdout(tmpdir, expectations_and_source):
    "confirm Results parsed correctly from path to StdOut"
    expected_results, input_path = expectations_and_source
    found_results = subprocess.check_output(['parser/parser.py', input_path])
    assert expected_results == found_results

def test_in_path_and_out_path(tmpdir, expectations_and_source):
    "confirm Results parsed correctly from in_path to out_path"
    expected_results, input_path = expectations_and_source
    output_path = 'tmp_out_file'
    output_path = str(tmpdir.join(output_path))
    subprocess.call(['parser/parser.py', input_path, output_path])
    with open(output_path) as parsed_results:
        found_results = parsed_results.read()
    assert expected_results == found_results

def test_stdin_and_out_path(tmpdir, expectations_and_source):
    "confirm Results parsed correctly from StdIn to out_path"
    expected_results, input_path = expectations_and_source
    output_path = 'tmp_out_file'
    output_path = str(tmpdir.join(output_path))
    with open(input_path) as input_file:
        subprocess.call(['parser/parser.py', '-', output_path], stdin=input_file)
    with open(output_path) as parsed_results:
        found_results = parsed_results.read()
    assert expected_results == found_results

