# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import sys


def log(msg):
    sys.stderr.write("APP: %s\n" % msg)
