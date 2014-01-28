import pytest
import subprocess

import settings
from parser.errors import InputError
from parser.parser import Parser

from common_tools import file_path_from_entry_lists
from common_tools import entry_list_from_account_string

class TestParser:
    " test the Parser class "

    @pytest.fixture
    def path_and_account_strings(self, tmpdir, get_account_string):
        " return path and list represented account strings in that file "
        entry_count = settings.approximate_entries_per_file
        account_strings = [get_account_string() for i in range(entry_count)]
        entry_lists = map(entry_list_from_account_string, account_strings)
        path = file_path_from_entry_lists(tmpdir, entry_lists)
        return path, account_strings

    @pytest.fixture
    def path(self, path_and_account_strings):
        " return a path to a valid input file "
        return path_and_account_strings[0]

    class TestInit:
        " test Parser initialization "

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_with_multiple_arguments(self, arg_count):
            " confirm Entry requires fewer than 2 arguments "
            pytest.raises(TypeError, Parser, *range(arg_count))

        def test_with_valid_path(self, path):
            " confirm Parser instantiates when given a valid path "
            p = Parser(path)
            assert isinstance(p, Parser)

    class TestInputValidation:
        " confirm Parser validates its input "

        def test_with_bad_path(self):
            " confirm Parser verifies ability to open file at given path "
            bad_path = 'mxyzptlk_foobarbaz'
            pytest.raises(IOError, Parser, bad_path)

        @pytest.fixture
        def path_to_abbreviated_file(self, path):
            " return path to a file missing its last line "
            with path.open('r') as F:
                lines = F.readlines()
            with path.open('w') as F:
                F.writelines(lines[:-1])
            return path

        def test_with_abbreviated_file(self, path_to_abbreviated_file):
            " confirm Parser recognizes insufficient length file "
            e = pytest.raises(InputError, Parser, path_to_abbreviated_file)
            assert e.value.message == 'file ended mid entry'

        @pytest.fixture
        def path_to_empty_file(self, tmpdir):
            " return path to an empty file "
            return  file_path_from_entry_lists(tmpdir, [])

        def test_with_empty_file(self, path_to_empty_file):
            " confirm Parser recognizes an empty file "
            e = pytest.raises(InputError, Parser, path_to_empty_file)
            assert e.value.message == 'nothing to parse'

    class TestFunctionality:
        " confirm Parser resolves file to list of correct account strings "

        def test_correctly_parses_file(self, path_and_account_strings):
            " confirm Parser identifies account strings from path "
            path, account_strings = path_and_account_strings
            assert Parser(path).account_strings == account_strings

        def test_main_parses_from_std_in(self, path_and_account_strings):
            " confirm Parser.main identifies accounts via std-in "
            path, account_strings = path_and_account_strings
            with path.open() as input_file:
                output = subprocess.check_output('parser/parser.py', 
                                                 stdin=input_file)
            assert output[:-1] == str(account_strings)

