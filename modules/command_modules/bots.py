from .. import irc, var, ini

# Fill commands dictionary.
def ins_command ():
    var.commands["bots"] = type("command", (object,), {})()
    var.commands["bots"].method = bots_reply
    var.commands["bots"].aliases = [".bots", ".bot"]
    var.commands["bots"].usage = ["{} - Get the .bots reply."]

# Command method.
def bots_reply (user, channel, word):
    if "str.bots_reply" in var.settings:
        irc.msg(channel, "{}".format(var.settings["str.bots_reply"]))
    else:
        irc.msg(channel, "Reporting in! [Python]")