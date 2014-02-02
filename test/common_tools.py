" functions used by multiple test modules "

from __future__ import print_function
import pytest
import random
import settings

def get_unknown_figure():
    " return Figure of valid length & Strokes, but no matching Numeral "
    for i in range(100):
        figure_characters = list(random.choice(settings.figures.keys()))
        random.shuffle(figure_characters)
        figure = ''.join(figure_characters)
        if settings.last_line_empty:
            figure = figure[:-settings.strokes_per_substring]
            figure = figure + ' ' * settings.strokes_per_substring
        if figure not in settings.figures.keys():
            return figure
    raise ValueError('Failed to generate an unknown figure string')

def figure_from_numeral(numeral):
    " return the Figure that represents the given Numeral "
    for figure in settings.figures:
        if settings.figures[figure] == numeral:
            return figure
    return get_unknown_figure()

def entry_from_account(account):
    " return the Entry (list of lines) that represents the given Account "
    figures = map(figure_from_numeral, account)
    figure_indexes = range(settings.figures_per_entry)
    slice_indexes = lambda line_index: (line_index * settings.strokes_per_substring,
                                        (line_index + 1)  * settings.strokes_per_substring)
    substring = lambda fi, li: figures[fi][slice(*slice_indexes(li))]
    line_substrings = lambda li: [substring(fi, li) for fi in figure_indexes]
    return map(''.join, map(line_substrings, range(settings.lines_per_entry)))

def file_path_from_entries(tmpdir, entries):
    " return path to a file containing the given Entry "
    lines = [line for entry in entries for line in entry]
    path = tmpdir.join('input_file.txt')
    with path.open('w') as F:
        for line in lines:
            print(line, file=F)
    return path

def invalid_lengths(valid_length, multiplier=4):
    " the list of ints 0 to (valid_length * multiplier) excluding valid_length "
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

def fit_to_length(value, length):
    " return duplicated & abbreviated version such that len(value) == length "
    if len(value) == length:
        return value
    elif len(value) > length:
        return value[:length]
    # Still too short. Double it and recurse.
    return fit_to_length(value+value, length)

def adulterate_string(string, adulterant):
    " return a string with a random character replaced by adulterant "
    victim_character_index = random.choice(range(len(string)))
    return '%s%s%s' % (string[:victim_character_index],
                       adulterant,
                       string[victim_character_index + 1:])

