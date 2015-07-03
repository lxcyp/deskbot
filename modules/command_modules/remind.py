import threading
from .. import irc, var
from ..tools import is_number

# Dictionary used by the message monitor.
onjoin_rem = {}

# Fill command dictionary.
def ins_command ():
    var.commands["remind"] = type("command", (object,), {})()
    var.commands["remind"].method = remind
    var.commands["remind"].tags = ["other"]
    var.commands["remind"].aliases = [".remind", ".remindme"]
    var.commands["remind"].usage = [
        "{} t message here. - Get a reminder in t minutes.",
        "{} j message here. - Get a reminder on the next time you join."
    ]

# Insert a message monitor.
def ins_monitor (message):
    # No point going further if there's no reminder.
    if not onjoin_rem:
        return
    
    # Parse for user and event.
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    if event in ["JOIN"]:
        # Grab channel name.
        try:
            channel = message.split(" :")[1]
        except IndexError:
            channel = message.split(" JOIN ")[1]
        
        # Check with the dictionary if he has a set reminder.
        if user in onjoin_rem:
            irc.msg(channel, "{}: {}".format(user, onjoin_rem[user]))
            del onjoin_rem[user]

# Command method.
def remind (user, channel, word):
    if len(word) < 3:
        irc.msg(channel, "Usage is {} [onjoin|time] message".format(word[0]))
        return
    
    if not is_number(word[1]):
        if word[1] in ["j", "-j", "join", "onjoin"]:
            # Add to the message monitor dictionary.
            onjoin_rem[user] = " ".join(word[2:])
            
            irc.msg(channel, "{}: Reminder set for when you join again.".format(user))
            return
        else:
            irc.msg(channel, "Please input a valid number for time.")
        return
    
    timespan = int(word[1])
    message  = " ".join(word[2:])
    
    if timespan > 1440:
        irc.msg(channel, "{}: Just write that on a piece of paper, come on.".format(user))
        return
    elif timespan < 1:
        irc.msg(channel, "{}: no".format(user))
        return
    
    threading.Timer(60*timespan, send, [user, channel, message]).start()
    irc.msg(channel, "{}: I'll remind you of that in {} minutes.".format(user, timespan))

# Reminder function.
def send (user, channel, message):
    irc.msg(channel, "{}: {}".format(user, message))
