from .. import irc, var, ini
from ..tools import is_identified, prefix
from ..tools import exec_python, nick_check
import random, re, os, sys, time

# Taiga quotes list.
quotes = [
    "I dreamt that you were a dog. And the dog was my husband. Anyway, it was the worst dream ever.",
    "Well, I'd better get back to my seat. The unmarried woman with her unmarried face is about to come to start the unmarried homeroom.",
    "The thing you wished for the most, is something you'll never get.",
    "The stupid chihuahua was really taking a shower. She was... boing... Boing... BOING!!",
    "How can I know what to do later when I don't know what to do right now?",
    "It was like a rough, dry wilderness. Also, it was really, really warm..."
]


###########################################
#           ins_command method            #
###########################################


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
    
    var.commands["disabled"] = type("command", (object,), {})()
    var.commands["disabled"].method = disabled
    var.commands["disabled"].aliases = [".disabled", ".rm'd"]
    var.commands["disabled"].usage = [
        "{} - List disabled command for this channel.",
        "{} #channel - List disabled commands for channel."
    ]

    var.commands["enable"] = type("command", (object,), {})()
    var.commands["enable"].method = enable
    var.commands["enable"].aliases = [".enable", ".add"]
    var.commands["enable"].usage = ["{} .command1 .command2 ... - Enable commands for this channel."]
    
    var.commands["nick"] = type("command", (object,), {})()
    var.commands["nick"].method = nick
    var.commands["nick"].aliases = [".nick"]
    var.commands["nick"].usage = ["{} nick - Change bot's nickname."]
    
    var.commands["passwd"] = type("command", (object,), {})()
    var.commands["passwd"].method = passwd
    var.commands["passwd"].aliases = [".passwd", ".pwd", ".pass"]
    var.commands["passwd"].usage = ["{} password - Change NickServ password the bot uses to identify."]
    
    var.commands["ctcp"] = type("command", (object,), {})()
    var.commands["ctcp"].method = ctcp
    var.commands["ctcp"].aliases = [".ctcp"]
    var.commands["ctcp"].usage = [
        "{} request - Check CTCP reply for request, if present.",
        "{} remove request - Remove entry for CTCP request reply.",
        "{} request reply - Add a CTCP reply for request."
    ]
    
    var.commands["restart"] = type("command", (object,), {})()
    var.commands["restart"].method = restart
    var.commands["restart"].aliases = [".restart"]
    var.commands["restart"].usage = [
        "{} - Restarts the bot.",
        "{} message - Restarts with bot with quit message."
    ]
    
    var.commands["ignore"] = type("command", (object,), {})()
    var.commands["ignore"].method = ignore
    var.commands["ignore"].aliases = [".ignore"]
    var.commands["ignore"].usage = [
        "{} - See ignored users list.",
        "{} user - Ignore a user."
    ]
    
    var.commands["py"] = type("command", (object,), {})()
    var.commands["py"].method = py_exec
    var.commands["py"].aliases = [".exec", ".py", ".python"]
    var.commands["py"].usage = [
        "{} line - Execute a line in python in commands.py."
    ]

###########################################
#              ident method               #
###########################################

# Require NickServ authentication for the admin.
def ident (f):
    def admin (user, channel, word):
        if (
            (user == irc.admin and is_identified(user)) or
            word[0] in [".disabled"]
        ):
            f(user, channel, word)
        elif word[0] in [".enable", ".disable"] and is_identified(user):
            if prefix(user, channel) in [
                var.settings["op.prefix"],
                var.settings["ircop.prefix"],
                var.settings["owner.prefix"],
                var.settings["admin.prefix"],
                var.settings["halfop.prefix"]
            ]:
                f(user, channel, word)
            else:
                irc.msg(channel, "{}: You need at least hop to do that.".format(user))
        else:
            irc.msg(channel, "{}: You don't have admin rights.".format(user))
    return admin


