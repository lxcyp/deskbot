from .. import var, ini
from .. import urldb

# This command uses a database, so allocate space for it.
def ins_db ():
    global list_urls, add_url
    global delete_url, replace_url
    
    var.data["desktops"] = ini.fill_dict("desktops.ini", "Desktops")
    
    list_urls = urldb.list_function(var.data["desktops"], "desktops")
    add_url = urldb.add_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")
    delete_url = urldb.delete_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")
    replace_url = urldb.replace_function(var.data["desktops"], "desktops", "desktops.ini", "Desktops")

# Fill command dictionary.
def ins_command ():
    var.commands["desktop"] = type("command", (object,), {})()
    var.commands["desktop"].method = read
    var.commands["desktop"].tags = ["databases", "urldb"]
    var.commands["desktop"].aliases = [
        ".desktop",
        ".dtop",
        ".dekstop"
    ]
    var.commands["desktop"].usage = [line.format("{}", n="desktop") for line in urldb.command_usage]

# This command will need NickServ auth sometimes.
ident = urldb.ident

# Used for the command method.
def read (user, channel, word):    
    if len(word) < 3:
        list_urls(user, channel, word)
    elif word[1] in urldb.add_strings:
        add_url(user, channel, word)
    elif word[1] in urldb.del_strings:
        delete_url(user, channel, word)
    elif word[1] in urldb.rep_strings:
        replace_url(user, channel, word)
    else:
        list_urls(user, channel, word)

# Functions. Start as None, will be filled by ins_db().
list_urls = None
add_url = None
delete_url = None
replace_url = None
