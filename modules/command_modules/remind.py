import threading
from .. import irc, var
from ..tools import is_number

# Fill command dictionary.
def ins_command ():
    var.commands["remind"] = type("command", (object,), {})()
    var.commands["remind"].method = remind
    var.commands["remind"].tags = ["other"]
    var.commands["remind"].aliases = [".remind", ".remindme"]
    var.commands["remind"].usage = ["{} t reminder message - Get a reminder in t minutes."]

# Command method.
def remind (user, channel, word):
    if len(word) < 3:
        irc.msg(channel, "Usage is {} t message".format(word[0]))
        return
    
    if not is_number(word[1]):
        irc.msg(channel, "Please input a valid number.")
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
