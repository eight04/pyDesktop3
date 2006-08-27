#!/usr/bin/env python

"""
Simple desktop integration for Python. This module provides desktop environment
detection and resource opening support for a selection of common and
standardised desktop environments.

Copyright (C) 2005, 2006 Paul Boddie <paul@boddie.org.uk>

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

Desktop Detection
-----------------

To detect a specific desktop environment, use the get_desktop function.
To detect whether the desktop environment is standardised (according to the
proposed DESKTOP_LAUNCH standard), use the is_standard function.

Opening URLs
------------

To open a URL in the current desktop environment, relying on the automatic
detection of that environment, use the desktop.open function as follows:

desktop.open("http://www.python.org")

To override the detected desktop, specify the desktop parameter to the open
function as follows:

desktop.open("http://www.python.org", "KDE") # Insists on KDE
desktop.open("http://www.python.org", "GNOME") # Insists on GNOME

Without overriding using the desktop parameter, the open function will attempt
to use the "standard" desktop opening mechanism which is controlled by the
DESKTOP_LAUNCH environment variable as described below.

Opening Dialogue Boxes (Dialogs)
--------------------------------

To open a dialogue box (dialog) in the current desktop environment, relying on
the automatic detection of that environment, use the desktop.dialog function as
follows:

desktop.dialog("question", text="Are you sure?")

To override the detected desktop, specify the desktop parameter to the dialog
function as follows:

desktop.dialog("question", "KDE", text="Are you sure?") # Insists on KDE
desktop.dialog("question", "GNOME", text="Are you sure?") # Insists on GNOME

The DESKTOP_LAUNCH Environment Variable
---------------------------------------

The DESKTOP_LAUNCH environment variable must be shell-quoted where appropriate,
as shown in some of the following examples:

DESKTOP_LAUNCH="kdialog --msgbox"       Should present any opened URLs in
                                        their entirety in a KDE message box.
                                        (Command "kdialog" plus parameter.)
DESKTOP_LAUNCH="my\ opener"             Should run the "my opener" program to
                                        open URLs.
                                        (Command "my opener", no parameters.)
DESKTOP_LAUNCH="my\ opener --url"       Should run the "my opener" program to
                                        open URLs.
                                        (Command "my opener" plus parameter.)

Details of the DESKTOP_LAUNCH environment variable convention can be found here:
http://lists.freedesktop.org/archives/xdg/2004-August/004489.html
"""

__version__ = "0.2.4"

import os
import sys

