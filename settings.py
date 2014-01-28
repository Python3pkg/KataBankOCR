" Static values that restate the problem description "

# An Entry consists of a list of lines (as strings)
# An Entry has a defined number of lines
lines_per_entry = 4
# An Entry has only whitespace in its final line
last_line_empty = True
# An Entry represents an Account string composed of account characters

# The four lines in this example entry represent the account string '123456789'
example_entry_list = ['    _  _     _  _  _  _  _ ',
                      '  | _| _||_||_ |_   ||_||_|',
                      '  ||_  _|  | _||_|  ||_| _|',
                      '                           ',]
# A Figure consist of a single string that represents an Account Character
# A Figure results from concatenating veritcally adjacent Substrings across Lines
# All Substrings have a known length
figure_width = 3
# All Figures have a known length
figure_length = figure_width * lines_per_entry  # 12

# All Entries contain the same number of Figures
figures_per_entry = 9
# All Lines have a known length
line_length = figure_width * figures_per_entry  # 27

# All Input Files contain _approximately_ the same number of entries
approximate_entries_per_file = 500

# Every Figure represents an Account Character
# Every Figure is composed only of spaces, underscores, and pipes
valid_figure_characters = tuple('_ |')
# Every Account Character consists of a single digit string
valid_account_characters = tuple('0123456789')
# A 1:1 relationship exists between Figures and Account Characters
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
