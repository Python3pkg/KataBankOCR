" Static values that restating the problem definition"

# An Entry consists of a list of lines (as strings)
# An Entry has a defined number of lines
lines_per_entry = 4
# An Entry has only whitespace in its final line
last_line_empty = True
# An Entry represents an Account string composed of account characters

# The four lines in this example entry represent the account string '123456789'
example_entry = """
    _  _     _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_|
  ||_  _|  | _||_|  ||_| _|
                           
"""
# Figures consist of a single string that represents an account character
# Figures result from concatenating veritcally adjacent substrings across lines
# All substrings have a known length
figure_width = 3
# All figures have a known length
figure_length = figure_width * lines_per_entry  # 12

# All entries contain the same number of figures
figures_per_entry = 9
# All lines have a known length
line_length = figure_width * figures_per_entry  # 27

# An input file represents _approximately_ 500 entries
approximate_entries_per_file = 500

# Every figure represents an account character
# Every figure is composed only of spaces, underscores, and pipes
valid_figure_characters = tuple('_ |')
# Every account character consists of a single digit string
valid_account_characters = tuple('0123456789')
# a 1:1 relationship exists between figures and account characters
figures = {' _ '+
           '| |'+
           '|_|'+
           '   ':'0',
           '   '+
           '  |'+
           '  |'+
           '   ':'1',
           ' _ '+
           ' _|'+
           '|_ '+
           '   ':'2',
           ' _ '+
           ' _|'+
           ' _|'+
           '   ':'3',
           '   '+
           '|_|'+
           '  |'+
           '   ':'4',
           ' _ '+
           '|_ '+
           ' _|'+
           '   ':'5',
           ' _ '+
           '|_ '+
           '|_|'+
           '   ':'6',
           ' _ '+
           '  |'+
           '  |'+
           '   ':'7',
           ' _ '+
           '|_|'+
           '|_|'+
           '   ':'8',
           ' _ '+
           '|_|'+
           ' _|'+
           '   ':'9'}
