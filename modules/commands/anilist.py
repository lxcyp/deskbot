from .. import var, ini
from .. import simpledb

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["anilists"] = ini.fill_dict("anilists.ini", "AniLists")
    
    # Pick first and only element in list.
    for entry in var.data["anilists"]:
        var.data["anilists"][entry] = var.data["anilists"][entry][0]
    
    access_db = simpledb.access_function(var.data["anilists"], "anime list")
    mod_entry = simpledb.mod_function(var.data["anilists"], "anime list", "anilists.ini", "AniLists")
    rm_entry = simpledb.rm_function(var.data["anilists"], "anime list", "anilists.ini", "AniLists")

# Fill commands dictionary.
def ins_command ():
    var.commands["anilist"] = type("command", (object,), {})()
    var.commands["anilist"].method = read
    var.commands["anilist"].tags = ["databases", "simpledb"]
    var.commands["anilist"].aliases = [".anilist", ".animelist", ".alist"]
    var.commands["anilist"].usage = [line.format("{}", n="anime list") for line in simpledb.command_usage]

# Grab ident function from simpledb.
ident = simpledb.ident

# Command method.
def read (user, channel, word):
    if len(word) > 2 and word[1] in simpledb.mod_strings:
        mod_entry(user, channel, word)
    elif len(word) > 1 and word[1] in simpledb.del_strings:
        rm_entry(user, channel, word)
    else:
        access_db(user, channel, word)

# Functions filled by ins_db(). Start as None.
access_db = None
mod_entry = None
rm_entry = None
