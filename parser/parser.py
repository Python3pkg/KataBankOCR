#!/usr/bin/env python

" The Parser module "

import settings

class ParserError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(ParserError):
    " Exception raised for errors in the input "
    def __init__(self,msg):
        self.message = msg

class Parser():
    " Parses file at path into account numbers and return them "

    def __init__(self,path):
        pass
