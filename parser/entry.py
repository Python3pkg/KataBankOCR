import settings

from validators import Validate
from errors import InputError
from figure import Figure

class Entry():
    " A list (of lines/strings) that represents an Account "

    @classmethod
    def check(cls, entry):
        " raise InputError on list or element with bad type or length "
        Validate.type(list, entry, 'Entry Input')
        Validate.length(settings.lines_per_entry, entry, 'Entry Input')
        Validate.element_types(str, entry, 'Entry Element')
        Validate.element_lengths(settings.strokes_per_line, entry, 'Entry Line')

    @classmethod
    def figures_from_entry(cls, entry):
        " return Figures within Entry "
        return map(''.join, zip(*map(cls._substrings_from_line, entry)))

    @classmethod
    def _substrings_from_line(cls, line):
        " return list of Substrings within a single Line "
        sub_from_line = cls._figure_substring_from_line
        substring = lambda figure_index: sub_from_line(line, figure_index)
        return map(substring, range(settings.figures_per_entry))

    @classmethod
    def _figure_substring_from_line(cls, line, figure_index):
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
        problem = cls._get_problem(account)
        if problem:
            return account + problem
        return account

    @classmethod
    def _get_problem(cls, account):
        " return appropriate problem flag for the Account "
        if settings.illegible_numeral in account:
            return settings.illegible_flag
        elif not settings.checksum(account):
            return settings.invalid_flag
        return None
