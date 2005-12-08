#! /usr/bin/env python

from distutils.core import setup

import desktop

setup(
    name         = "desktop",
    description  = "Simple desktop integration for Python.",
    author       = "Paul Boddie",
    author_email = "paul@boddie.org.uk",
    url          = "http://www.python.org/pypi/desktop",
    version      = desktop.__version__,
    py_modules   = ["desktop"]
    )
