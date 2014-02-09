"generator that yields Numerals and the functions that support it"

import settings
from validators import Validate

def numerals_from_figures(figures):
    "generator that consumes Figures and yields Numerals"
    for figure in figures:
        _validate_figure(figure)
        yield _numeral_from_figure(figure)

def _validate_figure(figure):
    "confirm figure type, length, and composition or raise ValueError"
    Validate.type(basestring, figure, 'Figure')
    Validate.length(settings.strokes_per_figure, figure, 'Figure')
    Validate.composition(settings.valid_strokes, figure, 'Figure')

def _numeral_from_figure(figure):
    "return Numeral represented by Figure"
    if figure in settings.figures:
        return settings.figures[figure]
    return settings.illegible_numeral

