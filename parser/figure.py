import settings
from errors import InputError
from validators import validate_type, validate_length

class Figure():
    """ A collection of Strokes (stored as a string) that represents
    a single Numeral """

    def __init__(self, input):
        " validate input as Figure and identify Numeral "
        figure = self._validate_input(input)
        self.numeral = self._to_numeral(figure)

    def _validate_input(self, input):
        " confirm type, length, and stroke composition or raise an error "
        validate_type(str, input, 'Figure input')
        validate_length(settings.strokes_per_figure, input, 'Figure')
        self._validate_strokes(input)
        return input
        
    def _validate_strokes(self, input):
        " confirm Figure composed only of valid Strokes "
        invalid_strokes = set(input) - set(settings.valid_strokes)
        if invalid_strokes:
            invalid_strokes = ''.join(sorted(list(invalid_strokes)))
            msg = 'Figure "%s" contains non-Stroke element(s): %s'
            raise(InputError(msg % (input, invalid_strokes)))

    def _to_numeral(self, figure):
        " find figure in settings dict or raise InputError "
        if figure in settings.figures:
            return settings.figures[figure]
        return settings.illegible_numeral

