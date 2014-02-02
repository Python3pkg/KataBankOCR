import settings
from errors import InputError
from validators import validate_type, validate_length

def _validate_strokes(string):
    " confirm Figure composed only of valid Strokes "
    invalid_strokes = set(string) - set(settings.valid_strokes)
    if invalid_strokes:
        invalid_strokes = ''.join(sorted(list(invalid_strokes)))
        msg = 'Figure "%s" contains non-Stroke element(s): %s'
        raise(InputError(msg % (string, invalid_strokes)))

class Figure():
    """ A collection of Strokes (stored as a string) that represents
    a single Numeral """

    @staticmethod
    def check(string):
        " confirm type, length, and strokes or raise InputError "
        validate_type(str, string, 'Figure input')
        validate_length(settings.strokes_per_figure, string, 'Figure')
        _validate_strokes(string)

    @staticmethod
    def get_numeral(string):
        " find figure in settings dict or raise InputError "
        if string in settings.figures:
            return settings.figures[string]
        return settings.illegible_numeral

