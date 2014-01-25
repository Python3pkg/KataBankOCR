#!/usr/bin/env python

" The Entry Module "

import settings

from validators import validate_input_length, validate_input_type
from errors import InputError
from figure import Figure

line_length = settings.figure_width * settings.figures_per_entry

class Entry():
    " A list of lines that represents an account string "

    def __init__(self,input):
        lines = self.sanitize_and_validate_input(input)
        self.account_string = self.parse_lines_to_account_string(lines)

    def sanitize_and_validate_input(self,input):
        " confirm type, remove line-feeds, and validate lines "
        lines = self.validate_input_as_list_of_strings(input)
        lines = self.trim_line_feeds_from_lines_if_necessary(lines)
        self.validate_lines(lines)
        return lines

    def validate_input_as_list_of_strings(self,input):
        " confirm input takes form of a list of strings "
        validate_input_type(input, list, 'Entry input')
        self.validate_elements_all_strings(input)
        return input

    def validate_elements_all_strings(self,input):
        " confirm elements of input all strings "
        for index in range(len(input)):
            validate_input_type(input[index], str, 
                                'Entry list element %d' % index)

    def trim_line_feeds_from_lines_if_necessary(self,lines):
        " remove any superfluous line-feeds "
        ends_in_line_feed = lambda line: line[-1:] == '\n'
        one_char_too_long = lambda line: len(line) == line_length + 1
        needs_trimming = lambda L: ends_in_line_feed(L) and one_char_too_long(L)
        return [line[:-1] if needs_trimming(line) else line for line in lines]

    def validate_lines(self, lines):
        " validate valid line count, lengths, and last line empty "
        expected = settings.lines_per_entry
        validate_input_length(lines, expected, 'Entry list of lines')
        self.validate_line_lengths(lines)
        self.validate_last_line_empty(lines)

    def validate_line_lengths(self, lines):
        " confirm each line in list has appropriate length "
        for i in range(len(lines)):
            validate_input_length(lines[i], line_length, 'Entry line %d' % i)

    def validate_last_line_empty(self, lines):
        " confirm last line in list contains only whitespace "
        last_line = lines[settings.lines_per_entry-1]
        if settings.last_line_empty and not last_line.isspace():
            raise(InputError('last line in list not empty'))

    def parse_lines_to_account_string(self, lines):
        " lines >-> figure_strings >-> figure_values >-> an account_string "
        figure_strings = self.parse_lines_to_figure_strings(lines)
        figure_values = [Figure(s).value for s in figure_strings]
        account_string = ''.join(v for v in figure_values)
        return account_string

    def parse_lines_to_figure_strings(self, lines):
        figure_count = settings.figures_per_entry
        figure_strings = ['' for i in range(figure_count)]
        for line_index in range(len(lines)):
            line = lines[line_index]
            for figure_index in range(figure_count):
                start_char_index = figure_index * settings.figure_width
                end_char_index = start_char_index + settings.figure_width
                substring = line[start_char_index:end_char_index]
                figure_strings[figure_index] += substring
        return figure_strings
