from .. import irc, var, ini
from ..tools import is_identified
from ..tools import prefix
import time

# Fill commands dictionary.
def ins_command ():
    var.commands["seen"] = type("command", (object,), {})()
    var.commands["seen"].method = seen
    var.commands["seen"].tags = ["other"]
    var.commands["seen"].aliases = [".seen"]
    var.commands["seen"].usage = ["{} user - Be notified of when user was last seen."]
    
    var.commands["track"] = type("command", (object,), {})()
    var.commands["track"].method = track
    var.commands["track"].tags = ["other"]
    var.commands["track"].aliases = [".track"]
    var.commands["track"].usage = ["{} - Start channel .seen tracking."]
    
    var.commands["untrack"] = type("command", (object,), {})()
    var.commands["untrack"].method = untrack
    var.commands["untrack"].tags = ["other"]
    var.commands["untrack"].aliases = [".untrack"]
    var.commands["untrack"].usage = ["{} - Stop channel .seen tracking."]

# Make space for it in var.data.
def ins_db ():
    var.data["seen"] = ini.fill_dict("seen.ini", "Seen")
    var.data["not_track"] = ini.fill_list("seen_blist.ini")

# ident function.
def ident (f):
    def seen (user, channel, word):
        if (
            (user == irc.admin and is_identified(user)) or
            word[0] in [".seen"]
        ):
            f(user, channel, word)
        elif word[0] in [".untrack", ".track"] and is_identified(user):
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
    return seen

# Insert message monitor.
def ins_monitor (message):
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    # The user joins a channel.
    if event == "JOIN":
        try:
            channel = message.split(" :")[1]
        except IndexError:
            channel = message.split(" JOIN ")[1]
        
        # Stop if the channel is on the untracked list.
        if channel in var.data["not_track"]:
            return
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = ["joining {}.".format(channel), "Time: {}. (GMT-3:00)".format(timestamp)]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen
    
    # The user leaves a channel.
    if event == "PART":
        channel = message.split(" PART ")[1].split(" :")[0]
        
        # Stop if the channel is on the untracked list.
        if channel in var.data["not_track"]:
            return
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = ["parting {}.".format(channel), "Time: {}. (GMT-3:00)".format(timestamp)]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen
        
    # A channel message is received.
    elif event == "PRIVMSG":
        channel = message.split(' ')[2] if message.split(' ')[2] != irc.botnick else user
        content = message.split(' :', 1)[1] if len(message.split(' :')) > 1 else ''
        
        # Stop if the channel is on the untracked list.
        if channel in var.data["not_track"]:
            return
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = [
            "in {} saying: {}".format(channel, content),
            "Time: {}. (GMT -3:00)".format(timestamp)
        ]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen

# Commad method.
def seen (user, channel, word):
    if len(word) == 1:
        irc.msg(channel, "Seen who?")
        return
    
    # Fun addition.
    if channel == "#rice" and irc.server == "irc.rizon.net" and word[1].lower() in [
        "kori", "kore", "coring", "cori",
        "curry", "corey", "koring", "koritos"
    ]:
        irc.msg(channel, "{}: kori's right there, what are you talking about?".format(user))
        return
    
    for nick in var.data["seen"]:
        if nick.lower() == word[1].lower():
            word[1] = nick
    
    if word[1] not in var.data["seen"]:
        irc.msg(channel, "{}: Sorry, I have not seen {}.".format(user, word[1]))
    else:
        irc.msg(channel, "{} was last seen {}".format(word[1], var.data["seen"][word[1]][0]))
        irc.msg(channel, var.data["seen"][word[1]][1])

# track command method.
def track (user, channel, word):
    if channel in var.data["not_track"]:
        var.data["not_track"].remove(channel)
        ini.remove_from_list(channel, "seen_blist.ini")
        
        irc.msg(channel, "{}: .seen will track your channel from now on.".format(user))
    else:
        irc.msg(channel, "{}: .seen is already tracking your channel.".format(user))

# untrack command method.
def untrack (user, channel, word):
    if channel not in var.data["not_track"]:
        var.data["not_track"].append(channel)
        ini.add_to_list(channel, "seen_blist.ini")
        
        irc.msg(channel, "{}: .seen won't track your channel from now on.".format(user))
    else:
        irc.msg(channel, "{}: .seen is already set not to track your channel.".format(user))
