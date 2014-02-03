#!/usr/bin/env python

#import fileinput
import io
import settings

from validators import Validate
from errors import InputLengthError

class Stream():
    " An input source providing lines "

    @classmethod
    def check(cls, stream):
        " raise InputError on non stream "
        Validate.type(io.TextIOWrapper, stream, 'Stream Input')

    @classmethod
    def trimmed_lines_from_stream(cls, stream):
        " read list lines from stream, trimming line-feeds as appropriate "
        lines = list(stream)
        lines = map(cls._trim_line_feed_if_necessary, lines)
        return lines

    @classmethod
    def _trim_line_feed_if_necessary(cls, line):
        return line[:-1] if cls._line_needs_trimmed(line) else line

    @classmethod
    def _line_needs_trimmed(cls, line):
        line_ends_in_line_feed = line[-1:] == '\n'
        line_one_char_too_long = len(line) == settings.strokes_per_line + 1
        return line_ends_in_line_feed and line_one_char_too_long

