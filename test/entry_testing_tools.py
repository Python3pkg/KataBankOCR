#!/usr/bin/env python

" Tools to assist with testing the figure module "

import settings

from testing_tools import random_valid_character

arbitrary_non_string_values = (0,1,-10,False,True,3.14359,(),[],{},set())

# Some static valid entry lines and their represented account numbers
entries= {
    (' _  _  _  _  _  _  _  _  _ ',
     '| || || || || || || || || |',
     '|_||_||_||_||_||_||_||_||_|',
     '                           '):'000000000',
    ('                           ',
     '  |  |  |  |  |  |  |  |  |',
     '  |  |  |  |  |  |  |  |  |',
     '                           '):'111111111',
    (' _  _  _  _  _  _  _  _  _ ',
     ' _| _| _| _| _| _| _| _| _|',
     '|_ |_ |_ |_ |_ |_ |_ |_ |_ ',
     '                           '):'222222222',
    (' _  _  _  _  _  _  _  _  _ ',
     ' _| _| _| _| _| _| _| _| _|',
     ' _| _| _| _| _| _| _| _| _|',
     '                           '):'333333333',
    ('                           ',
     '|_||_||_||_||_||_||_||_||_|',
     '  |  |  |  |  |  |  |  |  |',
     '                           '):'444444444',
    (' _  _  _  _  _  _  _  _  _ ',
     '|_ |_ |_ |_ |_ |_ |_ |_ |_ ',
     ' _| _| _| _| _| _| _| _| _|',
     '                           '):'555555555',
    (' _  _  _  _  _  _  _  _  _ ',
     '|_ |_ |_ |_ |_ |_ |_ |_ |_ ',
     '|_||_||_||_||_||_||_||_||_|',
     '                           '):'666666666',
    (' _  _  _  _  _  _  _  _  _ ',
     '  |  |  |  |  |  |  |  |  |',
     '  |  |  |  |  |  |  |  |  |',
     '                           '):'777777777',
    (' _  _  _  _  _  _  _  _  _ ',
     '|_||_||_||_||_||_||_||_||_|',
     '|_||_||_||_||_||_||_||_||_|',
     '                           '):'888888888',
    (' _  _  _  _  _  _  _  _  _ ',
     '|_||_||_||_||_||_||_||_||_|',
     ' _| _| _| _| _| _| _| _| _|',
     '                           '):'999999999',
    ('    _  _     _  _  _  _  _ ',
     '  | _| _||_||_ |_   ||_||_|',
     '  ||_  _|  | _||_|  ||_| _|',
     '                           '):'123456789',
    }


def numeral_to_figure_string(numeral):
    assert numeral in settings.figures.values()
    for figure in settings.figures:
        if settings.figures[figure] == numeral:
            return figure

def account_number_to_lines(account_number):
    figure_strings = [numeral_to_figure_string(n) for n in account_number]
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
    return lines

def random_entry_lines():
    return account_number_to_lines(random_account_number)

