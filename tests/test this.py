#!/usr/bin/env python
import os, sys, commands
os.system("kdialog " + "".join(map(commands.mkarg, sys.argv[1:])))
