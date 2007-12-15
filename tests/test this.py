#!/usr/bin/env python

"""
As a script with a space in the name, useful for testing with the desktop.open
function.
"""

import os, sys, commands

os.system("kdialog " + "".join(map(commands.mkarg, sys.argv[1:])))

# vim: tabstop=4 expandtab shiftwidth=4
