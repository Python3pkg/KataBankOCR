import settings

from validators import validate_input_length, validate_input_type
from errors import InputError
from figure import Figure

class Entry():
    " A list (of lines/strings) that represents an account string "

    def __init__(self,input):
        """ receive, sanitize, & validate entry lines (a list of strings)
        and then determine the account string represented by those lines """
        entry_list = self._sanitize_and_validate_input(input)
        self.account_string = self._account_string_from_entry_list(entry_list)
        self.problem = self._get_problem()

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
        one_char_too_long = lambda line: len(line) == settings.line_length + 1
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
            validate_input_length(lines[i], settings.line_length,
                                  'Entry line %d' % i)

    def _validate_last_line_empty(self, lines):
        " confirm last line in list contains only whitespace "
        last_line = lines[settings.lines_per_entry-1]
        if settings.last_line_empty and not last_line.isspace():
            raise(InputError('Last line in list not empty'))

    def _account_string_from_entry_list(self, entry_list):
        " parse lines into an account string "
        figures = map(Figure, self._figure_strings_from_lines(entry_list))
        return ''.join(f.account_character for f in figures)

    def _figure_strings_from_lines(self, lines):
        " build figure strings from substrings in each line "
        return map(''.join, zip(*map(self._substrings_from_line, lines)))

    def _substrings_from_line(self, line):
        " return list of figure substrings within a single line "
        sub_from_line = self._figure_substring_from_line
        substring = lambda figure_index: sub_from_line(line, figure_index)
        return map(substring, range(settings.figures_per_entry))

    def _figure_substring_from_line(self, line, figure_index):
        " return the portion of a figure string within a line "
        start_index = figure_index * settings.figure_width
        return line[start_index:start_index + settings.figure_width]

    def _get_problem(self):
        " return appropriate problem marker for the account string "
        if settings.illegible_account_character in self.account_string:
            return settings.illegible_account_marker
        elif not settings.checksum(self.account_string):
            return settings.invalid_account_marker
        return None
