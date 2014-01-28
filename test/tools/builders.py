" functions that build larger objects from smaller objects "

import settings

def figure_string_from_account_character(account_character):
    " return the figure string that represents the given account character "
    assert account_character in settings.figures.values()
    for figure in settings.figures:
        if settings.figures[figure] == account_character:
            return figure

def entry_list_from_account_string(account_string):
    " return the list of lines that represents the given account string "
    figure_strings = map(figure_string_from_account_character, account_string)
    figure_indexes = range(settings.figures_per_entry)
    slice_indexes = lambda line_index: (line_index * settings.figure_width,
                                        (line_index + 1)  * settings.figure_width)
    substring = lambda fi, li: figure_strings[fi][slice(*slice_indexes(li))]
    line_substrings = lambda li: [substring(fi, li) for fi in figure_indexes]
    return map(''.join, map(line_substrings, range(settings.lines_per_entry)))

def file_path_from_entry_lists(tmpdir, entry_lists):
    " return path to a file containing the given entry lists "
    # flatten all lines from entry_lists to one list of lines
    lines = [line for entry_list in entry_lists for line in entry_list]
    path = tmpdir.join('input_file.txt')
    F = path.open('w')
    for line in lines:
        F.write(line+'\n')
    F.close()
    return path

