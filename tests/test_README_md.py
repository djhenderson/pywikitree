#! python3
# -*- coding:utf-8 -*-

import sys
import doctest
try:
    import wt_apps
except ImportError:
    sys.path.insert(0, ".")

doctest.testfile("../README.md", optionflags=doctest.NORMALIZE_WHITESPACE, encoding="utf-8")
