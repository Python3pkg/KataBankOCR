#!/usr/bin/env python

import random

from settings import values as chars
from settings import figures_per_entry as length

class MakeAccountString:
    " collection of methods that each return an account number string "

    @classmethod
    def random(cls):
        " return an account number of valid length and character set "
        return ''.join(random.choice(chars) for i in range(length))
