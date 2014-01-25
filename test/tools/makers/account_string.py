#!/usr/bin/env python

import random

from settings import values as chars
from settings import figures_per_entry as length

class MakeAccountString:
    " collection of methods that each return an account string "

    @classmethod
    def random(cls):
        " return an account string of valid length and character set "
        return ''.join(random.choice(chars) for i in range(length))
