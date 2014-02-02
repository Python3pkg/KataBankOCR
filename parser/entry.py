import settings

from validators import validate_type, validate_length
from validators import validate_element_types, validate_element_lengths
from errors import InputError
from figure import Figure

class Entry():
    " A list (of lines/strings) that represents an Account "

    def __init__(self,input):
        """ receive, sanitize, & validate entry lines (a list of strings)
        and then determine the Account represented by those lines """
        entry_list = self._sanitize_and_validate(input)
        self.account = self._account_from_entry(entry_list)
        self.problem = self._get_problem()

    def _sanitize_and_validate(self, input):
        " confirm type, remove line-feeds, and validate lines "
        self._validate_input_as_list_of_strings(input)
        lines = self._trim_line_feeds_from_lines_as_necessary(input)
        self._validate_lines(lines)
        return lines

    def _validate_input_as_list_of_strings(self, input):
        validate_type(list, input, 'Entry Input')
        validate_element_types(str, input, 'Entry Element')

    def _trim_line_feeds_from_lines_as_necessary(self, lines):
        return map(self._trim_line_feed_if_necessary, lines)

    def _trim_line_feed_if_necessary(self, line):
        return line[:-1] if self._line_needs_trimmed(line) else line

    def _line_needs_trimmed(self, line):
        line_ends_in_line_feed = line[-1:] == '\n'
        line_one_char_too_long = len(line) == settings.strokes_per_line + 1
        return line_ends_in_line_feed and line_one_char_too_long

    def _validate_lines(self, lines):
        " validate valid line count, lengths, and last line empty "
        expected = settings.lines_per_entry
        validate_length(expected, lines, 'Entry line')
        validate_element_lengths(settings.strokes_per_line, lines, 'Entry Line')
        self._validate_last_line_empty(lines)

    def _validate_last_line_empty(self, lines):
        " confirm last line in Entry contains only whitespace "
        last_line = lines[settings.lines_per_entry-1]
        if settings.last_line_empty and not last_line.isspace():
            raise(InputError('Last line not empty'))

    def _account_from_entry(self, entry_list):
        " parse an Entry into an Account "
        numerals = map(Figure.get_numeral, self._figure_from_lines(entry_list))
        return ''.join(numerals)

    def _figure_from_lines(self, lines):
        " build a Figure from the Substrings in each Line "
        return map(''.join, zip(*map(self._substrings_from_line, lines)))

    def _substrings_from_line(self, line):
        " return list of Substrings within a single Line "
        sub_from_line = self._figure_substring_from_line
        substring = lambda figure_index: sub_from_line(line, figure_index)
        return map(substring, range(settings.figures_per_entry))

    def _figure_substring_from_line(self, line, figure_index):
        " return the Strokes of a figure found within a Line "
        start_index = figure_index * settings.strokes_per_substring
        end_index = start_index + settings.strokes_per_substring
        return line[start_index:end_index]

    def _get_problem(self):
        " return appropriate problem flag for the Account "
        if settings.illegible_numeral in self.account:
            return settings.illegible_flag
        elif not settings.checksum(self.account):
            return settings.invalid_flag
        return None
