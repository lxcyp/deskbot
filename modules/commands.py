import irc, sys, var
from command_modules import *

# Parsing text.

def read (msg):
    print msg
    
    # Check for server ping.
    if msg.startswith("PING :"):
        return irc.pong(msg.split(' :')[1])
    
    # If the message received isn't a server ping, proceed.
    user = msg.split('!')[0][1:]
    
    try:
        event = msg.split(' ')[1]
    except IndexError:
        event = ''
    
    if event == "PRIVMSG":
        channel = msg.split(' ')[2] if msg.split(' ')[2] != irc.botnick else user
        content = msg.split(' :', 1)[1] if len(msg.split(' :')) > 1 else ''
        privmsg(user, channel, content)
    elif event == "INVITE":
        channel = msg.split(' :')[1]
        invite(user, channel)

# Treating events.

def privmsg (user, channel, content):
    word = [w for w in content.split(' ') if w]
    
    if len(word) > 0 and word[0] in commands:
        commands[word[0]](user, channel, word)

def invite (user, channel):
    irc.join(channel)
    irc.msg(channel, "{} invited me here.".format(user))

# Should the user need to be identified, this function is called.

def ident (f):
    module = sys.modules[f.__module__]
    if hasattr(module, "ident"):
        return module.ident(f)
    else:
        return f

# Filling the command dictionary in var.

def fill_commands ():
    global commands
    for module in sys.modules:
        if hasattr(sys.modules[module], "ins_command"):
            sys.modules[module].ins_command()
    for command in var.commands:
        for alias in var.commands[command].aliases:
            commands[alias] = ident(var.commands[command].method)

# Dictionary responsible for handling commands.

commands = {}
