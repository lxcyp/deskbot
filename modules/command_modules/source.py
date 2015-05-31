from .. import irc, var, ini

# Fill commands dictionary.
def ins_command ():
    var.commands["source"] = type("command", (object,), {})()
    var.commands["source"].method = source
    var.commands["source"].aliases = [".source"]
    var.commands["source"].usage = ["{} - Get a link to the bots' source."]

# Command method.
def source (user, channel, word):
    if "str.source" in var.settings:
        irc.msg(channel, "{}".format(var.settings["str.source"]))
    else:
        irc.msg(channel, "Source: http://github.com/skewerr/deskbot")