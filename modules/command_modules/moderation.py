from .. import irc, var, ini
from ..tools import is_identified
from ..tools import is_number
from ..tools import prefix
import thread
import time

# This is where hostmasks will be stored.
hostmasks = {}

# This is the akick dictionary.
akick_dict = {}

# Fill commands dictionary.
def ins_command ():
    var.commands["warn"] = type("command", (object,), {})()
    var.commands["warn"].method = warn
    var.commands["warn"].tags = ["moderation"]
    var.commands["warn"].aliases = [".warn"]
    var.commands["warn"].usage = ["{} user message - Give user a warning, following moderation policy."]
    
    var.commands["warnings"] = type("command", (object,), {})()
    var.commands["warnings"].method = warnings
    var.commands["warnings"].tags = ["moderation"]
    var.commands["warnings"].aliases = [".warnings", ".warns"]
    var.commands["warnings"].usage = [
        "{} user - Check user's warnings, if existant.",
        "{} user all - Get details about user's warnings in PM."
    ]
    
    var.commands["akick"] = type("command", (object,), {})()
    var.commands["akick"].method = akick
    var.commands["akick"].tags = ["moderation"]
    var.commands["akick"].aliases = [".akick"]
    var.commands["akick"].usage = [
        "{} user - Put user on akick for a minute.",
        "{} user time - Put user on akick for set time."
    ]
    
    # Start ban-check thread.
    thread.start_new_thread(ban_check, ())

# Insert a message monitor.
def ins_monitor (message):
    global hostmasks
    
    # Grab event.
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    if event in ["JOIN", "PRIVMSG"]:
        # Grab channel name.
        try:
            channel = message.split(" :")[1]
        except IndexError:
            channel = message.split(" JOIN ")[1]
        
        # Update user's host.
        hostmasks[user] = "*!*@" + message.split()[0].split("@")[1]
        
        # Check for akicks.
        if user in akick_dict or hostmasks[user] in akick_dict:
            entry = user if user in akick_dict else hostmasks[user]
            ak_pairs = akick_dict[entry][:]
        else:
            return
        
        for pair in ak_pairs:
            if channel == pair[0]:
                # Kick them if they're still akick'd.
                if time.time() < pair[1]:
                    irc.kick(channel, user, "You're still akick'd.")
                    ban(channel, user)
                # Else leave them be and take them off the list.
                else:
                    if len(ak_pairs) > 1:
                        akick_dict[entry].remove(pair)
                    else:
                        del akick_dict[entry]

# Fill databases.
def ins_db ():
    var.data["bans"] = []
    var.data["warnings"] = ini.fill_dict("warnings.ini", "Warnings")
    
    for user in var.data["warnings"]:
        lines = var.data["warnings"][user][:]
        lines = [
            (
                line.split()[0],            # Warning number.
                line.split()[1],            # Channel.
                line.split()[2],            # Warning time.
                " ".join(line.split()[3:])  # Reason
            )
            for line in lines
        ]
        var.data["warnings"][user] = lines
        
        # Add the user to the ban list if he's got more than two warnings.
        if len(lines) > 2:
            ban_duration = time_ban(len(lines))
            
            # WORK, YOU DUMB.

# Ident function.
def ident (f):
    def check (user, channel, word):
        if (
            prefix(user, channel) in [
                var.settings["ircop.prefix"],
                var.settings["owner.prefix"],
                var.settings["admin.prefix"],
                var.settings["op.prefix"],
                var.settings["halfop.prefix"]
            ] and
            is_identified(user)
        ):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: Check your privilege.".format(user))
            
    return check

###################################
# Warn users when they misbehave. #
###################################

def warn (user, channel, word):
    # Check if the bot can kick/ban.
    if prefix(irc.botnick, channel) not in [
        var.settings["ircop.prefix"],
        var.settings["owner.prefix"],
        var.settings["admin.prefix"],
        var.settings["op.prefix"],
        var.settings["halfop.prefix"]
    ]:
        irc.msg(channel, "I can't kick or ban. ;-;")
        return
    
    irc.msg(channel, "{}: Still being worked on, sorry.".format(user))
    
    # WORK YOU DUMB.

###################################
#       Check users' warnings.    #
###################################

def warnings (user, channel, word):
    irc.msg(channel, "{}: Still being worked on, sorry.".format(user))
    
    # WORK, YOU DUMB.

###################################
#           Akick users.          #
###################################

def akick (user, channel, word):
    # Check if the bot can kick/ban.
    if prefix(irc.botnick, channel) not in [
        var.settings["ircop.prefix"],
        var.settings["owner.prefix"],
        var.settings["admin.prefix"],
        var.settings["op.prefix"],
        var.settings["halfop.prefix"]
    ]:
        irc.msg(channel, "I can't kick or ban. ;-;")
        return
    
    # Needs at least two pieces of information.
    if len(word) < 3:
        irc.notice(user, "Syntax is .akick time_in_minutes user1 user2 ...")
        return
    
    if not is_number(word[1]):
        irc.msg(channel, "{}: Invalid number.".format(user))
        return
    
    ak_time = time.time() + 60*int(word[1])
    user_list = word[2:]
    
    # Reasonable time.
    if int(word[1]) < 1:
        irc.msg(channel, "{}: Please akick people for at least a minute.".format(user))
        return
    
    # Add users, channel and time to akick list. Kick and ban them, too.
    for nick in user_list:
        host = hostmasks[nick] if nick in hostmasks else nick
        if host in akick_dict:
            akick_dict[host].append((channel, ak_time))
        else:
            akick_dict[host] = [(channel, ak_time)]
        irc.kick(channel, nick, "You're being akick'd for {} minute(s).".format(word[1]))
        ban(channel, nick)
        var.data["bans"].append((nick, channel, ak_time))
    
    irc.msg(channel, "{}: {} will be akick'd for {} minute(s).".format(user, ", ".join(user_list), word[1]))

###################################
#         Check user bans.        #
###################################

def ban_check ():
    # Loop fo' eva'
    while True:
        unbanned = []
        
        for ban in var.data["bans"]:
            user = ban[0]
            channel = ban[1]
            unban_time = ban[2]
            
            if time.time() >= unban_time:
                unban(channel, user)
                unbanned.append(ban)
        
        for ban in unbanned:
            var.data["bans"].remove(ban)
        
        time.sleep(1)
            

###################################
#     Miscellaneous functions.    #
###################################

def unban (channel, user):
    irc.mode(channel, user, "-b")
    irc.msg(user, "You were unbanned from {}. Disregard this message if you were already unbanned.".format(channel))

def ban (channel, user):
    irc.mode(channel, user, "+b")
