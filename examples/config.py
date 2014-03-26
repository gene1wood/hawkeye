# This file is a configuration file for hawkeye
{
    "log": [
    # Note stderr is the only module affected by command line options -v -q
        {
            "module": "stderr",
            "levels":  ["info", "error", "alert"]
        },
        {
            "module":   "file",
            "file":     "logs/debug.txt",
            "mode":     "w",
            "levels":  ["debug"]
        },
        {
            "module":   "file",
            "file":     "logs/info.txt",
            "mode":     "a",
            "levels":  ["info"]
        },
        {
            "module":   "file",
            "file":     "logs/error.txt",
            "mode":     "w",
            "levels":  ["error"]
        },
        {
            "module":   "file",
            "file":     "logs/alert.txt",
            "mode":     "a",
            "levels":  ["alert"]
        },
    ],
    "keys": [
        {
            "name":         "Account 1",
            "key_id":       "AK..................",
            "access_key":   "........................................",
        },{
            "name":         "Descriptive Name",
            "key_id":       "AK..................",
            "access_key":   "........................................",
        },{
            "name":         "Another Account",
            "key_id":       "AK..................",
            "access_key":   "........................................",
        },
    ],
}
