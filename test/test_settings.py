#!/usr/bin/env python

""" Test the settings file"""

import settings

setting_types = {int:('lines_per_entry',
                         'figures_per_entry',
                         'figure_width',
                         'characters_per_figure',),
                 tuple:('valid_figure_characters',),
                 dict:('figures',),
                 bool:('last_line_empty',),
                 }

def test_setting_existence():
    """ confirm each expected setting exists """
    for type in setting_types:
        for setting_name in setting_types[type]:
            assert settings.__dict__.has_key(setting_name)

def test_type_correctness():
    """ confirm each setting has the expected type """
    for type in setting_types:
        for setting_name in setting_types[type]:
            assert isinstance(settings.__dict__[setting_name],type)

""" Test the figures"""

figures = settings.figures

def test_uniqueness():
    """ confirm no duplicate figures exist """
    assert len(set(figures)) == len(figures)

def test_representativeness():
    """ confirm figures has exactly the expected values """
    assert set(figures.values()) == set(settings.values)

def test_length():
    """ confirm each figure contains the correct number of characters """
    for s in figures:
        assert len(s) == settings.characters_per_figure

def test_components():
    """ confirm each figure composed only of spaces, underscores, and pipes """
    chars = settings.valid_figure_characters
    for s in figures:
        assert set(chars).issuperset(s)



