" Various possible errors "

class InputError(Exception):
    " Exception raised for errors in the input "
    def __init__(self, msg):
        self.message = msg
    
class InputTypeError(InputError):
    " Exception raised for input of an unexpected type "
    def __init__(self, message):
        super(InputTypeError, self).__init__(message)

class InputLengthError(InputError):
    " Exception raised for input of an unexpected length "
    def __init__(self, message):
        super(InputLengthError, self).__init__(message)

