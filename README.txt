Introduction
------------

The desktop module provides desktop environment detection and resource opening
support for a selection of common and standardised desktop environments. See
the module docstring for a more extensive introduction.

Contact, Copyright and Licence Information
------------------------------------------

No Web page has yet been made available for this work, but the author can be
contacted at the following e-mail address:

paul@boddie.org.uk

Copyright and licence information can be found in the docs directory - see
docs/COPYING.txt and docs/LICENCE.txt for more information. Whilst I would
prefer to release my software under the LGPL or GPL, the Python Software
Foundation insists on other licences, and I have chosen one of those in the
hope that this module becomes a part of the Python standard library.

Notes
-----

Notes on desktop application/environment support:

KDE           Supports file and URL opening using kfmclient, where the openURL
              command opens the resource and the exec command runs the
              resource.

GNOME         Supports file and URL opening using gnome-open.

ROX-Filer     Supports file opening using "rox <filename>" but not URL
              opening.
