#!/usr/bin/env python

import desktop.dialog

def test_open(obj, desktop=None):
    try:
        return obj.open(desktop)
    except OSError:
        return None

"""
obj = desktop.dialog.Question("Are you sure?", 40, 5)
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")

obj = desktop.dialog.Message("Hello world!", 40, 5)
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")

obj = desktop.dialog.Warning("Beware of the penguin!", 40, 5)
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")

obj = desktop.dialog.Error("Penguin invasion complete!", 40, 5)
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")
"""

obj = desktop.dialog.Menu("Choose an animal", ["*", "Animal"], width=40, height=15, list_height=5)
obj.add("a", "Antelope")
obj.add("b", "Badger")
obj.add("c", "Cow")
obj.add("d", "Dog")
obj.add("e", "Elephant")
obj.add("f", "Fox")
obj.add("g", "Giraffe")
obj.add("h", "Horse")
obj.add("i", "Iguana")
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")

obj = desktop.dialog.CheckList("Choose some animals", ["S", "*", "Animal"], width=40, height=15, list_height=5)
obj.add("a", "Antelope")
obj.add("b", "Badger", 1)
obj.add("c", "Cow", 0)
obj.add("d", "Dog")
obj.add("e", "Elephant")
obj.add("f", "Fox", 1)
obj.add("g", "Giraffe")
obj.add("h", "Horse")
obj.add("i", "Iguana")
print test_open(obj)
print test_open(obj, "KDE")
print test_open(obj, "GNOME")
print test_open(obj, "X11")

# vim: tabstop=4 expandtab shiftwidth=4
