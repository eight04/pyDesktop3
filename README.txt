Notes on desktop application/environment support:

KDE           Supports file and URL opening using kfmclient, where the openURL
              command opens the resource and the exec command runs the
              resource.

GNOME         Supports file and URL opening using gnome-open.

ROX-Filer     Supports file opening using "rox <filename>" but not URL
              opening.

Usage of the DESKTOP_LAUNCH environment variable:

DESKTOP_LAUNCH="kdialog --msgbox"       Should present any opened URLs in
                                        their entirety in a message box.
DESKTOP_LAUNCH="test\ this"             Should run the "test this" program to
                                        open URLs.
