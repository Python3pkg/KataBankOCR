#!/usr/bin/env python

import random

import settings

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

