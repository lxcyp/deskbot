from .. import irc, var
from tools import is_identified

# Fill commands dictionary with usage.
def ins_help ():
    var.commands[".join"] = type("command", (object,), {})()
    var.commands[".join"].aliases = [".join"]
    var.commands[".join"].usage = ["{} #channel - Join channel."]
    
    var.commands[".part"] = type("command", (object,), {})()
    var.commands[".part"].aliases = [".part"]
    var.commands[".part"].usage = ["{} #channel - Part from channel."]
    
    var.commands[".raw"] = type("command", (object,), {})()
    var.commands[".raw"].aliases = [".raw"]
    var.commands[".raw"].usage = ["{} content - Send raw text to the server."]
    
    var.commands[".identify"] = type("command", (object,), {})()
    var.commands[".identify"].aliases = [".identify", ".ident"]
    var.commands[".identify"].usage = ["{} - Try to identify with NickServ using set password."]

# Require NickServ authentication for the admin.
def ident (f):
    def admin (user, channel, word):
        if user == irc.admin and is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: You don't have admin rights.".format(user))
    return admin

# Join a channel.
def join (user, channel, word):
    if len(word) > 1:
        irc.join(word[1])
    else:
        irc.msg(channel, "{}: Tell me a channel to join.".format(user))

# Part from a channel.
def part (user, channel, word):
    if len(word) > 1:
        irc.part(word[1], " ".join(word[2:]) if len(word) > 2 else "")
    else:
        irc.msg(channel, "{}: Tell me a channel to part from.".format(user))

# Send raw text to the server.
def raw (user, channel, word):
    if len(word) > 1:
        irc.ircsock.send(" ".join(word[1:]) + "\r\n")
    else:
        irc.msg(channel, "{}: Tell me something to send.".format(user))

# Sometimes the bot fails to identify with NickServ.
def identify (user, channel, word):
    irc.identify()
