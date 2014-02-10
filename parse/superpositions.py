"generator that yields SuperPositions and the functions that support it"

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
    if figure in settings.figures:
        return settings.figures[figure]
    return settings.illegible_superposition
