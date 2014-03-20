# This file is a configuration file for hawkeye
{
"log": {
    # Note stderr is the only module affected by command line options -v -q
    "stderr": {
        "options": {}, # None for stderr for now,
        "levels":  ["info", "error", "alert"]},
    },
    "file": {
        "options": { "file": "debug.log" },
        "levels":  ["debug", "info", "error", "alert"]},
    },
"keys": {
    "personal": {
        "key_id":     "A...................",
        "access_key": "A......................................."},
    },
}
