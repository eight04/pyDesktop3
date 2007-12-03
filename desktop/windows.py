#!/usr/bin/env python

"""
Simple desktop window enumeration for Python.

Copyright (C) 2005, 2006, 2007 Paul Boddie <paul@boddie.org.uk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

--------

Finding Open Windows on the Desktop
-----------------------------------

To obtain a list of windows, use the desktop.windows.list function as follows:

desktop.windows.list()
"""

from desktop import _is_x11, _get_x11_vars, _readfrom, use_desktop

def list(desktop=None):

    """
    Return a list of window handles for the current desktop. If the optional
    'desktop' parameter is specified then attempt to use that particular desktop
    environment's mechanisms to look for windows.
    """

    # NOTE: The desktop parameter is currently ignored and X11 is tested for
    # NOTE: directly.

    if _is_x11():
        s = _readfrom(_get_x11_vars() + "xlsclients -a -l", shell=1)
        prefix = "Window "
        prefix_end = len(prefix)
        handles = []

        for line in s.split("\n"):
            if line.startswith(prefix):
                handles.append(line[prefix_end:-1]) # NOTE: Assume ":" at end.
    else:
        raise OSError, "Desktop '%s' not supported" % use_desktop(desktop)

    return handles

# vim: tabstop=4 expandtab shiftwidth=4
