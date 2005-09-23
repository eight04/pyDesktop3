#!/usr/bin/env python

"Simple desktop integration for Python."

import os
import subprocess

def open(url, desktop=None):

    """
    Open the 'url' in the current desktop's preferred file browser. If the
    optional 'desktop' parameter is specified then attempt to use that
    particular desktop environment's mechanisms to open the 'url' instead of
    guessing or detecting which environment is being used.

    Suggested values for 'desktop' are "KDE" and "GNOME".
    """

    if desktop == "KDE" or \
        desktop is None and (os.environ.has_key("KDE_FULL_SESSION") or
            os.environ.has_key("KDE_MULTIHEAD")):

        cmd = ["kfmclient", "openURL", url]

    elif desktop == "GNOME" or \
        desktop is None and (os.environ.has_key("GNOME_DESKTOP_SESSION_ID") or
            os.environ.has_key("GNOME_KEYRING_SOCKET")):

        cmd = ["gnome-open", url]

    else:
        os.startfile(url)
        return

    subprocess.Popen(cmd)

# vim: tabstop=4 expandtab shiftwidth=4
