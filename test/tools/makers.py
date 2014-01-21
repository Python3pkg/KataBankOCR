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
    def _victim(cls):
        """ return a list of entry lines and a random index from that list 

        provides a mutable target to abuse """
        victim_list = list(cls.valid())
        victim_line_index = random.choice(range(len(victim_list)))
        return victim_list, victim_line_index

    @classmethod
    def containing_non_string(cls):
        " return (an otherwise valid) tuple containing one non-string "
        victim_list, victim_line_index = cls._victim()
        victim_line = victim_list[victim_line_index]
        arbitrary_non_string_values = (0,1,-10,False,True,3.14,(),[],{},set())
        non_string_value = random.choice(arbitrary_non_string_values)
        victim_list[victim_line_index] = non_string_value
        return tuple(victim_list)

    @classmethod
    def abbreviated_string(cls):
        " return (an otherwise valid) tuple containing one abbreviated string "
        victim_list, victim_line_index = cls._victim()
        victim_line = victim_list[victim_line_index]
        new_line_length = random.choice(range(len(victim_line)))
        abbreviated_line = victim_line[:new_line_length]
        victim_list[victim_line_index] = abbreviated_line
        return tuple(victim_list)

    @classmethod
    def extended_string(cls):
        " return (an otherwise valid) tuple containing one elongated string "
        victim_list, victim_line_index = cls._victim()
        victim_line = victim_list[victim_line_index]
        additional_length = random.choice(range(len(victim_line))) + 1
        additional_text = victim_line[:additional_length]
        excessively_long_line = victim_line + additional_text
        victim_list[victim_line_index] = excessively_long_line
        return tuple(victim_list)

    @classmethod
    def non_empty_last_line(cls):
        " return (an otherwise valid) tuple containing a non-empty last line "
        victim_list, foo = cls._victim()
        victim_line_index = settings.lines_per_entry -1
        victim_line = victim_list[victim_line_index]
        if len(victim_line.strip()) == 0:
            additional_character = MakeFigureCharacter.non_blank_valid()
            replaced_character_position = random.choice(range(len(victim_line)))
            char,pos = additional_character, replaced_character_position
            altered_line = victim_line[:pos] + char + victim_line[pos+1:]
            victim_list[victim_line_index] = altered_line
        return tuple(victim_list)

class MakeInputFile:
    " collection of methods that each returns an input file for scannerparser "

    @classmethod
    def valid():
        " return a file representing 500 random valid account numbers "
        pass
