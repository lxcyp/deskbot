import irc, commands, var, ini
import time, re

# Functions that don't return anything, but help do stuff.
def set_auth_method ():
    irc.msg("NickServ", "STATUS {}".format(irc.botnick))
    response = False
    
    while not response:
        irclist = [x for x in irc.ircsock.recv(2048).split("\r\n") if x]
        for msg in irclist:
            if msg.startswith(":NickServ"):
                response = msg
            else:
                commands.read(msg)
    
    if "STATUS" in response:
        var.settings["ident.method"] = "STATUS"
        ini.add_to_ini("Settings", "ident.method", "STATUS", "settings.ini")
    else:
        var.settings["ident.method"] = "ACC"
        ini.add_to_ini("Settings", "ident.method", "ACC", "settings.ini")

# Functions that return booleans.

# Check for NickServ authentication.
def is_identified (user):
    # Determine auth command with services.
    if "ident.method" not in var.settings:
        set_auth_method()
    
    # Send set auth command.
    irc.msg("NickServ", "{} {}".format(var.settings["ident.method"], user))
    response = False
    
    while not response:
        irclist = [x for x in irc.ircsock.recv(2048).split("\r\n") if x]
        for msg in irclist:
            if msg.startswith(":NickServ"):
                response = msg
            else:
                commands.read(msg)
    
    # Checking with ident.method for NickServ auth.
    if var.settings["ident.method"] == "STATUS":
        return bool("STATUS {} 3".format(user) in response)
    elif var.settings["ident.method"] == "ACC":
        return bool("{} ACC 3".format(user) in response)

# Check if a value is an integer.
def is_number (num):
    try:
        int(num)
        return True
    except ValueError:
        return False

# Functions that return values.

# Check prefix for user in channel.
def prefix (user, channel):
    irc.ircsock.send("NAMES {}\n".format(channel))
    prefix, loop = [], True
    
    while loop:
        irclist = [x for x in irc.ircsock.recv(2048).split("\r\n") if x]
        for msg in irclist:
            if "{} @ {}".format(irc.botnick, channel) in msg:
                prefix += msg.split(" :", 1)[1].split(" ")
            elif msg.endswith("{} {} :End of /NAMES list.".format(irc.botnick, channel)):
                loop = False
            else:
                commands.read(msg)
    
    # Now that the list is complete, let's make a dictionary.
    prefix = {nick[1:] if len(nick) > 1 else nick[0]:nick[0] for nick in prefix}
    
    # And look for user.
    if user in prefix:
        return prefix[user]
    elif user[1:] in prefix:
        return "Doesn't have a prefix."
    else:
        return "Not found."

# Make a CTCP request and return the reply.
def ctcp_req (user, request):
    reply, start, end = False, time.time(), time.time()
    
    # Check if the username is valid, so we don't waste our time.
    if not re.match("[a-zA-Z\[\]\\`_\^\{\|\}][a-zA-Z0-9\[\]\\`_\^\{\|\}]", user):
        return 1
    
    # Just for formality.
    request = request.upper()
    
    # Send the request.
    irc.msg(user, "\001{}\001".format(request))
    
    # Only listen for 20 seconds.
    while not reply and end - start < 20:
        irclist = [ x for x in irc.ircsock.recv(2048).split('\r\n') if x ]
        for msg in irclist:
            if request in msg and msg.startswith(":"+user) and " NOTICE " in msg:
                reply = msg.split(request, 1)[1].strip("\001").lstrip()
            else:
                commands.read(msg)
        end = time.time()
    
    # Return the reply, if it got one.
    if reply:
        return reply
    else:
        return ""

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
