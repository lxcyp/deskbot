from .. import irc, var, ini
from ..tools import is_identified
from .. import simpledb

# The user needs to be registered and identified.
def ident (f):
    def check (user, channel, word):
        if is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: Identify with NickServ first.".format(user))
    return check

# Insert a message monitor.
def ins_monitor (message):
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    if event in ["JOIN"]:
        # Grab channel name.
        try:
            channel = message.split(" :")[1]
        except IndexError:
            channel = message.split(" JOIN ")[1]
        
        greet(user, channel)

# Insert command to set intros.
def ins_command ():
    var.commands["intro"] = type("command", (object,), {})()
    var.commands["intro"].method = read
    var.commands["intro"].tags = ["databases", "simpledb"]
    var.commands["intro"].aliases = [".intro", ".introduction"]
    var.commands["intro"].usage = [
        "{} - See your greet message.",
        "{} -set intro - Set your greet message.",
        "{} -rm - Remove your greet message."
    ]

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["intros"] = ini.fill_dict("intros.ini", "Introductions")
    var.data["intros"] = {
        user:var.data["intros"][user][0] for user in var.data["intros"]
    }
    
    access_db = simpledb.access_function(var.data["intros"], "intro")
    mod_entry = simpledb.mod_function(var.data["intros"], "intro", "intros.ini", "Introductions")
    rm_entry = simpledb.rm_function(var.data["intros"], "intro", "intros.ini", "Introductions")

# Command method.
def read (user, channel, word):
    if len(word) > 2 and word[1] in ["-set", "-s"]:
        mod_entry(user, channel, word)
    elif len(word) > 1 and word[1] in ["-rm", "-remove"]:
        rm_entry(user, channel, word)
    else:
        access_db(user, channel, word)

# Greet the user, if possible.
def greet (user, channel):
    # Add entry for channel in settings if it isn't present.
    # Stop this madness if intros are disabled.
    if "intro.{}".format(channel) in var.settings:
        if not var.settings["intro.{}".format(channel)]:
            return
    else:
        var.settings["intro.{}".format(channel)] = True
        ini.add_to_ini("Settings", "intro.{}".format(channel), "true", "settings.ini")
    
    if user in var.data["intros"]:
        irc.msg(channel, "\x0f{}".format(var.data["intros"][user]))

# Functions filled by ins_db(). Start as None.
access_db = None
mod_entry = None
rm_entry = None
