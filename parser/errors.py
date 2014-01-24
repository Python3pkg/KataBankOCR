#!/usr/bin/env python

" Various possible errors "

class EntryError(Exception):
    " Base class for exceptions in this module "

class InputError(EntryError):
    " Base class for errors in the input "
    def __init__(self, msg):
        self.message = msg
    
class InputLengthError(InputError):
    " Exception raised for input of an unexpected length "
    def __init__(self, name, expected, found):
        msg = '%s of unexpected length. expected:%d. found:%d.'
        super(InputLengthError, self).__init__(msg % (name, expected, found))

class InputTypeError(InputError):
    " Exception raised for input of an unexpected type "
    def __init__(self, name, expected, found):
        msg = '%s of unexpected type. expected:%s. found:%s.'
        msg = msg % (name, str(expected), str(found))
        super(InputTypeError, self).__init__(msg)



