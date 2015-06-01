from .. import var, ini
from .. import urldb

# This command uses a database, so allocate space for it.
def ins_db ():
    global list_urls, add_url
    global delete_url, replace_url
    
    var.data["hscreens"] = ini.fill_dict("hscreens.ini", "Homescreens")
    
    list_urls = urldb.list_function(var.data["hscreens"], "homescreens")
    add_url = urldb.add_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")
    delete_url = urldb.delete_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")
    replace_url = urldb.replace_function(var.data["hscreens"], "homescreens", "hscreens.ini", "Homescreens")

# Fill command dictionary.
def ins_command ():
    var.commands["hscreen"] = type("command", (object,), {})()
    var.commands["hscreen"].method = read
    var.commands["hscreen"].tags = ["databases", "urldb"]
    var.commands["hscreen"].aliases = [
        ".hscreen",
        ".homescreen",
        ".hscr"
    ]
    var.commands["hscreen"].usage = [line.format("{}", n="homescreen") for line in urldb.command_usage]

# This command will need NickServ auth sometimes.
ident = urldb.ident

# Used for the command method.
def read (user, channel, word):    
    if len(word) < 3:
        list_urls(user, channel, word)
    elif word[1] in ["-a", "-add", "--add"]:
        add_url(user, channel, word)
    elif word[1] in ["-rm", "-remove", "--remove"]:
        delete_url(user, channel, word)
    elif word[1] in ["-re", "-replace", "--replace"]:
        replace_url(user, channel, word)
    else:
        list_urls(user, channel, word)

# Functions.
list_urls = None
add_url = None
delete_url = None
replace_url = None

