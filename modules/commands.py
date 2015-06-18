import irc, sys, var, ini
from command_modules import *
import time

# Misc. attributes.
split_line = ""

###########################################
#     Interpreting received messages.     #
###########################################

def read (msg, *args):
    global split_line
    
    print msg
    
    # Save a split line.
    if args:
        split_line = args[0]
    
    # Check for server ping.
    if msg.startswith("PING :"):
        irc.pong(msg.split(' :')[1])
        return
    
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
    elif event == "NOTICE":
        channel = msg.split(' ')[2] if msg.split(' ')[2] != irc.botnick else user
        content = msg.split(' :', 1)[1] if len(msg.split(' :')) > 1 else ''
        notice(user, channel, content)
    elif event == "INVITE":
        channel = msg.split(' :')[1]
        invite(user, channel)
    elif event == "NICK":
        if user == irc.admin:
            irc.admin = msg.split(' :')[1]
    
    # Finally, call the monitor functions.
    for function in monitor:
        function(msg)

###########################################
#            Treating events.             #
###########################################

def privmsg (user, channel, content):
    word = filter(bool, content.split(' '))
    
    # Ignored people get out.
    if user in var.ignored:
        return
    
    if len(word) and word[0] in commands:
        commands[word[0]](user, channel, word)
    elif len(word) and word[0].startswith("\001"):
        ctcp(user, word[0].strip("\001"))

def notice (user, channel, content):
    # Should the bot fail to identify the first time.
    if user == "NickServ" and "This nickname is registered and" in content:
        irc.identify()
        
        # Some channels might have +R enabled.
        for channel in var.channels:
            irc.join(channel)

def invite (user, channel):
    irc.join(channel)
    irc.msg(channel, "{} invited me here.".format(user))

def ctcp (user, request):
    if request in var.ctcp:
        irc.notice(user, "\001{} {}\001".format(request, var.ctcp[request]))

###########################################
#    Checking for ident functions and     #
#    disabled commands.                   #
###########################################

def ident (cmd_obj):
    module = sys.modules[cmd_obj.method.__module__]
    def dsbl_check (user, channel, word):
        if channel in cmd_obj.disabled:
            return
        elif hasattr(module, "ident"):
            return module.ident(cmd_obj.method)(user, channel, word)
        else:
            return cmd_obj.method(user, channel, word)
    return dsbl_check

###########################################
#       Filling command dictionary.       #
###########################################

def fill_commands ():
    global commands
    
    for module in sys.modules:
        # In case the command uses ini files.
        if hasattr(sys.modules[module], "ins_db"):
            sys.modules[module].ins_db()
        
        # Message monitor function.
        if hasattr(sys.modules[module], "ins_monitor"):
            monitor.append(sys.modules[module].ins_monitor)
        
        # Function that fills var.commands for every command.
        if hasattr(sys.modules[module], "ins_command"):
            sys.modules[module].ins_command()
    
    # Disabled commands dictionary. (command:list of channels)
    dsbl_commands = ini.fill_dict("settings.ini", "Disabled Commands")
    
    for command in var.commands:
        
        # Disable if set to. Give the user some time to read it.
        if command in dsbl_commands:
            var.commands[command].disabled = dsbl_commands[command]
            print "Disabling .{} in: {}".format(command, " ".join(dsbl_commands[command]))
        elif not hasattr(var.commands[command], "disabled"):
            var.commands[command].disabled = []
        
        # Add aliases to list.
        for alias in var.commands[command].aliases:
            commands[alias] = ident(var.commands[command])
    
    # Give the user some time to read the disabled commands list.
    if dsbl_commands:
        time.sleep(2)

###########################################
#            Executing lines.             #
###########################################

def exec_python (channel, command):
    try:
        exec(command)
    except:
        irc.msg(channel, "Check your line, an exception occurred.")

###########################################
#         Local names/variables.          #
###########################################

# Dictionary responsible for handling commands.
commands = {}

# List of functions to call once a message is received.
monitor = []