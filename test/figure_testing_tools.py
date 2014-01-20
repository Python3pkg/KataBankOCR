#!/usr/bin/env python

" Tools to assist with testing the figure module "

import random

import settings

def with_each(items):
    " decorate a function by calling it once for each item in iterable "
    def decorated_function(function):
        for i in items:
            function(i)
    return decorated_function

def gen_strings(requested_count,string_generator):
    " return a number of strings using the provided generator "
    generated_count = 0
    while generated_count <= requested_count:
        yield string_generator()
        generated_count += 1

def random_valid_character():
    " return a randomly selected valid figure character "
    return random.choice(settings.valid_figure_characters)

def random_valid_characters(length):
    " return a string built of randomly seleced valid figure characters "
    return ''.join(random_valid_character() for c in range(length))

# Arbitrary characters we hope don't exist in settings.valid_figure_characters
bad_characters = ['*','-','I','~']

def confirm_invalid_characters():
    " confirm none of the characers in bad_characters may appear in a figure "
    for bad_character in bad_characters:
        assert isinstance(bad_character,str)
        assert len(bad_character) == 1
        assert bad_character not in settings.valid_figure_characters

def random_valid_string():
    " return a random string of valid length with valid characters "
    return random_valid_characters(settings.characters_per_figure)

class StringType:

    @staticmethod
    def too_short():
        " return a random string of insufficient length "
        valid_length = settings.characters_per_figure
        possible_lengths = range(1, valid_length)
        length = random.choice(possible_lengths)
        return random_valid_characters(length)

    @staticmethod
    def too_long():
        " return a random string of excessive length "
        valid_length = settings.characters_per_figure
        possible_lengths = range(valid_length + 1, valid_length * 2)
        length = random.choice(possible_lengths)
        return random_valid_characters(length)

    @staticmethod
    def adulterated():
        " return random string containing at least one bad character "
        bad_character = random.choice(bad_characters)
        good_string = random_valid_string()
        victim_character = random.choice(good_string)
        return good_string.replace(victim_character,bad_character)

    @staticmethod
    def unrecognized():
        " return random valid string not found settings.figures "
        figure = random_valid_figure()
        while figure in settings.figures.keys():
            figure = random_valid_figure()
        return figure

    @staticmethod
    def recognized():
        " return a random valid figure format from settings.figures "
        return random.choice(settings.figures.keys())
