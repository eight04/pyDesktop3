#! /usr/bin/env python

import re

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

def read(file):
	with open(path.join(here, file), encoding='utf-8') as f:
		content = f.read()
	return content
	
def find_version(file):
	return re.search(r"__version__ = (\S*)", read(file)).group(1).strip("\"'")
	
setup(
    name         = "desktop3",
    description  = "Simple desktop integration for Python.",
    long_description = read("readme.rst"),
    author       = "Paul Boddie",
    author_email = "paul@boddie.org.uk",
    maintainer = "eight04",
    maintainer_email = "eight04@gmail.com",
    url          = "https://github.com/eight04/pyDesktop3",
    version      = find_version("desktop/__init__.py"),
    packages     = find_packages(),
    license = "LGPLv3+",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        # TODO: add OS list
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Desktop Environment",
        "Topic :: Utilities"
    ],
    keywords = "start startfile open opener launch launcher"
)