###########################################
#     .join, .part, .quit and .raw        #
###########################################


# Join a channel.
def join (user, channel, word):
    if len(word) > 1:
        irc.join(word[1])
        ini.add_to_list(word[1], "channels.ini")
    else:
        irc.msg(channel, "{}: Tell me a channel to join.".format(user))

# Part from a channel.
def part (user, channel, word):
    if len(word) > 1:
        irc.part(word[1], " ".join(word[2:]) if len(word) > 2 else "")
        ini.remove_from_list(word[1], "channels.ini")
    else:
        irc.msg(channel, "{}: Tell me a channel to part from.".format(user))

# Quit server and close bot.
def quit (user, channel, word):
    irc.quit(" ".join(word[1:]) if len(word) > 1 else random.choice(quotes))
    raise SystemExit

# Send raw text to the server.
def raw (user, channel, word):
    if len(word) > 1:
        irc.ircsock.send(" ".join(word[1:]) + "\r\n")
    else:
        irc.msg(channel, "{}: Tell me something to send.".format(user))


###########################################
#         .identify and .passwd           #
###########################################


# Sometimes the bot fails to identify with NickServ.
def identify (user, channel, word):
    irc.identify()

# Update NickServ password before identifying again.
def passwd (user, channel, word):
    if len(word) < 2:
        irc.msg(irc.admin, "Send me a password, moron.")
    else:
        irc.password = word[1]
        irc.msg(irc.admin, "Password updated.")


###########################################
#                 .nick                   #
###########################################


# Update botnick.
def nick (user, channel, word):
    if len(word) < 2:
        irc.msg(channel, "{}: You gotta tell me what nick to change to.".format(user))
    else:
        # Check if the nickname is valid.
        if not re.match("[a-zA-Z\[\]\\`_\^\{\|\}][a-zA-Z0-9\[\]\\`_\^\{\|\}]", word[1]):
            irc.msg(channel, "{}: Invalid nickname.".format(user))
        else:
            irc.nick(word[1])
            err = nick_check()
            if err:
                irc.notice(irc.admin, "{} is erroneous or already in use.".format(word[1]))
            else:
                irc.botnick = word[1]


###########################################
#         .disable and .enable            #
###########################################


# Disable commands. Can accept multiple commands.
def disable (user, channel, word):
    dsbl_list = [cmd for cmd in word if cmd not in [".disable", ".enable"]]
    disabled = []
    
    # Should .disable be the only thing issued, check .disabled.
    if len(word) == 1:
        disabled(user, channel, word)
        return
    
    # If there's nothing it can disable...
    if not dsbl_list:
        irc.msg(channel, "{}: No commands to disable.".format(user))
        return
    
    # Add channel to the command object disabled attribute, if not already in it.
    for command in dsbl_list:
        for cmd_name in var.commands:
            if (
                command in var.commands[cmd_name].aliases or
                (
                    hasattr(var.commands[cmd_name], "tags") and
                    command in var.commands[cmd_name].tags
                )
            ):
                if (
                    channel in var.commands[cmd_name].disabled and
                    command.startswith(".")
                ):
                    irc.notice(user, "{} is already disabled in this channel.".format(command))
                elif channel not in var.commands[cmd_name].disabled:
                    var.commands[cmd_name].disabled.append(channel)
                    channel_list = var.commands[cmd_name].disabled
                    ini.add_to_ini("Disabled Commands", cmd_name, "\n".join(channel_list), "settings.ini")
                    disabled.append(command if command.startswith(".") else ("." + cmd_name))
    
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
            if (
                command in var.commands[cmd_name].aliases or
                (
                    hasattr(var.commands[cmd_name], "tags") and
                    command in var.commands[cmd_name].tags
                )
            ):
                if (
                    channel not in var.commands[cmd_name].disabled and
                    command.startswith(".")
                ):
                    irc.notice(user, "{} is not disabled in this channel.".format(command))
                elif channel in var.commands[cmd_name].disabled:
                    var.commands[cmd_name].disabled.remove(channel)
                    channel_list = var.commands[cmd_name].disabled
                    ini.add_to_ini("Disabled Commands", cmd_name, "\n".join(channel_list), "settings.ini")
                    enabled.append(command if command.startswith(".") else ("." + cmd_name))
    
    # Phooey. Now check if anything was indeed enabled and what.
    if not enabled:
        irc.msg(channel, "{}: No commands were enabled.".format(user))
    else:
        irc.msg(channel, "{}: Enabled commands: {}".format(user, " ".join(enabled)))


