#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# ToDo:  Add module options

import sys

class HawkeyeLog:
    def __init__(self,modules,verbose):
        self._verbose = verbose
        for item in modules:
            self._initialize_module(item)

    def _initialize_module(self,mod):
        name = mod.get('module')
        if name is not None:
            module = self._import_module(name,mod)
            if module is not None:
                self._add_to_levels(mod,module)
            else:
                sys.exit("Logging module named " + str(name) + " not found.")
        else:
            sys.exit("No 'module' element specified in log module configuration")

    def _add_to_levels(self,mod,module):
        levels = mod.get('levels')
        if levels is not None:
            for level in mod['levels']:
                if level in self._levels:
                    self._levels[level].append(module)
        else:
            sys.exit("No logging levels specified for " + str(mod.get(module)) + ".")

    def _import_module(self,name,options):
        for alias in ["hawkeye.log." + name, name]:
            try:
                module = __import__(alias)
                components = alias.split('.')
                for comp in components[1:]:
                    module = getattr(module, comp)
                return module.init(options)
            except ImportError:
                pass # ignore import errors
        return None

    # todo: add more message sending options here, but for now all we're sending is strings
    # we want varying degrees of verbosity from a message so each module can choose how much it communicates
    def _log(self,level,message):
        for module in self._levels[level]:
            module.log(level,message,self._verbose)

    def debug(self,message):
        self._log('debug', message)

    def info(self,message):
        self._log('info', message)

    def error(self,message):
        self._log('error', message)

    def alert(self,message):
        self._log('alert', message)

    _levels = {
        "debug": [],
        "info": [],
        "error": [],
        "alert": [],
    }


