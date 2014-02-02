import settings
from errors import InputError
from validators import Validate

class Figure():
    " Strokes (stored as a string) that represent a single Numeral "

    @classmethod
    def check(cls, strokes):
        " confirm type, length, and composition or raise InputError "
        Validate.type(str, strokes, 'Figure input')
        Validate.length(settings.strokes_per_figure, strokes, 'Figure')
        cls._check_composition(strokes)

    @classmethod
    def _check_composition(cls, strokes):
        " confirm Figure composed only of valid Strokes "
        found_strokes = set(strokes)
        invalid_strokes = found_strokes - set(settings.valid_strokes)
        if invalid_strokes:
            sorted_invalid_strokes = ''.join(sorted(list(invalid_strokes)))
            msg = 'Figure "%s" contains non-Stroke element(s): %s'
            raise(InputError(msg % (strokes, sorted_invalid_strokes)))

    @classmethod
    def numeral_from_figure(cls, figure):
        " return Numeral represented by Figure "
        if figure in settings.figures:
            return settings.figures[figure]
        return settings.illegible_numeral

