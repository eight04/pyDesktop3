#!/usr/bin/env python

import desktop.dialog

def test_open(obj, desktop=None):
    try:
        return obj.open(desktop)
    except OSError:
        return None

def test_question():
    obj = desktop.dialog.Question("Are you sure?", 40, 5)
    print(test_open(obj))
    print(test_open(obj, "KDE"))
    print(test_open(obj, "GNOME"))
    print(test_open(obj, "X11"))

def test_message():
    obj = desktop.dialog.Message("Hello world!", 40, 5)
    print(test_open(obj))
    print(test_open(obj, "KDE"))
    print(test_open(obj, "GNOME"))
    print(test_open(obj, "X11"))

def test_warning():
    obj = desktop.dialog.Warning("Beware of the penguin!", 40, 5)
    print(test_open(obj))
    print(test_open(obj, "KDE"))
    print(test_open(obj, "GNOME"))
    print(test_open(obj, "X11"))

def test_error():
    obj = desktop.dialog.Error("Penguin invasion complete!", 40, 5)
    print(test_open(obj))
    print(test_open(obj, "KDE"))
    print(test_open(obj, "GNOME"))
    print(test_open(obj, "X11"))

def test_menu():
    obj = desktop.dialog.Menu("Choose an animal", ["Animal"], width=40, height=15, list_height=5)
    obj.add("a", "Antelope")
    obj.add("b", "Badger")
    obj.add("c", "Cow")
    obj.add("d", "Dog")
    obj.add("e", "Elephant")
    obj.add("f", "Fox")
    obj.add("g", "Giraffe")
    obj.add("h", "Horse")
    obj.add("i", "Iguana")
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_checklist():
    obj = desktop.dialog.CheckList("Choose some animals", ["Animal"], width=40, height=15, list_height=5)
    obj.add("a", "Antelope")
    obj.add("b", "Badger", 1)
    obj.add("c", "Cow", 0)
    obj.add("d", "Dog")
    obj.add("e", "Elephant")
    obj.add("f", "Fox", 1)
    obj.add("g", "Giraffe")
    obj.add("h", "Horse")
    obj.add("i", "Iguana")
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_radiolist():
    obj = desktop.dialog.RadioList("Choose one animal", ["Animal"], width=40, height=15, list_height=5)
    obj.add("a", "Antelope")
    obj.add("b", "Badger", 1)
    obj.add("c", "Cow", 0)
    obj.add("d", "Dog")
    obj.add("e", "Elephant")
    obj.add("f", "Fox", 1)
    obj.add("g", "Giraffe")
    obj.add("h", "Horse")
    obj.add("i", "Iguana")
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_pulldown():
    obj = desktop.dialog.Pulldown("Choose an animal", ["Animal"], width=40, height=15, list_height=5)
    obj.add("Antelope")
    obj.add("Badger")
    obj.add("Cow")
    obj.add("Dog")
    obj.add("Elephant")
    obj.add("Fox")
    obj.add("Giraffe")
    obj.add("Horse")
    obj.add("Iguana")
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_input():
    obj = desktop.dialog.Input("Enter your name!", "Monty", 40, 5)
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_password():
    obj = desktop.dialog.Password("Enter your password!", "Python", 40, 5)
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

def test_textfile():
    obj = desktop.dialog.TextFile("README.txt", "Showing file...", 80, 25)
    print(repr(test_open(obj)))
    print(repr(test_open(obj, "KDE")))
    print(repr(test_open(obj, "GNOME")))
    print(repr(test_open(obj, "X11")))

test_question()
test_message()
test_warning()
test_error()
test_menu()
test_checklist()
test_radiolist()
test_pulldown()
test_input()
test_password()
test_textfile()

# vim: tabstop=4 expandtab shiftwidth=4
