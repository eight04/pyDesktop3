#!/usr/bin/env python

"""
Simple desktop dialogue box support for Python.

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

Opening Dialogue Boxes (Dialogs)
--------------------------------

To open a dialogue box (dialog) in the current desktop environment, relying on
the automatic detection of that environment, use the appropriate dialogue box
class:

question = desktop.dialog.Question("Are you sure?")
question.open()

To override the detected desktop, specify the desktop parameter to the open
function as follows:

question.open("KDE") # Insists on KDE
question.open("GNOME") # Insists on GNOME

The dialogue box options are documented in each class's docstring.
"""

from desktop import use_desktop, _run, _readfrom, _status

# Dialogue parameter classes.

class String:

    "A generic parameter."

    def __init__(self, name):
        self.name = name

    def convert(self, value, program):
        return [value or ""]

class Strings(String):

    "Multiple string parameters."

    def convert(self, value, program):
        return value or []

class StringKeyword:

    "A keyword parameter."

    def __init__(self, keyword, name):
        self.keyword = keyword
        self.name = name

    def convert(self, value, program):
        return [self.keyword + "=" + (value or "")]

class StringKeywords:

    "Multiple keyword parameters."

    def __init__(self, keyword, name):
        self.keyword = keyword
        self.name = name

    def convert(self, value, program):
        l = []
        for v in value or []:
            l.append(self.keyword + "=" + v)
        return l

class Integer(String):

    "An integer parameter."

    defaults = {
        "width" : 40,
        "height" : 15,
        "list_height" : 10
        }

    def convert(self, value, program):
        if value is None:
            value = self.defaults[self.name]
        return [str(int(value))]

class IntegerKeyword(Integer):

    "An integer keyword parameter."

    def __init__(self, keyword, name):
        self.keyword = keyword
        self.name = name

    def convert(self, value, program):
        if value is None:
            value = self.defaults[self.name]
        return [self.keyword + "=" + str(int(value))]

class Boolean(String):

    "A boolean parameter."

    values = {
        "kdialog" : ["off", "on"],
        "zenity" : ["FALSE", "TRUE"],
        "Xdialog" : ["off", "on"]
        }

    def convert(self, value, program):
        values = self.values[program]
        if value:
            return [values[1]]
        else:
            return [values[0]]

class MenuItemList(String):

    "A menu item list parameter."

    def convert(self, value, program):
        l = []
        for v in value:
            l.append(v.value)
            l.append(v.text)
        return l

class ListItemList(String):

    "A radiolist/checklist item list parameter."

    def __init__(self, name, status_first=0):
        String.__init__(self, name)
        self.status_first = status_first

    def convert(self, value, program):
        l = []
        for v in value:
            boolean = Boolean(None)
            status = boolean.convert(v.status, program)
            if self.status_first:
                l += status
            l.append(v.value)
            l.append(v.text)
            if not self.status_first:
                l += status
        return l

# Dialogue argument values.

class MenuItem:

    "A menu item which can also be used with radiolists and checklists."

    def __init__(self, value, text, status=0):
        self.value = value
        self.text = text
        self.status = status

# Dialogue classes.

