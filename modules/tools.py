import irc, commands, var, ini
import time, re

###########################################
#    Determining whether services will    #
#    be using STATUS or ACC for auth      #
#    check.                               #
###########################################

def set_auth_method ():
    irc.msg("NickServ", "STATUS {}".format(irc.botnick))
    response = ""
    
    while not response or commands.split_line:
        line = irc.ircsock.recv(512)
        
        # Securi-tea
        
        if commands.split_line:
            commands.split_line += line.split("\r\n")[0]
            line = "\r\n".join(line.split("\r\n")[1:]) + "\r\n"
            commands.read(commands.split_line, "")
        
        if not (line.endswith("\r\n") or line.endswith("\r")):
            commands.split_line = line.split("\r\n")[-1]
            line = "\r\n".join(line.split("\r\n")[:-1])
        
        if line.endswith("\r"):
            line = line.rstrip("\r")
        
        if line.startswith("\n"):
            line = line.lstrip("\n")
        
        # End of securi-tea
        
        msg_list = [message for message in line.split("\r\n") if message]
        
        for message in msg_list:
            if not response and message.startswith(":NickServ"):
                response = message
            else:
                commands.read(message)
    
    if "STATUS" in response:
        var.settings["ident.method"] = "STATUS"
        ini.add_to_ini("Settings", "ident.method", "STATUS", "settings.ini")
    else:
        var.settings["ident.method"] = "ACC"
        ini.add_to_ini("Settings", "ident.method", "ACC", "settings.ini")

###########################################
#          NickServ auth check.           #
###########################################

def is_identified (user):
    # Determine auth command with services.
    if "ident.method" not in var.settings:
        set_auth_method()
    
    # Send set auth command.
    irc.msg("NickServ", "{} {}".format(var.settings["ident.method"], user))
    response = ""
    
    while not response or commands.split_line:
        line = irc.ircsock.recv(512)
        
        # Securi-tea
        
        if commands.split_line:
            commands.split_line += line.split("\r\n")[0]
            line = "\r\n".join(line.split("\r\n")[1:]) + "\r\n"
            commands.read(commands.split_line, "")
        
        if not (line.endswith("\r\n") or line.endswith("\r")):
            commands.split_line = line.split("\r\n")[-1]
            line = "\r\n".join(line.split("\r\n")[:-1])
        
        if line.endswith("\r"):
            line = line.rstrip("\r")
        
        if line.startswith("\n"):
            line = line.lstrip("\n")
        
        # End of securi-tea
        
        msg_list = [message for message in line.split("\r\n") if message]
        
        for message in msg_list:
            if message.startswith(":NickServ"):
                response = message
            else:
                commands.read(message)
    
    # Checking with ident.method for NickServ auth.
    if var.settings["ident.method"] == "STATUS":
        return bool("STATUS {} 3".format(user) in response)
    elif var.settings["ident.method"] == "ACC":
        return bool("{} ACC 3".format(user) in response)

###########################################
#       Check if num is an integer.       #
###########################################

def is_number (num):
    try:
        int(num)
        return True
    except ValueError:
        return False

###########################################
#        Checking users's prefix.         #
###########################################

# Check prefix for user in channel.
def prefix (user, channel):
    irc.ircsock.send("NAMES {}\n".format(channel))
    prefix, loop = [], True
    
    while loop or commands.split_line:
        line = irc.ircsock.recv(512)
        
        # Securi-tea
        
        if commands.split_line:
            commands.split_line += line.split("\r\n")[0]
            line = "\r\n".join(line.split("\r\n")[1:]) + "\r\n"
            commands.read(commands.split_line, "")
        
        if not (line.endswith("\r\n") or line.endswith("\r")):
            commands.split_line = line.split("\r\n")[-1]
            line = "\r\n".join(line.split("\r\n")[:-1])
        
        if line.endswith("\r"):
            line = line.rstrip("\r")
        
        if line.startswith("\n"):
            line = line.lstrip("\n")
        
        # End of securi-tea
        
        msg_list = [message for message in line.split("\r\n") if message]
        
        for message in msg_list:
            if re.match(":[^\s]+ \d{3} " + "{} [@|*|=] {}".format(irc.botnick, channel), message):
                prefix += filter(bool, message.split(" :", 1)[1].split(" "))
            elif message.endswith("{} {} :End of /NAMES list.".format(irc.botnick, channel)):
                loop = False
            else:
                commands.read(message)
    
    # Now that the list is complete, let's make a dictionary.
    prefix = {nick[1:] if len(nick) > 1 else nick[0]:nick[0] for nick in prefix}
    
    # And look for user.
    if user in prefix:
        return prefix[user]
    elif user[1:] in prefix:
        return "Doesn't have a prefix."
    else:
        return "Not found."

###########################################
#          Making a CTCP request.         #
###########################################

def ctcp_req (user, request, *param):
    start = end = time.time()
    reply = ""
        
    # Check if the username is valid, so we don't waste our time.
    if not re.match("[a-zA-Z\[\]\\`_\^\{\|\}][a-zA-Z0-9\[\]\\`_\^\{\|\}]", user):
        return 1
    
    # Just for formality.
    request = request.upper()
    
    # Send the request.
    if param:
        irc.msg(user, "\001{} {}\001".format(request, param[0]))
    else:
        irc.msg(user, "\001{}\001".format(request))
    
    # Only listen for 20 seconds.
    while (not reply and end - start < 20) or commands.split_line:
        line = irc.ircsock.recv(512)
        
        # Securi-tea
        
        if commands.split_line:
            commands.split_line += line.split("\r\n")[0]
            line = "\r\n".join(line.split("\r\n")[1:]) + "\r\n"
            commands.read(commands.split_line, "")
        
        if not (line.endswith("\r\n") or line.endswith("\r")):
            commands.split_line = line.split("\r\n")[-1]
            line = "\r\n".join(line.split("\r\n")[:-1])
        
        if line.endswith("\r"):
            line = line.rstrip("\r")
        
        if line.startswith("\n"):
            line = line.lstrip("\n")
        
        # End of securi-tea
        
        msg_list = [message for message in line.split("\r\n") if message]
        
        for message in msg_list:
            if (
                (not reply) and
                request in message and
                message.startswith(":"+user) and
                " NOTICE " in message
            ):
                reply = message.split(request, 1)[1].strip("\001").lstrip()
            else:
                commands.read(message)
        end = time.time()
    
    # Return the reply, if it got one.
    if reply:
        return reply
    else:
        return ""

###########################################
#            Changing strings.            #
###########################################

# We want to get rid of certain characters.
def trim (string):
    if "\x03" in string:
        string = string.split("\x03")[0]
    if "\x02" in string:
        str = string.split("\x02")[0]
    if "\x1d" in string:
        str = string.split("\x1d")[0]
    if "\x0f" in string:
        str = string.split("\x0f")[0]
    return string

# We want to tag NSFW urls as NSFW.
def nsfw_check (url_pair):
    if "!" in url_pair.split(" ")[1]:
        url_pair = "[\x034NSFW\x0f] {}".format(url_pair.split(" ")[1].strip("!"))
    return url_pair
