#! /usr/bin/env python

from distutils.core import setup

import desktop

setup(
    name         = "desktop",
    description  = "Simple desktop integration for Python.",
    author       = "Paul Boddie",
    author_email = "paul@boddie.org.uk",
    url          = "http://www.python.org/sf?id=1301512",
    version      = desktop.__version__,
    py_modules   = ["desktop"]
    )
