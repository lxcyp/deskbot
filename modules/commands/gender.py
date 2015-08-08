from .. import var, ini
from .. import simpledb

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["genders"] = ini.fill_dict("genders.ini", "Genders")
    
    # Pick first and only element in list.
    for entry in var.data["genders"]:
        var.data["genders"][entry] = var.data["genders"][entry][0]
    
    access_db = simpledb.access_function(var.data["genders"], "gender")
    mod_entry = simpledb.mod_function(var.data["genders"], "gender", "genders.ini", "Genders")
    rm_entry = simpledb.rm_function(var.data["genders"], "gender", "genders.ini", "Genders")

# Fill commands dictionary.
def ins_command ():
    var.commands["gender"] = type("command", (object,), {})()
    var.commands["gender"].method = read
    var.commands["gender"].tags = ["databases", "simpledb"]
    var.commands["gender"].aliases = [".gender"]
    var.commands["gender"].usage = [line.format("{}", n="gender") for line in simpledb.command_usage]

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