###########################################
#               .disabled                 #
###########################################


def disabled (user, channel, word):
    # In case the admin wants to check on another channel.
    if len(word) > 1:
        target_channel = word[1] if word[1].startswith("#") else "#" + word[1]
    else:
        target_channel = channel
    
    # Grab disabled commands list based on ini file.
    command_dict = ini.fill_dict("settings.ini", "Disabled Commands")
    command_list = [
        "." + command for command in command_dict if target_channel in command_dict[command]
    ]
    
    if command_list:
        irc.msg(channel, "Disabled commands for {}: {}".format(target_channel, " ".join(command_list)))
    else:
        irc.msg(channel, "No commands are disabled for {}.".format(target_channel))


###########################################
#                 .ctcp                   #
###########################################


# Add CTCP replies.
def ctcp (user, channel, word):
    # This command can accept only one piece of info.
    if len(word) < 3:
        # In case a request name is given.
        if len(word) == 2:
            request = word[1].upper()
            
            if request in var.ctcp:
                irc.msg(channel, "{}: {} [{}]".format(user, var.ctcp[request], request))
            else:
                irc.msg(channel, "{}: No reply set for {}.".format(user, request))
        # Not it does need a piece of info.
        else:
            irc.msg(channel, "{}: Wrong syntax. Check .help".format(user))
        
        return
    
    request = word[1].upper()
    reply = " ".join(word[2:])
    
    if request != "REMOVE":
        var.ctcp[request] = reply
        ini.add_to_ini("CTCP", request, reply, "ctcp.ini")
        irc.msg(channel, "{}: CTCP {} reply added successfully.".format(user, request))
    else:
        request = word[2].upper()
        
        # Check if it can be removed and remove it.
        if request in var.ctcp:
            del var.ctcp[request]
            ini.remove_from_ini("CTCP", request, "ctcp.ini")
            irc.msg(channel, "{}: CTCP {} reply removed successfully.".format(user, request))
        else:
            irc.msg(channel, "{}: There's nothing set for CTCP {}.".format(user, request))

###########################################
#                .ignore                  #
###########################################

def ignore (user, channel, word):
    if len(word) == 1:
        irc.notice(user, "Ignored users: {}".format(" ".join(var.ignored)))
    else:
        ignored = [nick for nick in word[1:] if nick not in var.ignored]
        
        for nick in ignored:
            ini.add_to_list(nick, "ignored.ini")
            var.ignored.append(nick)
        
        if ignored:
            irc.msg(channel, "{}: I'll ignore {} from now on.".format(user, ", ".join(ignored)))
        else:
            irc.msg(channel, "{}: No new nicks were ignored.".format(user))

###########################################
#                .restart                 #
###########################################

# Restart the bot.
def restart (user, channel, word):
    irc.quit(" ".join(word[1:]) if len(word) > 1 else random.choice(quotes))
    os.execl(sys.executable, *([sys.executable] + sys.argv + ["-b", irc.botnick]))

###########################################
#                   .py                   #
###########################################

# Execute a line given by the admins in commands.py.
def py_exec (user, channel, word):
    if len(word) < 2:
        irc.msg(channel, "{}: You have to give me a line to execute.".format(user))
    else:
        exec_python(channel, " ".join(word[1:]))
