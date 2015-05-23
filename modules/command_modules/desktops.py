from .. import var, ini
from .. import url_db

# This command uses a database, so allocate space for it.
var.data["desktops"] = ini.fill_dict("desktops.ini", "Desktops")

# Fill command dictionary.
def ins_command ():
    var.commands["desktop"] = type("command", (object,), {})()
    var.commands["desktop"].method = read
    var.commands["desktop"].aliases = [
        ".desktop",
        ".dtop",
        ".dekstop"
    ]
    var.commands["desktop"].usage = [line.format("{}", n="desktop") for line in url_db.command_usage]

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
list_urls = url_db.list_function(var.data["desktops"], "desktops")
add_url = url_db.add_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")
delete_url = url_db.delete_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")
replace_url = url_db.replace_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")
