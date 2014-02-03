import settings

from validators import Validate
from errors import InputLengthError

class Lines():
    " A list (of lines/strings) that contains Entries "

    @classmethod
    def check(cls, lines):
        " confirm type and length of list "
        Validate.type(list, lines, 'Lines Input')
        cls._validate_line_count(len(lines))

    @classmethod
    def _validate_line_count(cls, count):
        " confirm appropriate number of lines "
        if count == 0: 
            raise(InputLengthError('nothing to parse'))
        elif count.__mod__(settings.lines_per_entry) != 0:
            raise(InputLengthError('file ended mid entry'))

    @classmethod
    def entries_from_lines(cls, lines):
        " return Entries within Lines "
        entry_indexes = range(0, len(lines), settings.lines_per_entry)
        entry_from_index = lambda index: lines[index:index + settings.lines_per_entry]
        return map(entry_from_index, entry_indexes)
