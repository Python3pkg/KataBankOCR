#!/usr/bin/env python

import fileinput

from errors import InputError

class Parser():
    """ Take 4 optional callable arguments and use them to validate input,
    split it into elements, parse each element, finish, and return results """

    def __init__(self, checker=None, splitter=None, subparser=None, finisher=None):
        " store and validate received functions and parser "
        self.checker = checker      # function that validates input
        self.splitter = splitter    # function that prepares elements from input
        self.subparser = subparser  # parser applied to each element of input
        self.finisher = finisher    # function that performs final processing of results
        self._validate_arguments()

    def __call__(self, some_input):
        " check, split, subparse, finish, and return output"
        if self.checker:
            self.checker(some_input)
        output = some_input
        if self.splitter:
            output = self.splitter(output)
        if self.subparser:
            output = map(self.subparser, output)
        if self.finisher:
            output = self.finisher(output)
        return output

    def _validate_arguments(self):
        " validate each argument as None or callable "
        arguments = (self.checker, self.splitter, self.subparser, self.finisher)
        for arg in arguments:
            if arg is not None and not callable(arg):
                message = '"%s" not callable.' % repr(arg)
                raise(InputError(message))

def main():
    # TODO: Accept path via docopts.
    pass

"""
    entries_from_lines = Parser(
        checker=validate_iterator
        splitter=validate_iterator
        subparser=validate_iterator
        finisher=validate_iterator
        )
    lines = File.lines_from_path()  # No path given, so use StdIn
    entries = entries_from_lines(lines)
    results = results_from_entries(entries)
    with File.
    for result in results:
    results = Entry.result_from_entry

"""

if __name__ == "__main__":
    main()

