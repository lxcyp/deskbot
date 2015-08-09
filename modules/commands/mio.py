import random
from .. import irc, var, ini
from ..tools import is_identified

def ident (f):
    
    def check (user, channel, word):
        if len(word) > 2 and word[1] in ["add", "-a", "-add", "--add"]:
            if user == irc.admin and is_identified(user):
                f(user, channel, word)
            else:
                irc.msg(channel, "{}: You don't have admin rights.")
        else:
            f(user, channel, word)
    
    return check

def ins_command ():
    var.commands["mio"] = type("command", (object,), {})()
    var.commands["mio"].method = mio
    var.commands["mio"].tags = ["fun"]
    var.commands["mio"].aliases = [".mio"]
    var.commands["mio"].usage = ["{} - Get a random picture of Mio."]

def mio (user, channel, word):
    
    if len(word) > 2 and word[1] in ["add", "-a", "-add", "--add"]:
        url = word[2]
        ini.add_to_list(line = url, filename = "misc/mio.txt", raw_path = True)
        
        irc.msg(channel, "{}: Line added successfully.".format(user))
    else:
        f = open("misc/mio.txt", "r")
        p_list = [l.strip() for l in f.readlines()]
        f.close()
    
        irc.msg(channel, "Random picture of Mio: {}".format(random.choice(p_list)))
