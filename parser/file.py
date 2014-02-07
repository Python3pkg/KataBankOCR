import fileinput

import settings
from validators import Validate

class File():
    " Methods related to checking, reading, and grouping lines to Entries "

    @classmethod
    def lines_from_path(cls, path='-'):
        " yield lines from file at path or (default of) StdIn "
        for line in fileinput.input(path):
            yield str(line).rstrip('\n')

    @classmethod
    def validate_iterator(cls, lines):
        " confirm we can iterate over lines "
        Validate.iterable(lines)  # TODO: remove this

    @classmethod
    def entries_from_lines(cls, lines):
        " group Entry lines from Lines "
        entry = []
        for line in lines:
            entry.append(line)
            if len(entry) == settings.lines_per_entry:
                yield entry
                entry = []


