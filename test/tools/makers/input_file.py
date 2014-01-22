#!/usr/bin/env python

class MakeInputFile:
    " methods to create an input file and return its path "

    @classmethod
    def write(cls,tmpdir,lines):
        " write lines to temp file and return path "
        path = tmpdir.join('input_file.txt')
        F = path.open('w')
        for line in lines:
            F.write(line+'\n')
        F.close()
        return path

