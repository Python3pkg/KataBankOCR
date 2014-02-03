" Test the Stream module "

import pytest
import io

import settings
from parser.errors import InputTypeError
from parser.stream import Stream

class TestCheck:
    " test the Stream.check method "

    class TestType:
        " confirm Stream.check validates type "

        @pytest.fixture(params=(0, 1, -1, False, True, 'foo', '',
                                [],  (1,2,), {'a',}, set(), 3.14159))
        def non_stream(self, request):
            " return an arbitrary non-stream value "
            return request.param

        def test_with_non_stream(self, non_stream):
            " confirm Stream.check detects a non_stream "
            pytest.raises(InputTypeError, Stream.check, non_stream)

class TestTrimmedLinesFromStream:
    " test the Stream.trimmed_lines_from_stream method "

    @pytest.mark.parametrize('path, line_count',(('test/input_files/basic.txt', 44),
                                                 ('test/input_files/advanced.txt', 32),))
    def test_line_count_with_basic_input(self, path, line_count):
        " confirm Stream.trimmed_lines_from_stream reads correct line count "
        stream = io.open(path)
        expected = line_count
        lines = Stream.trimmed_lines_from_stream(stream)
        found = len(lines)
        assert expected == found

    def test_linefeeds_trimmed_with_basic_input(self):
        " confirm Stream.trimmed_lines_from_stream reads and trims line-feeds "
        path = 'test/input_files/basic.txt'
        stream = io.open(path)
        expected = settings.strokes_per_line
        lines = Stream.trimmed_lines_from_stream(stream)
        found = len(lines[0])
        assert expected == found
        
