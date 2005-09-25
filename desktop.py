#!/usr/bin/env python

"Simple desktop integration for Python."

import os
import sys
import subprocess

def open(url, desktop=None):

    """
    Open the 'url' in the current desktop's preferred file browser. If the
    optional 'desktop' parameter is specified then attempt to use that
    particular desktop environment's mechanisms to open the 'url' instead of
    guessing or detecting which environment is being used.

    Suggested values for 'desktop' are "KDE", "GNOME", "Mac OS X" and "generic",
    where "generic" uses an OPENER environment variable to open the specified
    'url'.

    The process identifier of the "opener" (ie. viewer, editor, browser or
    program) associated with the 'url' is returned by this function. If the
    process identifier cannot be determined, None is returned.
    """

    if desktop == "generic" or \
        desktop is None and os.environ.has_key("OPENER"):

        try:
            # NOTE: This may not handle sophisticated commands properly.
            cmd = os.environ["OPENER"].split()
            cmd.append(url)
        except KeyError, exc:
            raise OSError, "Desktop not supported (OPENER could not be used)"

    elif desktop == "KDE" or \
        desktop is None and (os.environ.has_key("KDE_FULL_SESSION") or
            os.environ.has_key("KDE_MULTIHEAD")):

        cmd = ["kfmclient", "exec", url]

    elif desktop == "GNOME" or \
        desktop is None and (os.environ.has_key("GNOME_DESKTOP_SESSION_ID") or
            os.environ.has_key("GNOME_KEYRING_SOCKET")):

        cmd = ["gnome-open", url]

    elif desktop == "Mac OS X" or \
        desktop is None and sys.platform == "darwin":

        cmd = ["open", url]

    else:
        try:
            # NOTE: This returns None in current implementations.
            return os.startfile(url)
        except AttributeError, exc:
            raise OSError, "Desktop not supported (os.startfile could not be used)"

    return subprocess.Popen(cmd).pid

# vim: tabstop=4 expandtab shiftwidth=4
