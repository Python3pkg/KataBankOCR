"generator that yields SuperPositions and the functions that support it"
from itertools import repeat

import settings
from validators import Validate

def superpositions_from_figures(figures):
    "generator that consumes Figures and yields SuperPositions"
    for figure in figures:
        _validate_figure(figure)
        yield _superposition_from_figure(figure)

def _validate_figure(figure):
    "confirm figure type, length, and composition or raise ValueError"
    Validate.type(basestring, figure, 'Figure')
    Validate.length(settings.strokes_per_figure, figure, 'Figure')
    Validate.composition(settings.valid_strokes, figure, 'Figure')

def _superposition_from_figure(figure):
    "return Superposition represented by Figure"
    d = {}
    for valid_figure, numeral in settings.figures.items():
        d.setdefault(_count_differences(figure, valid_figure), set()).add(numeral)
    return d

def _count_differences(figure_a, figure_b):
    "return count of differing strokes between two figures"
    stroke_from_each_figure = zip(figure_a, figure_b)
    return len(['' for (a, b) in stroke_from_each_figure if a != b])

