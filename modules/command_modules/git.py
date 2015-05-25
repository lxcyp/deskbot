from .. import var, ini
from .. import simpledb

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["gits"] = ini.fill_dict("gits.ini", "Gits")
    
    # Pick first and only element in list.
    for entry in var.data["gits"]:
        var.data["gits"][entry] = var.data["gits"][entry][0]
    
    access_db = simpledb.access_function(var.data["gits"], "git")
    mod_entry = simpledb.mod_function(var.data["gits"], "git", "gits.ini", "Gits")
    rm_entry = simpledb.rm_function(var.data["gits"], "git", "gits.ini", "Gits")

# Fill commands dictionary.
def ins_command ():
    var.commands["git"] = type("command", (object,), {})()
    var.commands["git"].method = read
    var.commands["git"].aliases = [".git"]
    var.commands["git"].usage = [line.format("{}", n="git") for line in simpledb.command_usage]

# Grab ident function from simpledb.
ident = simpledb.ident

# Command method.
def read (user, channel, word):
    if len(word) > 2 and word[1] in ["-set", "-s"]:
        mod_entry(user, channel, word)
    elif len(word) > 1 and word[1] in ["-rm", "-remove"]:
        rm_entry(user, channel, word)
    else:
        access_db(user, channel, word)

# Functions filled by ins_db(). Start as None.
access_db = None
mod_entry = None
rm_entry = None
