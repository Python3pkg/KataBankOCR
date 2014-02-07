" Test the File module "

import pytest

import settings
from parser.errors import InputTypeError, InputLengthError
from parser.file import File

class TestLineSourceFromPath:
    " test the File.lines_from_path method "

    @pytest.mark.parametrize('path, line_count',(("test/input_files/basic.txt", 44),
                                                 ("test/input_files/advanced.txt", 32),))
    def test_line_count_with_path(self, path, line_count):
        " confirm File.lines_from_path reads expected # of lines from path "
        expected = line_count
        source = File.lines_from_path(path)
        found = len(list(source))
        assert expected == found

    @pytest.mark.parametrize('path, line_length',(("test/input_files/basic.txt", 27),
                                                 ("test/input_files/advanced.txt", 27),))
    def test_line_length_with_path(self, path, line_length):
        " confirm File.lines_from_path trims line-feeds "
        lines = File.lines_from_path(path)
        expected = line_length
        for line in lines:
            found = len(line)
            assert expected == found

class TestValidateIterator:
    " test the File.validate_iterator method "

    @pytest.fixture(params=(0, 1, -10, False, True, 3.14159))
    def non_iterable(self, request):
        " return an arbitrary non-iterable value "
        return request.param

    def test_with_non_iterable(self, non_iterable):
        " confirm File.validate_iterator raises InputTypeError appropriately "
        e = pytest.raises(InputTypeError, File.validate_iterator, non_iterable)
        assert e.value.message == '"%s" not an interator' % str(non_iterable)

class TestEntriesFromLines:
    " test the File.entries_from_lines method "

    @pytest.mark.parametrize('lines, entries',(
            (['a', 'b', 'c', 'd'], [['a', 'b', 'c', 'd'],]),
            (['1', '2', '3', '4', '5', '6', '7', '8'], 
             [['1', '2', '3', '4'], ['5', '6', '7', '8'],]),
            (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'], 
             [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'],
              ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p'],]),
            ))
    def test_correctly_groups(self, lines, entries):
        " confirm File.entries_from_lines groups lines into Entries "
        expected = entries
        found = File.entries_from_lines(lines)
        assert expected == list(found)
