#!/usr/bin/env python

import random

from settings import characters_per_figure as valid_length
from settings import valid_figure_characters as valid_chars
from settings import figures

from tools.makers.figure_character import MakeFigureCharacter
class MakeFigureString:
    " collection of methods that each return a figure string "

    vfc = MakeFigureCharacter.valid

    bad_characters = ['*','-','I','~']
    for bad_character in bad_characters:
        assert isinstance(bad_character,str) and len(bad_character) == 1
        assert bad_character not in valid_chars

    @classmethod
    def too_short(cls):
        " return a random string of insufficient length "
        length = random.choice(range(1, valid_length))
        return ''.join(cls.vfc() for i in range(length))

    @classmethod
    def too_long(cls):
        " return a random string of excessive length "
        L = valid_length
        length = random.choice(range(L + 1, L * 2))
        return ''.join(cls.vfc() for i in range(length))

    @classmethod
    def adulterated(cls):
        " return random string containing at least one bad character "
        good_string = cls.known()
        bad_character = random.choice(cls.bad_characters)
        victim_character = random.choice(good_string)
        return good_string.replace(victim_character,bad_character)

    @classmethod
    def unknown(cls):
        " return random valid string not found in figures "
        while True:
            fs = ''.join(cls.vfc() for i in range(valid_length))
            if fs not in figures.keys():
                return fs

    @classmethod
    def known(cls):
        " return a random valid figure format from figures "
        return random.choice(figures.keys())
