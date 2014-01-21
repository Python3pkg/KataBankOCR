#!/usr/bin/env python

" Generators to assist with testing "

import random

import settings

from testing_tools import account_number_to_lines

class GenCharacter:
    " collection of methods that each return a single character "

    class Account:
        " collection of methods that each return a figure character "

        values = settings.values
        
        @classmethod
        def valid(cls):
            " return a randomly selected valid account character "
            return random.choice(cls.values)

    class Figure:
        " collection of methods that each return a figure character "
    
        values = settings.valid_figure_characters
        
        @classmethod
        def valid(cls):
            " return a randomly selected valid figure character "
            return random.choice(cls.values)

        @classmethod
        def non_blank_valid(cls):
            " return a randomly selected non-blank valid figure character "
            while True:
                fc = GenCharacter.Figure.valid()
                if len(fc.strip()) > 0:
                    return fc

class GenString:
    " collection of methods that each return string "

    class AccountNumber:
        " collection of methods that each return an account number "

        @classmethod
        def valid(cls):
            " return an account number of valid length and character set "
            L = settings.figures_per_entry
            ac = GenCharacter.Account.valid
            return ''.join(random.choice(ac()) for i in range(L))

    class Figure:
        " collection of methods that each return a figure string "

        valid_length = settings.characters_per_figure
        vfc = GenCharacter.Figure.valid

        bad_characters = ['*','-','I','~']
        for bad_character in bad_characters:
            assert isinstance(bad_character,str) and len(bad_character) == 1
            assert bad_character not in settings.valid_figure_characters

        @classmethod
        def too_short(cls):
            " return a random string of insufficient length "
            length = random.choice(range(1, cls.valid_length))
            return ''.join(cls.vfc() for i in range(length))

        @classmethod
        def too_long(cls):
            " return a random string of excessive length "
            L = cls.valid_length
            length = random.choice(range(L + 1, L * 2))
            return ''.join(cls.vfc() for i in range(length))

        @classmethod
        def adulterated(cls):
            " return random string containing at least one bad character "
            good_string = GenString.Figure.known()
            bad_character = random.choice(cls.bad_characters)
            victim_character = random.choice(good_string)
            return good_string.replace(victim_character,bad_character)

        @classmethod
        def unknown(cls):
            " return random valid string not found settings.figures "
            while True:
                fs = ''.join(cls.vfc() for i in range(cls.valid_length))
                if fs not in settings.figures.keys():
                    return fs

        @classmethod
        def known(cls):
            " return a random valid figure format from settings.figures "
            return random.choice(settings.figures.keys())

class GenLines:
    " collection of methods that each return a tuple of entry lines "
    @classmethod
    def random_entry_lines(cls):
        " return a tuple of lines representing a random account number "
        account_number = GenString.Account.valid()
        return account_number_to_lines(account_number)

class GenFile:
    " collection of methods that each return a file "
    @classmethod
    def valid():
        " return a file representing 500 random valid account numbers "
        pass
