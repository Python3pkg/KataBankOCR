"methods that provide values for testing and functions to support them"

import random
import fileinput
from functools import partial

from parse import settings

from common_tools import get_one_or_more, replace_element
import input_files

class Numerals:
    "functions that provide Numerals for testing"

    @classmethod
    def get_random(cls, count=None):
        "return random valid Numeral[s]"
        getter = lambda: random.choice(cls.valid())
        return get_one_or_more(getter, count)

    @staticmethod
    def valid():
        "return ordered list of valid Numerals"
        return sorted(list(settings.valid_numerals))

class Accounts:
    "functions that provide Accounts for testing"

    @staticmethod
    def get_random(count=None):
        "return random Account[s]"
        getter = lambda: ''.join(Numerals.get_random(settings.figures_per_entry))
        return get_one_or_more(getter, count)

    @staticmethod
    def of_example_accounts():
        "return Accounts from superpositions of example Accounts"
        return [t[1] for t in _example_accounts()]

    @staticmethod
    def of_basic_input_file():
        "return Accounts from basic input file"
        return input_files.Basic.accounts

class Figures:
    "methods that provide Figures for testing"

    @staticmethod
    def get_random(count=None):
        "return random valid Figure[s]"
        getter = lambda: random.choice(settings.figures.keys())
        return get_one_or_more(getter, count)

    @staticmethod
    def from_numeral(numeral):
        "return the Figure that represents the given Numeral"
        for figure in settings.figures:
            if settings.figures[figure] == numeral:
                return figure

    @classmethod
    def from_account(cls,account):
        "return the Figures that represent the given Account"
        return map(cls.from_numeral, list(account))

    @staticmethod
    def valid():
        "return ordered list of figures representing Numerals 0-9"
        figures = []
        for i in range(10):
            for figure, numeral in settings.figures.items():
                if int(numeral) == i:
                    figures.append(figure)
        return figures

    @staticmethod
    def flawed():
        "return ordered list of flawed Figures"
        figures = [f for f, _ in _flawed_figures()]
        return sorted(figures)

class Lines:
    "methods that provide Lines for testing"

    @classmethod
    def of_basic_input_file(cls):
        "return Lines from basic input file"
        lines = []
        for line in fileinput.input(input_files.Basic.path):
            line = str(line).rstrip('\n')
            lines.append(line)
        return lines

class Entries:
    "methods that provide Entries for testing"

    @classmethod
    def get_random(cls, count=None):
        "return one or more random Entries"
        getter = lambda: cls.from_account(Accounts.get_random())
        return get_one_or_more(getter, count)

    @classmethod
    def from_account(cls, account):
        "return the Entry (list of lines) that represents the given Account"
        figures = Figures.from_account(account)
        return cls.from_figures(figures)

    @classmethod
    def from_figures(cls, figures):
        "return the Entry (list of lines) that contains the given Figures"
        get_line = partial(cls._line_from_figures, figures=figures)
        return map(get_line, range(settings.lines_per_entry))

    @staticmethod
    def _line_from_figures(line_index, figures):
        "return a Line composed of Figures substrings"
        first_figure_stroke = line_index * settings.strokes_per_substring
        last_figure_stroke = first_figure_stroke + settings.strokes_per_substring
        slice_indexes = (first_figure_stroke, last_figure_stroke)
        figure_substrings = [figure[slice(*slice_indexes)] for figure in figures]
        line = ''.join(figure_substrings)
        return line

    @classmethod
    def get_flawed(cls, count=None):
        "return one or more random Entries that each contain a flawed Figure"
        return get_one_or_more(cls._get_one_flawed, count)

    @classmethod
    def _get_one_flawed(cls):
        "return one Entry that includes a single flawed Figure"
        figures = Figures.get_random(settings.figures_per_entry)
        flawed_figure = random.choice(Figures.flawed())
        figures = replace_element(figures, flawed_figure)
        return cls.from_figures(figures)

    @classmethod
    def of_basic_input_file(cls):
        "return Entries from basic input file"
        return map(cls.from_account, Accounts.of_basic_input_file())

