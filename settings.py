#!/usr/bin/env python

lines_per_entry=4
last_line_empty=True
figures_per_entry=9
characters_per_figure=12
figure_width=3
valid_figure_characters=(' ', '_', '|')

input_file_path='input_file.txt'

values=('0','1','2','3','4','5','6','7','8','9',)

# 10 strings composed of spaces, underscores and pipes
# that represent the characters 0 through 9
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

