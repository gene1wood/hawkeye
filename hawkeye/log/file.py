#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
from datetime import datetime

def init(options):
    return HawkeyeLogFile(options)

class HawkeyeLogFile:

    def __init__(self,options):
        # stderr has no real options, but still...
        outfile = options.get('file')
        mode = options.get('mode','a') # always default to safest option
        if outfile is not None:
            path = os.path.dirname(outfile)
            if os.path.exists(path):
                self._open_file(outfile,mode)
            else:
                sys.exit("The following path does not exist: " + str(path))

    def _open_file(self,outfile,mode):
        try:
            self._handle = open(outfile,mode)
        except:
            sys.exit("Unable to open log file for writing: " + str(outfile))

    def log(self,level,message,verbose=None):
        time = datetime.utcnow().isoformat() + "+0000"
        try:
            self._handle.write(time + " " + level + " " + message + "\n")
        except:
            sys.exit("Error writing to log file: " + str(self._handle.name))