class Superpositions:
    "methods that provide Superpositions for testing"

    @classmethod
    def from_numeral(cls, numeral):
        "return Superposition of Figure representing Numeral"
        superposition = cls.of_valid_figures()[int(numeral)]
        return superposition

    @classmethod
    def from_account(cls, account):
        "return list of Superpositions from Figures in Account's Numerals"
        return map(cls.from_numeral, account)

    @staticmethod
    def from_figure(figure):
        "return Superposition of Figure"
        d = dict(zip(Figures.figures, Figures.superpositions))
        return d[figure]

    @staticmethod
    def of_valid_figures():
        "return list of Superposisions of Figures representing Numerals 0-9"
        return [
        {0: {'0'}, 1: {'8'}, 2: {'6', '9'}, 3: {'2', '3', '5', '7'}, 4:{'1', '4'}},
        {0: {'1'}, 1: {'7'}, 2: {'4'}, 3: {'3'}, 4: {'0', '9'}, 5: {'2', '5', '8'}, 6: {'6'}},
        {0: {'2'}, 2: {'3', '8'}, 3: {'0', '6', '9'}, 4: {'5', '7'}, 5: {'1', '4'}},
        {0: {'3'}, 1: {'9'}, 2: {'2', '5', '7', '8'}, 3: {'0', '1', '4', '6'}},
        {0: {'4'}, 2: {'1', '9'}, 3: {'3', '5', '7', '8'}, 4: {'0', '6'}, 5: {'2'}},
        {0: {'5'}, 1: {'6', '9'}, 2: {'3', '8'}, 3: {'0', '4'}, 4: {'2', '7'}, 5: {'1'}},
        {0: {'6'}, 1: {'5', '8'}, 2: {'0', '9'}, 3: {'2', '3'}, 4: {'4'}, 5: {'7'}, 6: {'1'}},
        {0: {'7'}, 1: {'1'}, 2: {'3'}, 3: {'0', '4', '9'}, 4: {'2', '5', '8'}, 5: {'6'}},
        {0: {'8'}, 1: {'0', '6', '9'}, 2: {'2', '3', '5'}, 3: {'4'}, 4: {'7'}, 5: {'1'}},
        {0: {'9'}, 1: {'3', '5', '8'}, 2: {'0', '4', '6'}, 3: {'2', '7'}, 4: {'1'}},
        ]

    @classmethod
    def of_example_accounts(cls):
        "return Superpositions made from example accounts"
        example_accounts = [t[0] for t in _example_accounts()]
        return map(cls.from_account, example_accounts)

    @staticmethod
    def from_flawed_figures():
        "return Superpositions of flawed figures"
        return [s for _, s in _flawed_figures()]

class Results:
    "functions that provide Results for testing"
    
    @staticmethod
    def of_example_accounts():
        "return Results from example accounts"
        return [t[2] for t in _example_accounts()]

class ArbitraryValues:
    "functions that provide arbitrary values for testing"

    _all = [0, 1, -10, -999999999, 123456789, 3.14159, -.00000000001,
            False, True, [], (), {}, '', None, object, int, list, dict, bool,
            'abc', [1, 2, 3], {1:2}, {0}, (1, 2, 3), {1:'a', 2:'b'}]

    @classmethod
    def non_iterable(cls):
        "return a list of arbitrary values over which one cannot iterate"
        not_iterable = lambda v: not cls._iterable(v)
        return filter(not_iterable, cls._all)

    @staticmethod
    def _iterable(value):
        "return True if value iterable"
        try:
            iterator = iter(value)
            return True
        except TypeError:
            return False

    @classmethod
    def of_different_type(cls, value_or_type):
        "Return an arbitrary value not of value_or_type"
        avoided_type = cls._type(value_or_type)
        different_type = lambda value: not isinstance(value, avoided_type)
        return filter(different_type, cls._all)

    @staticmethod
    def _type(value_or_type):
        "return expected type"
        if isinstance(value_or_type, type):
            return value_or_type
        else:
            return type(value_or_type)

def _example_accounts():
    "return list of 3-tuples (account, account_from_superpositions, result)"
    return [
        ('123456789', '123456789', '123456789'),
        ('111111111', '711111111', '711111111'),
        ('777777777', '777777177', '777777177'),
        ('200000000', '200800000', '200800000'),
        ('333333333', '333393333', '333393333'),
        ('555555555', '555555555', '555555555 AMB'),
        ('666666666', '666666666', '666666666 AMB'),
        ('888888888', '888888888', '888888888 AMB'),
        ('999999999', '999999999', '999999999 AMB'),
        ('490067715', '490067715', '490067715 AMB'),
        ]

def _flawed_figures():
    "return dict of 2-tuples (flawed_figure, superposition)"
    return [
        ('   ' +
         ' _|' +
         '  |' +
         '   ', {1: {'1', '4'}, 2: {'3', '7'}, 3: {'9'}, 4: {'2', '5', '8'}, 5: {'0', '6'}}),
        ('   ' +
         '| |' +
         '|_|' +
         '   ', {1: {'0'}, 2: {'8'}, 3: {'1', '4', '6', '9'}, 4: {'2', '3', '5', '7'}}),
        (' _ ' +
         ' _ ' +
         ' _|' +
         '   ', {1: {'3', '5'}, 2: {'6', '9'}, 3: {'2', '7', '8'}, 4: {'0', '1', '4'}}),
        ]

