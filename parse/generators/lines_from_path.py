import fileinput

def lines_from_path(path):
    "generator that yields Lines from file at path or (default of) StdIn"
    for line in fileinput.input(path):
        yield str(line).rstrip('\n')
    fileinput.close()

