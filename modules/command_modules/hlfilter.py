from .. import irc, var, ini
from ..tools import is_identified

# Require NickServ authentication.
def ident (f):
    def command (user, channel, word):
        if is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: Identify with NickServ first.".format(user))
    
    return admin

# Register commands on the var module.
def ins_command ():
    var.commands["hloff"] = type("command", (object,), {})()
    var.commands["hloff"].method = hloff
    var.commands["hloff"].aliases = [".hloff", ".hlignore"]
    var.commands["hloff"].usage = ["{} - Stop the bot from highlighting you."]
    
    var.commands["hlon"] = type("command", (object,), {})()
    var.commands["hlon"].method = hlon
    var.commands["hlon"].aliases = [".hlon"]
    var.commands["hlon"].usage = ["{} - Let the bot highlight you(default)."]

# Populate data on the var module.
def ins_db ():
    var.data["hlignore"] = ini.fill_list("hlignore.ini")

# hloff command method.
def hloff (user, channel, word):
    if user.lower() not in var.data["hlignore"]:
        ini.add_to_list(user.lower(), "hlignore.ini")
        var.data["hlignore"].append(user.lower())
        
        irc.msg(channel, "{}: You won't be highlighted anymore.".format(user))
    else:
        irc.msg(channel, "{}: <-- You're not being highlighted.".format(user))

# hlon command method.
def hlon (user, channel, word):
    if user.lower() in var.data["hlignore"]:
        ini.remove_from_list(user.lower(), "hlignore.ini")
        var.data["hlignore"].remove(user.lower())
        
        irc.msg(channel, "{}: You'll be normally highlighted from now on.".format(user))
    else:
        irc.msg(channel, "{}: You're being normally highlighted already.".format(user))
