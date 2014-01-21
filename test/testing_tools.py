#!/usr/bin/env python

" Tools to assist with testing the figure module "

import random

import settings

def random_valid_character():
    " return a randomly selected valid figure character "
    return random.choice(settings.valid_figure_characters)

def repeats(count):
    " decorator that runs a function repeatedly "
    def decorator(function):
        def decorated_function(*args, **kwargs):
            for i in range(count):
                function(*args, **kwargs)
        return decorated_function
    return decorator
