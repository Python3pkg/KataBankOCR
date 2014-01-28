" The Entry Module "

import settings

from validators import validate_input_length, validate_input_type
from errors import InputError
from figure import Figure

line_length = settings.figure_width * settings.figures_per_entry

class Entry():
    " A list of lines that represents an account string "

    def __init__(self,input):
        """ receive, sanitize, & validate entry lines (a list of strings)
        and then determine the account string represented by those lines """
        entry_list = self._sanitize_and_validate_input(input)
        self.account_string = self._lines_to_account_string(entry_list)

    def _sanitize_and_validate_input(self,input):
        " confirm type, remove line-feeds, and validate lines "
        self._validate_input_as_list_of_strings(input)
        lines = self._trim_line_feeds_from_lines_if_necessary(input)
        self._validate_lines(lines)
        return lines

    def _validate_input_as_list_of_strings(self,input):
        " confirm input takes form of a list of strings "
        validate_input_type(input, list, 'Entry input')
        self._validate_elements_all_strings(input)

    def _validate_elements_all_strings(self,input):
        " confirm elements of input all strings "
        for index in range(len(input)):
            validate_input_type(input[index], str,
                                'Entry list element %d' % index)

    def _trim_line_feeds_from_lines_if_necessary(self,lines):
        " remove any superfluous line-feeds "
        ends_in_line_feed = lambda line: line[-1:] == '\n'
        one_char_too_long = lambda line: len(line) == line_length + 1
        needs_trimming = lambda L: ends_in_line_feed(L) and one_char_too_long(L)
        return [line[:-1] if needs_trimming(line) else line for line in lines]

    def _validate_lines(self, lines):
        " validate valid line count, lengths, and last line empty "
        expected = settings.lines_per_entry
        validate_input_length(lines, expected, 'Entry list of lines')
        self._validate_line_lengths(lines)
        self._validate_last_line_empty(lines)

    def _validate_line_lengths(self, lines):
        " confirm each line in list has appropriate length "
        for i in range(len(lines)):
            validate_input_length(lines[i], line_length, 'Entry line %d' % i)

    def _validate_last_line_empty(self, lines):
        " confirm last line in list contains only whitespace "
        last_line = lines[settings.lines_per_entry-1]
        if settings.last_line_empty and not last_line.isspace():
            raise(InputError('last line in list not empty'))

    def _lines_to_account_string(self, lines):
        " lines >-> figure_strings >-> account_characters >-> an account_string "
        figure_strings = self._lines_to_figure_strings(lines)
        account_characters = [Figure(s).account_character for s in figure_strings]
        account_string = ''.join(c for c in account_characters)
        return account_string

    def _lines_to_figure_strings(self, lines):
        " build figure strings form substrings in each line "
        figure_indexes = range(settings.figures_per_entry)
        figure_strings = ['' for i in figure_indexes]
        for line in lines:
            for figure_index in figure_indexes:
                substring = self._figure_substring_from_line(line, figure_index)
                figure_strings[figure_index] += substring
        return figure_strings

    def _figure_substring_from_line(self, line, figure_index):
        " return a portion of a figure string from a line "
        start_index = figure_index * settings.figure_width
        return line[start_index:start_index + settings.figure_width]

