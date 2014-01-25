#!/usr/bin/env python

figure_width = 3
figures_per_entry = 9
line_length = figure_width * figures_per_entry  # 27
lines_per_entry = 4
figure_length = figure_width * lines_per_entry  # 12
last_line_empty = True
valid_figure_characters = (' ', '_', '|')

values=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

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

