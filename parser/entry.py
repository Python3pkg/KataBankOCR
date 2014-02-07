import settings
from functools import partial

from validators import Validate
from errors import InputError
from figure import Figure

class Entry():
    " A list (of lines/strings) that represents an Account "

    @classmethod
    def validate_input(cls, entry):
        " raise InputError on list or element with bad type or length "
        Validate.type(list, entry, 'Entry Input')
        Validate.length(settings.lines_per_entry, entry, 'Entry Input')
        Validate.element_types(str, entry, 'Entry Element')
        Validate.element_lengths(settings.strokes_per_line, entry, 'Entry Line')

    @classmethod
    def figures_from_entry(cls, entry):
        " return Figures within Entry "
        lists_of_substrings_by_line = map(cls._substrings_from_line, entry)
        figure_strings = zip(*lists_of_substrings_by_line)
        figures = map(''.join, figure_strings)
        return figures

    @classmethod
    def _substrings_from_line(cls, line):
        " return list of Substrings within a single Line "
        substring = partial(cls._figure_substring_from_line, line=line)
        return map(substring, range(settings.figures_per_entry))

    @classmethod
    def _figure_substring_from_line(cls, figure_index, line):
        " return the Strokes of a figure found within a Line "
        start_index = figure_index * settings.strokes_per_substring
        end_index = start_index + settings.strokes_per_substring
        return line[start_index:end_index]

    @classmethod
    def account_from_numerals(cls, numerals):
        " return Account by joining Numerals "
        return ''.join(numerals)

    @classmethod
    def result_from_numerals(cls, numerals):
        " return result string of Account and Status "
        account = cls.account_from_numerals(numerals)
        problem = _get_problem(account)
        if problem:
            return account + problem
        return account

def _get_problem(account):
    " return appropriate problem status for the Account "
    if settings.illegible_numeral in account:
        return settings.illegible_status
    elif not settings.checksum(account):
        return settings.invalid_status
    return None
