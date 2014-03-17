#!/use/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# ToDo:  Add module options

class HawkeyeLog:
    def __init__(self,modules={}):
        _check_modules(modules) # If we return, awesome!
        for key in modules.keys():
            _initialize_module(modules[key])
        return self

    # This is subject to change, but the theory is sound
    # ToDo: Create better verbosity for the error messages
    # ToDo: Add module/levels type checking
    def _check_modules(modules):
        if type(modules) == dict:
            raise error("No logging modules supplied!")
        if len(modules) < 1:
            raise error("No logging modules suplied!")
        for key,value in modules:
            if type(value) == dict:
                raise error("Improperly formed configuration for " + str(key))
            if "module" not in value:
                raise error("No 'module' value set for " + str(key))
            if "levels" not in value:
                raise error("No configured logging levels set for " + str(key))
        # If we make it here, it's safe-ish to continue.

    # I don't like this, redo it.
    def _initialize_module(module):
        module = _import_module(module["name"])
        if module is not None:
            for level in module["levels"].split("\s*,\s*"):
                if level in self._levels:
                    level[level].append(module)

    def _import_module(name):
        #ImportError: No module named something.boto
        for alias in [name, "hawkeye.log." + name]:
            try:
                return __import__(name)
            except ImportError:
                pass
        return None

    # todo: add more message sending options here, but for now all we're sending is strings
    # we want varying degrees of verbosity from a message so each module can choose how much it communicates
    def log(level,message):
        for module in self._levels[level]:
            module.log(level,message)

    def debug(message):
        log('debug', message)

    def info(message):
        log('info', message)

    def notice(message):
        log('notice', message)

    def warn(message):
        log('warn', message)

    def error(message):
        log('error', message)

    def crit(message):
        log('crit', message)

    def alert(message):
        log('alert', message)

    _levels = {
        "debug": [],
        "info": [],
        "notice": [],
        "warn": [],
        "error": [],
        "crit": [],
        "alert": [],
    }