class Dialogue:

    commands = {
        "KDE" : "kdialog",
        "GNOME" : "zenity",
        "X11" : "Xdialog"
        }

    def open(self, desktop=None):

        """
        Open a dialogue box (dialog) using a program appropriate to the desktop
        environment in use.

        If the optional 'desktop' parameter is specified then attempt to use that
        particular desktop environment's mechanisms to open the dialog instead of
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

        # Get the program.

        try:
            program = self.commands[desktop_in_use]
        except KeyError:
            raise OSError, "Desktop '%s' not supported (no known dialogue box command could be suggested)" % desktop_in_use

        handler, options = self.info[program]

        cmd = [program]
        for option in options:
            if isinstance(option, str):
                cmd.append(option)
            else:
                value = getattr(self, option.name, None)
                cmd += option.convert(value, program)

        print cmd
        return handler(cmd, 0)

class Simple(Dialogue):
    def __init__(self, text, width=None, height=None):
        self.text = text
        self.width = width
        self.height = height

class Question(Simple):

    """
    A dialogue asking a question and showing response buttons.
    Options: text, width (in characters), height (in characters)
    """

    name = "question"
    info = {
        "kdialog" : (_status, ["--yesno", String("text")]),
        "zenity" : (_status, ["--question", StringKeyword("--text", "text")]),
        "Xdialog" : (_status, ["--stdout", "--yesno", String("text"), Integer("height"), Integer("width")]),
        }

class Warning(Simple):

    """
    A dialogue asking a question and showing response buttons.
    Options: text, width (in characters), height (in characters)
    """

    name = "warning"
    info = {
        "kdialog" : (_status, ["--warningyesno", String("text")]),
        "zenity" : (_status, ["--warning", StringKeyword("--text", "text")]),
        "Xdialog" : (_status, ["--stdout", "--yesno", String("text"), Integer("height"), Integer("width")]),
        }

class Message(Simple):

    """
    A message dialogue.
    Options: text, width (in characters), height (in characters)
    """

    name = "message"
    info = {
        "kdialog" : (_status, ["--msgbox", String("text")]),
        "zenity" : (_status, ["--info", StringKeyword("--text", "text")]),
        "Xdialog" : (_status, ["--stdout", "--msgbox", String("text"), Integer("height"), Integer("width")]),
        }

class Error(Simple):

    """
    An error dialogue.
    Options: text, width (in characters), height (in characters)
    """

    name = "error"
    info = {
        "kdialog" : (_status, ["--error", String("text")]),
        "zenity" : (_status, ["--error", StringKeyword("--text", "text")]),
        "Xdialog" : (_status, ["--stdout", "--msgbox", String("text"), Integer("height"), Integer("width")]),
        }

class Menu(Simple):

    """
    A menu of options, one of which being selectable.
    Options: text, width (in characters), height (in characters),
    list_height (in items), items (MenuItem objects)
    """

    name = "menu"
    info = {
        "kdialog" : (_readfrom, ["--menu", String("text"), MenuItemList("items")]),
        "zenity" : (_readfrom, ["--list", StringKeyword("--text", "text"), StringKeywords("--column", "titles"),
            MenuItemList("items")]
            ),
        "Xdialog" : (_readfrom, ["--stdout", "--menubox",
            String("text"), Integer("height"), Integer("width"), Integer("list_height"), MenuItemList("items")]
            ),
        }
    item = MenuItem

    def __init__(self, text, titles, items=None, width=None, height=None, list_height=None):

        """
        Initialise a menu with the given heading 'text', column 'titles', and
        optional 'items' (which may be added later), 'width' (in characters),
        'height' (in characters) and 'list_height' (in items).
        """

        Simple.__init__(self, text, width, height)
        self.titles = titles
        self.items = items or []
        self.list_height = list_height

    def add(self, *args, **kw):

        """
        Add an item, passing the given arguments to the appropriate item class.
        """

        self.items.append(self.item(*args, **kw))

class RadioList(Menu):

    """
    A list of radio buttons, one of which being selectable.
    Options: text, width (in characters), height (in characters),
    list_height (in items), items (MenuItem objects), titles
    """

    name = "radiolist"
    info = {
        "kdialog" : (_readfrom, ["--radiolist", String("text"), ListItemList("items")]),
        "zenity" : (_readfrom,
            ["--list", "--radiolist", StringKeyword("--text", "text"), StringKeywords("--column", "titles"),
            ListItemList("items", 1)]
            ),
        "Xdialog" : (_readfrom, ["--stdout", "--radiolist",
            String("text"), Integer("height"), Integer("width"), Integer("list_height"), ListItemList("items")]
            ),
        }

class CheckList(Menu):

    """
    A list of checkboxes, many being selectable.
    Options: text, width (in characters), height (in characters),
    list_height (in items), items (MenuItem objects), titles
    """

    name = "checklist"
    info = {
        "kdialog" : (_readfrom, ["--checklist", String("text"), ListItemList("items")]),
        "zenity" : (_readfrom,
            ["--list", "--checklist", StringKeyword("--text", "text"), StringKeywords("--column", "titles"),
            ListItemList("items", 1)]
            ),
        "Xdialog" : (_readfrom, ["--stdout", "--checklist",
            String("text"), Integer("height"), Integer("width"), Integer("list_height"), ListItemList("items")]
            ),
        }

class Pulldown(Menu):

    """
    A pull-down menu of options, one of which being selectable.
    Options: text, width (in characters), height (in characters),
    entries (list of values)
    """

    name = "pulldown"
    info = {
        "kdialog" : (_readfrom, ["--combobox", String("text"), Strings("items")]),
        "zenity" : (_readfrom, ["--list", "--radiolist", StringKeyword("--text", "text"), StringKeywords("--column", "titles"),
            Strings("items")]
            ),
        "Xdialog" : (_readfrom, ["--stdout", "--combobox", String("text"), Integer("height"), Integer("width"), Strings("items")]),
        }

class Input(Simple):

    """
    An input dialogue, consisting of an input field.
    Options: text, width (in characters), height (in characters),
    input
    """

    name = "input"
    info = {
        "kdialog" : (_readfrom, ["--inputbox", String("text"), String("data")]),
        "zenity" : (_readfrom, ["--entry", StringKeyword("--text", "text"), StringKeyword("--entry-text", "data")]),
        "Xdialog" : (_readfrom, ["--stdout", "--inputbox", String("text"), Integer("height"), Integer("width"), String("data")]),
        }

    def __init__(self, text, data, width=None, height=None):
        Simple.__init__(self, text, width, height)
        self.data = data

class Password(Input):

    """
    A password dialogue, consisting of a password entry field.
    Options: text, width (in characters), height (in characters),
    input
    """

    name = "password"
    info = {
        "kdialog" : (_readfrom, ["--password", String("text")]),
        "zenity" : (_readfrom, ["--password", StringKeyword("--text", "text"), "--hide-text"]),
        "Xdialog" : (_readfrom, ["--stdout", "--password", "--inputbox", String("text"), Integer("height"), Integer("width")]),
        }

class TextFile(Simple):

    """
    A text file input box.
    Options: text, width (in characters), height (in characters),
    filename
    """

    name = "textfile"
    info = {
        "kdialog" : (_readfrom, ["--textbox", String("filename"), String("width"), String("height")]),
        "zenity" : (_readfrom, ["--textbox", StringKeyword("--filename", "filename"), IntegerKeyword("--width", "width"),
            IntegerKeyword("--height", "height")]
            ),
        "Xdialog" : (_readfrom, ["--stdout", "--textbox", String("text"), Integer("height"), Integer("width")]),
        }

    def __init__(self, text, filename, width=None, height=None):
        Simple.__init__(self, text, width, height)
        self.filename = filename

# Available dialogues.

available = [Question, Warning, Message, Error, Menu, CheckList, RadioList, Input, Password, Pulldown, TextFile]

# vim: tabstop=4 expandtab shiftwidth=4
