"""
Bank OCR Kata Parser

Usage:
  parser.py ( - | <input_file> ) [<output_file>]
  parser.py [ - | <input_file> ]
  parser.py [options]
  parser.py

Options:
  -h --help               Show this screen.
  --version               Show version.
"""

from docopt import docopt

__version__ = open('parser/version.txt').read().strip()

def in_path_and_out_path():
    "return input_path and output_path from arguments"
    arguments = docopt(__doc__, version=version_name())
    if arguments['<input_file>'] is None:
        input_path = '-'
    else:
        input_path = arguments['<input_file>']
    output_path = arguments['<output_file>']
    return (input_path, output_path)

def version_name():
    "return input_path and output_path from arguments"
    parser_name = 'Bank OCR Parser (Kata)'
    return ' '.join((parser_name, 'version', __version__))
