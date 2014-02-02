import pytest
import mock
import subprocess

import settings
from parser.errors import InputError
from parser.parser import Parser

from common_tools import file_path_from_entries
from common_tools import entry_from_account

class TestParser:
    " test the Parser class "

    @pytest.fixture
    def path_and_accounts(self, tmpdir, get_account):
        """ Create a temp file containing Entries. Return both its
        path and the list of Accounts represented by those Entries. """
        entry_count = settings.approximate_entries_per_file
        accounts = [get_account() for i in range(entry_count)]
        entries = map(entry_from_account, accounts)
        path = file_path_from_entries(tmpdir, entries)
        return path, accounts

    @pytest.fixture
    def path(self, path_and_accounts):
        " return a path to a valid input file "
        return path_and_accounts[0]

    class TestInit:
        " test Parser initialization "

        #TODO test init with no arg

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_with_multiple_arguments(self, arg_count):
            " confirm Entry requires fewer than 2 arguments "
            pytest.raises(TypeError, Parser, *range(arg_count))

        def test_instantiation_with_invalid_path(self, path='blsdfasf'):
            " confirm Parser instantiates when given a valid path "
            with mock.patch.object(Parser, '_get_lines'):
                with mock.patch.object(Parser, '_validate_line_count'):
                    with mock.patch.object(Parser, '_lines_from_accounts'):
                        assert isinstance(Parser(path), Parser)

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
            return file_path_from_entries(tmpdir, [])

        def test_with_empty_file(self, path_to_empty_file):
            " confirm Parser recognizes an empty file "
            e = pytest.raises(InputError, Parser, path_to_empty_file)
            assert e.value.message == 'nothing to parse'

    class TestFunctionality:
        " confirm Parser resolves file to list of correct Accounts "

        def test_correctly_parses_file(self, path_and_accounts):
            " confirm Parser finds Accounts within path's file "
            path, accounts = path_and_accounts
            assert Parser(path).accounts == accounts

        def test_main_parses_from_std_in(self, path_and_accounts):
            " confirm Parser.main identifies accounts via std-in "
            path, accounts = path_and_accounts
            with path.open() as input_file:
                output = subprocess.check_output('parser/parser.py', 
                                                 stdin=input_file)
            assert output[:-1] == str(accounts)
