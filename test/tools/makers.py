#!/usr/bin/env python

" Class-grouped functions that create and return values useful for testing "

import random

import settings

from translators import account_number_to_lines

class MakeAccountCharacter:
    " collection of methods that each return an account character "

    @classmethod
    def valid(cls):
        " return a randomly selected valid account character "
        return random.choice(settings.values)

class MakeAccountString:
    " collection of methods that each return an account number string "

    @classmethod
    def valid(cls):
        " return an account number of valid length and character set "
        L = settings.figures_per_entry
        ac = MakeAccountCharacter.valid
        return ''.join(random.choice(ac()) for i in range(L))

class MakeFigureCharacter:
    " collection of methods that each return a figure character "

    @classmethod
    def valid(cls):
        " return a randomly selected valid figure character "
        return random.choice(settings.valid_figure_characters)

    # confirm at least one non-blank figure character exists
    assert len(''.join(settings.valid_figure_characters).strip()) > 0

    @classmethod
    def non_blank_valid(cls):
        " return a randomly selected non-blank valid figure character "
        while True:
            fc = cls.valid()
            if len(fc.strip()) > 0:
                return fc

class MakeFigureString:
    " collection of methods that each return a figure string "

    valid_length = settings.characters_per_figure
    vfc = MakeFigureCharacter.valid

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
        good_string = MakeFigureString.known()
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

class MakeEntryLines:
    " collection of methods that each return a tuple of entry lines "

    @classmethod
    def valid(cls):
        " return a tuple of lines representing a random account number "
        account_number = MakeAccountString.valid()
        return account_number_to_lines(account_number)

    @classmethod
    def _altered(cls,func,victim_line_index=None):
        " make a valid tuple of lines, func a [random] line, return tuple "
        victim_list = list(cls.valid())
        if victim_line_index is None:
            victim_line_index = random.choice(range(len(victim_list)))
        victim_list[victim_line_index] = func(victim_list[victim_line_index])
        return tuple(victim_list)

    @classmethod
    def containing_non_string(cls):
        " return (an otherwise valid) tuple containing one non-string "
        arbitrary_non_string_values = (0,1,-10,False,True,3.14,(),[],{},set())
        non_string_value = random.choice(arbitrary_non_string_values)
        return cls._altered(lambda L:non_string_value)

    @classmethod
    def abbreviated_string(cls):
        " return (an otherwise valid) tuple containing one abbreviated string "
        line_length = settings.figures_per_entry * settings.figure_width
        new_line_length = random.choice(range(line_length))
        return cls._altered(lambda L:L[new_line_length])

    @classmethod
    def extended_string(cls):
        " return (an otherwise valid) tuple containing one extended string "
        def extend_line(line):
            additional_length = random.choice(range(len(line))) + 1
            additional_text = line[:additional_length]
            return line + additional_text
        return cls._altered(extend_line)

    @classmethod
    def non_empty_last_line(cls):
        " return (an otherwise valid) tuple containing a non-empty last line "
        def adulterate_line(line):
            if len(line.strip()) == 0:
                new_char = MakeFigureCharacter.non_blank_valid()
                char_index = random.choice(range(len(line)))
                line = line[:char_index] + new_char + line[char_index+1:]
            return line
        return cls._altered(adulterate_line, settings.lines_per_entry - 1)

class MakeInputFile:
    " collection of methods that each returns an input file for scannerparser "

    @classmethod
    def valid():
        " return a file representing 500 random valid account numbers "
        pass
