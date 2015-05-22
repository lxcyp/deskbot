import os
from .. import irc, var
from ..tools import is_identified

# Fill commands dictionary.
def ins_command ():
    var.commands["join"] = type("command", (object,), {})()
    var.commands["join"].method = join
    var.commands["join"].aliases = [".join"]
    var.commands["join"].usage = ["{} #channel - Join channel."]
    
    var.commands["part"] = type("command", (object,), {})()
    var.commands["part"].method = part
    var.commands["part"].aliases = [".part"]
    var.commands["part"].usage = ["{} #channel - Part from channel."]
    
    var.commands["quit"] = type("command", (object,), {})()
    var.commands["quit"].method = quit
    var.commands["quit"].aliases = [".quit"]
    var.commands["quit"].usage = [
        "{} - Quit server and close bot.",
        "{} message - Use quit message when quitting from server."
    ]
    
    var.commands["raw"] = type("command", (object,), {})()
    var.commands["raw"].method = raw
    var.commands["raw"].aliases = [".raw"]
    var.commands["raw"].usage = ["{} content - Send raw text to the server."]
    
    var.commands["identify"] = type("command", (object,), {})()
    var.commands["identify"].method = identify
    var.commands["identify"].aliases = [".identify", ".ident"]
    var.commands["identify"].usage = ["{} - Try to identify with NickServ using set password."]
    
    var.commands["disable"] = type("command", (object,), {})()
    var.commands["disable"].method = disable
    var.commands["disable"].aliases = [".disable", ".rm"]
    var.commands["disable"].usage = ["{} .command1 .command2 ... - Disable commands for this channel."]
    
    var.commands["enable"] = type("command", (object,), {})()
    var.commands["enable"].method = enable
    var.commands["enable"].aliases = [".enable", ".add"]
    var.commands["enable"].usage = ["{} .command1 .command2 ... - Enable commands for this channel."]

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

# Quit server and close bot.
def quit (user, channel, word):
    irc.quit(" ".join(word[1:]) if len(word) > 1 else "")

# Send raw text to the server.
def raw (user, channel, word):
    if len(word) > 1:
        irc.ircsock.send(" ".join(word[1:]) + "\r\n")
    else:
        irc.msg(channel, "{}: Tell me something to send.".format(user))

# Sometimes the bot fails to identify with NickServ.
def identify (user, channel, word):
    irc.identify()

# Disable commands. Can accept multiple commands.
def disable (user, channel, word):
    dsbl_list = [cmd for cmd in word if cmd not in [".disable", ".enable"]]
    disabled = []
    
    # If there's nothing it can disable...
    if not dsbl_list:
        irc.msg(channel, "{}: No commands to disable.".format(user))
        return
    
    # Add channel to the command object disabled attribute, if not already in it.
    for command in dsbl_list:
        for cmd_name in var.commands:
            if command in var.commands[cmd_name].aliases:
                if channel in var.commands[cmd_name].disabled:
                    irc.notice(user, "{} is already disabled in this channel.".format(command))
                else:
                    var.commands[cmd_name].disabled.append(channel)
                    disabled.append(command)
    
    # Phew. Now check if anything was indeed disabled and what.
    if not disabled:
        irc.msg(channel, "{}: No commands were disabled.".format(user))
    else:
        irc.msg(channel, "{}: Disabled commands: {}".format(user, " ".join(disabled)))

# Enable commands. Can accept multiple commands.
def enable (user, channel, word):
    enbl_list = [cmd for cmd in word if cmd not in [".disable", ".enable"]]
    enabled = []
    
    # If there's nothing it can enable...
    if not enbl_list:
        irc.msg(channel, "{}: No commands to enable.".format(user))
        return
    
    # Remove channel from the command object disabled attribute, if in it.
    for command in enbl_list:
        for cmd_name in var.commands:
            if command in var.commands[cmd_name].aliases:
                if channel not in var.commands[cmd_name].disabled:
                    irc.notice(user, "{} is not disabled in this channel.".format(command))
                else:
                    var.commands[cmd_name].disabled.remove(channel)
                    enabled.append(command)
    
    # Phooey. Now check if anything was indeed enabled and what.
    if not enabled:
        irc.msg(channel, "{}: No commands were enabled.".format(user))
    else:
        irc.msg(channel, "{}: Enabled commands: {}".format(user, " ".join(enabled)))
