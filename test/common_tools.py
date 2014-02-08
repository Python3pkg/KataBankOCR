" functions used by multiple test modules "

from __future__ import print_function
import pytest
import random
from itertools import chain

import settings

def get_unknown_figure():
    " return Figure of valid length & Strokes, but no matching Numeral "
    for i in range(100):
        valid_figures = settings.figures.keys()
        strokes = list(random.choice(valid_figures))
        random.shuffle(strokes)
        figure = ''.join(strokes)
        if figure not in valid_figures:
            return figure
    raise ValueError('Failed to generate an unknown figure')

def figure_from_numeral(numeral):
    " return the Figure that represents the given Numeral "
    for figure in settings.figures:
        if settings.figures[figure] == numeral:
            return figure
    return get_unknown_figure()

def figures_from_account(account):
    " return the Figures that represent the given Account "
    return map(figure_from_numeral, list(account))

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
    " return duplicated & abbreviated value such that len(value) == length "
    if len(value) == length:
        return value
    elif len(value) > length:
        return value[:length]
    # Still too short. Double it and recurse.
    return fit_to_length(value + value, length)

def replace_element(target, new_element, target_index=None):
    " Return string or list after replacing a [random] element "
    assert isinstance(target, basestring) or isinstance(target, list)
    if target_index is None:
        target_index = random.randrange(0, len(target))
    if isinstance(target, basestring):
        return replace_character_in_string(target, target_index, new_element)
    elif isinstance(target, list):
        target[target_index] = new_element
        return target
    else:
        raise ValuError('replace_random_element received "%s" ' % target +
                        "instead of a string or list.")

def replace_character_in_string(string, index, new_character):
    " Return string after replacing a character "
    return '%s%s%s' % (string[:index], new_character, string[index + 1:])

def replace_element_in_list(target_list, index, new_element):
    " Return list after replacing an element "
    return target_list[:index] + [new_element,] + target_list[index + 1:]

def flatten(iterable_of_iterables):
    " flatten one level of nested iterables "
    return chain.from_iterable(iterable_of_iterables)

