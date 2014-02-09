"generator that yields Entries"

from itertools import islice

import settings

def entries_from_lines(lines):
    "generator that reads Lines and yields an Entry"
    entry = []
    for line in lines:
        entry.append(line)
        if len(entry) == settings.lines_per_entry:
            yield entry
            entry = []
    if entry:
        message = 'File ended mid-Entry. Partial Entry:%s' % str(entry)
        raise(ValueError(message))
