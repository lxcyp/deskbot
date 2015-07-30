import time
import irc
import sys
import var
import ini
import parser
from command_modules import *

###########################################
#     Interpreting received messages.     #
###########################################

def read (line):
    print(line)
    
    if var.log:
        ini.add_to_list(line, "log/{}.log".format(irc.server), raw_path = True)
    
    # Check for server ping.
    if line.startswith("PING :"):
        irc.pong(line.split(" :")[1])
        return
    
    # Parse line into a line object.
    line_obj = parser.parse(line)
    
    if line_obj.event == "PRIVMSG":
        privmsg(line_obj.user, line_obj.target, line_obj.message)

    elif line_obj.event == "NOTICE":
        notice(line_obj.user, line_obj.target, line_obj.message)
    
    elif line_obj.event == "INVITE":
        invite(line_obj.user, line_obj.channel)
    
    elif line_obj.event == "NICK":
        nick(line_obj.user, line_obj.new_nick)
    
    elif line_obj.event == "KICK":
        kick(line_obj.user, line_obj.channel, line_obj.target, line_obj.reason)
    
    elif line_obj.event == "NUMREP":
        numrep(line_obj.code, line_obj.message)
    
    # Finally, call the monitor functions.
    for function in monitor:
        function(line_obj)

###########################################
#            Treating events.             #
###########################################

def privmsg (user, channel, content):
    word = filter(bool, content.split(" "))
    
    # Ignored people get out.
    if user in var.ignored:
        return
    
    # Channel should be the user if it's a PM.
    if channel == irc.botnick:
        channel = user
    
    if len(word) and word[0] in commands:
        commands[word[0]](user, channel, word)
    elif len(word) and word[0].startswith("\001"):
        ctcp(user, word[0].strip("\001"))

def notice (user, channel, content):
    if user == "NickServ" and "This nickname is registered" in content:
        irc.identify()
        
        for channel in var.channels:
            irc.join(channel)

def invite (user, channel):
    irc.notice(user, "I'll let {} know you invited me to {}.".format(irc.admin, channel))
    irc.msg(irc.admin, "Invite to {} from {}.".format(channel, user))

def ctcp (user, request):
    if request in var.ctcp:
        irc.notice(user, "\001{} {}\001".format(request, var.ctcp[request]))

def nick (user, new_nick):
    if user == irc.admin:
        irc.admin = new_nick

def kick (user, channel, target, reason):
    if target == irc.botnick:
        irc.msg(irc.admin, "{} was kicked from {} by {}.".format(target, channel, user))
        irc.msg(irc.admin, "Reason: {}".format(reason) if reason
                else "No reason was given.")
        
        var.channels.remove(channel)
        ini.remove_from_list(channel, "channels.ini")

def numrep (code, message):
    return

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
            print("WARNING: Disabling .{} in: {}".format(command, " ".join(dsbl_commands[command])))
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
    except Exception as exc:
        irc.msg(channel, "Exception: {}".format(exc))

###########################################
#         Local names/variables.          #
###########################################

# Dictionary responsible for handling commands.
commands = {}

# List of functions to call once a message is received.
monitor = []
