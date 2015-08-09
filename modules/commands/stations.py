from .. import var, ini
from .. import urldb

# This command uses a database, so allocate space for it.
def ins_db ():
    global list_urls, add_url
    global delete_url, replace_url
    
    var.data["stations"] = ini.fill_dict("stations.ini", "Stations")
    
    namespace = urldb.namespace(
        url_dictionary  = var.data["stations"],
        dictionary_name = "stations",
        section_name    = "Stations",
        filename        = "stations.ini",
        max             = 5
    )
    
    list_urls   = namespace.list_function
    add_url     = namespace.add_function
    delete_url  = namespace.delete_function
    replace_url = namespace.replace_function

# Fill command dictionary.
def ins_command ():
    var.commands["station"] = type("command", (object,), {})()
    var.commands["station"].method = read
    var.commands["station"].tags = ["databases", "urldb"]
    var.commands["station"].aliases = [
        ".station",
        ".stn"
    ]
    var.commands["station"].usage = [line.format("{}", n="station") for line in urldb.command_usage]

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
