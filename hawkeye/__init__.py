#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os

def _open_config(path):
    try:
        return file(path,"r").read()
    except:
        sys.exit("Error reading configuration file " + str(path))

def _parse_config(data):
    try:
        return eval(data)
    except:
        sys.exit("Error parsing configuration file " + str(path) +
            ".\nTry executing 'python " + str(path) + "' for more information.")

def get_config(path):
    """ simple python config file reader """
    if os.path.exists(path):
        data = _open_config(path)
        return _parse_config(data)
    else:
        sys.exit("Configuration file does not exist: "+str(path))

