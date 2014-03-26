#######
Hawkeye
#######

Hawkeye is a simple policy and compliance auditing tool for Amazon AWS.  It's designed to use user-supplied policy rules and compare them against AWS configurations, then report the pass/fail results to the user.

Hawkeye is written using Python and Boto.

Summary of operation
====================

Hawkeye take two operations to complete a successful audit:

* Dump AWS configuration data to a normalized JSON file
* Compare the JSON file against user-supplied rules

The logic to dump configurations locally is two fold:

* It allows for the audit module to be more simple and focused, without having to worry about connection issues, authentication, queries, etc
* Dumping locally also allows a hawkeye user to freeze a configuration for a moment in time. This allows for:
    * A record of change (in addition to Cloud Trail)
    * The ability to audit past configurations with newly created rules
    * More?
* and because I initially wrote a scrape script before the idea to audit came be.  ;-)

Current State
=============

This tool is fairly new and being actively developed.  It's not guarenteed to work at all for you at this time.

That being said, I am working hard to get the initial tools working and to get my development more open and github friendly.

Installation
============

Within a shell, execute the following commands

    $ git clone https://github.com/neoCrimeLabs/hawkeye.git
    $ cd hawkeye
    $ sudo python setup.py

Once this is in a stable operating state, I'll add it to the python package repository.

Configuration
=============

TODO

Execution
=========

Dumping configuration
---------------------

TODO

Auditing a dumpfile
-------------------

TODO

Creating new rules
------------------

TODO

Contact
-------

TODO
