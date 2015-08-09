from .. import var, ini
from .. import urldb

# This command uses a database, so allocate space for it.
def ins_db ():
    global list_urls, add_url
    global delete_url, replace_url
    
    var.data["hscreens"] = ini.fill_dict("hscreens.ini", "Homescreens")
    
    namespace = urldb.namespace(
        url_dictionary  = var.data["hscreens"],
        dictionary_name = "homescreens",
        section_name    = "Homescreens",
        filename        = "hscreens.ini",
        max             = 5
    )
    
    list_urls   = namespace.list_function
    add_url     = namespace.add_function
    delete_url  = namespace.delete_function
    replace_url = namespace.replace_function

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
    var.commands["hscreen"].usage = [line.format("{}", n="homescreen") \
                                        for line in urldb.command_usage]

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

# Functions.
list_urls = None
add_url = None
delete_url = None
replace_url = None
