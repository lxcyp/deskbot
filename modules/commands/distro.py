from .. import var, ini
from .. import simpledb

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["distros"] = ini.fill_dict("distros.ini", "Distros")
    
    # Pick first and only element in list.
    for entry in var.data["distros"]:
        var.data["distros"][entry] = var.data["distros"][entry][0]
    
    namespace = simpledb.namespace(
        string_dictionary = var.data["distros"],
        dictionary_name   = "distro",
        section_name      = "Distros",
        filename          = "distros.ini"
    )
    
    access_db = namespace.access_function
    mod_entry = namespace.modify_function
    rm_entry  = namespace.remove_function

# Fill commands dictionary.
def ins_command ():
    var.commands["distro"] = type("command", (object,), {})()
    var.commands["distro"].method = read
    var.commands["distro"].tags = ["databases", "simpledb"]
    var.commands["distro"].aliases = [".distro", ".distribution"]
    var.commands["distro"].usage = [line.format("{}", n="distro") \
                                    for line in simpledb.command_usage]

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
