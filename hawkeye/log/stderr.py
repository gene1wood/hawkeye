#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from sys import stderr

def init(options):
    return HawkeyeLogStdErr(options)

class HawkeyeLogStdErr:

    def __init__(self,options):
        # stderr has no real options, but still...
        self._options = options

    def log(self,level,message,verbose=None):
        # act differently based on verbosity
        # Regardless of config stderr won't print debug unless asked to with -v
        if verbose is None:
            if level in ['info','error','alert']:
                print >> stderr, level + ": " + message
        elif verbose == "verbose":
            print >> stderr, level + ": " + message
        # do nothing otherwise