try:
    import subprocess
    def _run(cmd, shell, wait):
        opener = subprocess.Popen(cmd, shell=shell)
        if wait: opener.wait()
        return opener.pid

    def _readfrom(cmd, shell):
        opener = subprocess.Popen(cmd, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        opener.stdin.close()
        return opener.stdout.read()

    def _status(cmd, shell):
        opener = subprocess.Popen(cmd, shell=shell)
        opener.wait()
        return opener.returncode == 0

except ImportError:
    import popen2
    def _run(cmd, shell, wait):
        opener = popen2.Popen3(cmd)
        if wait: opener.wait()
        return opener.pid

    def _readfrom(cmd, shell):
        opener = popen2.Popen3(cmd)
        opener.tochild.close()
        opener.childerr.close()
        return opener.fromchild.read()

    def _status(cmd, shell):
        opener = popen2.Popen3(cmd)
        opener.wait()
        return opener.poll() == 0

import commands

# Internal data.

_dialog_commands = {
    "KDE" : "kdialog",
    "GNOME" : "zenity",
    "X11" : "Xdialog"
    }

_dialog_options = {
    "KDE" : {
        "question" :    (_status, ["--yesno"], ["text"]),
        "message" :     (_status, ["--msgbox"], ["text"]),
        "input" :       (_readfrom, ["--inputbox"], ["text", "input"]),
        "password" :    (_readfrom, ["--password"], ["text"]),
        "textfile" :    (_readfrom, ["--textbox"], ["filename", "width", "height"]),
        "menu" :        (_readfrom, ["--menu"], ["text", "entries2"]),
        "radiolist" :   (_readfrom, ["--radiolist"], ["text", "entries3"]),
        "checklist" :   (_readfrom, ["--checklist"], ["text", "entries3"]),
        "pulldown" :    (_readfrom, ["--combobox"], ["text", "entries1"]),
        },
    "X11" : {
        "question" :    (_status, ["--stdout", "--yesno"], ["text", "height", "width"]),
        "message" :     (_status, ["--stdout", "--msgbox"], ["text", "height", "width"]),
        "input" :       (_readfrom, ["--stdout", "--inputbox"], ["text", "height", "width", "input"]),
        "password" :    (_readfrom, ["--stdout", "--password", "--inputbox"], ["text", "height", "width"]),
        "textfile" :    (_readfrom, ["--stdout", "--textbox"], ["text", "height", "width"]),
        "menu" :        (_readfrom, ["--stdout", "--menubox"], ["text", "height", "width", "menu_height", "entries2"]),
        "radiolist" :   (_readfrom, ["--stdout", "--radiolist"], ["text", "height", "width", "list_height", "entries3"]),
        "checklist" :   (_readfrom, ["--stdout", "--checklist"], ["text", "height", "width", "list_height", "entries3"]),
        "pulldown" :    (_readfrom, ["--stdout", "--combobox"], ["text", "height", "width", "entries1"]),
        },
    }

_dialog_defaults = {
    "width" : 40, "height" : 30, "menu_height" : 20, "list_height" : 20
    }

# Introspection functions.

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
    elif os.environ.has_key("DISPLAY"):
        return "X11"
    else:
        return None

def use_desktop(desktop):

    """
    Decide which desktop should be used, based on the detected desktop and a
    supplied 'desktop' argument (which may be None). Return an identifier
    indicating the desktop type as being either "standard" or one of the results
    from the 'get_desktop' function.
    """

    # Attempt to detect a desktop environment.

    detected = get_desktop()

    # Start with desktops whose existence can be easily tested.

    if (desktop is None or desktop == "standard") and is_standard():
        return "standard"
    elif (desktop is None or desktop == "Windows") and detected == "Windows":
        return "Windows"

    # Test for desktops where the overriding is not verified.

    elif (desktop or detected) == "KDE":
        return "KDE"
    elif (desktop or detected) == "GNOME":
        return "GNOME"
    elif (desktop or detected) == "Mac OS X":
        return "Mac OS X"
    elif (desktop or detected) == "X11":
        return "X11"
    else:
        return None

def is_standard():

    """
    Return whether the current desktop supports standardised application
    launching.
    """

    return os.environ.has_key("DESKTOP_LAUNCH")

# Activity functions.

def open(url, desktop=None, wait=0):

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

    An optional 'wait' parameter is also available for advanced usage and, if
    'wait' is set to a true value, this function will wait for the launching
    mechanism to complete before returning (as opposed to immediately returning
    as is the default behaviour).
    """

    # Decide on the desktop environment in use.

    desktop_in_use = use_desktop(desktop)

    if desktop_in_use == "standard":
        arg = "".join([os.environ["DESKTOP_LAUNCH"], commands.mkarg(url)])
        return _run(arg, 1, wait)

    elif desktop_in_use == "Windows":
        # NOTE: This returns None in current implementations.
        return os.startfile(url)

    elif desktop_in_use == "KDE":
        cmd = ["kfmclient", "exec", url]

    elif desktop_in_use == "GNOME":
        cmd = ["gnome-open", url]

    elif desktop_in_use == "Mac OS X":
        cmd = ["open", url]

    # Finish with an error where no suitable desktop was identified.

    else:
        raise OSError, "Desktop not supported (neither DESKTOP_LAUNCH nor os.startfile could be used)"

    return _run(cmd, 0, wait)

def dialog(dialog_type, desktop=None, **options):

    """
    Open a dialogue box (dialog) using a program appropriate to the desktop
    environment in use. The specified 'dialog_type' may be one of the following:

    question    A dialogue asking a question and showing response buttons.
                Options: text, width (in characters), height (in characters)

    message     A message dialogue.
                Options: text, level ("warning", "error", "info")

    menu        A menu of options, one of which being selectable.
                Options: text, width (in characters), height (in characters),
                menu_height (in entries), entries (list of (value, text) tuples)

    radiolist   A list of radio buttons, one of which being selectable.
                Options: text, width (in characters), height (in characters),
                list_height (in entries), entries (list of (value, text, status)
                tuples)

    checklist   A list of checkboxes, many being selectable.
                Options: text, width (in characters), height (in characters),
                list_height (in entries), entries (list of (value, text, status)
                tuples)

    pulldown    A pull-down menu of options, one of which being selectable.
                Options: text, width (in characters), height (in characters),
                entries (list of values)

    input       An input dialogue, consisting of an input field.
                Options: text, width (in characters), height (in characters),
                input

    password    A password dialogue, consisting of a password entry field.
                Options: text, width (in characters), height (in characters),
                input

    textfile    A text file input box.
                Options: text, width (in characters), height (in characters),
                filename

    If the optional 'desktop' parameter is specified then attempt to use that
    particular desktop environment's mechanisms to open the 'url' instead of
    guessing or detecting which environment is being used.

    Suggested values for 'desktop' are "standard", "KDE", "GNOME", "Mac OS X",
    "Windows".

    The result of the dialogue interaction may be a string indicating user
    input (for input, password, menu, radiolist, pulldown), a list of strings
    indicating selections of one or more items (for checklist), or a value
    indicating true or false (for question).
    """

    # Decide on the desktop environment in use.

    desktop_in_use = use_desktop(desktop)

    # Get the base command.

    cmd = _dialog_commands[desktop_in_use]

    # Get the handler for the command, along with required command options and
    # the fields that the command expects.

    handler, cmd_options, fields = _dialog_options[desktop_in_use][dialog_type]

    # Form a command list.

    l = [cmd] + cmd_options

    # Process the fields, adding values if found or defaults if available.

    for field in fields:
        if field[-1].isdigit():
            n = int(field[-1])
            field = field[:-1]
        else:
            n = 0 # not list

        if options.has_key(field):
            if n == 0:
                l.append(str(options[field]))
            else:
                values = options[field]
                for value in values:
                    if n == 1:
                        l.append(str(value))
                    else:
                        for i in range(0, n):
                            l.append(str(value[i]))
        elif _dialog_defaults.has_key(field):
            l.append(str(_dialog_defaults[field]))
        else:
            raise ValueError, "Field '%s' missing from options." % field

    print l
    return handler(l, 0)

# vim: tabstop=4 expandtab shiftwidth=4
