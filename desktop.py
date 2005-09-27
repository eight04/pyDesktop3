#!/usr/bin/env python

"""
Simple desktop integration for Python. This module provides desktop environment
detection and resource opening support for a selection of common and
standardised desktop environments.

To detect a specific desktop environment, use the get_desktop function.
To detect whether the desktop environment is standardised (according to a
proposed DESKTOP_LAUNCH standard), use the is_standard function.

Details of the DESKTOP_LAUNCH environment variable convention can be found here:
http://lists.freedesktop.org/archives/xdg/2004-August/004489.html
"""

import os
import sys
import subprocess
import commands

def get_desktop():

    """
    Detect the current desktop environment, returning the name of the
    environment. If no environment could be detected, None is returned.
    """

    if os.environ.has_key("KDE_FULL_SESSION") or \
        os.environ.has_key("KDE_MULTIHEAD"):
        return "KDE"
    elif os.environ.has_key("GNOME_DESKTOP_SESSION_ID") or \
        os.environ.has_key("GNOME_KEYRING_SOCKET"):
        return "GNOME"
    elif sys.platform == "darwin":
        return "Mac OS X"
    elif hasattr(os, "startfile"):
        return "Windows"
    else:
        return None

def is_standard():

    """
    Return whether the current desktop supports standardised application
    launching.
    """

    return os.environ.has_key("DESKTOP_LAUNCH")

def open(url, desktop=None):

    """
    Open the 'url' in the current desktop's preferred file browser. If the
    optional 'desktop' parameter is specified then attempt to use that
    particular desktop environment's mechanisms to open the 'url' instead of
    guessing or detecting which environment is being used.

    Suggested values for 'desktop' are "standard", "KDE", "GNOME", "Mac OS X",
    "Windows" where "standard" employs a DESKTOP_LAUNCH environment variable to
    open the specified 'url'. DESKTOP_LAUNCH should be a command, possibly
    followed by arguments, and must have any special characters shell-escaped. 

    The process identifier of the "opener" (ie. viewer, editor, browser or
    program) associated with the 'url' is returned by this function. If the
    process identifier cannot be determined, None is returned.
    """

    # Attempt to detect a desktop environment.

    detected = get_desktop()

    # Start with desktops whose existence can be easily tested.

    if (desktop is None or desktop == "standard") and is_standard():
        arg = "".join([os.environ["DESKTOP_LAUNCH"], commands.mkarg(url)])
        return subprocess.Popen(arg, shell=1).pid

    elif (desktop is None or desktop == "Windows") and detected == "Windows":
        # NOTE: This returns None in current implementations.
        return os.startfile(url)

    # Test for desktops where the overriding is not verified.

    elif (desktop or detected) == "KDE":
        cmd = ["kfmclient", "exec", url]

    elif (desktop or detected) == "GNOME":
        cmd = ["gnome-open", url]

    elif (desktop or detected) == "Mac OS X":
        cmd = ["open", url]

    # Finish with an error where no suitable desktop was identified.

    else:
        raise OSError, "Desktop not supported (neither DESKTOP_LAUNCH nor os.startfile could be used)"

    return subprocess.Popen(cmd).pid

# vim: tabstop=4 expandtab shiftwidth=4
