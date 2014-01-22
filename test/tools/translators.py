#!/usr/bin/env python

" Tools to assist with testing "

import settings

def numeral_to_figure_string(numeral):
    " return the figure string that represents the given numeral "
    assert numeral in settings.figures.values()
    for figure in settings.figures:
        if settings.figures[figure] == numeral:
            return figure

def account_string_to_lines(account_string):
    " return the tuple of lines that represents the given account string "
    figure_strings = [numeral_to_figure_string(n) for n in account_string]
    lines = []
    for line_index in range(settings.lines_per_entry):
        line = ''
        for figure_index in range(len(figure_strings)):
            figure_string = figure_strings[figure_index]
            first_char_index = line_index * settings.figure_width
            last_char_index = first_char_index + settings.figure_width
            substring = figure_string[first_char_index:last_char_index]
            line += substring
        lines.append(line)
    return tuple(lines)

