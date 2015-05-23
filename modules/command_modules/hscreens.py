from .. import var, ini
from .. import url_db

# This command uses a database, so allocate space for it.
var.data["hscreens"] = ini.fill_dict("hscreens.ini", "Homescreens")

# Fill command dictionary.
def ins_command ():
    var.commands["hscreen"] = type("command", (object,), {})()
    var.commands["hscreen"].method = read
    var.commands["hscreen"].aliases = [
        ".hscreen",
        ".homescreen",
        ".hscr"
    ]
    var.commands["hscreen"].usage = [line.format("{}", n="homescreen") for line in url_db.command_usage]

# This command will need NickServ auth sometimes.
ident = url_db.ident

# Used for the command method.
def read (user, channel, word):    
    if len(word) < 3:
        list_urls(user, channel, word)
    elif word[1] in ["-a", "-add"]:
        add_url(user, channel, word)
    elif word[1] in ["-rm", "-remove"]:
        delete_url(user, channel, word)
    elif word[1] in ["-re", "-replace"]:
        replace_url(user, channel, word)
    else:
        list_urls(user, channel, word)

# Functions.
list_urls = url_db.list_function(var.data["hscreens"], "homescreens")
add_url = url_db.add_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")
delete_url = url_db.delete_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")
replace_url = url_db.replace_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")
