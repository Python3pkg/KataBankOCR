#!/usr/bin/env python

" Tools to assist with testing "

import random

import settings

def random_valid_character():
    " return a randomly selected valid figure character "
    return random.choice(settings.valid_figure_characters)

def random_non_blank_valid_character():
    while True:
        rvc = random_valid_character()
        if len(rvc.strip()) > 0:
            return rvc

def random_account_number():
    " return an account number of appropriate length and character set "
    length = settings.figures_per_entry
    return ''.join(random.choice(settings.values) for i in range(length))

def repeats(count):
    " decorator that runs a function repeatedly "
    def decorator(function):
        def decorated_function(*args, **kwargs):
            for i in range(count):
                function(*args, **kwargs)
        return decorated_function
    return decorator
