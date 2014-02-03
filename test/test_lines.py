" Test the Lines module "

import pytest

import settings
from parser.errors import InputTypeError, InputLengthError
from parser.lines import Lines

class TestCheck:
    " test the Lines.check method "

    class TestType:
        " confirm Lines.check validates type "

        @pytest.fixture(params=(0, 1, -10, False, True, 'foo', '', (1,2,), {'a',}, set(), 3.14159))
        def non_list(self, request):
            " return an arbitrary non-list value "
            return request.param

        def test_with_non_list(self, non_list):
            " confirm Entry.check detects a non_list "
            pytest.raises(InputTypeError, Lines.check, non_list)

    class TestLength:
        " confirm Lines.check validates length "

        def test_with_empty_list(self):
            " confirm Parser recognizes an empty file "
            e = pytest.raises(InputLengthError, Lines.check, [])
            assert e.value.message == 'nothing to parse'

        def test_with_abbreviated_list(self):
            " confirm Lines.check recognizes insufficient length list "
            if settings.lines_per_entry > 1:
                entry_count = settings.approximate_entries_per_file
                line_count = entry_count * settings.lines_per_entry
                lines = ['\n'] * line_count
                abbreviated_list = lines[:-1]
                e = pytest.raises(InputLengthError, Lines.check, abbreviated_list)
                assert e.value.message == 'file ended mid entry'

class TestEntriesFromLines:
    " test the Lines.entries_from_lines method "

    @pytest.mark.parametrize('lines, entries',(
            (['a', 'b', 'c', 'd'], [['a', 'b', 'c', 'd'],]),
            ([1,2,3,4,5,6,7,8,], [[1,2,3,4],[5,6,7,8],]),
            ([1,2,3,4,5,6,7,8,9,10,11,12], [[1,2,3,4],[5,6,7,8],[9,10,11,12]]),
            ))
    def test_correctly_splits_entries_from_lines(self, lines, entries):
        " confirm Lines.entries_from_lines splits Lines into Entries "
        expected = entries
        found = Lines.entries_from_lines(lines)
        assert expected == found
