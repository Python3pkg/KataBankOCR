" functions used by multiple test modules "

from __future__ import print_function
import pytest
import random
import settings

def get_unknown_figure_string():
    " return string of good length & charset, not matching an account character "
    for i in range(100):
        figure_characters = list(random.choice(settings.figures.keys()))
        random.shuffle(figure_characters)
        figure_string = ''.join(figure_characters)
        if settings.last_line_empty:
            figure_string = figure_string[:-settings.figure_width]
            figure_string = figure_string + ' ' * settings.figure_width
        if figure_string not in settings.figures.keys():
            return figure_string
    raise ValueError('Failed to generate an unknown figure string')

def figure_string_from_account_character(account_character):
    " return the figure string that represents the given account character "
    for figure in settings.figures:
        if settings.figures[figure] == account_character:
            return figure
    return get_unknown_figure_string()

def entry_list_from_account_string(account_string):
    " return the list of lines that represents the given account string "
    figure_strings = map(figure_string_from_account_character, account_string)
    figure_indexes = range(settings.figures_per_entry)
    slice_indexes = lambda line_index: (line_index * settings.figure_width,
                                        (line_index + 1)  * settings.figure_width)
    substring = lambda fi, li: figure_strings[fi][slice(*slice_indexes(li))]
    line_substrings = lambda li: [substring(fi, li) for fi in figure_indexes]
    return map(''.join, map(line_substrings, range(settings.lines_per_entry)))

def file_path_from_entry_lists(tmpdir, entry_lists):
    " return path to a file containing the given entry lists "
    # flatten all lines from entry_lists to one list of lines
    lines = [line for entry_list in entry_lists for line in entry_list]
    path = tmpdir.join('input_file.txt')
    F = path.open('w')
    for line in lines:
        print(line, file=F)
    F.close()
    return path

def invalid_lengths(valid_length, multiplier=4):
    " the list of ints 0 to (valid_length * multiplier) excluding valid_length "
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

def fit_string_to_length(string, length):
    " return duplicated & abbreviated string such that len(string) == length "
    if len(string) == length:
        return string
    elif len(string) > length:
        return string[:length]
    # Still too short. Double it and recurse.
    return fit_string_to_length(string+string, length)

def adulterate_string(string, adulterant):
    " return a string with a random character replaced by adulterant "
    victim_character_index = random.choice(range(len(string)))
    return '%s%s%s' % (string[:victim_character_index],
                       adulterant,
                       string[victim_character_index + 1:])

